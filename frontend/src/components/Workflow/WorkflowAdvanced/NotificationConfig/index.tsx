import React, { useEffect, useState } from 'react';
import { Box, Paper, Typography, Button, TextField, FormControl, FormLabel, RadioGroup, FormControlLabel, Radio, Icon, Tooltip, InputAdornment, Stack, Chip } from '@mui/material';
import Grid from '@mui/material/Grid2';
import TemplateEditor from '../../../commonComponents/inputs/TemplateEditor';
import Autocomplete from '@mui/material/Autocomplete';
import { getSimpleNotificationList } from '../../../../services/notification';
import { INotification, IFormSchema } from '../../../../types/workflow';
import { useTranslation } from 'react-i18next';



// 定义通知项的类型
interface NotificationItem {
    id: string;
    name: string;
    description: string;
    label?: any;
    [key: string]: any;
}

interface NotificationConfigProps {
    onNotificationConfigChange: (notificationConfig: INotification) => void;
    notificationConfig: INotification;
    formSchema: IFormSchema;
}


function NotificationConfig({ onNotificationConfigChange, notificationConfig, formSchema }: NotificationConfigProps) {
    console.log(formSchema);
    const [notificationConfigInfo, setNotificationConfigInfo] = useState(notificationConfig);
    const [titleTemplate, setTitleTemplate] = useState('');
    const [contentTemplate, setContentTemplate] = useState('');
    const [notificationList, setNotificationList] = useState<NotificationItem[]>([]);
    const [selectedNotifications, setSelectedNotifications] = useState<NotificationItem[]>([]);
    const [availableFields, setAvailableFields] = useState<{ key: string; label: string }[]>([]);
    const { t } = useTranslation();

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

    useEffect(() => {
        const fields: { key: string; label: string }[] = [];

        formSchema.componentInfoList.forEach((component) => {
            // 如果是 IWorkflowComponentRow 类型，需要遍历其 children
            if (component.type === 'row' && 'children' in component) {
                component.children.forEach((childComponent) => {
                    fields.push({
                        key: childComponent.componentKey,
                        label: childComponent.componentName
                    });
                });
            } else {
                // 如果是 IWorkflowComponent 类型，直接添加
                fields.push({
                    key: component.componentKey,
                    label: component.componentName
                });
            }
        });
        fields.push({ key: 'createdAt', label: t('common.createdAt') });
        fields.push({ key: 'updatedAt', label: t('common.updatedAt') });
        fields.push({ key: 'creator', label: t('common.creator') });

        setAvailableFields(fields);
    }, [formSchema]);

    const handlePropertyChange = (key: string, value: any) => {
        const newNotificationConfig = { ...notificationConfigInfo, [key]: value };
        setNotificationConfigInfo(newNotificationConfig);
        onNotificationConfigChange(newNotificationConfig);
    };

    return (
        <Box>
            <Stack spacing={3}>
                <Grid container alignItems="flex-start" spacing={2}>
                    <Grid size={3} sx={{ minWidth: 100, pt: 1 }}>
                        <FormLabel>{t('workflow.advancedSettingLabel.notificationSettingLabel.notificationTitleTemplate')}</FormLabel>
                    </Grid>
                    <Grid size={9}>
                        <TemplateEditor
                            value={notificationConfigInfo.titleTemplate}
                            onChange={(e) => handlePropertyChange('titleTemplate', e)}
                            availableFields={availableFields}
                            placeholder={t('workflow.advancedSettingLabel.notificationSettingLabel.notificationTitleTemplatePlaceholder')}
                        />
                    </Grid>
                </Grid>
                <Grid container alignItems="flex-start" spacing={2}>
                    <Grid size={3} sx={{ minWidth: 100, pt: 1 }}>
                        <FormLabel>{t('workflow.advancedSettingLabel.notificationSettingLabel.notificationContentTemplate')}</FormLabel>
                    </Grid>
                    <Grid size={9}>
                        <TemplateEditor
                            value={notificationConfigInfo.contentTemplate}
                            onChange={(e) => handlePropertyChange('contentTemplate', e)}
                            availableFields={availableFields}
                            placeholder={t('workflow.advancedSettingLabel.notificationSettingLabel.notificationContentTemplatePlaceholder')}
                        />
                    </Grid>
                </Grid>
                <Grid container alignItems="flex-start" spacing={2}>
                    <Grid size={3} sx={{ minWidth: 100, pt: 1 }}>
                        <FormLabel>{t('workflow.advancedSettingLabel.notificationSettingLabel.notificationSelectedChannelList')}</FormLabel>
                    </Grid>
                    <Grid size={9}>
                        <Autocomplete
                            multiple
                            disablePortal
                            options={notificationList || []}
                            value={notificationList.filter((item) => notificationConfigInfo.selectedChannelList.includes(item.id))}
                            onChange={(event, newValue) => {
                                handlePropertyChange('selectedChannelList', newValue.map((item: any) => item.id));
                            }}
                            getOptionLabel={(option) => option.name || ''}
                            isOptionEqualToValue={(option, value) => option.id === value.id}
                            sx={{ width: 300 }}
                            renderInput={(params) => <TextField {...params} label={t('workflow.advancedSettingLabel.notificationSettingLabel.notificationSelectedChannelList')} />}
                            renderOption={(props, option) => (
                                <li {...props} key={option.id}>
                                    <div>
                                        <div>{option.name}</div>
                                        <div style={{ fontSize: '0.8em', color: '#666' }}>
                                            {option.description}
                                        </div>
                                    </div>
                                </li>
                            )}
                            renderTags={(value, getTagProps) =>
                                value.map((option, index) => {
                                    const { key, ...otherProps } = getTagProps({ index });
                                    return <Chip
                                        key={key}
                                        label={option.name}
                                        size="small"
                                        {...otherProps}
                                    />
                                }
                                )
                            }
                        />
                    </Grid>
                </Grid>
            </Stack>
        </Box>
    );
}

export default NotificationConfig;