import { useState, useMemo, useCallback } from 'react';
import { useTranslation } from 'react-i18next';
import { Paper, Box } from '@mui/material';

import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Grid from '@mui/material/Grid2';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import NotificationConfig from './NotificationConfig';
import PermissionConfig from './PermissionConfig';
import CustomizeConfig from './CustomizeConfig';
import { INotification, IpermissionInfo, ICustomizationInfo, IAdvancedSchema, IFormSchema } from '../../../types/workflow';

interface WorkflowAdvancedProps {
    onAdvancedChange: (advancedSchema: IAdvancedSchema) => void;
    advancedSchema: IAdvancedSchema;
    formSchema: IFormSchema;
}

function WorkflowAdvanced({ onAdvancedChange, advancedSchema, formSchema }: WorkflowAdvancedProps) {
    const { t } = useTranslation();
    const [advancedSchemaInfo, setAdvancedSchemaInfo] = useState(advancedSchema);
    const [tabIndex, setTabIndex] = useState(0);

    const tabList = useMemo(() => ([
        { label: t('workflow.advancedSettingLabel.notificationSetting'), value: 0 },
        { label: t('workflow.advancedSettingLabel.permissionSetting'), value: 1 },
        { label: t('workflow.advancedSettingLabel.customizeSetting'), value: 2 },
    ]), [t]);

    const onNotificationConfigChange = useCallback((notificationConfig: INotification) => {
        setAdvancedSchemaInfo(prev => {
            const newState = {
                ...prev,
                notificationInfo: notificationConfig
            };
            onAdvancedChange(newState);
            return newState;
        });
    }, [onAdvancedChange]);

    const onPermissionConfigChange = useCallback((permissionConfig: IpermissionInfo) => {
        console.log('onPermissionConfigChange:', permissionConfig);
        setAdvancedSchemaInfo(prev => {
            const newState = {
                ...prev,
                permissionInfo: permissionConfig
            };
            onAdvancedChange(newState);
            return newState;
        });
    }, [onAdvancedChange]);

    const onCustomizeConfigChange = useCallback((customizeConfig: ICustomizationInfo) => {
        setAdvancedSchemaInfo(prev => {
            const newState = {
                ...prev,
                customizationInfo: customizeConfig
            };
            onAdvancedChange(newState);
            return newState;
        });
    }, [onAdvancedChange]);

    const NotificatinComponent = useMemo(() => (
        <NotificationConfig
            onNotificationConfigChange={onNotificationConfigChange}
            notificationConfig={advancedSchemaInfo.notificationInfo}
            formSchema={formSchema}
            key="notification-config" />
    ), [advancedSchemaInfo.notificationInfo, formSchema, onNotificationConfigChange]);

    const PermissionComponent = useMemo(() => (
        <PermissionConfig
            onPermissionConfigChange={onPermissionConfigChange}
            permissionConfig={advancedSchemaInfo.permissionInfo}
            key="permission-config" />
    ), [advancedSchemaInfo.permissionInfo, onPermissionConfigChange]);

    const CustomizeComponent = useMemo(() => (
        <CustomizeConfig
            onCustomizeConfigChange={onCustomizeConfigChange}
            customizeConfig={advancedSchemaInfo.customizationInfo}
            key="customize-config" />
    ), [advancedSchemaInfo.customizationInfo, onCustomizeConfigChange]);

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
                                    <Box>{NotificatinComponent}</Box>
                                )}
                                {tabIndex === 1 && (
                                    <Box>{PermissionComponent}</Box>
                                )}
                                {tabIndex === 2 && (
                                    <Box>{CustomizeComponent}</Box>
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