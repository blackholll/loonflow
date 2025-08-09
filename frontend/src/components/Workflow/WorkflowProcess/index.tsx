import React, { useState, useCallback, useRef, useEffect, useMemo } from 'react';
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
    ConnectionMode,
    NodeChange,
    EdgeChange
} from '@xyflow/react';
import { Box, Paper, Drawer, IconButton, Tooltip, Divider, Snackbar, Alert } from '@mui/material';
import '@xyflow/react/dist/style.css';

import NodePanel from './NodePanel';
import Toolbar from './Toolbar';
import PropertyPanel from './PropertyPanel';
import { CustomNode } from './CustomNode';
import { CustomEdge } from './CustomEdge';
import { IProcessSchema, IWorkflowNode, IWorkflowEdge, IFormSchema } from '../../../types/workflow';
import { v4 as uuidv4 } from 'uuid';

// edge definition, move to the outside of the component to avoid re-creation
const edgeTypes: EdgeTypes = {
    custom: CustomEdge,
};

// move to the outside of the component to avoid re-creation
const nodeTypes: NodeTypes = {
    start: (props: any) => <CustomNode {...props} />,
    normal: (props: any) => <CustomNode {...props} />,
    end: (props: any) => <CustomNode {...props} />,
    parallelGateway: (props: any) => <CustomNode {...props} />,
    exclusiveGateway: (props: any) => <CustomNode {...props} />,
    timer: (props: any) => <CustomNode {...props} />,
    hook: (props: any) => <CustomNode {...props} />,
};

