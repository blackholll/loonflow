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
import useSnackbar from '../../../hooks/useSnackbar';

import { componentCategories } from './componentCategories';
import type { IFormField } from './componentCategories';

// 将 IFormField 重命名为 FormField 以保持兼容性
type FormField = IFormField;

// 定义布局类型
interface LayoutConfig {
    type: 'vertical' | 'horizontal';
    gutter?: number;
    span?: number; // 组件在行中的跨度 (3=1/4, 4=1/3, 6=1/2, 12=全宽)
}

// 定义组件接口
interface FormComponent {
    id: string;
    type: string;
    label?: string;
    placeholder?: string;
    options?: string[];
    layout: LayoutConfig;
    [key: string]: any;
}

// 定义行容器接口
interface RowContainer {
    id: string;
    type: 'row';
    layout: LayoutConfig;
    components: FormComponent[];
    label?: string; // 添加可选的 label 属性
}

// 定义表单结构接口
interface FormStructure {
    type: 'form';
    layout: LayoutConfig;
    components: (RowContainer | FormComponent)[];
}

interface ComponentTemplate {
    type: string;
    label: string;
    icon: React.ReactNode;
    defaultProps: Partial<FormField>;
}

interface FormDesignProps {
    fieldInfoList?: any[];
}

function WorkflowForm({ fieldInfoList }: FormDesignProps) {
    const [formStructure, setFormStructure] = useState<FormStructure>({
        type: 'form',
        layout: { type: 'vertical', gutter: 16 },
        components: []
    });
    const [selectedComponent, setSelectedComponent] = useState<FormComponent | RowContainer | null>(null);
    const [isDragging, setIsDragging] = useState(false);
    const [dragOver, setDragOver] = useState(false);
    const canvasRef = useRef<HTMLDivElement>(null);
    const [isMoving, setIsMoving] = useState(false);
    const [movingComponent, setMovingComponent] = useState<string | null>(null);
    const [activeTab, setActiveTab] = useState(0); // 0: 设计, 1: 预览
    const { showMessage } = useSnackbar();
    const generateId = () => `component_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

    const handleDragStart = (e: React.DragEvent, template: ComponentTemplate) => {
        setIsDragging(true);
        e.dataTransfer.setData('application/json', JSON.stringify(template));
    };

    const handleDragOver = (e: React.DragEvent) => {
        e.preventDefault();
        setDragOver(true);
    };

    const handleDragLeave = () => {
        setDragOver(false);
    };

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        setDragOver(false);
        setIsDragging(false);

        try {
            const data = e.dataTransfer.getData('application/json');
            const parsedData = JSON.parse(data);

            if (parsedData.type === 'move') {
                return;
            }

            const template: ComponentTemplate = parsedData;
            const newComponent: FormComponent = {
                id: generateId(),
                type: template.type,
                label: template.defaultProps.label || '新字段',
                placeholder: template.defaultProps.placeholder || '',
                options: template.defaultProps.options || [],
                layout: { type: 'horizontal', span: 6 } // 默认1/2宽度
            };

            // 查找最后一个行容器，如果不存在或已满，创建新行
            const lastRow = formStructure.components[formStructure.components.length - 1] as RowContainer;

            if (lastRow && lastRow.type === 'row' && lastRow.components.length < 4) {
                // 检查当前行是否有足够空间
                const currentRowWidth = lastRow.components.reduce((sum: number, comp: FormComponent) => sum + (comp.layout.span || 12), 0);
                const componentSpan = newComponent.layout.span || 12;
                if (currentRowWidth + componentSpan <= 12) {
                    // 添加到现有行
                    setFormStructure(prev => ({
                        ...prev,
                        components: prev.components.map(comp => {
                            if (comp.id === lastRow.id) {
                                return {
                                    ...comp,
                                    components: [...comp.components, newComponent]
                                };
                            }
                            return comp;
                        })
                    }));
                    return;
                }
            }

            // 创建新行并添加组件
            const newRow: RowContainer = {
                id: generateId(),
                type: 'row',
                layout: { type: 'horizontal', gutter: 8 },
                components: [newComponent]
            };

            setFormStructure(prev => ({
                ...prev,
                components: [...prev.components, newRow]
            }));
        } catch (error) {
            console.log('拖拽数据解析失败，可能是组件移动操作');
        }
    };

    const handleComponentClick = (component: FormComponent | RowContainer) => {
        setSelectedComponent(component);
    };

    const handleComponentDelete = (componentId: string) => {
        setFormStructure(prev => ({
            ...prev,
            components: prev.components.filter(comp => comp.id !== componentId)
        }));
        if (selectedComponent?.id === componentId) {
            setSelectedComponent(null);
        }
    };

    const handleComponentUpdate = (updatedComponent: FormComponent | RowContainer) => {
        function updateInList(list: (FormComponent | RowContainer)[]): (FormComponent | RowContainer)[] {
            return list.map(comp => {
                if (comp.id === updatedComponent.id) {
                    return updatedComponent;
                }
                if (comp.type === 'row' && Array.isArray(comp.components)) {
                    return {
                        ...comp,
                        components: updateInList(comp.components)
                    };
                }
                return comp;
            });
        }
        setFormStructure(prev => ({
            ...prev,
            components: updateInList(prev.components)
        }));
        setSelectedComponent(updatedComponent);
    };

    const addNewRow = () => {
        const newRow: RowContainer = {
            id: generateId(),
            type: 'row',
            layout: { type: 'horizontal', gutter: 4 },
            components: []
        };

        setFormStructure(prev => ({
            ...prev,
            components: [...prev.components, newRow]
        }));
    };

    const addComponentToRow = (rowId: string, template: ComponentTemplate) => {
        const newComponent: FormComponent = {
            id: generateId(),
            type: template.type,
            label: template.defaultProps.label || '新字段',
            placeholder: template.defaultProps.placeholder || '',
            options: template.defaultProps.options || [],
            layout: { type: 'horizontal', span: 6 }
        };

        setFormStructure(prev => ({
            ...prev,
            components: prev.components.map(comp => {
                if (comp.id === rowId && comp.type === 'row') {
                    return {
                        ...comp,
                        components: [...comp.components, newComponent]
                    };
                }
                return comp;
            })
        }));
    };

    const removeComponentFromRow = (rowId: string, componentId: string) => {
        setFormStructure(prev => ({
            ...prev,
            components: prev.components.map((comp: RowContainer | FormComponent) => {
                if (comp.id === rowId && comp.type === 'row') {
                    return {
                        ...comp,
                        components: comp.components.filter((c: FormComponent) => c.id !== componentId)
                    };
                }
                return comp;
            }).filter((comp: RowContainer | FormComponent) => {
                // 如果行中没有组件了，删除整行
                if (comp.type === 'row' && comp.components.length === 0) {
                    return false;
                }
                return true;
            })
        }));
    };

    const renderFieldComponent = (component: FormComponent) => {
        const commonProps = {
            fullWidth: true,
            size: 'small' as const,
            variant: 'outlined' as const,
            placeholder: component.placeholder,
        };

        switch (component.type) {
            case 'text':
                return <TextField {...commonProps} />;
            case 'textarea':
                return <TextField {...commonProps} multiline rows={3} />;
            case 'select':
                return (
                    <FormControl fullWidth size="small">
                        <Select placeholder={component.placeholder}>
                            {component.options?.map((option, index) => (
                                <MenuItem key={index} value={option}>{option}</MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                );
            case 'date':
                return <TextField {...commonProps} type="date" InputLabelProps={{ shrink: true }} />;
            case 'file':
                return <TextField {...commonProps} type="file" InputLabelProps={{ shrink: true }} />;
            default:
                return <TextField {...commonProps} />;
        }
    };

    const handleComponentDragStart = (e: React.DragEvent, component: FormComponent | RowContainer) => {
        e.stopPropagation();
        e.dataTransfer.setData('application/json', JSON.stringify({
            type: 'move',
            componentId: component.id,
            componentType: component.type,
            sourceRowId: component.type === 'row' ? component.id : null
        }));
        e.dataTransfer.effectAllowed = 'move';
        setIsMoving(true);
        setMovingComponent(component.id);
    };

    const handleComponentDragOver = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        e.dataTransfer.dropEffect = 'move';
    };

    const handleComponentDrop = (e: React.DragEvent, targetComponentId: string) => {
        e.preventDefault();
        e.stopPropagation();
        const data = JSON.parse(e.dataTransfer.getData('application/json'));

        if (data.type === 'move' && data.componentId !== targetComponentId) {
            // 如果是行容器之间的拖拽
            if (data.componentType === 'row') {
                const sourceIndex = formStructure.components.findIndex((c: RowContainer | FormComponent) => c.id === data.componentId);
                const targetIndex = formStructure.components.findIndex((c: RowContainer | FormComponent) => c.id === targetComponentId);

                if (sourceIndex !== -1 && targetIndex !== -1) {
                    setFormStructure(prev => {
                        const newComponents = [...prev.components];
                        const [movedComponent] = newComponents.splice(sourceIndex, 1);
                        newComponents.splice(targetIndex, 0, movedComponent);
                        return { ...prev, components: newComponents };
                    });
                }
            }
        }

        setIsMoving(false);
        setMovingComponent(null);
    };

    const handleComponentDragEnd = (e: React.DragEvent) => {
        e.stopPropagation();
        setIsMoving(false);
        setMovingComponent(null);
    };

    // 行内组件拖拽处理
    const handleFieldComponentDrop = (e: React.DragEvent, targetComponentId: string, targetRowId: string) => {
        e.preventDefault();
        e.stopPropagation();
        const data = JSON.parse(e.dataTransfer.getData('application/json'));

        if (data.type === 'move' && data.componentId !== targetComponentId) {
            // 找到源组件和目标组件的位置
            let sourceComponent: FormComponent | null = null;
            let sourceRowId: string | null = null;
            let sourceIndex: number = -1;
            let targetIndex: number = -1;

            // 查找源组件
            formStructure.components.forEach((row: RowContainer | FormComponent) => {
                if (row.type === 'row') {
                    const index = row.components.findIndex((comp: FormComponent) => comp.id === data.componentId);
                    if (index !== -1) {
                        sourceComponent = row.components[index];
                        sourceRowId = row.id;
                        sourceIndex = index;
                    }
                }
            });

            // 查找目标组件
            const targetRow = formStructure.components.find((row: RowContainer | FormComponent) => row.id === targetRowId);
            if (targetRow && targetRow.type === 'row') {
                targetIndex = targetRow.components.findIndex((comp: FormComponent) => comp.id === targetComponentId);
            }

            if (sourceComponent && sourceRowId && sourceIndex !== -1 && targetIndex !== -1) {
                // 检查目标行的span总和是否超过12
                const targetRowData = formStructure.components.find((row: RowContainer | FormComponent) => row.id === targetRowId);
                if (targetRowData && targetRowData.type === 'row') {
                    const currentSpanSum = targetRowData.components.reduce((sum: number, comp: FormComponent) => {
                        // 如果是同一个组件，不计算其span
                        if (comp.id === (sourceComponent as FormComponent).id) {
                            return sum;
                        }
                        return sum + (comp.layout.span || 12);
                    }, 0);

                    const newSpanSum = currentSpanSum + ((sourceComponent as FormComponent).layout.span || 12);
                    if (newSpanSum > 12) {
                        console.log('行内组件span总和不能超过12');
                        showMessage('行内组件宽度不得超过1', 'error');
                        setIsMoving(false);
                        setMovingComponent(null);
                        return;
                    }
                }

                setFormStructure(prev => {
                    const newComponents = [...prev.components];

                    // 从源行移除组件
                    const sourceRowIndex = newComponents.findIndex(row => row.id === sourceRowId);
                    if (sourceRowIndex !== -1) {
                        const sourceRow = { ...newComponents[sourceRowIndex] };
                        sourceRow.components = [...sourceRow.components];
                        sourceRow.components.splice(sourceIndex, 1);
                        newComponents[sourceRowIndex] = sourceRow;
                    }

                    // 添加到目标行
                    const targetRowIndex = newComponents.findIndex(row => row.id === targetRowId);
                    if (targetRowIndex !== -1) {
                        const targetRow = { ...newComponents[targetRowIndex] };
                        targetRow.components = [...targetRow.components];
                        targetRow.components.splice(targetIndex, 0, sourceComponent!);
                        newComponents[targetRowIndex] = targetRow;
                    }

                    return { ...prev, components: newComponents };
                });
            }
        }

        setIsMoving(false);
        setMovingComponent(null);
    };

    // 行容器onDrop
    const handleDropToRow = (e: React.DragEvent, rowId: string) => {
        e.preventDefault();
        setDragOver(false);
        setIsDragging(false);
        try {
            const data = e.dataTransfer.getData('application/json');
            const parsedData = JSON.parse(data);

            // 如果是组件移动操作
            if (parsedData.type === 'move') {
                // 找到源组件
                let sourceComponent: FormComponent | null = null;
                let sourceRowId: string | null = null;
                let sourceIndex: number = -1;

                formStructure.components.forEach((row: RowContainer | FormComponent) => {
                    if (row.type === 'row') {
                        const index = row.components.findIndex((comp: FormComponent) => comp.id === parsedData.componentId);
                        if (index !== -1) {
                            sourceComponent = row.components[index];
                            sourceRowId = row.id;
                            sourceIndex = index;
                        }
                    }
                });

                // 如果找到源组件且不是同一个行
                if (sourceComponent && sourceRowId && sourceRowId !== rowId) {
                    // 检查目标行的span总和是否超过12
                    const targetRowData = formStructure.components.find((row: RowContainer | FormComponent) => row.id === rowId);
                    if (targetRowData && targetRowData.type === 'row') {
                        const currentSpanSum = targetRowData.components.reduce((sum: number, comp: FormComponent) => {
                            return sum + (comp.layout.span || 12);
                        }, 0);

                        const newSpanSum = currentSpanSum + ((sourceComponent as FormComponent).layout?.span || 12);
                        console.log('newSpanSum', newSpanSum);
                        if (newSpanSum > 12) {
                            console.log('行内组件span总和不能超过12');
                            setIsMoving(false);
                            setMovingComponent(null);
                            return;
                        }
                    }

                    setFormStructure(prev => {
                        const newComponents = [...prev.components];

                        // 从源行移除组件
                        const sourceRowIndex = newComponents.findIndex(row => row.id === sourceRowId);
                        if (sourceRowIndex !== -1) {
                            const sourceRow = { ...newComponents[sourceRowIndex] };
                            sourceRow.components = [...sourceRow.components];
                            sourceRow.components.splice(sourceIndex, 1);
                            newComponents[sourceRowIndex] = sourceRow;
                        }

                        // 添加到目标行
                        const targetRowIndex = newComponents.findIndex(row => row.id === rowId);
                        if (targetRowIndex !== -1) {
                            const targetRow = { ...newComponents[targetRowIndex] };
                            targetRow.components = [...targetRow.components];
                            targetRow.components.push(sourceComponent!);
                            newComponents[targetRowIndex] = targetRow;
                        }

                        return { ...prev, components: newComponents };
                    });
                }
                return;
            }

            // 原有的从组件库拖拽逻辑
            const template: ComponentTemplate = parsedData;
            const newComponent: FormComponent = {
                id: generateId(),
                type: template.type,
                label: template.defaultProps.label || '新字段',
                placeholder: template.defaultProps.placeholder || '',
                options: template.defaultProps.options || [],
                layout: { type: 'horizontal', span: 6 }
            };
            setFormStructure(prev => ({
                ...prev,
                components: prev.components.map(comp => {
                    if (comp.id === rowId && comp.type === 'row') {
                        // 检查行内宽度
                        const currentRowWidth = comp.components.reduce((sum: number, c: FormComponent) => sum + (c.layout.span || 12), 0);
                        const componentSpan = newComponent.layout.span || 12;
                        if (currentRowWidth + componentSpan <= 12) {
                            return {
                                ...comp,
                                components: [...comp.components, newComponent]
                            };
                        } else {
                            showMessage('行内组件宽度不得超过1', 'error');
                        }
                    }
                    return comp;
                })
            }));
        } catch (error) {
            console.log('拖拽数据解析失败，可能是组件移动操作');
        }
    };

    // 渲染设计模式
    const renderDesignMode = () => (
        <Paper
            ref={canvasRef}
            sx={{
                flex: 1,
                p: 3,
                overflow: 'auto',
                backgroundColor: dragOver ? 'action.hover' : 'background.paper',
                border: dragOver ? '2px dashed' : '1px solid',
                borderColor: dragOver ? 'primary.main' : 'divider',
                transition: 'all 0.2s'
            }}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={(e) => {
                // 只有拖到空白处才新建行
                if (e.target === canvasRef.current) handleDrop(e);
            }}
        >
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="body2" color="text.secondary" sx={{ fontStyle: 'italic' }}>
                    提示：可以直接拖拽组件来调整位置
                </Typography>
                <Button
                    variant="outlined"
                    size="small"
                    startIcon={<AddIcon />}
                    onClick={addNewRow}
                >
                    添加行
                </Button>
            </Box>

            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                {formStructure.components.map((component) => {
                    if (component.type === 'row') {
                        return (
                            <Box
                                key={component.id}
                                sx={{
                                    border: selectedComponent?.id === component.id ? '2px solid' : '1px solid',
                                    borderColor: selectedComponent?.id === component.id ? 'primary.main' : 'divider',
                                    borderRadius: 1,
                                    p: 1,
                                    backgroundColor: selectedComponent?.id === component.id ? 'action.selected' : 'transparent',
                                    opacity: movingComponent === component.id ? 0.6 : 1,
                                    transition: 'all 0.2s ease',
                                    '&:hover': {
                                        borderColor: 'primary.main',
                                        backgroundColor: selectedComponent?.id === component.id ? 'action.selected' : 'action.hover',
                                    }
                                }}
                                onClick={() => handleComponentClick(component)}
                                draggable
                                onDragStart={(e) => handleComponentDragStart(e, component)}
                                onDragOver={handleDragOver}
                                onDrop={(e) => handleDropToRow(e, component.id)}
                                onDragEnd={handleComponentDragEnd}
                            >
                                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                                    <DragIcon sx={{ fontSize: 16, mr: 1, color: 'text.secondary' }} />
                                    <Typography variant="caption" color="text.secondary">
                                        行容器
                                    </Typography>
                                    <Box sx={{ flex: 1 }} />
                                    <IconButton
                                        size="small"
                                        color="error"
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            handleComponentDelete(component.id);
                                        }}
                                    >
                                        <DeleteIcon fontSize="small" />
                                    </IconButton>
                                </Box>

                                <Grid container spacing={1}>
                                    {component.components.map((fieldComponent: FormComponent) => (
                                        <Grid
                                            key={fieldComponent.id}
                                            size={fieldComponent.layout.span || 12}
                                        >
                                            <Box
                                                sx={{
                                                    position: 'relative',
                                                    p: 1,
                                                    border: selectedComponent?.id === fieldComponent.id ? '2px solid' : '1px solid',
                                                    borderColor: selectedComponent?.id === fieldComponent.id ? 'primary.main' : 'transparent',
                                                    borderRadius: 1,
                                                    cursor: 'grab',
                                                    display: 'flex',
                                                    alignItems: 'center',
                                                    backgroundColor: selectedComponent?.id === fieldComponent.id ? 'action.selected' : 'transparent',
                                                    opacity: movingComponent === fieldComponent.id ? 0.6 : 1,
                                                    transition: 'all 0.2s ease',
                                                    '&:hover': {
                                                        borderColor: 'primary.main',
                                                        backgroundColor: selectedComponent?.id === fieldComponent.id ? 'action.selected' : 'action.hover',
                                                        '& .delete-button': {
                                                            opacity: 1
                                                        }
                                                    }
                                                }}
                                                onClick={(e) => {
                                                    e.stopPropagation();
                                                    handleComponentClick(fieldComponent);
                                                }}
                                                draggable
                                                onDragStart={(e) => handleComponentDragStart(e, fieldComponent)}
                                                onDragOver={handleComponentDragOver}
                                                onDrop={(e) => handleFieldComponentDrop(e, fieldComponent.id, component.id)}
                                                onDragEnd={handleComponentDragEnd}
                                            >
                                                <Box sx={{ flex: 1, display: 'flex', alignItems: 'center', gap: 2 }}>
                                                    <Typography
                                                        variant="body2"
                                                        sx={{
                                                            minWidth: '80px',
                                                            fontWeight: 'normal',
                                                        }}
                                                    >
                                                        {fieldComponent.label}
                                                    </Typography>
                                                    <Box sx={{ flex: 1 }}>
                                                        {renderFieldComponent(fieldComponent)}
                                                    </Box>
                                                </Box>
                                                <Box
                                                    className="delete-button"
                                                    sx={{
                                                        width: 20,
                                                        height: 40,
                                                        display: 'flex',
                                                        alignItems: 'center',
                                                        justifyContent: 'center',
                                                        cursor: 'pointer',
                                                        ml: 1,
                                                        userSelect: 'none',
                                                        opacity: 0,
                                                        transition: 'opacity 0.2s',
                                                        color: 'error.main',
                                                        '&:hover': {
                                                            backgroundColor: 'error.light',
                                                            borderRadius: 1
                                                        }
                                                    }}
                                                    onClick={e => {
                                                        e.stopPropagation();
                                                        removeComponentFromRow(component.id, fieldComponent.id);
                                                    }}
                                                >
                                                    <span style={{ fontSize: 16 }}>×</span>
                                                </Box>
                                            </Box>
                                        </Grid>
                                    ))}
                                </Grid>

                                {component.components.length === 0 && (
                                    <Box
                                        sx={{
                                            display: 'flex',
                                            alignItems: 'center',
                                            justifyContent: 'center',
                                            height: 60,
                                            border: '1px dashed',
                                            borderColor: 'divider',
                                            borderRadius: 1,
                                            color: 'text.secondary'
                                        }}
                                    >
                                        <Typography variant="body2">拖拽组件到此行</Typography>
                                    </Box>
                                )}
                            </Box>
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
                    <DragIcon sx={{ fontSize: 48, mb: 2 }} />
                    <Typography variant="h6">拖拽组件到此处</Typography>
                    <Typography variant="body2">从左侧组件库拖拽组件到画布中</Typography>
                </Box>
            )}
        </Paper>
    );

    // 渲染预览模式
    const renderPreviewMode = () => (
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
            <Typography variant="h6" gutterBottom>
                表单预览
            </Typography>
            <Divider sx={{ mb: 3 }} />

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
                                            <Typography variant="body2" fontWeight="medium" sx={{ minWidth: 80 }}>
                                                {fieldComponent.label}
                                            </Typography>
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
                                        {template.label}
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
                {activeTab === 0 ? renderDesignMode() : renderPreviewMode()}
            </Box>

            {/* 右侧属性面板 */}
            <Paper sx={{ width: 300, p: 2, overflow: 'auto' }}>
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

// 组件属性编辑组件
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
        return (
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <Typography variant="subtitle1" color="primary">
                    行容器设置
                </Typography>

                <FormControl fullWidth size="small">
                    <InputLabel>间距</InputLabel>
                    <Select
                        value={component.layout.gutter || 8}
                        label="间距"
                        onChange={(e) => handleLayoutChange('gutter', e.target.value)}
                    >
                        <MenuItem value={4}>4px</MenuItem>
                        <MenuItem value={8}>8px</MenuItem>
                        <MenuItem value={16}>16px</MenuItem>
                        <MenuItem value={24}>24px</MenuItem>
                    </Select>
                </FormControl>
            </Box>
        );
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

export default WorkflowForm; 