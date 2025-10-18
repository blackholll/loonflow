import { HelpOutline as HelpIcon } from '@mui/icons-material';
import { Box, Paper, Tooltip, Typography } from '@mui/material';
import Grid from '@mui/material/Grid2';
import React from 'react';
import { useTranslation } from 'react-i18next';
import { IFormSchema, IWorkflowComponent, IWorkflowComponentRow } from '../../../../types/workflow';

interface FormPreviewProps {
    formSchemaInfo: IFormSchema;
    renderFieldComponent: (component: IWorkflowComponent, handleComponentUpdate?: (updatedComponent: IWorkflowComponent) => void) => React.ReactNode;
}

function FormPreview({ formSchemaInfo, renderFieldComponent }: FormPreviewProps) {
    const { t } = useTranslation();
    // in preview mode, we don't need to handle component update, so pass an empty update function
    const handleComponentUpdate = (updatedComponent: IWorkflowComponent) => {
        // in preview mode, we don't need to handle component update, so do nothing
        console.log('Preview mode: component update ignored', updatedComponent);
    };

    return (
        <Paper
            sx={{
                flex: 1,
                p: 3,
                overflow: 'auto',
                backgroundColor: 'background.paper',
                border: '1px solid',
                borderColor: 'divider'
            }}
        >
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                {formSchemaInfo.componentInfoList.map((component) => {
                    if (component.type === 'row') {
                        return (
                            <Grid container spacing={2} key={component.id}>
                                {(component as IWorkflowComponentRow).children.map((fieldComponent: IWorkflowComponent) => (
                                    <Grid
                                        key={fieldComponent.id}
                                        size={fieldComponent.layout.span || 12}
                                    >
                                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                                            <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                                <Typography
                                                    variant="body2"
                                                    fontWeight="medium"
                                                    sx={{
                                                        minWidth: 80,
                                                    }}
                                                >
                                                    {fieldComponent.componentName}{fieldComponent.description && (
                                                        <Tooltip
                                                            title={fieldComponent.description}
                                                            placement="top"
                                                            arrow
                                                        >
                                                            <HelpIcon
                                                                sx={{
                                                                    fontSize: 16,
                                                                    color: 'text.secondary',
                                                                    cursor: 'help',
                                                                    ml: 0.25
                                                                }}
                                                            />
                                                        </Tooltip>
                                                    )}
                                                </Typography>

                                            </Box>
                                            <Box sx={{ flex: 1 }}>
                                                {renderFieldComponent(fieldComponent, handleComponentUpdate)}
                                            </Box>
                                        </Box>
                                    </Grid>
                                ))}
                            </Grid>
                        );
                    }
                    return null;
                })}
            </Box>

            {formSchemaInfo.componentInfoList.length === 0 && (
                <Box
                    sx={{
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                        justifyContent: 'center',
                        height: 300,
                        color: 'text.secondary'
                    }}
                >
                    <Typography variant="h6">{t('workflow.noFormContent')}</Typography>
                    <Typography variant="body2">{t('workflow.pleaseAddComponentsInDesignMode')}</Typography>
                </Box>
            )}
        </Paper>
    );
}

export default FormPreview; 