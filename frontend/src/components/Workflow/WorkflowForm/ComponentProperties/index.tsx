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
    Alert,
    Tab,
    FormControlLabel,
    Checkbox
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
    Edit as EditIcon,
    Visibility as VisibilityIcon,
    VisibilityOff as VisibilityOffIcon
} from '@mui/icons-material';
import useSnackbar from '../../../../hooks/useSnackbar';
import { FormOption } from '../../../../types/workflowDesign';
import { IWorkflowComponent, IWorkflowComponentRow } from '../../../../types/workflow';



interface ComponentPropertiesProps {
    component: IWorkflowComponent | IWorkflowComponentRow;
    onUpdate: (component: IWorkflowComponent | IWorkflowComponentRow) => void;
}

function ComponentProperties({ component, onUpdate }: ComponentPropertiesProps) {
    const [showOptionKeys, setShowOptionKeys] = useState(false);
    const { showMessage } = useSnackbar();

    const handleChange = (key: string, value: any) => {
        //todo: for props
        if (['multiple', 'placeholder', 'defaultValue', 'format', 'timeFormat', 'dateFormat', 'timeZone', 'timeZoneName'].indexOf(key) !== -1) {
            onUpdate({
                ...component,
                props: {
                    ...(component as IWorkflowComponent).props,
                    [key]: value
                }
            });
            return;
        }
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

        const formComponent = component as IWorkflowComponent;
        const newOptionsWithKeys = [...(formComponent.props?.optionsWithKeys || [])];
        newOptionsWithKeys[index] = {
            ...newOptionsWithKeys[index],
            label: value
        };
        handleChange('optionsWithKeys', newOptionsWithKeys);
    };

    const addOption = () => {
        if (component.type === 'row') return;

        const formComponent = component as IWorkflowComponent;
        const newOption: FormOption = {
            id: `option_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
            label: `选项${(formComponent.props?.optionsWithKeys?.length || 0) + 1}`,
            key: `custom_field_option_${Math.random().toString(36).substr(2, 5)}`
        };
        const newOptionsWithKeys = [...(formComponent.props?.optionsWithKeys || []), newOption];
        handleChange('optionsWithKeys', newOptionsWithKeys);
    };

    const removeOption = (index: number) => {
        if (component.type === 'row') return;

        const formComponent = component as IWorkflowComponent;
        const newOptionsWithKeys = (formComponent.props?.optionsWithKeys || []).filter((_: FormOption, i: number) => i !== index);
        handleChange('optionsWithKeys', newOptionsWithKeys);
    };

    const toggleOptionKeysVisibility = () => {
        setShowOptionKeys(!showOptionKeys);
    };

    if (component.type === 'row') {
        return null;
    }

    return (
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <TextField
                label="字段标识"
                value={(component as IWorkflowComponent).componentKey || ''}
                fullWidth
                size="small"
                disabled
                helperText="系统自动生成的唯一标识，不可修改, 用于定时开发时的API调用"
            />

            <TextField
                label="名称"
                value={(component as IWorkflowComponent).componentName || ''}
                onChange={(e) => handleChange('componentName', e.target.value)}
                fullWidth
                size="small"
                required
                error={!((component as IWorkflowComponent).componentName || '').trim()}
                helperText={!((component as IWorkflowComponent).componentName || '').trim() ? '名称为必填项' : ''}
            />

            <TextField
                label="描述"
                value={(component as IWorkflowComponent).description || ''}
                onChange={(e) => handleChange('description', e.target.value)}
                fullWidth
                size="small"
                multiline
                rows={2}
                placeholder="输入字段描述，将在表单中显示为提示信息"
            />

            {(component.type === 'text' || component.type === 'textarea') && (
                <TextField
                    label="占位符"
                    value={(component as IWorkflowComponent).props.placeholder || ''}
                    onChange={(e) => handleChange('placeholder', e.target.value)}
                    fullWidth
                    size="small"
                />
            )}

            {['select', 'user', 'department'].indexOf(component.type) !== -1 && (
                <FormControlLabel
                    control={
                        <Checkbox
                            checked={(component as IWorkflowComponent).props?.multiple || false}
                            onChange={(e) => handleChange('multiple', e.target.checked)}
                            size="small"
                        />
                    }
                    label="支持多选"
                />
            )}

            <FormControl fullWidth size="small">
                <InputLabel>宽度</InputLabel>
                <Select
                    value={(component as IWorkflowComponent).layout.span || 12}
                    label="宽度"
                    onChange={(e) => handleLayoutChange('span', Number(e.target.value))}
                >
                    <MenuItem value={3}>1/4</MenuItem>
                    <MenuItem value={4}>1/3</MenuItem>
                    <MenuItem value={6}>1/2</MenuItem>
                    <MenuItem value={12}>全宽</MenuItem>
                </Select>
            </FormControl>
            {component.type === 'time' ? (<FormControl fullWidth size="small">
                <InputLabel>时间格式</InputLabel>
                <Select
                    value={(component as IWorkflowComponent).layout.span || 12}
                    label="格式"
                    onChange={(e) => handleLayoutChange('format', e.target.value)}
                >
                    <MenuItem value={"hh:mm:ss a"}>时:分:秒 上午/下午</MenuItem>
                    <MenuItem value={"hh aa"}>时 上午/下午</MenuItem>
                    <MenuItem value={"mm:ss"}>分:秒</MenuItem>
                </Select>
            </FormControl>) : null}

            {(component.type === 'select' || component.type === 'radio' || component.type === 'checkbox') && (
                <Box>
                    <Typography variant="subtitle2" gutterBottom>
                        选项
                    </Typography>

                    <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
                        <Button
                            variant="outlined"
                            size="small"
                            onClick={addOption}
                            startIcon={<AddIcon />}
                            sx={{ flex: 1 }}
                        >
                            添加选项
                        </Button>
                        <Button
                            variant="outlined"
                            size="small"
                            onClick={toggleOptionKeysVisibility}
                            startIcon={showOptionKeys ? <VisibilityOffIcon /> : <VisibilityIcon />}
                            sx={{ flex: 1 }}
                        >
                            {showOptionKeys ? '隐藏选项标识' : '显示选项标识'}
                        </Button>
                    </Box>

                    {showOptionKeys && <Alert severity="info">选项标识可用于API调用的参数</Alert>}

                    {(component as IWorkflowComponent).props?.optionsWithKeys?.map((option: FormOption, index: number) => (
                        <Box key={option.id} sx={{ display: 'flex', gap: 1, mb: 1 }}>
                            <TextField
                                value={showOptionKeys ? `${option.label} (${option.key})` : option.label}
                                onChange={(e) => handleOptionChange(index, e.target.value)}
                                size="small"
                                sx={{ flex: 1 }}
                                disabled={showOptionKeys}
                            />
                            {showOptionKeys ? null : <IconButton
                                size="small"
                                color="error"
                                onClick={() => removeOption(index)}
                            >
                                <DeleteIcon fontSize="small" />
                            </IconButton>}
                        </Box>
                    ))}
                </Box>
            )}
        </Box>
    );
}

export default ComponentProperties;