import {
    CloudUpload,
    Delete,
    Download,
    FilePresent
} from '@mui/icons-material';
import {
    Alert,
    Box,
    CircularProgress,
    FormControl,
    IconButton,
    List,
    ListItem,
    ListItemSecondaryAction,
    ListItemText,
    Typography
} from '@mui/material';
import React, { useRef, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { uploadTicketFile, uploadDraftFile } from '../../services/ticket';
import apiClient from '../../services/api';
import ViewField from './ViewField';

/** 文件字段持久化格式：JSON 数组 [{ file_name, file_path }, ...] */
export interface FileFieldItem {
    file_name: string;
    file_path: string;
}

interface FileFieldProps {
    /** 值为 JSON 字符串或 FileFieldItem[]，格式为 [{ file_name, file_path }, ...] */
    value: string | FileFieldItem[];
    fieldRequired: boolean;
    onChange: (value: FileFieldItem[]) => void;
    mode: 'view' | 'edit';
    props: any;
    /** 工单 ID；有则用工单上传接口，无则用草稿上传（新建工单场景，提交时后端会迁移到工单目录） */
    ticketId?: string;
}

const TICKET_FILE_URL_PREFIX = '/api/v1.0/tickets/';

function FileField({
    value = '',
    fieldRequired,
    onChange,
    mode,
    props,
    ticketId,
}: FileFieldProps) {
    const { t } = useTranslation();

    const [uploading, setUploading] = useState(false);
    const [error, setError] = useState<string>('');
    const fileInputRef = useRef<HTMLInputElement>(null);

    // 解析为统一展示格式 [{ file_name, file_path }, ...]
    const parseFileValue = (val: any): FileFieldItem[] => {
        if (!val) return [];
        if (typeof val === 'string') {
            try {
                const parsed = JSON.parse(val);
                if (!Array.isArray(parsed)) return [];
                return parsed.filter((x: any) => x && typeof x.file_name === 'string' && typeof x.file_path === 'string');
            } catch {
                return [];
            }
        }
        if (Array.isArray(val)) {
            return val.filter((x: any) => x && typeof x.file_name === 'string' && typeof x.file_path === 'string');
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

    // 选择文件后先上传（有 ticketId 用工单上传，无则用草稿上传），再写入格式 [{ file_name, file_path }, ...]
    const handleFileSelect = async (event: React.ChangeEvent<HTMLInputElement>) => {
        const files = event.target.files;
        if (!files || files.length === 0) return;

        setError('');
        setUploading(true);

        const maxFiles = props?.maxFiles || 10;
        const maxSize = props?.maxSize || 10 * 1024 * 1024; // 默认 10MB
        const currentFiles = parseFileValue(value);

        for (const file of Array.from(files)) {
            if (file.size > maxSize) {
                setError(`${t('common.fileUpload.fileTooLarge')}: ${file.name} (${formatFileSize(maxSize)})`);
                setUploading(false);
                if (fileInputRef.current) fileInputRef.current.value = '';
                return;
            }
        }
        if (currentFiles.length + files.length > maxFiles) {
            setError(`${t('common.fileUpload.tooManyFiles')}: ${maxFiles}`);
            setUploading(false);
            if (fileInputRef.current) fileInputRef.current.value = '';
            return;
        }

        const uploadOne = ticketId
            ? (file: File) => uploadTicketFile(ticketId, file)
            : uploadDraftFile;

        try {
            const uploadedList: FileFieldItem[] = [];
            for (let i = 0; i < files.length; i++) {
                const file = files[i];
                const res = await uploadOne(file) as { code?: number; msg?: string; data?: { url: string; name: string; size: number } };
                if (res?.code === 0 && res?.data) {
                    uploadedList.push({
                        file_name: res.data.name,
                        file_path: res.data.url
                    });
                } else {
                    setError((res as { msg?: string })?.msg || t('common.fileUpload.uploadFailed'));
                    setUploading(false);
                    if (fileInputRef.current) fileInputRef.current.value = '';
                    return;
                }
            }
            onChange([...currentFiles, ...uploadedList]);
        } catch (err) {
            setError(t('common.fileUpload.fileProcessingFailed'));
        } finally {
            setUploading(false);
            if (fileInputRef.current) fileInputRef.current.value = '';
        }
    };

    // 删除文件（按 file_path 区分）
    const handleDeleteFile = (filePath: string) => {
        const currentFiles = parseFileValue(value);
        onChange(currentFiles.filter(f => f.file_path !== filePath));
    };

    // 下载文件（工单附件需带鉴权请求）
    const handleDownloadFile = async (file: FileFieldItem) => {
        if (!file.file_path) return;
        if (file.file_path.startsWith(TICKET_FILE_URL_PREFIX)) {
            try {
                const res = await apiClient.get(file.file_path, { responseType: 'blob' });
                const blob = res.data as Blob;
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = file.file_name || 'download';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            } catch {
                setError(t('common.fileUpload.downloadFailed'));
            }
            return;
        }
        window.open(file.file_path, '_blank');
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
                        key={file.file_path}
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
                        <Typography sx={{ fontSize: '1.2em' }}>{getFileIcon('')}</Typography>
                        <Box sx={{ flex: 1 }}>
                            <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                                {file.file_name}
                            </Typography>
                        </Box>
                        <IconButton
                            size="small"
                            onClick={() => handleDownloadFile(file)}
                            title={t('common.fileUpload.downloadFile')}
                        >
                            <Download fontSize="small" />
                        </IconButton>
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
                        {t('common.fileUpload.clickToSelect')}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                        {t('common.fileUpload.multipleFilesHint')} {t('common.fileUpload.fileSizeLimit')} {formatFileSize(props?.maxSize || 10 * 1024 * 1024)}
                    </Typography>
                    {props?.maxFiles && (
                        <Typography variant="caption" color="text.secondary">
                            {t('common.fileUpload.maxFilesLimit')} {props.maxFiles} {t('common.fileUpload.filesAllowed')}
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
                        <Typography variant="body2">{t('common.fileUpload.uploading')}</Typography>
                    </Box>
                )}

                {/* 文件列表 */}
                {files.length > 0 && (
                    <Box sx={{ mt: 2 }}>
                        <Typography variant="subtitle2" sx={{ mb: 1 }}>
                            {t('common.fileUpload.selectedFiles')} ({files.length})
                        </Typography>
                        <List dense>
                            {files.map((file) => (
                                <ListItem
                                    key={file.file_path}
                                    sx={{
                                        border: '1px solid #e0e0e0',
                                        borderRadius: 1,
                                        mb: 1,
                                        backgroundColor: '#fff'
                                    }}
                                >
                                    <FilePresent sx={{ mr: 1, color: '#666' }} />
                                    <ListItemText primary={file.file_name} />
                                    <ListItemSecondaryAction>
                                        <IconButton
                                            size="small"
                                            onClick={() => handleDownloadFile(file)}
                                            title={t('common.fileUpload.downloadFile')}
                                        >
                                            <Download fontSize="small" />
                                        </IconButton>
                                        <IconButton
                                            size="small"
                                            onClick={() => handleDeleteFile(file.file_path)}
                                            title={t('common.fileUpload.deleteFile')}
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
                        {t('common.fileUpload.requiredField')}
                    </Typography>
                )}
            </Box>
        </FormControl>
    );
}

export default FileField;
