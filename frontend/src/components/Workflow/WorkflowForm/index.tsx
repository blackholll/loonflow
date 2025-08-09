import React, { useState, useRef, useEffect, useCallback } from 'react';
import {
    Box,
    Paper,
    Typography,
    Card,
    TextField,
    Divider,
    Tabs,
    Tab,
    RadioGroup,
    Radio,
    FormControlLabel,
    Checkbox,
    FormGroup,
    Chip,
    ListItemText,
    Autocomplete
} from '@mui/material';
import {
    Visibility as PreviewIcon,
    Edit as EditIcon
} from '@mui/icons-material';
import useSnackbar from '../../../hooks/useSnackbar';
import { FormStructure, ComponentTemplate, FormDesignProps } from '../../../types/workflowDesign';
import componentCategories from './ComponentCategories';
import ComponentProperties from './ComponentProperties';
import FormDesign from './FormDesign';
import FormPreview from './FormPreview';
import { TimePicker } from '@mui/x-date-pickers/TimePicker';
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';
import { IWorkflowComponent, IWorkflowComponentRow, IFormSchema, createEmptyWorkflowFullDefinition } from '../../../types/workflow';
import { v4 as uuidv4 } from 'uuid';

interface WorkflowFormProps {
    onFormSchemaChange: (newFormSchema: IFormSchema) => void;
    formSchema: { componentInfoList: (IWorkflowComponent | IWorkflowComponentRow)[]; }
}


