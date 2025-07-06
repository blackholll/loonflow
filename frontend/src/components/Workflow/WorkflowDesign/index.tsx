import React, { useState, useCallback, useRef } from 'react';
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
    NodeTypes,
    EdgeTypes,
    ReactFlowProvider,
    ConnectionMode
} from '@xyflow/react';
import { Box, Paper, Drawer, IconButton, Tooltip, Divider, Snackbar, Alert } from '@mui/material';
import {
    Clear as ClearIcon,
    Undo as UndoIcon,
    Redo as RedoIcon,
    Delete as DeleteIcon,
    ContentCopy as CopyIcon,
} from '@mui/icons-material';
import '@xyflow/react/dist/style.css';

import NodePanel from './NodePanel';
import Toolbar from './Toolbar';
import PropertyPanel from './PropertyPanel';
import { CustomNode } from './CustomNode';
import { CustomEdge } from './CustomEdge';

// 节点类型定义 - 将在组件内部定义

// 边类型定义
const edgeTypes: EdgeTypes = {
    custom: CustomEdge,
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
            properties: {
                name: '开始节点',
                description: '流程的起始点',
                assignee: '',
                timeout: 0,
            }
        },
    },
];

// 初始边
const initialEdges: Edge[] = [];

const WorkflowDesign: React.FC = () => {
    const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
    const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
    const [selectedElement, setSelectedElement] = useState<Node | Edge | null>(null);
    const [propertyPanelOpen, setPropertyPanelOpen] = useState(false);
    const [snackbarOpen, setSnackbarOpen] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState('');
    const [snackbarSeverity, setSnackbarSeverity] = useState<'error' | 'warning' | 'info' | 'success'>('error');
    const reactFlowWrapper = useRef<HTMLDivElement>(null);

    // 节点类型定义
    const nodeTypes: NodeTypes = {
        startNode: (props: any) => <CustomNode {...props} />,
        normalNode: (props: any) => <CustomNode {...props} />,
        endNode: (props: any) => <CustomNode {...props} />,
        parallelGateway: (props: any) => <CustomNode {...props} />,
        exclusiveGateway: (props: any) => <CustomNode {...props} />,
        timerNode: (props: any) => <CustomNode {...props} />,
        hookNode: (props: any) => <CustomNode {...props} />,
    };

    // 连接处理
    const onConnect = useCallback(
        (params: Connection) => {
            console.log('onConnect 被调用:', params);

            // 验证连接是否有效
            if (!params.source || !params.target) {
                console.log('连接参数无效:', params);
                return;
            }

            // 验证只能从 source 类型的 Handle 发起连线
            if (!params.sourceHandle) {
                console.log('必须从 source 类型的 Handle 发起连线');
                return;
            }

            // 验证只能连接到 target 类型的 Handle
            if (!params.targetHandle) {
                console.log('必须连接到 target 类型的 Handle');
                return;
            }

            // 额外验证：确保连接方向正确
            // 通过检查 Handle 的样式来验证类型（绿色 = source，红色 = target）
            const sourceNode = nodes.find(node => node.id === params.source);
            const targetNode = nodes.find(node => node.id === params.target);

            if (!sourceNode || !targetNode) {
                console.log('找不到源节点或目标节点');
                return;
            }

            // 使用React Flow的addEdge函数创建连线
            const newEdge: Edge = {
                ...params,
                id: `edge-${params.source}-${params.sourceHandle}-${params.target}-${params.targetHandle}-${Date.now()}`,
                type: 'custom',
                data: {
                    label: '',
                    properties: {
                        name: '',
                        condition: '',
                        description: '',
                    }
                },
                style: {
                    strokeWidth: 2,
                    stroke: '#555',
                },
            };

            console.log('创建新连线:', newEdge);
            setEdges((eds) => addEdge(newEdge, eds));
        },
        [setEdges, nodes]
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

    // 监听连线标签点击事件
    React.useEffect(() => {
        const handleEdgeLabelClick = (event: CustomEvent) => {
            const edgeId = event.detail.edgeId;
            const edge = edges.find(e => e.id === edgeId);
            if (edge) {
                setSelectedElement(edge);
                setPropertyPanelOpen(true);
            }
        };

        document.addEventListener('edgeLabelClick', handleEdgeLabelClick as EventListener);

        return () => {
            document.removeEventListener('edgeLabelClick', handleEdgeLabelClick as EventListener);
        };
    }, [edges]);

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
                properties: {
                    name: nodeData.label,
                    description: '',
                    assignee: '',
                    timeout: 0,
                    ...nodeData.properties,
                }
            },
        };
        setNodes((nds) => [...nds, newNode]);
    }, [setNodes]);

    // 更新节点属性
    const onUpdateNodeProperties = useCallback((nodeId: string, properties: any) => {
        setNodes((nds) =>
            nds.map((node) =>
                node.id === nodeId
                    ? {
                        ...node,
                        data: {
                            ...node.data,
                            properties,
                            // 如果修改了 name 属性，同时更新 label
                            ...(properties.name && { label: properties.name })
                        }
                    }
                    : node
            )
        );
    }, [setNodes]);

    // 更新边属性
    const onUpdateEdgeProperties = useCallback((edgeId: string, properties: any) => {
        setEdges((eds) =>
            eds.map((edge) =>
                edge.id === edgeId
                    ? { ...edge, data: { ...edge.data, properties } }
                    : edge
            )
        );
    }, [setEdges]);

    // 工具栏操作
    const handleClear = useCallback(() => {
        setNodes([]);
        setEdges([]);
        setSelectedElement(null);
        setPropertyPanelOpen(false);
    }, [setNodes, setEdges]);

    const handleUndo = useCallback(() => {
        // 实现撤销功能
        console.log('撤销');
    }, []);

    const handleRedo = useCallback(() => {
        // 实现重做功能
        console.log('重做');
    }, []);

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

    const handleCopy = useCallback(() => {
        if (selectedElement) {
            // 实现复制功能
            console.log('复制', selectedElement);
        }
    }, [selectedElement]);

    return (
        <ReactFlowProvider>
            <Box sx={{ display: 'flex', height: '100vh', width: '100vw' }}>
                {/* 左侧节点面板 */}
                <Box sx={{ width: 280, borderRight: 1, borderColor: 'divider' }}>
                    <NodePanel onAddNode={onAddNode} />
                </Box>

                {/* 主要内容区域 */}
                <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
                    {/* 顶部工具栏 */}
                    <Toolbar
                        onClear={handleClear}
                        onUndo={handleUndo}
                        onRedo={handleRedo}
                        onDelete={handleDelete}
                        onCopy={handleCopy}
                        canDelete={!!selectedElement}
                        canCopy={!!selectedElement}
                    />

                    {/* 流程图画布 */}
                    <Box sx={{ flex: 1, position: 'relative' }} ref={reactFlowWrapper}>
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
                            edgeTypes={edgeTypes}
                            connectionMode={ConnectionMode.Loose}
                            // isValidConnection={isValidConnection}
                            fitView
                            attributionPosition="bottom-left"
                            snapToGrid={true}
                            snapGrid={[15, 15]}
                            onInit={(reactFlowInstance) => {
                                console.log('ReactFlow 初始化完成:', reactFlowInstance);
                            }}
                            onLoad={(reactFlowInstance) => {
                                console.log('ReactFlow 加载完成:', reactFlowInstance);
                            }}
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
                    <PropertyPanel
                        element={selectedElement}
                        onUpdateNodeProperties={onUpdateNodeProperties}
                        onUpdateEdgeProperties={onUpdateEdgeProperties}
                    />
                </Drawer>
            </Box>

            {/* 提示信息 Snackbar */}
            <Snackbar
                open={snackbarOpen}
                autoHideDuration={3000}
                onClose={() => setSnackbarOpen(false)}
                anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
            >
                <Alert
                    onClose={() => setSnackbarOpen(false)}
                    severity={snackbarSeverity}
                    sx={{ width: '100%' }}
                >
                    {snackbarMessage}
                </Alert>
            </Snackbar>
        </ReactFlowProvider>
    );
};

export default WorkflowDesign; 