import React, { useState, useCallback } from 'react';
import {
    ReactFlow,
    Node,
    Edge,
    addEdge,
    Connection,
    useNodesState,
    useEdgesState,
    Controls,
    Background,
    ReactFlowProvider,
} from '@xyflow/react';
import { Box, Paper, Drawer, Typography, Button } from '@mui/material';
import '@xyflow/react/dist/style.css';

// 简化的节点组件
const SimpleNode: React.FC<any> = ({ data, selected }) => {
    const getNodeColor = (nodeType: string) => {
        switch (nodeType) {
            case 'start':
                return '#4caf50';
            case 'end':
                return '#f44336';
            case 'parallel':
                return '#ff9800';
            case 'exclusive':
                return '#9c27b0';
            default:
                return '#2196f3';
        }
    };

    const nodeType = data?.nodeType || 'normal';
    const color = getNodeColor(nodeType);

    return (
        <Paper
            elevation={selected ? 8 : 2}
            sx={{
                width: 120,
                height: 60,
                backgroundColor: color,
                border: selected ? '2px solid #1976d2' : '2px solid transparent',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                cursor: 'pointer',
            }}
        >
            <Typography
                variant="body2"
                sx={{
                    color: 'white',
                    fontWeight: 'bold',
                    textAlign: 'center',
                }}
            >
                {data?.label || '节点'}
            </Typography>
        </Paper>
    );
};

// 节点类型定义
const nodeTypes = {
    startNode: SimpleNode,
    normalNode: SimpleNode,
    endNode: SimpleNode,
    parallelGateway: SimpleNode,
    exclusiveGateway: SimpleNode,
};

// 初始节点
const initialNodes: Node[] = [
    {
        id: '1',
        type: 'startNode',
        position: { x: 250, y: 100 },
        data: {
            label: '开始节点',
            nodeType: 'start',
        },
    },
];

// 初始边
const initialEdges: Edge[] = [];