function WorkflowForm({ onFormSchemaChange, formSchema }: WorkflowFormProps) {
    const [formSchemaInfo, setFormSchemaInfo] = useState<IFormSchema>(formSchema);
    const [selectedComponent, setSelectedComponent] = useState<IWorkflowComponent | IWorkflowComponentRow | null>(null);
    const [isDragging, setIsDragging] = useState(false);
    const [dragOver, setDragOver] = useState(false);
    const [isMoving, setIsMoving] = useState(false);
    const [movingComponent, setMovingComponent] = useState<string | null>(null);
    const [activeTab, setActiveTab] = useState(0); // 0: 设计, 1: 预览
    const generateId = () => `temp_${uuidv4()}`;


    const handleFormSchemaChange = useCallback((newFormSchema: IFormSchema) => {
        setFormSchemaInfo(newFormSchema);
        onFormSchemaChange(newFormSchema);
    }, [onFormSchemaChange]);

    // 生成5位随机英文字母
    const generateRandomLetters = () => {
        const letters = 'abcdefghijklmnopqrstuvwxyz';
        let result = '';
        for (let i = 0; i < 5; i++) {
            result += letters.charAt(Math.floor(Math.random() * letters.length));
        }
        return result;
    };

    // 生成唯一的字段标识
    const generateUniqueFieldKey = (existingComponents: (IWorkflowComponent | IWorkflowComponentRow)[]) => {
        const getAllFieldKeys = (components: (IWorkflowComponent | IWorkflowComponentRow)[]): string[] => {
            const keys: string[] = [];
            components.forEach(comp => {
                if (comp.type === 'row') {
                    (comp as IWorkflowComponentRow).children.forEach((fieldComp: IWorkflowComponent) => {
                        if (fieldComp.componentKey) {
                            keys.push(fieldComp.componentKey);
                        }
                    });
                } else if ((comp as IWorkflowComponent).componentKey) {
                    keys.push((comp as IWorkflowComponent).componentKey!);
                }
            });
            return keys;
        };

        const existingKeys = getAllFieldKeys(existingComponents);
        let newKey: string;
        let attempts = 0;
        const maxAttempts = 100; // 防止无限循环

        do {
            newKey = `custom_field_${generateRandomLetters()}`;
            attempts++;
            if (attempts > maxAttempts) {
                // 如果尝试次数过多，使用时间戳作为后缀
                newKey = `custom_field_${generateRandomLetters()}_${Date.now()}`;
                break;
            }
        } while (existingKeys.includes(newKey));

        return newKey;
    };

    // 生成唯一的选项标识
    const generateUniqueOptionKey = (existingComponents: (IWorkflowComponent | IWorkflowComponentRow)[]) => {
        const getAllOptionKeys = (components: (IWorkflowComponentRow | IWorkflowComponent)[]): string[] => {
            const keys: string[] = [];
            components.forEach(comp => {
                if (comp.type === 'row') {
                    (comp as IWorkflowComponentRow).children.forEach((fieldComp: IWorkflowComponent) => {
                        if ((fieldComp as IWorkflowComponent).props?.optionsWithKeys) {
                            (fieldComp as IWorkflowComponent).props?.optionsWithKeys?.forEach((option: any) => {
                                keys.push(option.key);
                            });
                        }
                    });
                } else if ((comp as IWorkflowComponent).props?.optionsWithKeys) {
                    (comp as IWorkflowComponent).props?.optionsWithKeys!.forEach((option: any) => {
                        keys.push(option.key);
                    });
                }
            });
            return keys;
        };

        const existingKeys = getAllOptionKeys(existingComponents);
        let newKey: string;
        let attempts = 0;
        const maxAttempts = 100; // 防止无限循环

        do {
            newKey = `custom_field_option_${generateRandomLetters()}`;
            attempts++;
            if (attempts > maxAttempts) {
                // 如果尝试次数过多，使用时间戳作为后缀
                newKey = `custom_field_option_${generateRandomLetters()}_${Date.now()}`;
                break;
            }
        } while (existingKeys.includes(newKey));

        return newKey;
    };

    const handleDragStart = (e: React.DragEvent, template: ComponentTemplate) => {
        setIsDragging(true);
        e.dataTransfer.setData('application/json', JSON.stringify(template));
    };

    const handleComponentUpdate = (updatedComponent: IWorkflowComponent | IWorkflowComponentRow) => {
        function updateInList(list: (IWorkflowComponentRow | IWorkflowComponent)[]): (IWorkflowComponentRow | IWorkflowComponent)[] {
            return list.map(comp => {
                if (comp.id === updatedComponent.id) {
                    return updatedComponent;
                }
                if (comp.type === 'row' && Array.isArray((comp as IWorkflowComponentRow).children)) {
                    return {
                        ...comp,
                        children: (comp as IWorkflowComponentRow).children.map(field =>
                            field.id === updatedComponent.id ? updatedComponent as IWorkflowComponent : field
                        )
                    };
                }
                return comp;
            });
        }

        const updatedFormSchema = {
            ...formSchemaInfo,
            componentInfoList: updateInList(formSchemaInfo.componentInfoList) as (IWorkflowComponent[] | IWorkflowComponentRow[])
        };
        console.log('updatedFormSchema', updatedFormSchema);
        setFormSchemaInfo(updatedFormSchema);
        setSelectedComponent(updatedComponent);
        onFormSchemaChange(updatedFormSchema);
    };

    const renderFieldComponent = (component: IWorkflowComponent) => {
        const commonProps = {
            fullWidth: true,
            size: 'small' as const,
            variant: 'outlined' as const,
            placeholder: component.props.placeholder,
        };

        // 获取选项数据，只使用optionsWithKeys
        const getOptions = () => {
            return component.props?.optionsWithKeys?.map((option: any) => option.label) || [];
        };

        const options = getOptions();

        switch (component.type) {
            case 'text':
                return <TextField {...commonProps} />;
            case 'textarea':
                return <TextField {...commonProps} multiline rows={3} />;
            case 'number':
                return <TextField type="number" {...commonProps} />;
            case 'select':
                return (
                    <Autocomplete
                        options={options}
                        multiple={component.props?.multiple || false}
                        size="small"
                        onChange={(_, newValue) => {
                            // 更新组件值
                            const updatedComponent = {
                                ...component,
                                value: newValue
                            };
                            handleComponentUpdate(updatedComponent);
                        }}
                        freeSolo={false}
                        disableClearable={false}
                        renderInput={(params) => (
                            <TextField
                                {...params}
                                placeholder={component.props.placeholder}
                                variant="outlined"
                                size="small"
                            />
                        )}
                        renderTags={(value, getTagProps) =>
                            value.map((option, index) => (
                                <Chip
                                    variant="outlined"
                                    label={option as string}
                                    size="small"
                                    {...getTagProps({ index })}
                                />
                            ))
                        }
                        renderOption={(props, option) => (
                            <li {...props}>
                                <ListItemText primary={option as string} />
                            </li>
                        )}
                        filterOptions={(options, { inputValue }) => {
                            const filtered = options.filter((option: any) =>
                                option.toLowerCase().includes(inputValue.toLowerCase())
                            );
                            return filtered;
                        }}
                        noOptionsText="未找到匹配的选项"
                        clearOnBlur={false}
                        selectOnFocus
                        clearOnEscape
                        isOptionEqualToValue={(option, value) => option === value}
                    />
                );
            case 'radio':
                return (
                    <RadioGroup row>
                        {options.map((option: any, index: any) => (
                            <FormControlLabel key={index} value={option} control={<Radio />} label={option as string} />
                        ))}
                    </RadioGroup>)
            case 'checkbox':
                return (
                    <FormGroup row>
                        {options.map((option: any, index: any) => (
                            <FormControlLabel key={index} value={option} control={<Checkbox />} label={option as string} />
                        ))}
                    </FormGroup>
                )
            case 'time':
                return <TimePicker format="hh:mm::ss aa" slotProps={{
                    textField: { fullWidth: true }
                }} />
            case 'date':
                return <DateTimePicker slotProps={{
                    textField: { fullWidth: true }
                }} />
            case 'user':
                return (
                    <Autocomplete
                        options={['张三', '李四']}
                        multiple={component.props?.multiple || false}
                        size="small"
                        onChange={(_, newValue) => {
                            // 更新组件值
                            const updatedComponent = {
                                ...component,
                                value: newValue
                            };
                            handleComponentUpdate(updatedComponent);
                        }}
                        freeSolo={false}
                        disableClearable={false}
                        renderInput={(params) => (
                            <TextField
                                {...params}
                                placeholder={component.props.placeholder}
                                variant="outlined"
                                size="small"
                            />
                        )}
                        renderTags={(value, getTagProps) =>
                            value.map((option, index) => (
                                <Chip
                                    variant="outlined"
                                    label={option}
                                    size="small"
                                    {...getTagProps({ index })}
                                />
                            ))
                        }
                        renderOption={(props, option) => (
                            <li {...props}>
                                <ListItemText primary={option} />
                            </li>
                        )}
                        filterOptions={(options, { inputValue }) => {
                            const filtered = options.filter(option =>
                                option.toLowerCase().includes(inputValue.toLowerCase())
                            );
                            return filtered;
                        }}
                        noOptionsText="未找到匹配的选项"
                        clearOnBlur={false}
                        selectOnFocus
                        clearOnEscape
                        isOptionEqualToValue={(option, value) => option === value}
                    />
                );
            case 'department':
                return (
                    <Autocomplete
                        options={['行政部', '财务部']}
                        multiple={component.props?.multiple || false}
                        size="small"
                        onChange={(_, newValue) => {
                            // 更新组件值
                            const updatedComponent = {
                                ...component,
                                value: newValue
                            };
                            handleComponentUpdate(updatedComponent);
                        }}
                        freeSolo={false}
                        disableClearable={false}
                        renderInput={(params) => (
                            <TextField
                                {...params}
                                placeholder={component.props.placeholder}
                                variant="outlined"
                                size="small"
                            />
                        )}
                        renderTags={(value, getTagProps) =>
                            value.map((option, index) => (
                                <Chip
                                    variant="outlined"
                                    label={option}
                                    size="small"
                                    {...getTagProps({ index })}
                                />
                            ))
                        }
                        renderOption={(props, option) => (
                            <li {...props}>
                                <ListItemText primary={option} />
                            </li>
                        )}
                        filterOptions={(options, { inputValue }) => {
                            const filtered = options.filter(option =>
                                option.toLowerCase().includes(inputValue.toLowerCase())
                            );
                            return filtered;
                        }}
                        noOptionsText="未找到匹配的选项"
                        clearOnBlur={false}
                        selectOnFocus
                        clearOnEscape
                        isOptionEqualToValue={(option, value) => option === value}
                    />
                );
            case 'file':
                return <TextField {...commonProps} type="file" InputLabelProps={{ shrink: true }} />;
            default:
                return <TextField {...commonProps} />;
        }
    };


    return (
        <Box sx={{ display: 'flex', height: 'calc(100vh - 100px)', gap: 2, p: 2 }}>
            {/* 左侧组件库 */}
            <Paper sx={{ width: 250, p: 2, overflow: 'auto' }}>
                <Typography variant="h6" gutterBottom>
                    组件库
                </Typography>
                <Divider sx={{ mb: 2 }} />

                {Object.entries(componentCategories).map(([categoryKey, category]) => (
                    <Box key={categoryKey} sx={{ mb: 3 }}>
                        <Typography variant="subtitle2" color="primary" gutterBottom>
                            {category.title}
                        </Typography>
                        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                            {category.components.map((template) => (
                                <Card
                                    key={template.type}
                                    sx={{
                                        cursor: 'grab',
                                        '&:hover': {
                                            boxShadow: 2,
                                            backgroundColor: 'action.hover'
                                        },
                                        display: 'flex',
                                        alignItems: 'center',
                                        p: 1,
                                        transition: 'all 0.2s',
                                        width: 'calc(50% - 4px)',
                                        boxSizing: 'border-box',
                                        minHeight: '40px',
                                    }}
                                    draggable
                                    onDragStart={(e) => handleDragStart(e, template)}
                                >
                                    <Box sx={{
                                        color: 'primary.main',
                                        mr: 0.5,
                                        display: 'flex',
                                        alignItems: 'center'
                                    }}>
                                        {React.cloneElement(template.icon as React.ReactElement, {
                                            sx: { fontSize: 16 }
                                        })}
                                    </Box>
                                    <Typography variant="body2" sx={{ flex: 1 }} style={{ fontSize: 11 }}>
                                        {template.componentName}
                                    </Typography>
                                </Card>
                            ))}
                        </Box>
                    </Box>
                ))}
            </Paper>

            {/* 中间画布区域 */}
            <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
                {/* Tab 切换 */}
                <Paper sx={{ mb: 2 }}>
                    <Tabs value={activeTab} onChange={(_, newValue) => setActiveTab(newValue)}>
                        <Tab
                            icon={<EditIcon />}
                            label="设计"
                            iconPosition="start"
                        />
                        <Tab
                            icon={<PreviewIcon />}
                            label="预览"
                            iconPosition="start"
                        />
                    </Tabs>
                </Paper>

                {/* 画布内容 */}
                {activeTab === 0 ? (
                    <FormDesign
                        formSchemaInfo={formSchemaInfo}
                        selectedComponent={selectedComponent}
                        isDragging={isDragging}
                        dragOver={dragOver}
                        isMoving={isMoving}
                        movingComponent={movingComponent}
                        onFormSchemaChange={handleFormSchemaChange}
                        onSelectedComponentChange={setSelectedComponent}
                        onIsDraggingChange={setIsDragging}
                        onDragOverChange={setDragOver}
                        onIsMovingChange={setIsMoving}
                        onMovingComponentChange={setMovingComponent}
                        generateId={generateId}
                        generateUniqueFieldKey={generateUniqueFieldKey}
                        generateUniqueOptionKey={generateUniqueOptionKey}
                        renderFieldComponent={renderFieldComponent}
                    />
                ) : (
                    <FormPreview
                        formSchemaInfo={formSchemaInfo}
                        renderFieldComponent={renderFieldComponent}
                    />
                )}
            </Box>

            {/* 右侧属性面板 */}
            <Paper sx={{ width: 350, p: 2, overflow: 'auto' }}>
                <Typography variant="h6" gutterBottom>
                    属性设置
                </Typography>
                <Divider sx={{ mb: 2 }} />

                {selectedComponent ? (
                    <ComponentProperties
                        component={selectedComponent}
                        onUpdate={handleComponentUpdate}
                    />
                ) : (
                    <Typography variant="body2" color="text.secondary">
                        选择一个组件来编辑其属性
                    </Typography>
                )}
            </Paper>
        </Box>
    );
}



export default WorkflowForm; 