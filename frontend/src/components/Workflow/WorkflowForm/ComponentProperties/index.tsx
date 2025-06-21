import React, { useState, useRef } from 'react';
import {
    Box,
    Paper,
    Typography,
    Card,
    CardContent,
    TextField,
    Select,
    MenuItem,
    FormControl,
    InputLabel,
    Button,
    Divider,
    IconButton,
    Tooltip,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    Tabs,
    Tab
} from '@mui/material';
import Grid from '@mui/material/Grid2';
import {
    TextFields as TextFieldsIcon,
    CheckBox as CheckBoxIcon,
    RadioButtonChecked as RadioButtonIcon,
    ViewList as SelectIcon,
    Schedule as DateIcon,
    AttachFile as FileIcon,
    Delete as DeleteIcon,
    Settings as SettingsIcon,
    DragIndicator as DragIcon,
    Add as AddIcon,
    ViewColumn as RowIcon,
    Visibility as PreviewIcon,
    Edit as EditIcon
} from '@mui/icons-material';
import useSnackbar from '../../../../hooks/useSnackbar';
import { FormStructure, FormComponent, RowContainer, ComponentTemplate, FormDesignProps } from '../../../../types/workflowDesign';



interface ComponentPropertiesProps {
    component: FormComponent | RowContainer;
    onUpdate: (component: FormComponent | RowContainer) => void;
}

function ComponentProperties({ component, onUpdate }: ComponentPropertiesProps) {
    const handleChange = (key: string, value: any) => {
        onUpdate({
            ...component,
            [key]: value
        });
    };

    const handleLayoutChange = (key: string, value: any) => {
        onUpdate({
            ...component,
            layout: {
                ...component.layout,
                [key]: value
            }
        });
    };

    const handleOptionChange = (index: number, value: string) => {
        if (component.type === 'row') return;

        const formComponent = component as FormComponent;
        const newOptions = [...(formComponent.options || [])];
        newOptions[index] = value;
        handleChange('options', newOptions);
    };

    const addOption = () => {
        if (component.type === 'row') return;

        const formComponent = component as FormComponent;
        const newOptions = [...(formComponent.options || []), `选项${(formComponent.options?.length || 0) + 1}`];
        handleChange('options', newOptions);
    };

    const removeOption = (index: number) => {
        if (component.type === 'row') return;

        const formComponent = component as FormComponent;
        const newOptions = formComponent.options?.filter((_: string, i: number) => i !== index) || [];
        handleChange('options', newOptions);
    };

    if (component.type === 'row') {
        return null;
    }

    return (
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <TextField
                label="字段标签"
                value={(component as FormComponent).label || ''}
                onChange={(e) => handleChange('label', e.target.value)}
                fullWidth
                size="small"
            />

            {(component.type === 'text' || component.type === 'textarea') && (
                <TextField
                    label="占位符"
                    value={(component as FormComponent).placeholder || ''}
                    onChange={(e) => handleChange('placeholder', e.target.value)}
                    fullWidth
                    size="small"
                />
            )}

            <FormControl fullWidth size="small">
                <InputLabel>宽度</InputLabel>
                <Select
                    value={(component as FormComponent).layout.span || 12}
                    label="宽度"
                    onChange={(e) => handleLayoutChange('span', Number(e.target.value))}
                >
                    <MenuItem value={3}>1/4</MenuItem>
                    <MenuItem value={4}>1/3</MenuItem>
                    <MenuItem value={6}>1/2</MenuItem>
                    <MenuItem value={12}>全宽</MenuItem>
                </Select>
            </FormControl>

            {(component.type === 'select' || component.type === 'radio' || component.type === 'checkbox') && (
                <Box>
                    <Typography variant="subtitle2" gutterBottom>
                        选项
                    </Typography>
                    {(component as FormComponent).options?.map((option, index) => (
                        <Box key={index} sx={{ display: 'flex', gap: 1, mb: 1 }}>
                            <TextField
                                value={option}
                                onChange={(e) => handleOptionChange(index, e.target.value)}
                                size="small"
                                sx={{ flex: 1 }}
                            />
                            <IconButton
                                size="small"
                                color="error"
                                onClick={() => removeOption(index)}
                            >
                                <DeleteIcon fontSize="small" />
                            </IconButton>
                        </Box>
                    ))}
                    <Button
                        variant="outlined"
                        size="small"
                        onClick={addOption}
                        fullWidth
                    >
                        添加选项
                    </Button>
                </Box>
            )}
        </Box>
    );
}

export default ComponentProperties;