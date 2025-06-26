import React, { useRef } from 'react';
import {
    Box,
    Paper,
    Typography,
    Button,
    IconButton,
    Tooltip
} from '@mui/material';
import Grid from '@mui/material/Grid2';

import {
    Delete as DeleteIcon,
    DragIndicator as DragIcon,
    Add as AddIcon,
    HelpOutline as HelpIcon
} from '@mui/icons-material';
import { FormStructure, IFormField, RowContainer, ComponentTemplate, FormOption } from '../../../../types/workflowDesign';
import useSnackbar from '../../../../hooks/useSnackbar';

interface FormDesignProps {
    formStructure: FormStructure;
    selectedComponent: IFormField | RowContainer | null;
    isDragging: boolean;
    dragOver: boolean;
    isMoving: boolean;
    movingComponent: string | null;
    onFormStructureChange: (structure: FormStructure) => void;
    onSelectedComponentChange: (component: IFormField | RowContainer | null) => void;
    onIsDraggingChange: (dragging: boolean) => void;
    onDragOverChange: (dragOver: boolean) => void;
    onIsMovingChange: (moving: boolean) => void;
    onMovingComponentChange: (componentId: string | null) => void;
    generateId: () => string;
    generateUniqueFieldKey: (existingComponents: (RowContainer | IFormField)[]) => string;
    generateUniqueOptionKey: (existingComponents: (RowContainer | IFormField)[]) => string;
    renderFieldComponent: (component: IFormField) => React.ReactNode;
}

