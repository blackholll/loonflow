import { Alert, Box, Drawer, Snackbar } from '@mui/material';
import {
    addEdge,
    Background,
    Connection,
    ConnectionMode,
    Controls,
    Edge,
    EdgeChange,
    EdgeTypes,
    Node,
    NodeChange,
    NodeTypes,
    ReactFlow,
    ReactFlowProvider,
    useEdgesState,
    useNodesState
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';

import { useTranslation } from 'react-i18next';
import { v4 as uuidv4 } from 'uuid';
import { IFormSchema, IProcessSchema, IWorkflowEdge, IWorkflowNode } from '../../../types/workflow';
import { CustomEdge } from './CustomEdge';
import { CustomNode } from './CustomNode';
import NodePanel from './NodePanel';
import PropertyPanel from './PropertyPanel';
import Toolbar from './Toolbar';

// edge definition, move to the outside of the component to avoid re-creation
const edgeTypes: EdgeTypes = {
    custom: CustomEdge,
};

// move to the outside of the component to avoid re-creation
const nodeTypes: NodeTypes = {
    start: (props: any) => <CustomNode {...props} />,
    normal: (props: any) => <CustomNode {...props} />,
    end: (props: any) => <CustomNode {...props} />,
    parallel: (props: any) => <CustomNode {...props} />,
    exclusive: (props: any) => <CustomNode {...props} />,
    timer: (props: any) => <CustomNode {...props} />,
    hook: (props: any) => <CustomNode {...props} />,
};

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
        type: node.type as 'start' | 'end' | 'normal' | 'parallel' | 'exclusive' | 'timer' | 'hook',
        name: workflowNodeName,
        label: workflowLabel,
        layout: {
            x: node.position.x,
            y: node.position.y,
        },
        props: workflowProps
    };
};

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
    simpleViewMode?: boolean;
    selectedNodeIds?: string[];
    onProcessSchemaChange?: (processSchema: IProcessSchema) => void;
}

