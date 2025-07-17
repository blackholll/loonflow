import React, { useState } from 'react';
import { Box, Tabs, Tab, Paper } from '@mui/material';

const tabList = [
    { label: '通知配置', value: 0 },
    { label: '权限配置', value: 1 },
    { label: '定制配置', value: 2 },
];

const WorkflowAdvanced: React.FC = () => {
    const [tabIndex, setTabIndex] = useState(0);

    return (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'flex-start', width: '100%', minHeight: 400 }}>
            {/* 左侧Tab栏 */}
            <Paper sx={{ minWidth: 180, borderRadius: 2, mr: 4, p: 0 }}>
                <Tabs
                    orientation="vertical"
                    value={tabIndex}
                    onChange={(_, v) => setTabIndex(v)}
                    variant="scrollable"
                    sx={{ minHeight: 320 }}
                >
                    {tabList.map(tab => (
                        <Tab key={tab.value} label={tab.label} />
                    ))}
                </Tabs>
            </Paper>
            {/* 右侧内容区 */}
            <Box sx={{ flex: 1, minWidth: 400, maxWidth: 600 }}>
                {tabIndex === 0 && (
                    <Box>通知配置内容（待实现）</Box>
                )}
                {tabIndex === 1 && (
                    <Box>权限配置内容（待实现）</Box>
                )}
                {tabIndex === 2 && (
                    <Box>定制配置内容（待实现）</Box>
                )}
            </Box>
        </Box>
    );
};

export default WorkflowAdvanced;