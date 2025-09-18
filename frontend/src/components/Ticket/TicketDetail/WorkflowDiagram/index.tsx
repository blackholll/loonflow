import React, { useState, useEffect } from 'react';
import WorkflowProcess from '../../../Workflow/WorkflowProcess';
import {
    ReactFlow,
    Node,
    Edge,
    useNodesState,
    useEdgesState,
    Controls,
    Background,
    NodeTypes,
    EdgeTypes,
    ReactFlowProvider,
    ConnectionMode
} from '@xyflow/react';
import { Box, Paper, Tooltip, Typography, CircularProgress, Alert } from '@mui/material';
import {
    PlayArrow as StartIcon,
    Stop as EndIcon,
    AccountTree as ParallelIcon,
    CallSplit as ExclusiveIcon,
    Timer as TimerIcon,
    Webhook as WebhookIcon,
    Circle as NormalIcon
} from '@mui/icons-material';
import '@xyflow/react/dist/style.css';

import { IWorkflowDiagram, IWorkflowNode, IWorkflowEdge } from '../../../../types/workflow';
import { getWorkflowDiagram } from '../../../../services/workflow';

// 自定义节点组件 - 只读模式
const ReadOnlyCustomNode = ({ data, selected }: any) => {
    const [showTooltip, setShowTooltip] = useState(false);

    const getNodeIcon = (nodeType: string, isIconOnlyNode: boolean = false) => {
        const fontSize = isIconOnlyNode ? 18 : 12;
        const iconProps = { sx: { fontSize } };

        switch (nodeType) {
            case 'start':
                return <StartIcon {...iconProps} sx={{ ...iconProps.sx, color: '#4caf50' }} />;
            case 'end':
                return <EndIcon {...iconProps} sx={{ ...iconProps.sx, color: '#f44336' }} />;
            case 'parallel':
                return <ParallelIcon {...iconProps} sx={{ ...iconProps.sx, color: '#ff9800' }} />;
            case 'exclusive':
                return <ExclusiveIcon {...iconProps} sx={{ ...iconProps.sx, color: '#9c27b0' }} />;
            case 'timer':
                return <TimerIcon {...iconProps} sx={{ ...iconProps.sx, color: '#2196f3' }} />;
            case 'hook':
                return <WebhookIcon {...iconProps} sx={{ ...iconProps.sx, color: '#2196f3' }} />;
            default:
                return <NormalIcon {...iconProps} sx={{ ...iconProps.sx, color: '#2196f3' }} />;
        }
    };

    const nodeType = data?.properties?.type || 'normal';
    const nodeName = data?.properties?.name || '节点';
    const isDiamond = nodeType === 'exclusive' || nodeType === 'parallel';
    const isIconOnly = nodeType === 'timer' || nodeType === 'hook';

    // 格式化属性信息用于 Tooltip
    const formatProperties = (properties: any) => {
        if (!properties) return '';

        const excludeKeys = ['name', 'type', 'label'];
        const filteredProps = Object.entries(properties)
            .filter(([key]) => !excludeKeys.includes(key))
            .filter(([, value]) => value !== null && value !== undefined && value !== '');

        if (filteredProps.length === 0) return '无额外属性';

        return filteredProps.map(([key, value]) => {
            let displayValue = value;
            if (typeof value === 'object') {
                displayValue = JSON.stringify(value);
            }
            return `${key}: ${displayValue}`;
        }).join('\n');
    };

    const tooltipContent = (
        <Box sx={{ p: 1 }}>
            <Typography variant="subtitle2" sx={{ fontWeight: 'bold', mb: 1 }}>
                节点信息
            </Typography>
            <Typography variant="body2" sx={{ mb: 0.5 }}>
                <strong>名称:</strong> {nodeName}
            </Typography>
            <Typography variant="body2" sx={{ mb: 0.5 }}>
                <strong>类型:</strong> {nodeType}
            </Typography>
            {formatProperties(data?.properties) !== '无额外属性' && (
                <Box sx={{ mt: 1 }}>
                    <Typography variant="body2" sx={{ fontWeight: 'bold', mb: 0.5 }}>
                        属性:
                    </Typography>
                    <Typography variant="body2" sx={{ whiteSpace: 'pre-line', fontSize: '0.75rem' }}>
                        {formatProperties(data?.properties)}
                    </Typography>
                </Box>
            )}
        </Box>
    );

    return (
        <Tooltip
            title={tooltipContent}
            open={showTooltip}
            onOpen={() => setShowTooltip(true)}
            onClose={() => setShowTooltip(false)}
            placement="top"
            arrow
        >
            <Box
                sx={{
                    cursor: 'pointer',
                    position: 'relative'
                }}
                onMouseEnter={() => setShowTooltip(true)}
                onMouseLeave={() => setShowTooltip(false)}
            >
                {isIconOnly ? (
                    // 纯图标节点
                    <Box
                        sx={{
                            width: 40,
                            height: 40,
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            borderRadius: '50%',
                            backgroundColor: selected ? '#e3f2fd' : '#f5f5f5',
                            border: selected ? '2px solid #1976d2' : '2px solid #ccc',
                            '&:hover': {
                                backgroundColor: '#e3f2fd',
                                border: '2px solid #1976d2',
                            },
                        }}
                    >
                        {getNodeIcon(nodeType, true)}
                    </Box>
                ) : isDiamond ? (
                    // 菱形节点
                    <Box
                        sx={{
                            width: 40,
                            height: 40,
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            border: selected ? '2px solid #1976d2' : '2px solid #ccc',
                            backgroundColor: 'transparent',
                            transform: 'rotate(45deg)',
                            '&:hover': {
                                border: '2px solid #1976d2',
                            },
                        }}
                    >
                        <Box sx={{ transform: 'rotate(-45deg)' }}>
                            {getNodeIcon(nodeType)}
                        </Box>
                    </Box>
                ) : (
                    // 普通矩形节点
                    <Paper
                        elevation={selected ? 8 : 2}
                        sx={{
                            width: 100,
                            height: 30,
                            backgroundColor: 'white',
                            border: selected ? '2px solid #1976d2' : '2px solid #ccc',
                            display: 'flex',
                            alignItems: 'center',
                            cursor: 'pointer',
                            '&:hover': {
                                elevation: 4,
                                border: '2px solid #1976d2',
                            },
                        }}
                    >
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
                            <Typography
                                variant="body2"
                                sx={{
                                    color: '#333',
                                    fontSize: '0.75rem',
                                    fontWeight: 'bold',
                                    textAlign: 'left',
                                    lineHeight: 1,
                                }}
                            >
                                {nodeName}
                            </Typography>
                        </Box>
                    </Paper>
                )}
            </Box>
        </Tooltip>
    );
};

