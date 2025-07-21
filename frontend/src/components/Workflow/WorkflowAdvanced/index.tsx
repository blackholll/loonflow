import react, { useState, useEffect } from 'react';
import { Paper, Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField, FormControl, FormLabel, RadioGroup, FormControlLabel, Radio, Icon, Box, Tooltip, InputAdornment } from '@mui/material';

import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid2';
import Markdown from 'react-markdown';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import NotificationConfig from './NotificationConfig';
import PermissionConfig from './PermissionConfig';
import CustomizeConfig from './CustomizeConfig';

interface WorkflowBasicProps {
    onBasicChange: (name: string, description: string) => void;
    basicInfo?: {
        name: string;
        description: string;
    };
}

const tabList = [
    { label: '通知配置', value: 0 },
    { label: '权限配置', value: 1 },
    { label: '定制配置', value: 2 },
];

function WorkflowAdvanced({ onBasicChange, basicInfo }: WorkflowBasicProps) {
    const [name, setName] = useState(basicInfo?.name || '');
    const [description, setDescription] = useState(basicInfo?.description || '');
    const [activeTab, setActiveTab] = useState('description');
    const [tabIndex, setTabIndex] = useState(0);

    // 监听 basicInfo 变化，更新表单值
    useEffect(() => {
        if (basicInfo) {
            setName(basicInfo.name || '');
            setDescription(basicInfo.description || '');
        }
    }, [basicInfo]);

    const handleTabChange = (event: React.SyntheticEvent, newValue: string) => {
        console.log(newValue);
        setActiveTab(newValue);
    };

    return (
        <Grid
            container
            justifyContent="center"
            sx={{
                minHeight: "100vh",
                backgroundColor: "#EFF0F1",
                p: 2,
            }}
        >
            <Grid size={{ xs: 6, sm: 6, md: 6 }} >
                <Card elevation={3}>
                    <CardContent sx={{ p: 4 }}>
                        <Box sx={{ display: 'flex', justifyContent: 'left', alignItems: 'flex-start', width: '100%', minHeight: 800 }}>
                            {/* 左侧Tab栏 */}
                            <Paper
                                sx={{
                                    minWidth: 180,
                                    borderRadius: 0,
                                    mr: 0,
                                    p: 0,
                                    boxShadow: 'none',
                                    borderRight: '1px solid #e0e0e0',
                                    borderTop: 'none',
                                    borderBottom: 'none',
                                    borderLeft: 'none',
                                }}
                            >
                                <Tabs
                                    orientation="vertical"
                                    value={tabIndex}
                                    onChange={(_, v) => setTabIndex(v)}
                                    variant="scrollable"
                                    sx={{ minHeight: 320, pl: 0 }}
                                >
                                    {tabList.map(tab => (
                                        <Tab key={tab.value} label={tab.label} />
                                    ))}
                                </Tabs>
                            </Paper>
                            {/* 右侧内容区 */}
                            <Box sx={{ flex: 1, minWidth: 400, maxWidth: 600 }}>
                                {tabIndex === 0 && (
                                    <Box><NotificationConfig /></Box>
                                )}
                                {tabIndex === 1 && (
                                    <Box><PermissionConfig /></Box>
                                )}
                                {tabIndex === 2 && (
                                    <Box><CustomizeConfig /></Box>
                                )}
                            </Box>
                        </Box>

                    </CardContent>
                </Card>
            </Grid>
        </Grid>
    );
}

export default WorkflowAdvanced;