function WorkflowProcess({
    processSchema = { nodeInfoList: [], edgeInfoList: [] },
    formSchema = { componentInfoList: [] },
    simpleViewMode = false,
    selectedNodeIds = [],
    onProcessSchemaChange
}: WorkflowProcessProps) {
    const initialNodes: Node[] = processSchema.nodeInfoList.map(convertWorkflowNodeToReactFlowNode);
    const initialEdges: Edge[] = processSchema.edgeInfoList.map(convertWorkflowEdgeToReactFlowEdge);
    const [currentFormSchema, setCurrentFormSchema] = useState<IFormSchema>(formSchema);

    const [nodes, setNodes, onNodesChangeBase] = useNodesState(initialNodes);
    const [edges, setEdges, onEdgesChangeBase] = useEdgesState(initialEdges);
    const [selectedElement, setSelectedElement] = useState<Node | Edge | null>(null);
    const [propertyPanelOpen, setPropertyPanelOpen] = useState(false);
    const [snackbarOpen, setSnackbarOpen] = useState(false);
    const [snackbarMessage] = useState('');
    const [snackbarSeverity] = useState<'error' | 'warning' | 'info' | 'success'>('error');
    const reactFlowWrapper = useRef<HTMLDivElement>(null);
    const { t } = useTranslation();

    // hover tooltip state (only enabled in simpleViewMode) 
    const [hoverTooltip, setHoverTooltip] = useState<{
        visible: boolean;
        x: number;
        y: number;
        title: string;
        lines: string[];
    }>({ visible: false, x: 0, y: 0, title: '', lines: [] });

    // undo redo history
    const [history, setHistory] = useState<Array<{ nodes: Node[]; edges: Edge[] }>>([
        { nodes: initialNodes, edges: initialEdges }
    ]);
    const [historyIndex, setHistoryIndex] = useState(0);

    useEffect(() => {
        setCurrentFormSchema(formSchema);
    }, [formSchema]);

    // use isCurrent to mark the current workflow node, decouple from the interactive selected state
    useEffect(() => {
        const key = Array.isArray(selectedNodeIds) ? selectedNodeIds.join(',') : '';
        if (!key) {
            return;
        }
        setNodes((nds) => {
            let changed = false;
            const updated = nds.map((n) => {
                const nextIsCurrent = !!(selectedNodeIds && selectedNodeIds.includes(n.id));
                const prevIsCurrent = !!((n.data as any)?.properties?.isCurrent);
                if (nextIsCurrent !== prevIsCurrent) {
                    changed = true;
                    return {
                        ...n,
                        data: {
                            ...n.data,
                            properties: {
                                ...(n.data as any)?.properties,
                                isCurrent: nextIsCurrent
                            }
                        }
                    };
                }
                return n;
            });
            return changed ? updated : nds;
        });
    }, [selectedNodeIds, setNodes]);


    // save history
    const saveToHistory = useCallback((newNodes: Node[], newEdges: Edge[]) => {
        const newHistoryEntry = { nodes: newNodes, edges: newEdges };
        setHistory(prev => {
            // remove the history after the current position
            const newHistory = prev.slice(0, historyIndex + 1);
            // add the new history
            newHistory.push(newHistoryEntry);
            // limit the history length, avoid memory leak
            if (newHistory.length > 50) {
                newHistory.shift();
            }
            return newHistory;
        });
        setHistoryIndex(prev => prev + 1);
    }, [historyIndex]);

    // notify the parent component of the data change
    const notifyParentChange = useCallback((newNodes: Node[], newEdges: Edge[]) => {
        if (onProcessSchemaChange) {
            const newProcessSchema: IProcessSchema = {
                nodeInfoList: newNodes.map(convertReactFlowNodeToWorkflowNode),
                edgeInfoList: newEdges.map(convertReactFlowEdgeToWorkflowEdge)
            };
            onProcessSchemaChange(newProcessSchema);
        }
    }, [onProcessSchemaChange]);

    // custom node change handling, add the logic to notify the parent component
    const onNodesChange = useCallback((changes: NodeChange[]) => {
        const processedChanges = simpleViewMode ? changes.filter((c: any) => c.type !== 'select') : changes;
        onNodesChangeBase(processedChanges);
        // delay the notification to the parent component, avoid frequent updates
        setTimeout(() => {
            notifyParentChange(nodes, edges);
        }, 100);
    }, [onNodesChangeBase, nodes, edges, notifyParentChange, simpleViewMode]);

    // custom edge change handling, add the logic to notify the parent component
    const onEdgesChange = useCallback((changes: EdgeChange[]) => {
        onEdgesChangeBase(changes);
        // delay the notification to the parent component, avoid frequent updates
        setTimeout(() => {
            notifyParentChange(nodes, edges);
        }, 100);
    }, [onEdgesChangeBase, nodes, edges, notifyParentChange]);



    // determine the edge name and type based on the source node and target node properties
    const getEdgeNameAndType = useCallback((sourceNode: Node, targetNode: Node, sourceHandle?: string, targetHandle?: string) => {
        const sourceType = sourceNode.type;

        // default edge type and name
        let edgeType: 'agree' | 'reject' | 'other' | 'condition' = 'agree';
        let edgeName = t('workflow.propertyPanelLabel.edgeNameAccept');
        if (sourceType === 'start') {
            edgeType = 'agree';
            edgeName = t('workflow.propertyPanelLabel.edgeStartName');
        } else if (sourceType === 'parallel') {
            edgeType = 'other';
            edgeName = t('workflow.propertyPanelLabel.edgeParallelName');
        } else if (sourceType === 'exclusive') {
            edgeType = 'condition';
            edgeName = t('workflow.propertyPanelLabel.edgeConditionName');
        }

        return { edgeType, edgeName };
    }, [t]);

    // connect handling
    const onConnect = useCallback(
        (params: Connection) => {
            console.log('onConnect 被调用:', params);

            // validate the connection is valid
            if (!params.source || !params.target) {
                console.log('连接参数无效:', params);
                return;
            }

            // validate that only the source type handle can start the connection
            if (!params.sourceHandle) {
                console.log('必须从 source 类型的 Handle 发起连线');
                return;
            }

            // validate that only the target type handle can be connected to
            if (!params.targetHandle) {
                console.log('必须连接到 target 类型的 Handle');
                return;
            }

            // additional validation: ensure the connection direction is correct
            // validate the type based on the handle style (green = source, red = target)
            const sourceNode = nodes.find(node => node.id === params.source);
            const targetNode = nodes.find(node => node.id === params.target);

            if (!sourceNode || !targetNode) {
                console.log('source node or target node not found');
                return;
            }

            // determine the edge name and type based on the source node and target node properties
            const { edgeType, edgeName } = getEdgeNameAndType(
                sourceNode,
                targetNode,
                params.sourceHandle,
                params.targetHandle
            );

            // use the React Flow addEdge function to create the edge
            const newEdge: Edge = {
                ...params,
                id: `temp_${uuidv4()}`,
                type: 'custom',
                data: {
                    properties: {
                        name: edgeName,
                        condition: '',
                        type: edgeType
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
        [setEdges, nodes, saveToHistory, notifyParentChange, getEdgeNameAndType]
    );


    // node selection handling
    const onNodeClick = useCallback((event: React.MouseEvent, node: Node) => {
        if (simpleViewMode) {
            return;
        }
        setSelectedElement(node);
        setPropertyPanelOpen(true);
    }, [simpleViewMode]);

    // edge selection handling
    const onEdgeClick = useCallback((event: React.MouseEvent, edge: Edge) => {
        if (simpleViewMode) {
            return;
        }
        setSelectedElement(edge);
        setPropertyPanelOpen(true);
    }, [simpleViewMode]);

    // node/edge hover tooltip (only enabled in simpleViewMode)
    const updateTooltipPosition = useCallback((event: React.MouseEvent) => {
        if (!reactFlowWrapper.current) return { x: 0, y: 0 };
        const rect = reactFlowWrapper.current.getBoundingClientRect();
        return { x: event.clientX - rect.left + 12, y: event.clientY - rect.top + 12 };
    }, []);

    const onNodeMouseEnter = useCallback((event: React.MouseEvent, node: Node) => {
        if (!simpleViewMode) return;
        const pos = updateTooltipPosition(event);
        const props: any = (node.data as any)?.properties || {};
        setHoverTooltip({
            visible: true,
            x: pos.x,
            y: pos.y,
            title: props.name || props.label || t('workflow.node'),
            lines: [
                `类型: ${node.type || ''}`,
                `nodeId: ${node.id}`,
                ...(props.assignee ? [`${t('common.assignee')}: ${props.assignee}`] : []),
                ...(props.description ? [`${t('common.description')}: ${props.description}`] : [])
            ]
        });
    }, [simpleViewMode, updateTooltipPosition, t]);

    const onNodeMouseMove = useCallback((event: React.MouseEvent, node: Node) => {
        if (!simpleViewMode) return;
        if (!hoverTooltip.visible) return;
        const pos = updateTooltipPosition(event);
        setHoverTooltip(prev => ({ ...prev, x: pos.x, y: pos.y }));
    }, [simpleViewMode, hoverTooltip.visible, updateTooltipPosition]);

    const onNodeMouseLeave = useCallback(() => {
        if (!simpleViewMode) return;
        setHoverTooltip(prev => ({ ...prev, visible: false }));
    }, [simpleViewMode]);

    const onEdgeMouseEnter = useCallback((event: React.MouseEvent, edge: Edge) => {
        if (!simpleViewMode) return;
        const pos = updateTooltipPosition(event);
        const props: any = (edge.data as any)?.properties || {};
        setHoverTooltip({
            visible: true,
            x: pos.x,
            y: pos.y,
            title: props.name || props.label || t('workflow.edge'),
            lines: [
                `类型: ${props.type || 'other'}`,
                `edgeId: ${edge.id}`,
                ...(props.condition ? [`${t('common.condition')}: ${props.condition}`] : [])
            ]
        });
    }, [simpleViewMode, updateTooltipPosition, t]);

    const onEdgeMouseMove = useCallback((event: React.MouseEvent, edge: Edge) => {
        if (!simpleViewMode) return;
        if (!hoverTooltip.visible) return;
        const pos = updateTooltipPosition(event);
        setHoverTooltip(prev => ({ ...prev, x: pos.x, y: pos.y }));
    }, [simpleViewMode, hoverTooltip.visible, updateTooltipPosition]);

    const onEdgeMouseLeave = useCallback(() => {
        if (!simpleViewMode) return;
        setHoverTooltip(prev => ({ ...prev, visible: false }));
    }, [simpleViewMode]);

    // listen to the edge label click event
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

    // canvas click handling
    const onPaneClick = useCallback(() => {
        setSelectedElement(null);
        setPropertyPanelOpen(false);
    }, []);

    // add node
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

    // update node properties
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
                            // if the name property is modified, also update the label
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

    // update edge properties
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

    // toolbar operations
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
                // delete edge
                setEdges((eds) => {
                    const newEdges = eds.filter((edge) => edge.id !== selectedElement.id);
                    saveToHistory(nodes, newEdges);
                    notifyParentChange(nodes, newEdges);
                    return newEdges;
                });
            } else {
                // delete node and related edges
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
                // copy edge
                const newEdge: Edge = {
                    ...selectedElement,
                    id: `temp_${uuidv4()}`,
                    source: selectedElement.source,
                    target: selectedElement.target,
                    data: {
                        ...selectedElement.data,
                        properties: {
                            ...(selectedElement.data?.properties && typeof selectedElement.data.properties === 'object' ? selectedElement.data.properties : {}),
                            name: `${(selectedElement.data?.properties as any)?.name || t('workflow.edge')} (副本)`,
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
                // copy node
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
                            ...(selectedElement.data?.properties && typeof selectedElement.data.properties === 'object' ? selectedElement.data.properties : {}),
                            name: `${(selectedElement.data?.properties as any)?.name || t('workflow.node')} (副本)`,
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
    }, [selectedElement, setNodes, setEdges, nodes, edges, saveToHistory, notifyParentChange, t]);


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
                {/* left node panel */}
                {!simpleViewMode ?
                    <Box sx={{ width: 280, borderRight: 1, borderColor: 'divider' }}>
                        <NodePanel onAddNode={onAddNode} />
                    </Box> : null}

                {/* main content area */}
                <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
                    {/* top toolbar */}
                    {!simpleViewMode ?
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
                        /> : null}

                    {/* workflow canvas */}
                    <Box sx={{ flex: 1, position: 'relative' }} ref={reactFlowWrapper}>
                        <ReactFlow
                            nodes={nodes}
                            edges={edges}
                            onNodesChange={onNodesChange}
                            onEdgesChange={onEdgesChange}
                            onConnect={onConnect}
                            onNodeClick={onNodeClick}
                            onEdgeClick={onEdgeClick}
                            onPaneClick={!simpleViewMode ? onPaneClick : undefined}
                            onNodeMouseEnter={onNodeMouseEnter}
                            onNodeMouseMove={onNodeMouseMove}
                            onNodeMouseLeave={onNodeMouseLeave}
                            onEdgeMouseEnter={onEdgeMouseEnter}
                            onEdgeMouseMove={onEdgeMouseMove}
                            onEdgeMouseLeave={onEdgeMouseLeave}
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

                            {/* hover tooltip layer */}
                            {simpleViewMode && hoverTooltip.visible ? (
                                <Box
                                    sx={{
                                        position: 'absolute',
                                        left: hoverTooltip.x,
                                        top: hoverTooltip.y,
                                        pointerEvents: 'none',
                                        backgroundColor: 'rgba(33, 33, 33, 0.9)',
                                        color: '#fff',
                                        p: 1,
                                        borderRadius: 1,
                                        boxShadow: 3,
                                        maxWidth: 260,
                                        fontSize: 12,
                                        zIndex: 20
                                    }}
                                >
                                    <div style={{ fontWeight: 600, marginBottom: 4 }}>{hoverTooltip.title}</div>
                                    {hoverTooltip.lines.map((line, idx) => (
                                        <div key={idx} style={{ whiteSpace: 'pre-wrap' }}>{line}</div>
                                    ))}
                                </Box>
                            ) : null}

                            {/* orange border说明提示：仅在存在 selectedNodeIds 时显示 */}
                            {selectedNodeIds && selectedNodeIds.length > 0 ? (
                                <Box
                                    sx={{
                                        position: 'absolute',
                                        left: 12,
                                        top: 12,
                                        pointerEvents: 'none',
                                        backgroundColor: 'rgba(33, 33, 33, 0.75)',
                                        color: '#fff',
                                        px: 1,
                                        py: 0.5,
                                        borderRadius: 1,
                                        boxShadow: 2,
                                        fontSize: 12,
                                        zIndex: 20
                                    }}
                                >
                                    {t('workflow.orangeBorderTip')}
                                </Box>
                            ) : null}
                        </ReactFlow>
                    </Box>
                </Box>

                {/* right property panel */}
                {!simpleViewMode ? <Drawer
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
                </Drawer> : null}
            </Box>

            {/* snackbar for message */}
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