// 自定义边组件 - 只读模式
const ReadOnlyCustomEdge = (props: any) => {
    const {
        id,
        sourceX,
        sourceY,
        targetX,
        targetY,
        sourcePosition,
        targetPosition,
        style = {},
        selected,
        data,
    } = props;
    const [showTooltip, setShowTooltip] = useState(false);

    // 计算边的路径
    const getSmoothStepPath = (params: any) => {
        const { sourceX, sourceY, targetX, targetY, sourcePosition, targetPosition } = params;

        let path = `M ${sourceX} ${sourceY}`;

        if (sourcePosition === 'right' && targetPosition === 'left') {
            const midX = (sourceX + targetX) / 2;
            path = `M ${sourceX} ${sourceY} L ${midX} ${sourceY} L ${midX} ${targetY} L ${targetX} ${targetY}`;
        } else if (sourcePosition === 'bottom' && targetPosition === 'top') {
            const midY = (sourceY + targetY) / 2;
            path = `M ${sourceX} ${sourceY} L ${sourceX} ${midY} L ${targetX} ${midY} L ${targetX} ${targetY}`;
        } else {
            path = `M ${sourceX} ${sourceY} L ${targetX} ${targetY}`;
        }

        const labelX = (sourceX + targetX) / 2;
        const labelY = (sourceY + targetY) / 2;

        return [path, labelX, labelY] as [string, number, number];
    };

    const [edgePath, labelX, labelY] = getSmoothStepPath({
        sourceX,
        sourceY,
        targetX,
        targetY,
        sourcePosition,
        targetPosition,
    });

    const arrowMarkerId = `arrow-${id}`;

    // 格式化边属性信息用于 Tooltip
    const formatEdgeProperties = (properties: any) => {
        if (!properties) return '';

        const excludeKeys = ['name', 'type', 'label'];
        const filteredProps = Object.entries(properties)
            .filter(([key]) => !excludeKeys.includes(key))
            .filter(([, value]) => value !== null && value !== undefined && value !== '');

        if (filteredProps.length === 0) return '无额外属性';

        return filteredProps.map(([key, value]) => {
            let displayValue = value;
            if (typeof value === 'object') {
                displayValue = JSON.stringify(value);
            }
            return `${key}: ${displayValue}`;
        }).join('\n');
    };

    const edgeName = data?.properties?.name || '';
    const tooltipContent = (
        <Box sx={{ p: 1 }}>
            <Typography variant="subtitle2" sx={{ fontWeight: 'bold', mb: 1 }}>
                连线信息
            </Typography>
            {edgeName && (
                <Typography variant="body2" sx={{ mb: 0.5 }}>
                    <strong>名称:</strong> {edgeName}
                </Typography>
            )}
            <Typography variant="body2" sx={{ mb: 0.5 }}>
                <strong>类型:</strong> {data?.properties?.type || 'other'}
            </Typography>
            {formatEdgeProperties(data?.properties) !== '无额外属性' && (
                <Box sx={{ mt: 1 }}>
                    <Typography variant="body2" sx={{ fontWeight: 'bold', mb: 0.5 }}>
                        属性:
                    </Typography>
                    <Typography variant="body2" sx={{ whiteSpace: 'pre-line', fontSize: '0.75rem' }}>
                        {formatEdgeProperties(data?.properties)}
                    </Typography>
                </Box>
            )}
        </Box>
    );

    return (
        <Tooltip
            title={tooltipContent}
            open={showTooltip}
            onOpen={() => setShowTooltip(true)}
            onClose={() => setShowTooltip(false)}
            placement="top"
            arrow
        >
            <g>
                <defs>
                    <marker
                        id={arrowMarkerId}
                        viewBox="0 0 10 10"
                        refX="8"
                        refY="5"
                        markerWidth="6"
                        markerHeight="6"
                        orient="auto"
                    >
                        <path d="M 0 0 L 10 5 L 0 10 z" fill={selected ? '#1976d2' : 'gray'} />
                    </marker>
                </defs>

                <path
                    id={id}
                    style={{
                        ...style,
                        strokeWidth: selected ? 2 : 1.5,
                        stroke: selected ? '#1976d2' : 'gray',
                        fill: 'none',
                        cursor: 'pointer',
                    }}
                    className="react-flow__edge-path"
                    d={edgePath}
                    markerEnd={`url(#${arrowMarkerId})`}
                    onMouseEnter={() => setShowTooltip(true)}
                    onMouseLeave={() => setShowTooltip(false)}
                />

                {/* 连线标签 */}
                {edgeName && (
                    <>
                        {/* 可悬浮的背景区域 */}
                        <rect
                            x={String(labelX - 50)}
                            y={String(labelY - 15)}
                            width="100"
                            height="30"
                            fill="transparent"
                            style={{ cursor: 'pointer' }}
                            onMouseEnter={() => setShowTooltip(true)}
                            onMouseLeave={() => setShowTooltip(false)}
                        />
                        {/* 文字标签 */}
                        <text
                            x={String(labelX)}
                            y={String(labelY)}
                            textAnchor="middle"
                            dominantBaseline="middle"
                            style={{
                                fontSize: '12px',
                                fontWeight: 'bold',
                                fill: selected ? '#1976d2' : 'gray',
                                cursor: 'pointer',
                                userSelect: 'none',
                                textShadow: '0 0 2px rgba(255, 255, 255, 0.8)',
                            }}
                            onMouseEnter={() => setShowTooltip(true)}
                            onMouseLeave={() => setShowTooltip(false)}
                        >
                            {edgeName}
                        </text>
                    </>
                )}
            </g>
        </Tooltip>
    );
};

