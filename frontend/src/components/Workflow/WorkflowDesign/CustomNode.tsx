import React, { memo, useState } from 'react';
import { Handle, Position, NodeProps } from '@xyflow/react';
import { Box, Typography, Paper, TextField } from '@mui/material';
import {
    PlayArrow as StartIcon,
    Circle as NormalIcon,
    Stop as EndIcon,
    AccountTree as ParallelIcon,
    CallSplit as ExclusiveIcon,
} from '@mui/icons-material';
import zIndex from '@mui/material/styles/zIndex';
import { transform } from 'lodash';

type NodeShape = 'rectangle' | 'ellipse' | 'diamond';

interface WorkflowNodeData {
    label: string;
    nodeType: string;
    properties?: {
        name: string;
        description: string;
        assignee: string;
        timeout: number;
        [key: string]: any;
    };
}


const CustomNode = ({ data, selected }: NodeProps) => {
    const [isEditing, setIsEditing] = useState(false);
    const [editName, setEditName] = useState((data as any)?.label || '节点');
    const [showHandles, setShowHandles] = useState(false);

    const getNodeIcon = (nodeType: string) => {
        switch (nodeType) {
            case 'start':
                return <StartIcon sx={{ fontSize: 12, color: '#4caf50' }} />;
            case 'end':
                return <EndIcon sx={{ fontSize: 12, color: '#f44336' }} />;
            case 'parallel':
                return <ParallelIcon sx={{ fontSize: 12, color: '#ff9800' }} />;
            case 'exclusive':
                return <ExclusiveIcon sx={{ fontSize: 12, color: '#9c27b0' }} />;
            default:
                return <NormalIcon sx={{ fontSize: 12, color: '#2196f3' }} />;
        }
    };

    const nodeType = (data as any)?.nodeType || 'normal';

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
        isDiamond ? (
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
                        border: selected ? '2px solid #1976d2' : '2px solid #ccc',
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
                elevation={selected ? 8 : 2}
                sx={{
                    width: 100,
                    height: 30,
                    backgroundColor: 'transparent',
                    border: selected ? '2px solid #1976d2' : '2px solid #ccc',
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