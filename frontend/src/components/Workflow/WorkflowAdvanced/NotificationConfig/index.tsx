import { Box, Chip, FormLabel, Stack, TextField } from '@mui/material';
import Autocomplete from '@mui/material/Autocomplete';
import Grid from '@mui/material/Grid2';
import { useCallback, useEffect, useMemo, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { getSimpleNotificationList } from '../../../../services/notification';
import { IFormSchema, INotification } from '../../../../types/workflow';
import TemplateEditor from '../../../commonComponents/inputs/TemplateEditor';



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
    const [titleTemplate, setTitleTemplate] = useState(notificationConfig.titleTemplate || '');
    const [contentTemplate, setContentTemplate] = useState(notificationConfig.contentTemplate || '');
    const [notificationList, setNotificationList] = useState<NotificationItem[]>([]);
    const [availableFields, setAvailableFields] = useState<{ key: string; label: string }[]>([]);
    const { t } = useTranslation();

    // 使用useMemo计算选中的通知项，避免无限循环
    const selectedNotifications = useMemo(() => {
        if (!notificationConfig.selectedChannelList || !Array.isArray(notificationConfig.selectedChannelList) || notificationConfig.selectedChannelList.length === 0) {
            return [];
        }
        return notificationList.filter((item) =>
            notificationConfig.selectedChannelList.includes(item.id)
        );
    }, [notificationConfig.selectedChannelList, notificationList]);

    // 同步notificationConfig prop到独立状态
    useEffect(() => {
        setTitleTemplate(notificationConfig.titleTemplate || '');
        setContentTemplate(notificationConfig.contentTemplate || '');
    }, [notificationConfig]);

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
        fields.push({ key: 'created_at', label: t('common.createdAt') });
        fields.push({ key: 'updated_at', label: t('common.updatedAt') });
        fields.push({ key: 'creator', label: t('common.creator') });

        setAvailableFields(fields);
    }, [formSchema, t]);


    const handleTitleTemplateChange = useCallback((value: string) => {
        setTitleTemplate(value);
        onNotificationConfigChange({ ...notificationConfig, titleTemplate: value });
    }, [onNotificationConfigChange, notificationConfig]);

    const handleContentTemplateChange = useCallback((value: string) => {
        setContentTemplate(value);
        onNotificationConfigChange({ ...notificationConfig, contentTemplate: value });
    }, [onNotificationConfigChange, notificationConfig]);

    const handleSelectedChannelListChange = useCallback((value: NotificationItem[]) => {
        onNotificationConfigChange({ ...notificationConfig, selectedChannelList: value.map((item: any) => item.id) });
    }, [onNotificationConfigChange, notificationConfig]);

    return (
        <Box>
            <Stack spacing={3}>
                <Grid container alignItems="flex-start" spacing={2}>
                    <Grid size={3} sx={{ minWidth: 100, pt: 1 }}>
                        <FormLabel>{t('workflow.advancedSettingLabel.notificationSettingLabel.notificationTitleTemplate')}</FormLabel>
                    </Grid>
                    <Grid size={9}>
                        <TemplateEditor
                            value={titleTemplate}
                            onChange={handleTitleTemplateChange}
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
                            value={contentTemplate}
                            onChange={handleContentTemplateChange}
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
                            value={selectedNotifications}
                            onChange={(event, newValue) => {
                                handleSelectedChannelListChange(newValue);
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