// 节点和边类型定义
const nodeTypes: NodeTypes = {
    start: ReadOnlyCustomNode,
    normal: ReadOnlyCustomNode,
    end: ReadOnlyCustomNode,
    parallelGateway: ReadOnlyCustomNode,
    exclusiveGateway: ReadOnlyCustomNode,
    timer: ReadOnlyCustomNode,
    hook: ReadOnlyCustomNode,
};

const edgeTypes: EdgeTypes = {
    custom: ReadOnlyCustomEdge,
};

// 将 IWorkflowNode 转换为 React Flow Node
const convertWorkflowNodeToReactFlowNode = (workflowNode: IWorkflowNode): Node => {
    return {
        id: workflowNode.id,
        type: workflowNode.type,
        position: { x: workflowNode.layout.x, y: workflowNode.layout.y },
        data: {
            properties: {
                label: workflowNode.label,
                name: workflowNode.name,
                type: workflowNode.type,
                ...workflowNode.props
            }
        },
    };
};

// 将 IWorkflowEdge 转换为 React Flow Edge
const convertWorkflowEdgeToReactFlowEdge = (workflowEdge: IWorkflowEdge): Edge => {
    console.log('转换边数据:', workflowEdge);
    console.log('边 layout:', workflowEdge.layout);

    return {
        id: workflowEdge.id,
        source: workflowEdge.sourceNodeId,
        target: workflowEdge.targetNodeId,
        sourceHandle: workflowEdge.layout.souceHandle,
        targetHandle: workflowEdge.layout.targetHandle,
        type: 'custom',
        data: {
            properties: {
                name: workflowEdge.name,
                type: workflowEdge.type,
                label: workflowEdge.props.label,
                ...workflowEdge.props
            }
        },
        style: {
            strokeWidth: 2,
            stroke: '#555',
        },
    };
};

