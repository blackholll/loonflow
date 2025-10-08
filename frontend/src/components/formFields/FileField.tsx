import React, { useState, useRef } from 'react';
import {
    FormControl,
    Button,
    Box,
    Typography,
    IconButton,
    List,
    ListItem,
    ListItemText,
    ListItemSecondaryAction,
    Alert,
    CircularProgress
} from '@mui/material';
import {
    CloudUpload,
    AttachFile,
    Delete,
    Download,
    FilePresent
} from '@mui/icons-material';
import ViewField from './ViewField';

interface FileInfo {
    id: string;
    name: string;
    size: number;
    type: string;
    url?: string;
    file?: File;
}

interface FileFieldProps {
    value: string | FileInfo[];
    fieldRequired: boolean;
    onChange: (value: string | FileInfo[]) => void;
    mode: 'view' | 'edit';
    props: any;
}

function FileField({
    value = '',
    fieldRequired,
    onChange,
    mode,
    props,
}: FileFieldProps) {

    const [uploading, setUploading] = useState(false);
    const [error, setError] = useState<string>('');
    const fileInputRef = useRef<HTMLInputElement>(null);

    // 解析文件值
    const parseFileValue = (val: any): FileInfo[] => {
        if (!val) return [];

        if (typeof val === 'string') {
            try {
                // 尝试解析 JSON 字符串
                const parsed = JSON.parse(val);
                return Array.isArray(parsed) ? parsed : [];
            } catch {
                // 如果不是 JSON，可能是文件名字符串
                return val ? [{ id: '1', name: val, size: 0, type: '' }] : [];
            }
        }

        if (Array.isArray(val)) {
            return val;
        }

        return [];
    };

    // 格式化文件大小
    const formatFileSize = (bytes: number): string => {
        if (bytes === 0) return '0 B';
        const k = 1024;
        const sizes = ['B', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    };

    // 获取文件图标
    const getFileIcon = (fileType: string) => {
        if (fileType.includes('image')) return '🖼️';
        if (fileType.includes('pdf')) return '📄';
        if (fileType.includes('word') || fileType.includes('doc')) return '📝';
        if (fileType.includes('excel') || fileType.includes('sheet')) return '📊';
        if (fileType.includes('zip') || fileType.includes('rar')) return '📦';
        return '📎';
    };

    // 处理文件选择
    const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
        const files = event.target.files;
        if (!files || files.length === 0) return;

        setError('');
        setUploading(true);

        try {
            const newFiles: FileInfo[] = Array.from(files).map((file, index) => ({
                id: `file_${Date.now()}_${index}`,
                name: file.name,
                size: file.size,
                type: file.type,
                file: file
            }));

            const currentFiles = parseFileValue(value);
            const updatedFiles = [...currentFiles, ...newFiles];

            // 限制文件数量
            const maxFiles = props?.maxFiles || 10;
            if (updatedFiles.length > maxFiles) {
                setError(`最多只能上传 ${maxFiles} 个文件`);
                setUploading(false);
                return;
            }

            // 限制文件大小
            const maxSize = props?.maxSize || 10 * 1024 * 1024; // 默认 10MB
            const oversizedFiles = newFiles.filter(file => file.size > maxSize);
            if (oversizedFiles.length > 0) {
                setError(`文件 ${oversizedFiles[0].name} 超过大小限制 ${formatFileSize(maxSize)}`);
                setUploading(false);
                return;
            }

            onChange(updatedFiles);
        } catch (err) {
            setError('文件处理失败');
        } finally {
            setUploading(false);
            // 清空 input 值，允许重复选择同一文件
            if (fileInputRef.current) {
                fileInputRef.current.value = '';
            }
        }
    };

    // 删除文件
    const handleDeleteFile = (fileId: string) => {
        const currentFiles = parseFileValue(value);
        const updatedFiles = currentFiles.filter(file => file.id !== fileId);
        onChange(updatedFiles);
    };

    // 下载文件
    const handleDownloadFile = (file: FileInfo) => {
        if (file.url) {
            // 如果有 URL，直接下载
            window.open(file.url, '_blank');
        } else if (file.file) {
            // 如果是本地文件，创建下载链接
            const url = URL.createObjectURL(file.file);
            const a = document.createElement('a');
            a.href = url;
            a.download = file.name;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }
    };

    // view mode - 只显示文件列表
    if (mode === 'view') {
        const files = parseFileValue(value);

        if (files.length === 0) {
            return <ViewField type='file' value='-' props={props} />;
        }

        return (
            <Box>
                {files.map((file) => (
                    <Box
                        key={file.id}
                        sx={{
                            display: 'flex',
                            alignItems: 'center',
                            gap: 1,
                            mb: 1,
                            p: 1,
                            border: '1px solid #e0e0e0',
                            borderRadius: 1,
                            backgroundColor: '#f5f5f5'
                        }}
                    >
                        <Typography sx={{ fontSize: '1.2em' }}>
                            {getFileIcon(file.type)}
                        </Typography>
                        <Box sx={{ flex: 1 }}>
                            <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                                {file.name}
                            </Typography>
                            <Typography variant="caption" color="text.secondary">
                                {formatFileSize(file.size)}
                            </Typography>
                        </Box>
                        {file.url && (
                            <IconButton
                                size="small"
                                onClick={() => handleDownloadFile(file)}
                                title="下载文件"
                            >
                                <Download fontSize="small" />
                            </IconButton>
                        )}
                    </Box>
                ))}
            </Box>
        );
    }

    // edit mode - 支持上传和管理文件
    const files = parseFileValue(value);

    return (
        <FormControl fullWidth={true}>
            <Box>
                {/* 文件上传区域 */}
                <Box
                    sx={{
                        border: '2px dashed #ccc',
                        borderRadius: 2,
                        p: 3,
                        textAlign: 'center',
                        backgroundColor: '#fafafa',
                        cursor: 'pointer',
                        '&:hover': {
                            backgroundColor: '#f0f0f0',
                            borderColor: '#999'
                        }
                    }}
                    onClick={() => fileInputRef.current?.click()}
                >
                    <CloudUpload sx={{ fontSize: 48, color: '#666', mb: 1 }} />
                    <Typography variant="body1" sx={{ mb: 1 }}>
                        点击选择文件或拖拽文件到此处
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                        支持多个文件，单个文件不超过 {formatFileSize(props?.maxSize || 10 * 1024 * 1024)}
                    </Typography>
                    {props?.maxFiles && (
                        <Typography variant="caption" color="text.secondary">
                            最多 {props.maxFiles} 个文件
                        </Typography>
                    )}
                </Box>

                {/* 隐藏的文件输入 */}
                <input
                    ref={fileInputRef}
                    type="file"
                    multiple
                    accept={props?.accept || '*'}
                    onChange={handleFileSelect}
                    style={{ display: 'none' }}
                />

                {/* 错误提示 */}
                {error && (
                    <Alert severity="error" sx={{ mt: 1 }}>
                        {error}
                    </Alert>
                )}

                {/* 上传进度 */}
                {uploading && (
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 1 }}>
                        <CircularProgress size={20} />
                        <Typography variant="body2">正在处理文件...</Typography>
                    </Box>
                )}

                {/* 文件列表 */}
                {files.length > 0 && (
                    <Box sx={{ mt: 2 }}>
                        <Typography variant="subtitle2" sx={{ mb: 1 }}>
                            已选择的文件 ({files.length})
                        </Typography>
                        <List dense>
                            {files.map((file) => (
                                <ListItem
                                    key={file.id}
                                    sx={{
                                        border: '1px solid #e0e0e0',
                                        borderRadius: 1,
                                        mb: 1,
                                        backgroundColor: '#fff'
                                    }}
                                >
                                    <FilePresent sx={{ mr: 1, color: '#666' }} />
                                    <ListItemText
                                        primary={file.name}
                                        secondary={`${formatFileSize(file.size)} • ${file.type || '未知类型'}`}
                                    />
                                    <ListItemSecondaryAction>
                                        <IconButton
                                            size="small"
                                            onClick={() => handleDownloadFile(file)}
                                            title="下载"
                                        >
                                            <Download fontSize="small" />
                                        </IconButton>
                                        <IconButton
                                            size="small"
                                            onClick={() => handleDeleteFile(file.id)}
                                            title="删除"
                                            color="error"
                                        >
                                            <Delete fontSize="small" />
                                        </IconButton>
                                    </ListItemSecondaryAction>
                                </ListItem>
                            ))}
                        </List>
                    </Box>
                )}

                {/* 必填提示 */}
                {fieldRequired && files.length === 0 && (
                    <Typography variant="caption" color="error" sx={{ mt: 1, display: 'block' }}>
                        此字段为必填项
                    </Typography>
                )}
            </Box>
        </FormControl>
    );
}

export default FileField;