function FormDesign(props: FormDesignProps) {
    const {
        formStructure,
        selectedComponent,
        dragOver,
        movingComponent,
        onFormStructureChange,
        onSelectedComponentChange,
        onIsDraggingChange,
        onDragOverChange,
        onIsMovingChange,
        onMovingComponentChange,
        generateId,
        generateUniqueFieldKey,
        generateUniqueOptionKey,
        renderFieldComponent
    } = props;

    const canvasRef = useRef<HTMLDivElement>(null);
    const { showMessage } = useSnackbar();

    const handleDragOver = (e: React.DragEvent) => {
        e.preventDefault();
        onDragOverChange(true);
    };

    const handleDragLeave = () => {
        onDragOverChange(false);
    };

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        onDragOverChange(false);
        onIsDraggingChange(false);

        try {
            const data = e.dataTransfer.getData('application/json');
            const parsedData = JSON.parse(data);

            if (parsedData.type === 'move') {
                return;
            }

            const template: ComponentTemplate = parsedData;

            // 为有选项的组件生成选项标识
            let optionsWithKeys: FormOption[] | undefined;
            if (template.defaultProps.extendedProps?.optionsWithKeys && template.defaultProps.extendedProps.optionsWithKeys.length > 0) {
                optionsWithKeys = template.defaultProps.extendedProps.optionsWithKeys.map((option: FormOption) => ({
                    id: generateId(),
                    label: option.label,
                    key: generateUniqueOptionKey(formStructure.components)
                }));
            }

            const newComponent: IFormField = {
                id: generateId(),
                type: template.type,
                label: template.defaultProps.label || '新字段',
                description: template.defaultProps.description || '',
                fieldKey: generateUniqueFieldKey(formStructure.components),
                placeholder: template.defaultProps.placeholder || '',
                extendedProps: {
                    multiple: template.defaultProps.extendedProps?.multiple || false,
                    optionsWithKeys: optionsWithKeys,
                },
                layout: { span: 6 }
            };

            // 查找最后一个行容器，如果不存在或已满，创建新行
            const lastRow = formStructure.components[formStructure.components.length - 1] as RowContainer;

            if (lastRow && lastRow.type === 'row' && lastRow.components.length < 4) {
                // 检查当前行是否有足够空间
                const currentRowWidth = lastRow.components.reduce((sum: number, comp: IFormField) => sum + (comp.layout.span || 12), 0);
                const componentSpan = newComponent.layout.span || 12;
                if (currentRowWidth + componentSpan <= 12) {
                    // 添加到现有行
                    onFormStructureChange({
                        ...formStructure,
                        components: formStructure.components.map(comp => {
                            if (comp.id === lastRow.id) {
                                return {
                                    ...comp,
                                    components: [...(comp as RowContainer).components, newComponent]
                                };
                            }
                            return comp;
                        })
                    });
                    return;
                }
            }

            // 创建新行并添加组件
            const newRow: RowContainer = {
                id: generateId(),
                type: 'row',
                layout: { span: 6 },
                components: [newComponent]
            };

            onFormStructureChange({
                ...formStructure,
                components: [...formStructure.components, newRow]
            });
        } catch (error) {
            console.log('拖拽数据解析失败，可能是组件移动操作');
        }
    };

    const handleComponentClick = (component: IFormField | RowContainer) => {
        onSelectedComponentChange(component);
    };

    const handleComponentDelete = (componentId: string) => {
        onFormStructureChange({
            ...formStructure,
            components: formStructure.components.filter(comp => comp.id !== componentId)
        });
        if (selectedComponent?.id === componentId) {
            onSelectedComponentChange(null);
        }
    };

    const addNewRow = () => {
        const newRow: RowContainer = {
            id: generateId(),
            type: 'row',
            layout: { span: 12 },
            components: []
        };

        onFormStructureChange({
            ...formStructure,
            components: [...formStructure.components, newRow]
        });
    };

    const removeComponentFromRow = (rowId: string, componentId: string) => {
        onFormStructureChange({
            ...formStructure,
            components: formStructure.components.map((comp: RowContainer | IFormField) => {
                if (comp.id === rowId && comp.type === 'row') {
                    return {
                        ...comp,
                        components: (comp as RowContainer).components.filter((c: IFormField) => c.id !== componentId)
                    };
                }
                return comp;
            }).filter((comp: RowContainer | IFormField) => {
                // 如果行中没有组件了，删除整行
                if (comp.type === 'row' && (comp as RowContainer).components.length === 0) {
                    return false;
                }
                return true;
            })
        });
    };

    const handleComponentDragStart = (e: React.DragEvent, component: IFormField | RowContainer) => {
        e.stopPropagation();
        e.dataTransfer.setData('application/json', JSON.stringify({
            type: 'move',
            componentId: component.id,
            componentType: component.type,
            sourceRowId: component.type === 'row' ? component.id : null
        }));
        e.dataTransfer.effectAllowed = 'move';
        onIsMovingChange(true);
        onMovingComponentChange(component.id);
    };

    const handleComponentDragOver = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        e.dataTransfer.dropEffect = 'move';
    };

    const handleComponentDragEnd = (e: React.DragEvent) => {
        e.stopPropagation();
        onIsMovingChange(false);
        onMovingComponentChange(null);
    };

    // 行内组件拖拽处理
    const handleFieldComponentDrop = (e: React.DragEvent, targetComponentId: string, targetRowId: string) => {
        e.preventDefault();
        e.stopPropagation();
        const data = JSON.parse(e.dataTransfer.getData('application/json'));

        if (data.type === 'move' && data.componentId !== targetComponentId) {
            // 找到源组件和目标组件的位置
            let sourceComponent: IFormField | null = null;
            let sourceRowId: string | null = null;
            let sourceIndex: number = -1;
            let targetIndex: number = -1;

            // 查找源组件
            formStructure.components.forEach((row: RowContainer | IFormField) => {
                if (row.type === 'row') {
                    const index = (row as RowContainer).components.findIndex((comp: IFormField) => comp.id === data.componentId);
                    if (index !== -1) {
                        sourceComponent = (row as RowContainer).components[index];
                        sourceRowId = row.id;
                        sourceIndex = index;
                    }
                }
            });

            // 查找目标组件
            const targetRow = formStructure.components.find((row: RowContainer | IFormField) => row.id === targetRowId);
            if (targetRow && targetRow.type === 'row') {
                targetIndex = (targetRow as RowContainer).components.findIndex((comp: IFormField) => comp.id === targetComponentId);
            }

            if (sourceComponent && sourceRowId && sourceIndex !== -1 && targetIndex !== -1) {
                // 检查目标行的span总和是否超过12
                const targetRowData = formStructure.components.find((row: RowContainer | IFormField) => row.id === targetRowId);
                if (targetRowData && targetRowData.type === 'row') {
                    const currentSpanSum = (targetRowData as RowContainer).components.reduce((sum: number, comp: IFormField) => {
                        // 如果是同一个组件，不计算其span
                        if (comp.id === (sourceComponent as IFormField).id) {
                            return sum;
                        }
                        return sum + (comp.layout.span || 12);
                    }, 0);

                    const newSpanSum = currentSpanSum + ((sourceComponent as IFormField).layout.span || 12);
                    if (newSpanSum > 12) {
                        console.log('行内组件span总和不能超过12');
                        showMessage('行内组件宽度不得超过1', 'error');
                        onIsMovingChange(false);
                        onMovingComponentChange(null);
                        return;
                    }
                }

                const newComponents = [...formStructure.components];

                // 从源行移除组件
                const sourceRowIndex = newComponents.findIndex(row => row.id === sourceRowId);
                if (sourceRowIndex !== -1) {
                    const sourceRow = newComponents[sourceRowIndex];
                    if (sourceRow.type === 'row') {
                        const newSourceRow = { ...sourceRow, components: [...(sourceRow as RowContainer).components] };
                        newSourceRow.components.splice(sourceIndex, 1);
                        newComponents[sourceRowIndex] = newSourceRow;
                    }
                    newComponents[sourceRowIndex] = sourceRow;
                }

                // 添加到目标行
                const targetRowIndex = newComponents.findIndex(row => row.id === targetRowId);
                if (targetRowIndex !== -1) {
                    const targetRow = newComponents[targetRowIndex];
                    if (targetRow.type === 'row') {
                        const newTargetRow = { ...targetRow, components: [...(targetRow as RowContainer).components] };
                        newTargetRow.components.splice(targetIndex, 0, sourceComponent!);
                        newComponents[targetRowIndex] = newTargetRow;
                    }
                }

                onFormStructureChange({ ...formStructure, components: newComponents });
            }
        }

        onIsMovingChange(false);
        onMovingComponentChange(null);
    };

    // 行容器onDrop
    const handleDropToRow = (e: React.DragEvent, rowId: string) => {
        e.preventDefault();
        onDragOverChange(false);
        onIsDraggingChange(false);
        try {
            const data = e.dataTransfer.getData('application/json');
            const parsedData = JSON.parse(data);

            // 如果是组件移动操作
            if (parsedData.type === 'move') {
                // 找到源组件
                let sourceComponent: IFormField | null = null;
                let sourceRowId: string | null = null;
                let sourceIndex: number = -1;

                formStructure.components.forEach((row: RowContainer | IFormField) => {
                    if (row.type === 'row') {
                        const index = (row as RowContainer).components.findIndex((comp: IFormField) => comp.id === parsedData.componentId);
                        if (index !== -1) {
                            sourceComponent = (row as RowContainer).components[index];
                            sourceRowId = row.id;
                            sourceIndex = index;
                        }
                    }
                });

                // 如果找到源组件且不是同一个行
                if (sourceComponent && sourceRowId && sourceRowId !== rowId) {
                    // 检查目标行的span总和是否超过12
                    const targetRowData = formStructure.components.find((row: RowContainer | IFormField) => row.id === rowId);
                    if (targetRowData && targetRowData.type === 'row') {
                        const currentSpanSum = (targetRowData as RowContainer).components.reduce((sum: number, comp: IFormField) => {
                            return sum + (comp.layout.span || 12);
                        }, 0);

                        const newSpanSum = currentSpanSum + ((sourceComponent as IFormField).layout?.span || 12);
                        console.log('newSpanSum', newSpanSum);
                        if (newSpanSum > 12) {
                            console.log('行内组件span总和不能超过12');
                            onIsMovingChange(false);
                            onMovingComponentChange(null);
                            return;
                        }
                    }

                    const newComponents = [...formStructure.components];

                    // 从源行移除组件
                    const sourceRowIndex = newComponents.findIndex(row => row.id === sourceRowId);
                    if (sourceRowIndex !== -1) {
                        const sourceRow = { ...newComponents[sourceRowIndex] };
                        (sourceRow as RowContainer).components = [...(sourceRow as RowContainer).components];
                        (sourceRow as RowContainer).components.splice(sourceIndex, 1);
                        newComponents[sourceRowIndex] = sourceRow;
                    }

                    // 添加到目标行
                    const targetRowIndex = newComponents.findIndex(row => row.id === rowId);
                    if (targetRowIndex !== -1) {
                        const targetRow = newComponents[targetRowIndex];
                        if (targetRow.type === 'row') {
                            const newTargetRow = { ...targetRow, components: [...(targetRow as RowContainer).components] };
                            newTargetRow.components.push(sourceComponent!);
                            newComponents[targetRowIndex] = newTargetRow;
                        }
                    }

                    onFormStructureChange({ ...formStructure, components: newComponents });
                }
                return;
            }

            // 原有的从组件库拖拽逻辑
            const template: ComponentTemplate = parsedData;

            // 为有选项的组件生成选项标识
            let optionsWithKeys: FormOption[] | undefined;
            if (template.defaultProps.extendedProps?.optionsWithKeys && template.defaultProps.extendedProps.optionsWithKeys.length > 0) {
                optionsWithKeys = template.defaultProps.extendedProps.optionsWithKeys.map((option: FormOption) => ({
                    id: generateId(),
                    label: option.label,
                    key: generateUniqueOptionKey(formStructure.components)
                }));
            }

            const newComponent: IFormField = {
                id: generateId(),
                type: template.type,
                label: template.defaultProps.label || '新字段',
                description: template.defaultProps.description || '',
                fieldKey: generateUniqueFieldKey(formStructure.components),
                placeholder: template.defaultProps.placeholder || '',
                extendedProps: {
                    multiple: template.defaultProps.extendedProps?.multiple || false,
                    optionsWithKeys: optionsWithKeys,
                },
                layout: { span: 6 }
            };
            onFormStructureChange({
                ...formStructure,
                components: formStructure.components.map(comp => {
                    if (comp.id === rowId && comp.type === 'row') {
                        // 检查行内宽度
                        const currentRowWidth = (comp as RowContainer).components.reduce((sum: number, c: IFormField) => sum + (c.layout.span || 12), 0);
                        const componentSpan = newComponent.layout.span || 12;
                        if (currentRowWidth + componentSpan <= 12) {
                            return {
                                ...comp,
                                components: [...(comp as RowContainer).components, newComponent]
                            };
                        } else {
                            showMessage('行内组件宽度不得超过1', 'error');
                        }
                    }
                    return comp;
                })
            });
        } catch (error) {
            console.log('拖拽数据解析失败，可能是组件移动操作');
        }
    };

    return (
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
                                    {(component as RowContainer).components.map((fieldComponent: IFormField) => (
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
                                                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                                        <Typography
                                                            variant="body2"
                                                            sx={{
                                                                minWidth: '80px',
                                                                fontWeight: 'normal',
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

                                {(component as RowContainer).components.length === 0 && (
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
                    <Typography variant="body2">添加行后,从左侧组件库将组件拖拽到行容器中</Typography>
                </Box>
            )}
        </Paper>
    );
}

export default FormDesign;