// 将 IWorkflowNode 转换为 React Flow Node
const convertWorkflowNodeToReactFlowNode = (workflowNode: IWorkflowNode): Node => {
    console.log(' workflowNode.type workflowNode.type:', workflowNode)
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

const convertReactFlowNodeToWorkflowNode = (node: Node): IWorkflowNode => {
    const properties: any = node.data.properties || {};
    const workflowNodeName = properties.name || '';
    const workflowLabel = properties.label || {};
    const { name, label, ...workflowProps } = properties;

    return {
        id: node.id,
        type: node.type as 'start' | 'end' | 'common' | 'parallel' | 'exclusive' | 'timer' | 'hook',
        name: workflowNodeName,
        label: workflowLabel,
        layout: {
            x: node.position.x,
            y: node.position.y,
        },
        props: workflowProps
    };
};

// 将 React Flow Edge 转换为 IWorkflowEdge
const convertReactFlowEdgeToWorkflowEdge = (edge: Edge): IWorkflowEdge => {
    const properties: any = edge.data?.properties || {};
    return {
        id: edge.id,
        name: properties.name || edge.data?.label || '',
        type: properties.type || 'other',
        sourceNodeId: edge.source,
        targetNodeId: edge.target,
        label: properties.label,
        props: {
            validateField: false,
            condition: properties.condition || '',
            confirmMessage: '',
            ...properties
        },
        layout: {
            souceHandle: edge.sourceHandle || '',
            targetHandle: edge.targetHandle || '',
        }
    };
};

interface WorkflowProcessProps {
    processSchema?: IProcessSchema;
    formSchema?: IFormSchema;
    onProcessSchemaChange?: (processSchema: IProcessSchema) => void;
}

function WorkflowProcess({
    processSchema = { nodeInfoList: [], edgeInfoList: [] },
    formSchema = { componentInfoList: [] },
    onProcessSchemaChange
}: WorkflowProcessProps) {
    // 初始化节点和边
    const initialNodes: Node[] = processSchema.nodeInfoList.map(convertWorkflowNodeToReactFlowNode);
    const initialEdges: Edge[] = processSchema.edgeInfoList.map(convertWorkflowEdgeToReactFlowEdge);
    const [currentFormSchema, setCurrentFormSchema] = useState<IFormSchema>(formSchema);

    const [nodes, setNodes, onNodesChangeBase] = useNodesState(initialNodes);
    const [edges, setEdges, onEdgesChangeBase] = useEdgesState(initialEdges);
    const [selectedElement, setSelectedElement] = useState<Node | Edge | null>(null);
    const [propertyPanelOpen, setPropertyPanelOpen] = useState(false);
    const [snackbarOpen, setSnackbarOpen] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState('');
    const [snackbarSeverity, setSnackbarSeverity] = useState<'error' | 'warning' | 'info' | 'success'>('error');
    const reactFlowWrapper = useRef<HTMLDivElement>(null);

    // 撤销重做历史记录
    const [history, setHistory] = useState<Array<{ nodes: Node[]; edges: Edge[] }>>([
        { nodes: initialNodes, edges: initialEdges }
    ]);
    const [historyIndex, setHistoryIndex] = useState(0);

    useEffect(() => {
        setCurrentFormSchema(formSchema);
        console.log('formSchema22222222', formSchema);
    }, [formSchema]);


    // 保存历史记录
    const saveToHistory = useCallback((newNodes: Node[], newEdges: Edge[]) => {
        const newHistoryEntry = { nodes: newNodes, edges: newEdges };
        setHistory(prev => {
            // 移除当前位置之后的历史记录
            const newHistory = prev.slice(0, historyIndex + 1);
            // 添加新的历史记录
            newHistory.push(newHistoryEntry);
            // 限制历史记录数量，避免内存泄漏
            if (newHistory.length > 50) {
                newHistory.shift();
            }
            return newHistory;
        });
        setHistoryIndex(prev => prev + 1);
    }, [historyIndex]);

    // 通知父组件数据变化
    const notifyParentChange = useCallback((newNodes: Node[], newEdges: Edge[]) => {
        if (onProcessSchemaChange) {
            const newProcessSchema: IProcessSchema = {
                nodeInfoList: newNodes.map(convertReactFlowNodeToWorkflowNode),
                edgeInfoList: newEdges.map(convertReactFlowEdgeToWorkflowEdge)
            };
            onProcessSchemaChange(newProcessSchema);
        }
    }, [onProcessSchemaChange]);

    // 自定义节点变化处理，添加通知父组件的逻辑
    const onNodesChange = useCallback((changes: NodeChange[]) => {
        onNodesChangeBase(changes);
        // 延迟通知父组件，避免频繁更新
        setTimeout(() => {
            notifyParentChange(nodes, edges);
        }, 100);
    }, [onNodesChangeBase, nodes, edges, notifyParentChange]);

    // 自定义边变化处理，添加通知父组件的逻辑
    const onEdgesChange = useCallback((changes: EdgeChange[]) => {
        onEdgesChangeBase(changes);
        // 延迟通知父组件，避免频繁更新
        setTimeout(() => {
            notifyParentChange(nodes, edges);
        }, 100);
    }, [onEdgesChangeBase, nodes, edges, notifyParentChange]);



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
                id: `temp_${uuidv4()}`,
                type: 'custom',
                data: {
                    properties: {
                        name: '同意',
                        condition: '',
                        type: 'accept'
                    }
                },
                style: {
                    strokeWidth: 2,
                    stroke: '#555',
                },
            };

            console.log('创建新连线:', newEdge);
            setEdges((eds) => {
                const newEdges = addEdge(newEdge, eds);
                saveToHistory(nodes, newEdges);
                notifyParentChange(nodes, newEdges);
                return newEdges;
            });
        },
        [setEdges, nodes, saveToHistory, notifyParentChange]
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
            id: `temp_${uuidv4()}`,
            type: nodeType,
            position: { x: 100, y: 100 },
            data: {
                ...nodeData,
                properties: {
                    name: nodeData.properties.name ?? '',
                    description: '',
                    assignee: '',
                    ...nodeData.properties,
                }
            },
        };
        setNodes((nds) => {
            const newNodes = [...nds, newNode];
            saveToHistory(newNodes, edges);
            notifyParentChange(newNodes, edges);
            return newNodes;
        });
    }, [setNodes, edges, saveToHistory, notifyParentChange]);

    // 更新节点属性
    const onUpdateNodeProperties = useCallback((nodeId: string, properties: any) => {
        console.log('onUpdateNodeProperties:', nodeId, properties);
        setNodes((nds) => {
            const newNodes = nds.map((node) =>
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
            );
            saveToHistory(newNodes, edges);
            notifyParentChange(newNodes, edges);
            return newNodes;
        });
    }, [setNodes, edges, saveToHistory, notifyParentChange]);

    // 更新边属性
    const onUpdateEdgeProperties = useCallback((edgeId: string, properties: any) => {
        setEdges((eds) => {
            const newEdges = eds.map((edge) =>
                edge.id === edgeId
                    ? { ...edge, data: { ...edge.data, properties } }
                    : edge
            );
            saveToHistory(nodes, newEdges);
            notifyParentChange(nodes, newEdges);
            return newEdges;
        });
    }, [setEdges, nodes, saveToHistory, notifyParentChange]);

    // 工具栏操作
    const handleClear = useCallback(() => {
        setNodes([]);
        setEdges([]);
        setSelectedElement(null);
        setPropertyPanelOpen(false);
        notifyParentChange([], []);
    }, [setNodes, setEdges, notifyParentChange]);

    const handleUndo = useCallback(() => {
        if (historyIndex > 0) {
            const newIndex = historyIndex - 1;
            const historyEntry = history[newIndex];
            setNodes(historyEntry.nodes);
            setEdges(historyEntry.edges);
            setHistoryIndex(newIndex);
            setSelectedElement(null);
            setPropertyPanelOpen(false);
            notifyParentChange(historyEntry.nodes, historyEntry.edges);
        }
    }, [historyIndex, history, setNodes, setEdges, notifyParentChange]);

    const handleRedo = useCallback(() => {
        if (historyIndex < history.length - 1) {
            const newIndex = historyIndex + 1;
            const historyEntry = history[newIndex];
            setNodes(historyEntry.nodes);
            setEdges(historyEntry.edges);
            setHistoryIndex(newIndex);
            setSelectedElement(null);
            setPropertyPanelOpen(false);
            notifyParentChange(historyEntry.nodes, historyEntry.edges);
        }
    }, [historyIndex, history, setNodes, setEdges, notifyParentChange]);

    const handleDelete = useCallback(() => {
        if (selectedElement) {
            if ('source' in selectedElement) {
                // 删除边
                setEdges((eds) => {
                    const newEdges = eds.filter((edge) => edge.id !== selectedElement.id);
                    saveToHistory(nodes, newEdges);
                    notifyParentChange(nodes, newEdges);
                    return newEdges;
                });
            } else {
                // 删除节点和相关的边
                const nodeId = selectedElement.id;
                setNodes((nds) => {
                    const newNodes = nds.filter((node) => node.id !== nodeId);
                    setEdges((eds) => {
                        const newEdges = eds.filter((edge) =>
                            edge.source !== nodeId && edge.target !== nodeId
                        );
                        saveToHistory(newNodes, newEdges);
                        notifyParentChange(newNodes, newEdges);
                        return newEdges;
                    });
                    return newNodes;
                });
            }
            setSelectedElement(null);
            setPropertyPanelOpen(false);
        }
    }, [selectedElement, setNodes, setEdges, nodes, saveToHistory, notifyParentChange]);

    const handleCopy = useCallback(() => {
        if (selectedElement) {
            if ('source' in selectedElement) {
                // 复制边
                const newEdge: Edge = {
                    ...selectedElement,
                    id: `temp_${uuidv4()}`,
                    source: selectedElement.source,
                    target: selectedElement.target,
                    data: {
                        ...selectedElement.data,
                        properties: {
                            ...(selectedElement.data?.properties || {}),
                            name: `${(selectedElement.data?.properties as any)?.name || '连线'} (副本)`,
                        }
                    }
                };
                setEdges((eds) => {
                    const newEdges = [...eds, newEdge];
                    saveToHistory(nodes, newEdges);
                    notifyParentChange(nodes, newEdges);
                    return newEdges;
                });
            } else {
                // 复制节点
                const newNode: Node = {
                    ...selectedElement,
                    id: `temp_${uuidv4()}`,
                    position: {
                        x: selectedElement.position.x + 50,
                        y: selectedElement.position.y + 50,
                    },
                    data: {
                        ...selectedElement.data,
                        properties: {
                            ...(selectedElement.data?.properties || {}),
                            name: `${(selectedElement.data?.properties as any)?.name || '节点'} (副本)`,
                        }
                    }
                };
                setNodes((nds) => {
                    const newNodes = [...nds, newNode];
                    saveToHistory(newNodes, edges);
                    notifyParentChange(newNodes, edges);
                    return newNodes;
                });
            }
            setSelectedElement(null);
            setPropertyPanelOpen(false);
        }
    }, [selectedElement, setNodes, setEdges, nodes, edges, saveToHistory, notifyParentChange]);


    const propertyPanelComponent = useMemo(() => (
        <PropertyPanel
            element={selectedElement}
            formSchema={currentFormSchema}
            onUpdateNodeProperties={onUpdateNodeProperties}
            onUpdateEdgeProperties={onUpdateEdgeProperties}
        />
    ), [currentFormSchema, onUpdateNodeProperties, onUpdateEdgeProperties, selectedElement]);


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
                        canUndo={historyIndex > 0}
                        canRedo={historyIndex < history.length - 1}
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
                            width: 450,
                            boxSizing: 'border-box',
                        },
                    }}
                >
                    {propertyPanelComponent}
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

export default WorkflowProcess; 