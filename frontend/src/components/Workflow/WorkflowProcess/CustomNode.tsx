import React, { useState } from 'react';
import { Handle, Position, NodeProps } from '@xyflow/react';
import { Box, Typography, Paper, TextField } from '@mui/material';
import {
    PlayArrow as StartIcon,
    Circle as NormalIcon,
    Stop as EndIcon,
    AccountTree as ParallelIcon,
    CallSplit as ExclusiveIcon,
    Timer as TimerIcon,
    Webhook as WebhookIcon
} from '@mui/icons-material';




const CustomNode = ({ data, selected }: NodeProps) => {
    const [isEditing, setIsEditing] = useState(false);
    const [editName, setEditName] = useState((data as any)?.properties?.name || '节点');
    const [showHandles, setShowHandles] = useState(false);


    // 当 name 变化时，更新 editName
    const currentName = (data as any)?.properties?.name;
    React.useEffect(() => {
        setEditName(currentName || '节点');
    }, [currentName]);

    const getNodeIcon = (nodeType: string, isIconOnlyNode: boolean = false) => {
        const fontSize = isIconOnlyNode ? 18 : 12;
        console.log('nodeTypenodeType:', nodeType);
        switch (nodeType) {
            case 'start':
                return <StartIcon sx={{ fontSize, color: '#4caf50' }} />;
            case 'end':
                return <EndIcon sx={{ fontSize, color: '#f44336' }} />;
            case 'parallel':
                return <ParallelIcon sx={{ fontSize, color: '#ff9800' }} />;
            case 'exclusive':
                return <ExclusiveIcon sx={{ fontSize, color: '#9c27b0' }} />;
            case 'timer':
                return <TimerIcon sx={{ fontSize, color: '#2196f3' }} />;
            case 'hook':
                return <WebhookIcon sx={{ fontSize, color: '#2196f3' }} />;
            default:
                return <NormalIcon sx={{ fontSize, color: '#2196f3' }} />;
        }
    };

    const nodeType = (data as any)?.properties?.type || 'normal';
    const isCurrent = Boolean((data as any)?.properties?.isCurrent);
    const isSelectedOnly = Boolean(selected && !isCurrent);
    const borderColor = isCurrent ? '#ff6f00' : (isSelectedOnly ? '#1976d2' : '#ccc');
    const bgColor = (isCurrent || isSelectedOnly) ? '#e3f2fd' : '#f5f5f5';

    const handleNodeClick = (event: React.MouseEvent) => {
        if (event.detail === 2) { // 双击编辑
            setIsEditing(true);
        }
    };

    const handleNameChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setEditName(event.target.value);
    };

    const handleNameBlur = () => {
        setIsEditing(false);
        // 这里可以添加更新节点名称的逻辑
        console.log('节点名称更新为:', editName);
    };

    const handleKeyPress = (event: React.KeyboardEvent) => {
        if (event.key === 'Enter') {
            setIsEditing(false);
            console.log('节点名称更新为:', editName);
        }
    };


    const isDiamond = nodeType === 'exclusive' || nodeType === 'parallel';
    const isIconOnly = nodeType === 'timer' || nodeType === 'hook';
    // start/end 变量未使用，移除

    const rectHandleCommon = {
        opacity: showHandles ? 1 : 0,
        transition: 'opacity 0.2s',
        width: 3,
        height: 3,
        backgroundColor: '#1976d2',
        borderRadius: '50%',
        margin: '-1px',
        minWidth: '3px',
        minHeight: '3px'
    };



    return (
        isIconOnly ? (
            // 纯图标节点（定时器和钩子）
            <Box
                sx={{
                    width: 40,
                    height: 40,
                    position: 'relative',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    background: 'transparent',
                }}
                onClick={handleNodeClick}
                onMouseEnter={() => setShowHandles(true)}
                onMouseLeave={() => setShowHandles(false)}
            >
                <Box
                    sx={{
                        width: 32,
                        height: 32,
                        borderRadius: '50%',
                        backgroundColor: bgColor,
                        border: `2px solid ${borderColor}`,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        '&:hover': {
                            backgroundColor: '#e3f2fd',
                            border: '2px solid #1976d2',
                        },
                    }}
                >
                    {getNodeIcon(nodeType, true)}
                </Box>
                <Handle id="top" type="source" position={Position.Top} style={{ ...rectHandleCommon }} />
                <Handle id="bottom" type="source" position={Position.Bottom} style={{ ...rectHandleCommon }} />
                <Handle id="left" type="source" position={Position.Left} style={{ ...rectHandleCommon }} />
                <Handle id="right" type="source" position={Position.Right} style={{ ...rectHandleCommon }} />
            </Box>
        ) : isDiamond ? (
            <Box
                sx={{
                    width: 40,
                    height: 40,
                    position: 'relative',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    background: 'transparent',
                }}
                onClick={handleNodeClick}
                onMouseEnter={() => setShowHandles(true)}
                onMouseLeave={() => setShowHandles(false)}
            >
                {/* 旋转的矩形作为菱形 */}
                <Box
                    sx={{
                        width: 28, // 80 * 0.707 ≈ 56 (考虑旋转后的视觉效果)
                        height: 28,
                        border: `2px solid ${borderColor}`,
                        backgroundColor: 'transparent',
                        transform: 'rotate(45deg)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        '&:hover': {
                            elevation: 4,
                            border: '2px solid #1976d2',
                        },
                    }}
                >
                    {/* 图标（反向旋转保持正向） */}
                    <Box sx={{ transform: 'rotate(-45deg)' }}>
                        {getNodeIcon(nodeType)}
                    </Box>
                </Box>
                <Handle id="top" type="source" position={Position.Top} style={{ ...rectHandleCommon }} />
                <Handle id="bottom" type="source" position={Position.Bottom} style={{ ...rectHandleCommon }} />
                <Handle id="left" type="source" position={Position.Left} style={{ ...rectHandleCommon }} />
                <Handle id="right" type="source" position={Position.Right} style={{ ...rectHandleCommon }} />
            </Box>
        ) : (
            // 普通矩形节点
            <Paper
                elevation={(isCurrent || isSelectedOnly) ? 8 : 2}
                sx={{
                    width: 100,
                    height: 30,
                    backgroundColor: 'transparent',
                    border: `2px solid ${borderColor}`,
                    display: 'flex',
                    alignItems: 'center',
                    position: 'relative',
                    cursor: 'pointer',
                    '&:hover': {
                        elevation: 4,
                        border: '2px solid #1976d2',
                    },
                }}
                onClick={handleNodeClick}
                onMouseEnter={() => setShowHandles(true)}
                onMouseLeave={() => setShowHandles(false)}
            >
                <Handle id="top" type="source" position={Position.Top} style={{ ...rectHandleCommon }} />
                <Handle id="bottom" type="source" position={Position.Bottom} style={{ ...rectHandleCommon }} />
                <Handle id="left" type="source" position={Position.Left} style={{ ...rectHandleCommon }} />
                {/* 右侧连接点 */}
                <Handle id="right" type="source" position={Position.Right} style={{ ...rectHandleCommon }} />
                <Box
                    sx={{
                        width: 30,
                        height: '100%',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        borderRight: '1px solid #ccc',
                    }}
                >
                    {getNodeIcon(nodeType)}
                </Box>

                <Box
                    sx={{
                        flex: 1,
                        height: '100%',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'flex-start',
                        px: 2,
                    }}
                >
                    {isEditing ? (
                        <TextField
                            value={editName}
                            onChange={handleNameChange}
                            onBlur={handleNameBlur}
                            onKeyPress={handleKeyPress}
                            variant="standard"
                            size="small"
                            sx={{
                                '& .MuiInputBase-root': {
                                    color: '#333',
                                    fontSize: '0.9rem',
                                    fontWeight: 'bold',
                                },
                                '& .MuiInputBase-input': {
                                    color: '#333',
                                    fontSize: '0.9rem',
                                    fontWeight: 'bold',
                                },
                                '& .MuiInput-underline:before': {
                                    borderBottomColor: '#ccc',
                                },
                                '& .MuiInput-underline:after': {
                                    borderBottomColor: '#1976d2',
                                },
                            }}
                            autoFocus
                        />
                    ) : (
                        <Typography
                            variant="body2"
                            sx={{
                                color: '#333',
                                fontSize: '0.4rem',
                                fontWeight: 'bold',
                                textAlign: 'left',
                                lineHeight: 1,
                                cursor: 'text',
                            }}
                        >
                            {editName}
                        </Typography>
                    )}
                </Box>
            </Paper>
        )
    );
};

export { CustomNode }; 