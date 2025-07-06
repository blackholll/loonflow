import React, { useState, useEffect } from 'react';
import {
    Box,
    Typography,
    TextField,
    FormControl,
    InputLabel,
    Select,
    MenuItem,
    Button,
    Divider,
    Paper,
    IconButton,
} from '@mui/material';
import { Close as CloseIcon } from '@mui/icons-material';
import { Node, Edge } from '@xyflow/react';

interface PropertyPanelProps {
    element: Node | Edge | null;
    onUpdateNodeProperties: (nodeId: string, properties: any) => void;
    onUpdateEdgeProperties: (edgeId: string, properties: any) => void;
}

const PropertyPanel: React.FC<PropertyPanelProps> = ({
    element,
    onUpdateNodeProperties,
    onUpdateEdgeProperties,
}) => {
    const [properties, setProperties] = useState<any>({});

    useEffect(() => {
        if (element) {
            if ('source' in element) {
                // 边属性
                setProperties(element.data?.properties || {});
            } else {
                // 节点属性
                setProperties(element.data?.properties || {});
            }
        }
    }, [element]);

    const handlePropertyChange = (key: string, value: any) => {
        const newProperties = { ...properties, [key]: value };
        setProperties(newProperties);

        if (element) {
            if ('source' in element) {
                // 更新边属性
                onUpdateEdgeProperties(element.id, newProperties);
            } else {
                // 更新节点属性
                onUpdateNodeProperties(element.id, newProperties);
            }
        }
    };

    if (!element) {
        return (
            <Box sx={{ p: 2 }}>
                <Typography variant="h6" gutterBottom>
                    属性面板
                </Typography>
                <Typography variant="body2" color="text.secondary">
                    请选择一个节点或连线来查看和编辑属性
                </Typography>
            </Box>
        );
    }

    const isEdge = 'source' in element;
    const elementType = isEdge ? '连线' : '节点';
    const elementLabel = isEdge ? '连线属性' : (element.data?.label as string) || '节点属性';

    return (
        <Box sx={{ p: 2, height: '100%', overflow: 'auto' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
                <Typography variant="h6">
                    {elementLabel}
                </Typography>
                <IconButton size="small">
                    <CloseIcon />
                </IconButton>
            </Box>

            <Divider sx={{ mb: 2 }} />

            {isEdge ? (
                // 边属性
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                    <TextField
                        label="连线名称"
                        value={properties.name || ''}
                        onChange={(e) => handlePropertyChange('name', e.target.value)}
                        size="small"
                        fullWidth
                    />

                    <TextField
                        label="连线描述"
                        value={properties.description || ''}
                        onChange={(e) => handlePropertyChange('description', e.target.value)}
                        size="small"
                        multiline
                        rows={3}
                        fullWidth
                    />

                    <FormControl size="small" fullWidth>
                        <InputLabel>连线类型</InputLabel>
                        <Select
                            value={properties.type || 'normal'}
                            label="连线类型"
                            onChange={(e) => handlePropertyChange('type', e.target.value)}
                        >
                            <MenuItem value="normal">普通连线</MenuItem>
                            <MenuItem value="conditional">条件连线</MenuItem>
                            <MenuItem value="default">默认连线</MenuItem>
                        </Select>
                    </FormControl>

                    {properties.type === 'conditional' && (
                        <TextField
                            label="条件表达式"
                            value={properties.condition || ''}
                            onChange={(e) => handlePropertyChange('condition', e.target.value)}
                            size="small"
                            multiline
                            rows={2}
                            fullWidth
                            placeholder="例如: status === 'approved'"
                        />
                    )}
                </Box>
            ) : (
                // 节点属性
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                    <TextField
                        label="节点名称"
                        value={properties.name || ''}
                        onChange={(e) => handlePropertyChange('name', e.target.value)}
                        size="small"
                        fullWidth
                    />

                    <TextField
                        label="节点描述"
                        value={properties.description || ''}
                        onChange={(e) => handlePropertyChange('description', e.target.value)}
                        size="small"
                        multiline
                        rows={3}
                        fullWidth
                    />

                    <TextField
                        label="处理人"
                        value={properties.assignee || ''}
                        onChange={(e) => handlePropertyChange('assignee', e.target.value)}
                        size="small"
                        fullWidth
                        placeholder="输入处理人姓名或ID"
                    />

                    <TextField
                        label="超时时间（分钟）"
                        type="number"
                        value={properties.timeout || 0}
                        onChange={(e) => handlePropertyChange('timeout', parseInt(e.target.value) || 0)}
                        size="small"
                        fullWidth
                        inputProps={{ min: 0 }}
                    />

                    {/* 网关特定属性 */}
                    {(element.data?.nodeType === 'parallel' || element.data?.nodeType === 'exclusive') && (
                        <>
                            <Divider sx={{ my: 1 }} />
                            <Typography variant="subtitle2" color="primary">
                                网关配置
                            </Typography>

                            <FormControl size="small" fullWidth>
                                <InputLabel>网关类型</InputLabel>
                                <Select
                                    value={properties.gatewayType || element.data?.nodeType}
                                    label="网关类型"
                                    onChange={(e) => handlePropertyChange('gatewayType', e.target.value)}
                                >
                                    <MenuItem value="parallel">并行网关</MenuItem>
                                    <MenuItem value="exclusive">排他网关</MenuItem>
                                </Select>
                            </FormControl>

                            {properties.gatewayType === 'exclusive' && (
                                <TextField
                                    label="默认分支"
                                    value={properties.defaultBranch || ''}
                                    onChange={(e) => handlePropertyChange('defaultBranch', e.target.value)}
                                    size="small"
                                    fullWidth
                                    placeholder="默认分支的连线ID"
                                />
                            )}
                        </>
                    )}

                    {/* 开始节点特定属性 */}
                    {element.data?.nodeType === 'start' && (
                        <>
                            <Divider sx={{ my: 1 }} />
                            <Typography variant="subtitle2" color="primary">
                                开始节点配置
                            </Typography>

                            <TextField
                                label="流程名称"
                                value={properties.processName || ''}
                                onChange={(e) => handlePropertyChange('processName', e.target.value)}
                                size="small"
                                fullWidth
                            />

                            <TextField
                                label="流程描述"
                                value={properties.processDescription || ''}
                                onChange={(e) => handlePropertyChange('processDescription', e.target.value)}
                                size="small"
                                multiline
                                rows={2}
                                fullWidth
                            />
                        </>
                    )}

                    {/* 结束节点特定属性 */}
                    {element.data?.nodeType === 'end' && (
                        <>
                            <Divider sx={{ my: 1 }} />
                            <Typography variant="subtitle2" color="primary">
                                结束节点配置
                            </Typography>

                            <FormControl size="small" fullWidth>
                                <InputLabel>结束类型</InputLabel>
                                <Select
                                    value={properties.endType || 'normal'}
                                    label="结束类型"
                                    onChange={(e) => handlePropertyChange('endType', e.target.value)}
                                >
                                    <MenuItem value="normal">正常结束</MenuItem>
                                    <MenuItem value="terminate">终止流程</MenuItem>
                                    <MenuItem value="error">错误结束</MenuItem>
                                </Select>
                            </FormControl>

                            {properties.endType === 'error' && (
                                <TextField
                                    label="错误代码"
                                    value={properties.errorCode || ''}
                                    onChange={(e) => handlePropertyChange('errorCode', e.target.value)}
                                    size="small"
                                    fullWidth
                                />
                            )}
                        </>
                    )}
                </Box>
            )}
        </Box>
    );
};

export default PropertyPanel; 