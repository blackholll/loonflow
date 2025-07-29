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

interface NodePanelProps {
    onAddNode: (nodeType: string, nodeData: any) => void;
}

// 节点配置
const nodeConfigs = {
    // 基础节点
    basicNodes: [
        {
            type: 'startNode',
            label: '开始节点',
            icon: StartIcon,
            color: '#4caf50',
            properties: {
                name: '开始节点1',
                nodeType: 'start',
                canConnect: true,
                canDisconnect: false,
            }
        },
        {
            type: 'normalNode',
            label: '普通节点',
            icon: NormalIcon,
            color: '#2196f3',
            properties: {
                name: '普通节点1',
                nodeType: 'normal',
                canConnect: true,
                canDisconnect: true,
            }
        },
        {
            type: 'endNode',
            label: '结束节点',
            icon: EndIcon,
            color: '#f44336',
            properties: {
                name: '结束节点1',
                nodeType: 'end',
                canConnect: false,
                canDisconnect: true,
            }
        },
    ],
    // 网关节点
    gatewayNodes: [
        {
            type: 'parallelGateway',
            label: '并行网关',
            icon: ParallelIcon,
            color: '#ff9800',
            properties: {
                nodeType: 'parallel',
                canConnect: true,
                canDisconnect: true,
                gatewayType: 'parallel',
            }
        },
        {
            type: 'exclusiveGateway',
            label: '排他网关',
            icon: ExclusiveIcon,
            color: '#9c27b0',
            properties: {
                nodeType: 'exclusive',
                canConnect: true,
                canDisconnect: true,
                gatewayType: 'exclusive',
            }
        },
    ],

    advancedNodes: [
        {
            type: 'timerNode',
            icon: TimerIcon,
            label: '定时器节点',
            color: '#9c27b0',
            properties: {
                nodeType: 'timer',
                canConnect: true,
                canDisconnect: true,
            }
        },
        {
            type: 'hookNode',
            icon: WebhookIcon,
            label: '钩子节点',
            color: '#9c27b0',
            properties: {
                nodeType: 'hook',
                canConnect: true,
                canDisconnect: true,
            }
        }
    ]
};

const NodePanel: React.FC<NodePanelProps> = ({ onAddNode }) => {
    const handleNodeDrag = (nodeConfig: any) => {
        onAddNode(nodeConfig.type, {
            label: nodeConfig.label,
            nodeType: nodeConfig.properties.nodeType,
            color: nodeConfig.color,
            properties: nodeConfig.properties,
        });
    };

    return (
        <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
            <Box sx={{ p: 2, borderBottom: 1, borderColor: 'divider' }}>
                <Typography variant="h6" component="h2">
                    节点库
                </Typography>
            </Box>

            <Box sx={{ flex: 1, overflow: 'auto', p: 1 }}>
                {/* 基础节点 */}
                <Typography variant="subtitle2" sx={{ px: 1, py: 1, fontWeight: 'bold' }}>
                    基础节点
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

                {/* 网关节点 */}
                <Typography variant="subtitle2" sx={{ px: 1, py: 1, fontWeight: 'bold' }}>
                    网关节点
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
                    高级节点
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