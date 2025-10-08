import React, { useState, useEffect } from 'react';
import WorkflowProcess from '../../../Workflow/WorkflowProcess';
import { Box, Typography, CircularProgress, Alert } from '@mui/material';
import '@xyflow/react/dist/style.css';

import { IWorkflowDiagram } from '../../../../types/workflow';
import { getWorkflowDiagram } from '../../../../services/workflow';
import { getTicketCurrentNodeInfos } from '../../../../services/ticket';

interface WorkflowDiagramProps {
    workflowId: string;
    workflowVersionId: string;
    ticketId?: string;
}

function WorkflowDiagram({ workflowId, workflowVersionId, ticketId }: WorkflowDiagramProps) {
    const [workflowDiagram, setWorkflowDiagram] = useState<IWorkflowDiagram>();
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [selectedNodeIds, setSelectedNodeIds] = useState<string[]>([]);

    useEffect(() => {
        const fetchWorkflowDiagram = async () => {
            try {
                setLoading(true);
                setError(null);
                const res = await getWorkflowDiagram(workflowId, workflowVersionId);
                if (res.code === 0) {
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

        const fetchCurrentNodes = async () => {
            if (!ticketId) {
                setSelectedNodeIds([]);
                return;
            }
            try {
                const res = await getTicketCurrentNodeInfos(ticketId);
                if (res.code === 0) {
                    const ids = res.data.currentNodeInfoList?.map((n: any) => n.id) || [];
                    console.log('----IDSID:', ids)
                    setSelectedNodeIds(ids);
                }
            } catch (e) {
                console.error('获取工单当前节点失败', e);
            }
        };

        if (workflowId && workflowVersionId) {
            fetchWorkflowDiagram();
            fetchCurrentNodes();
        }
    }, [workflowId, workflowVersionId, ticketId]);

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
            selectedNodeIds={selectedNodeIds}
        />
    );
}

export default WorkflowDiagram;
