import React, { useEffect } from 'react';
import { Box, Paper, Typography, Button, TextField, FormControl, FormLabel, RadioGroup, FormControlLabel, Radio, Icon, Tooltip, InputAdornment, Stack, Chip } from '@mui/material';
import Grid from '@mui/material/Grid2';
import TemplateEditor from './TemplateEditor';
import Autocomplete from '@mui/material/Autocomplete';
import { getSimpleNotificationList } from '../../../../services/notification';

const availableFields = [
    { key: 'title', label: '标题' },
    { key: 'country.label', label: '国家' },
    { key: 'username', label: '用户名' },
    // 可根据实际表单设计动态生成
];

// 定义通知项的类型
interface NotificationItem {
    id: string;
    name: string;
    description: string;
    label?: any;
    [key: string]: any;
}

function NotificationConfig() {
    const [titleTemplate, setTitleTemplate] = React.useState('');
    const [contentTemplate, setContentTemplate] = React.useState('');
    const [notificationList, setNotificationList] = React.useState<NotificationItem[]>([]);
    const [selectedNotifications, setSelectedNotifications] = React.useState<NotificationItem[]>([]);

    useEffect(() => {
        getSimpleNotificationList('', 1, 1000).then((res) => {
            if (res.code === 0 && res.data && res.data.notificationList) {
                setNotificationList(res.data.notificationList)
            }
        }).catch((error) => {
            console.error('获取通知列表失败:', error);
            setNotificationList([]);
        });
    }, []);

    return (
        <Box>
            <Stack spacing={3}>
                <Grid container alignItems="flex-start" spacing={2}>
                    <Grid size={3} sx={{ minWidth: 100, pt: 1 }}>
                        <FormLabel>通知标题模板</FormLabel>
                    </Grid>
                    <Grid size={9}>
                        <TemplateEditor
                            value={titleTemplate}
                            onChange={setTitleTemplate}
                            availableFields={availableFields}
                            placeholder="请输入通知标题模板"
                        />
                    </Grid>
                </Grid>
                <Grid container alignItems="flex-start" spacing={2}>
                    <Grid size={3} sx={{ minWidth: 100, pt: 1 }}>
                        <FormLabel>通知内容模板</FormLabel>
                    </Grid>
                    <Grid size={9}>
                        <TemplateEditor
                            value={contentTemplate}
                            onChange={setContentTemplate}
                            availableFields={availableFields}
                            placeholder="请输入通知内容模板"
                        />
                    </Grid>
                </Grid>
                <Grid container alignItems="flex-start" spacing={2}>
                    <Grid size={3} sx={{ minWidth: 100, pt: 1 }}>
                        <FormLabel>通知方式</FormLabel>
                    </Grid>
                    <Grid size={9}>
                        <Autocomplete
                            multiple
                            disablePortal
                            options={notificationList || []}
                            value={selectedNotifications}
                            onChange={(event, newValue) => {
                                setSelectedNotifications(newValue);
                            }}
                            getOptionLabel={(option) => option.name || ''}
                            isOptionEqualToValue={(option, value) => option.id === value.id}
                            sx={{ width: 300 }}
                            renderInput={(params) => <TextField {...params} label="通知方式" />}
                            renderOption={(props, option) => (
                                <li {...props}>
                                    <div>
                                        <div>{option.name || '未命名'}</div>
                                        <div style={{ fontSize: '0.8em', color: '#666' }}>
                                            {option.description || '无描述'}
                                        </div>
                                    </div>
                                </li>
                            )}
                            renderTags={(value, getTagProps) =>
                                value.map((option, index) => (
                                    <Chip
                                        label={option.name}
                                        size="small"
                                        {...getTagProps({ index })}
                                    />
                                ))
                            }
                        />
                    </Grid>
                </Grid>
            </Stack>
        </Box>
    );
}

export default NotificationConfig;