interface WorkflowDiagramProps {
    workflowId: string;
    workflowVersionId: string;
}

function WorkflowDiagram({ workflowId, workflowVersionId }: WorkflowDiagramProps) {
    const [workflowDiagram, setWorkflowDiagram] = useState<IWorkflowDiagram>();
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    // 初始化节点和边
    const initialNodes: Node[] = workflowDiagram?.nodeInfoList?.map(convertWorkflowNodeToReactFlowNode) || [];
    const initialEdges: Edge[] = workflowDiagram?.edgeInfoList?.map(convertWorkflowEdgeToReactFlowEdge) || [];

    const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
    const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

    useEffect(() => {
        const fetchWorkflowDiagram = async () => {
            try {
                setLoading(true);
                setError(null);
                const res = await getWorkflowDiagram(workflowId, workflowVersionId);
                if (res.code === 0) {
                    console.log('获取到的流程图数据:', res.data.processSchema);
                    setWorkflowDiagram(res.data.processSchema);
                } else {
                    setError('获取流程图数据失败');
                }
            } catch (err) {
                setError('获取流程图数据时发生错误');
                console.error('Error fetching workflow diagram:', err);
            } finally {
                setLoading(false);
            }
        };

        if (workflowId && workflowVersionId) {
            fetchWorkflowDiagram();
        }
    }, [workflowId, workflowVersionId]);

    // 当数据更新时，更新节点和边

    if (loading) {
        return (
            <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 400, flexDirection: 'column', gap: 2 }}>
                <CircularProgress />
                <Typography variant="body2" color="text.secondary">加载流程图中...</Typography>
            </Box>
        );
    }

    if (error) {
        return (
            <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 400 }}>
                <Alert severity="error" sx={{ maxWidth: 400 }}>
                    {error}
                </Alert>
            </Box>
        );
    }

    if (!workflowDiagram || (workflowDiagram.nodeInfoList.length === 0 && workflowDiagram.edgeInfoList.length === 0)) {
        return (
            <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 400 }}>
                <Alert severity="info" sx={{ maxWidth: 400 }}>
                    暂无流程图数据
                </Alert>
            </Box>
        );
    }

    return (
        <WorkflowProcess
            processSchema={workflowDiagram}
            key="workflow-process"
            simpleViewMode={true}
        />
    );
}

export default WorkflowDiagram;
