import React from 'react';
import { Paper, Typography, Divider, Box, Tooltip } from '@mui/material';
import Grid from '@mui/material/Grid2';
import { HelpOutline as HelpIcon } from '@mui/icons-material';
import { FormStructure, FormComponent, RowContainer } from '../../../../types/workflowDesign';

interface FormPreviewProps {
    formStructure: FormStructure;
    renderFieldComponent: (component: FormComponent) => React.ReactNode;
}

function FormPreview({ formStructure, renderFieldComponent }: FormPreviewProps) {
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
                {formStructure.components.map((component) => {
                    if (component.type === 'row') {
                        return (
                            <Grid container spacing={2} key={component.id}>
                                {component.components.map((fieldComponent: FormComponent) => (
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
                                                    {fieldComponent.label}{fieldComponent.description && (
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
                                                {renderFieldComponent(fieldComponent)}
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

            {formStructure.components.length === 0 && (
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
                    <Typography variant="h6">暂无表单内容</Typography>
                    <Typography variant="body2">请在设计模式下添加组件</Typography>
                </Box>
            )}
        </Paper>
    );
}

export default FormPreview; 