const SimpleFlowEditor: React.FC = () => {
    const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
    const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
    const [selectedElement, setSelectedElement] = useState<Node | Edge | null>(null);
    const [propertyPanelOpen, setPropertyPanelOpen] = useState(false);

    // 连接处理
    const onConnect = useCallback(
        (params: Connection) => {
            setEdges((eds) => addEdge(params, eds));
        },
        [setEdges]
    );

    // 节点选择处理
    const onNodeClick = useCallback((event: React.MouseEvent, node: Node) => {
        setSelectedElement(node);
        setPropertyPanelOpen(true);
    }, []);

    // 边选择处理
    const onEdgeClick = useCallback((event: React.MouseEvent, edge: Edge) => {
        setSelectedElement(edge);
        setPropertyPanelOpen(true);
    }, []);

    // 画布点击处理
    const onPaneClick = useCallback(() => {
        setSelectedElement(null);
        setPropertyPanelOpen(false);
    }, []);

    // 添加节点
    const onAddNode = useCallback((nodeType: string, nodeData: any) => {
        const newNode: Node = {
            id: `${nodeType}-${Date.now()}`,
            type: nodeType,
            position: { x: 100, y: 100 },
            data: {
                ...nodeData,
            },
        };
        setNodes((nds) => [...nds, newNode]);
    }, [setNodes]);

    // 清空画布
    const handleClear = useCallback(() => {
        setNodes([]);
        setEdges([]);
        setSelectedElement(null);
        setPropertyPanelOpen(false);
    }, [setNodes, setEdges]);

    // 删除选中元素
    const handleDelete = useCallback(() => {
        if (selectedElement) {
            if ('source' in selectedElement) {
                // 删除边
                setEdges((eds) => eds.filter((edge) => edge.id !== selectedElement.id));
            } else {
                // 删除节点
                setNodes((nds) => nds.filter((node) => node.id !== selectedElement.id));
                // 同时删除相关的边
                setEdges((eds) => eds.filter((edge) =>
                    edge.source !== selectedElement.id && edge.target !== selectedElement.id
                ));
            }
            setSelectedElement(null);
            setPropertyPanelOpen(false);
        }
    }, [selectedElement, setNodes, setEdges]);

    return (
        <ReactFlowProvider>
            <Box sx={{ display: 'flex', height: '100vh', width: '100vw' }}>
                {/* 左侧节点面板 */}
                <Box sx={{ width: 280, borderRight: 1, borderColor: 'divider', p: 2 }}>
                    <Typography variant="h6" gutterBottom>
                        节点库
                    </Typography>

                    <Box sx={{ mb: 2 }}>
                        <Typography variant="subtitle2" gutterBottom>
                            基础节点
                        </Typography>
                        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                            <Button
                                variant="outlined"
                                size="small"
                                onClick={() => onAddNode('startNode', { label: '开始节点', nodeType: 'start' })}
                            >
                                开始节点
                            </Button>
                            <Button
                                variant="outlined"
                                size="small"
                                onClick={() => onAddNode('normalNode', { label: '普通节点', nodeType: 'normal' })}
                            >
                                普通节点
                            </Button>
                            <Button
                                variant="outlined"
                                size="small"
                                onClick={() => onAddNode('endNode', { label: '结束节点', nodeType: 'end' })}
                            >
                                结束节点
                            </Button>
                        </Box>
                    </Box>

                    <Box>
                        <Typography variant="subtitle2" gutterBottom>
                            网关节点
                        </Typography>
                        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                            <Button
                                variant="outlined"
                                size="small"
                                onClick={() => onAddNode('parallelGateway', { label: '并行网关', nodeType: 'parallel' })}
                            >
                                并行网关
                            </Button>
                            <Button
                                variant="outlined"
                                size="small"
                                onClick={() => onAddNode('exclusiveGateway', { label: '排他网关', nodeType: 'exclusive' })}
                            >
                                排他网关
                            </Button>
                        </Box>
                    </Box>
                </Box>

                {/* 主要内容区域 */}
                <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
                    {/* 顶部工具栏 */}
                    <Box sx={{ p: 2, borderBottom: 1, borderColor: 'divider', display: 'flex', gap: 1 }}>
                        <Button
                            variant="outlined"
                            size="small"
                            onClick={handleClear}
                        >
                            清空
                        </Button>
                        <Button
                            variant="outlined"
                            size="small"
                            onClick={handleDelete}
                            disabled={!selectedElement}
                        >
                            删除
                        </Button>
                    </Box>

                    {/* 流程图画布 */}
                    <Box sx={{ flex: 1, position: 'relative' }}>
                        <ReactFlow
                            nodes={nodes}
                            edges={edges}
                            onNodesChange={onNodesChange}
                            onEdgesChange={onEdgesChange}
                            onConnect={onConnect}
                            onNodeClick={onNodeClick}
                            onEdgeClick={onEdgeClick}
                            onPaneClick={onPaneClick}
                            nodeTypes={nodeTypes}
                            fitView
                            attributionPosition="bottom-left"
                        >
                            <Controls />
                            <Background color="#aaa" gap={16} />
                        </ReactFlow>
                    </Box>
                </Box>

                {/* 右侧属性面板 */}
                <Drawer
                    anchor="right"
                    open={propertyPanelOpen}
                    onClose={() => setPropertyPanelOpen(false)}
                    sx={{
                        '& .MuiDrawer-paper': {
                            width: 320,
                            boxSizing: 'border-box',
                        },
                    }}
                >
                    <Box sx={{ p: 2 }}>
                        <Typography variant="h6" gutterBottom>
                            属性面板
                        </Typography>
                        {selectedElement && (
                            <Typography variant="body2">
                                选中元素: {('source' in selectedElement ? '连线' : '节点')} - {selectedElement.id}
                            </Typography>
                        )}
                    </Box>
                </Drawer>
            </Box>
        </ReactFlowProvider>
    );
};

export default SimpleFlowEditor; 