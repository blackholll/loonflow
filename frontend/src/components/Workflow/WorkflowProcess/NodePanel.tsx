import React from 'react';
import {
    Box,
    Typography,
    Paper,
    List,
    ListItem,
    ListItemButton,
    ListItemIcon,
    ListItemText,
    Divider,
} from '@mui/material';
import {
    PlayArrow as StartIcon,
    Circle as NormalIcon,
    Stop as EndIcon,
    AccountTree as ParallelIcon,
    CallSplit as ExclusiveIcon,
    Timer as TimerIcon,
    Webhook as WebhookIcon
} from '@mui/icons-material';
import { useTranslation } from 'react-i18next';
interface NodePanelProps {
    onAddNode: (nodeType: string, nodeData: any) => void;
}

// 创建获取节点配置的函数
const getNodeConfigs = (t: any) => ({
    // 基础节点
    basicNodes: [
        {
            type: 'start',
            label: t('workflow.nodePanelLabel.startNode'),
            icon: StartIcon,
            color: '#4caf50',
            properties: {
                name: t('workflow.nodePanelLabel.startNode'),
                type: 'start',
                canConnect: true,
                canDisconnect: false,
            }
        },
        {
            type: 'normal',
            label: t('workflow.nodePanelLabel.normalNode'),
            icon: NormalIcon,
            color: '#2196f3',
            properties: {
                name: t('workflow.nodePanelLabel.normalNodeName'),
                type: 'normal',
                canConnect: true,
                canDisconnect: true,
            }
        },
        {
            type: 'end',
            label: t('workflow.nodePanelLabel.endNode'),
            icon: EndIcon,
            color: '#f44336',
            properties: {
                name: t('workflow.nodePanelLabel.endNode'),
                type: 'end',
                canConnect: false,
                canDisconnect: true,
            }
        },
    ],
    // 网关节点
    gatewayNodes: [
        {
            type: 'parallelGateway',
            label: t('workflow.nodePanelLabel.parallelNode'),
            icon: ParallelIcon,
            color: '#ff9800',
            properties: {
                type: 'parallel',
                canConnect: true,
                canDisconnect: true,
                gatewayType: 'parallel',
            }
        },
        {
            type: 'exclusiveGateway',
            label: t('workflow.nodePanelLabel.exclusiveNode'),
            icon: ExclusiveIcon,
            color: '#9c27b0',
            properties: {
                type: 'exclusive',
                canConnect: true,
                canDisconnect: true,
                gatewayType: 'exclusive',
            }
        },
    ],

    advancedNodes: [
        {
            type: 'timer',
            icon: TimerIcon,
            label: t('workflow.nodePanelLabel.timerNode'),
            color: '#9c27b0',
            properties: {
                type: 'timer',
                canConnect: true,
                canDisconnect: true,
            }
        },
        {
            type: 'hook',
            icon: WebhookIcon,
            label: t('workflow.nodePanelLabel.hookNode'),
            color: '#9c27b0',
            properties: {
                type: 'hook',
                canConnect: true,
                canDisconnect: true,
            }
        }
    ]
});

function NodePanel(props: NodePanelProps) {
    const { onAddNode } = props;
    const { t } = useTranslation();
    const nodeConfigs = getNodeConfigs(t);
    const handleNodeDrag = (nodeConfig: any) => {
        onAddNode(nodeConfig.type, {
            label: nodeConfig.properties.name,
            type: nodeConfig.properties.type,
            color: nodeConfig.color,
            properties: nodeConfig.properties,
        });
    };

    return (
        <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
            <Box sx={{ p: 2, borderBottom: 1, borderColor: 'divider' }}>
                <Typography variant="h6" component="h2">
                    {t('workflow.nodePanelLabel.nodeLibrary')}
                </Typography>
            </Box>

            <Box sx={{ flex: 1, overflow: 'auto', p: 1 }}>
                {/* basic nodes */}
                <Typography variant="subtitle2" sx={{ px: 1, py: 1, fontWeight: 'bold' }}>
                    {t('workflow.nodePanelLabel.basicNodes')}
                </Typography>
                <Paper variant="outlined" sx={{ mb: 2 }}>
                    <List dense>
                        {nodeConfigs.basicNodes.map((nodeConfig) => (
                            <ListItem key={nodeConfig.type} disablePadding>
                                <ListItemButton
                                    onClick={() => handleNodeDrag(nodeConfig)}
                                    sx={{
                                        '&:hover': {
                                            backgroundColor: 'action.hover',
                                        },
                                    }}
                                >
                                    <ListItemIcon>
                                        <nodeConfig.icon sx={{ color: nodeConfig.color }} />
                                    </ListItemIcon>
                                    <ListItemText
                                        primary={nodeConfig.label}
                                        primaryTypographyProps={{ variant: 'body2' }}
                                    />
                                </ListItemButton>
                            </ListItem>
                        ))}
                    </List>
                </Paper>

                <Divider sx={{ my: 1 }} />

                <Typography variant="subtitle2" sx={{ px: 1, py: 1, fontWeight: 'bold' }}>
                    {t('workflow.nodePanelLabel.gatewayNodes')}
                </Typography>
                <Paper variant="outlined">
                    <List dense>
                        {nodeConfigs.gatewayNodes.map((nodeConfig) => (
                            <ListItem key={nodeConfig.type} disablePadding>
                                <ListItemButton
                                    onClick={() => handleNodeDrag(nodeConfig)}
                                    sx={{
                                        '&:hover': {
                                            backgroundColor: 'action.hover',
                                        },
                                    }}
                                >
                                    <ListItemIcon>
                                        <nodeConfig.icon sx={{ color: nodeConfig.color }} />
                                    </ListItemIcon>
                                    <ListItemText
                                        primary={nodeConfig.label}
                                        primaryTypographyProps={{ variant: 'body2' }}
                                    />
                                </ListItemButton>
                            </ListItem>
                        ))}
                    </List>
                </Paper>

                {/* 高级节点 */}
                <Typography variant="subtitle2" sx={{ px: 1, py: 1, fontWeight: 'bold' }}>
                    {t('workflow.nodePanelLabel.advancedNodes')}
                </Typography>
                <Paper variant="outlined">
                    <List dense>
                        {nodeConfigs.advancedNodes.map((nodeConfig) => (
                            <ListItem key={nodeConfig.type} disablePadding>
                                <ListItemButton
                                    onClick={() => handleNodeDrag(nodeConfig)}
                                    sx={{
                                        '&:hover': {
                                            backgroundColor: 'action.hover',
                                        },
                                    }}
                                >
                                    <ListItemIcon>
                                        <nodeConfig.icon sx={{ color: nodeConfig.color }} />
                                    </ListItemIcon>
                                    <ListItemText
                                        primary={nodeConfig.label}
                                        primaryTypographyProps={{ variant: 'body2' }}
                                    />
                                </ListItemButton>
                            </ListItem>
                        ))}
                    </List>
                </Paper>
            </Box>
        </Box>
    );
};

export default NodePanel; 