import React, { useRef, useState, useEffect } from 'react';
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
import { ComponentTemplate, FormOption } from '../../../../types/workflowDesign';
import { IWorkflowComponent, IWorkflowComponentRow, IFormSchema } from '../../../../types/workflow';
import useSnackbar from '../../../../hooks/useSnackbar';

interface FormDesignProps {
    formSchemaInfo: IFormSchema;
    selectedComponent: IWorkflowComponent | IWorkflowComponentRow | null;
    isDragging: boolean;
    dragOver: boolean;
    isMoving: boolean;
    movingComponent: string | null;
    onFormSchemaChange: (formSchamaeInfo: IFormSchema) => void;
    onSelectedComponentChange: (component: IWorkflowComponent | IWorkflowComponentRow | null) => void;
    onIsDraggingChange: (dragging: boolean) => void;
    onDragOverChange: (dragOver: boolean) => void;
    onIsMovingChange: (moving: boolean) => void;
    onMovingComponentChange: (componentId: string | null) => void;
    generateId: () => string;
    generateUniqueFieldKey: (existingComponents: (IWorkflowComponentRow | IWorkflowComponent)[]) => string;
    generateUniqueOptionKey: (existingComponents: (IWorkflowComponentRow | IWorkflowComponent)[]) => string;
    renderFieldComponent: (component: IWorkflowComponent, handleComponentUpdate: (updatedComponent: IWorkflowComponent) => void) => React.ReactNode;
}

function FormDesign(props: FormDesignProps) {
    const {
        formSchemaInfo,
        selectedComponent,
        dragOver,
        movingComponent,
        onFormSchemaChange,
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
    const [formSchemaDesignInfo, setFormSchemaDesignInfo] = useState<IFormSchema>(formSchemaInfo);

    // 同步 props 到本地状态
    useEffect(() => {
        setFormSchemaDesignInfo(formSchemaInfo);
    }, [formSchemaInfo]);

    // 使用 useRef 来避免重复日志
    const prevFormSchemaRef = useRef<IFormSchema | null>(null);
    useEffect(() => {
        // 只有当 formSchemaDesignInfo 真正改变时才记录日志
        if (prevFormSchemaRef.current !== formSchemaDesignInfo) {
            console.log('formSchemaDesignInfo', formSchemaDesignInfo);
            prevFormSchemaRef.current = formSchemaDesignInfo;
        }
    }, [formSchemaDesignInfo]);

    // 辅助函数：同时更新本地状态和通知父组件
    const updateFormSchema = (newFormSchema: IFormSchema) => {
        setFormSchemaDesignInfo(newFormSchema);
        onFormSchemaChange(newFormSchema);
    };

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
                    key: generateUniqueOptionKey(formSchemaDesignInfo.componentInfoList)
                }));
            }

            const newComponent: IWorkflowComponent = {
                id: generateId(),
                type: template.type as 'text' | 'textarea' | 'number' | 'select' | 'radio' | 'checkbox' | 'time' | 'date' | 'user' | 'department' | 'file',
                componentName: template.componentName || '新字段',
                label: {},
                description: template.defaultProps.description || '',
                componentKey: generateUniqueFieldKey(formSchemaDesignInfo.componentInfoList),
                props: {
                    placeholder: template.defaultProps.placeholder || '',
                    multiple: template.defaultProps.extendedProps?.multiple || false,
                    optionsWithKeys: optionsWithKeys,
                },
                layout: { span: 6 }
            };

            // 查找最后一个行容器，如果不存在或已满，创建新行
            const lastRow = formSchemaDesignInfo.componentInfoList[formSchemaDesignInfo.componentInfoList.length - 1] as IWorkflowComponentRow;

            if (lastRow && lastRow.type === 'row' && lastRow.children.length < 4) {
                // 检查当前行是否有足够空间
                const currentRowWidth = lastRow.children.reduce((sum: number, comp: IWorkflowComponent) => sum + (comp.layout.span || 12), 0);
                const componentSpan = newComponent.layout.span || 12;
                if (currentRowWidth + componentSpan <= 12) {
                    // 添加到现有行
                    updateFormSchema({
                        ...formSchemaDesignInfo,
                        componentInfoList: formSchemaDesignInfo.componentInfoList.map(comp => {
                            if (comp.id === lastRow.id) {
                                return {
                                    ...comp,
                                    children: [...(comp as IWorkflowComponentRow).children, newComponent]
                                };
                            }
                            return comp;
                        })
                    });
                    return;
                }
            }

            // 创建新行并添加组件
            const newRow: IWorkflowComponentRow = {
                id: generateId(),
                type: 'row',
                layout: { span: 6 },
                componentKey: generateUniqueFieldKey(formSchemaDesignInfo.componentInfoList),
                componentName: '新行',
                description: '',
                label: {},
                props: {},
                children: [newComponent]
            };

            updateFormSchema({
                ...formSchemaDesignInfo,
                componentInfoList: [...formSchemaDesignInfo.componentInfoList, newRow]
            });
        } catch (error) {
            console.log('拖拽数据解析失败，可能是组件移动操作');
        }
    };

    const handleComponentClick = (component: IWorkflowComponent | IWorkflowComponentRow) => {
        onSelectedComponentChange(component);
    };

    const handleComponentDelete = (componentId: string) => {
        updateFormSchema({
            ...formSchemaDesignInfo,
            componentInfoList: formSchemaDesignInfo.componentInfoList.filter(comp => comp.id !== componentId)
        });
        if (selectedComponent?.id === componentId) {
            onSelectedComponentChange(null);
        }
    };

    const addNewRow = () => {
        const newRow: IWorkflowComponentRow = {
            id: generateId(),
            type: 'row',
            layout: { span: 12 },
            componentKey: generateUniqueFieldKey(formSchemaDesignInfo.componentInfoList),
            componentName: '新行',
            description: '',
            label: {},
            props: {},
            children: []
        };

        const updatedFormSchema = {
            ...formSchemaDesignInfo,
            componentInfoList: [...formSchemaDesignInfo.componentInfoList, newRow]
        };

        updateFormSchema(updatedFormSchema);
    };

    const removeComponentFromRow = (rowId: string, componentId: string) => {
        updateFormSchema({
            ...formSchemaDesignInfo,
            componentInfoList: formSchemaDesignInfo.componentInfoList.map((comp: IWorkflowComponentRow | IWorkflowComponent) => {
                if (comp.id === rowId && comp.type === 'row') {
                    return {
                        ...comp,
                        children: (comp as IWorkflowComponentRow).children.filter((c: IWorkflowComponent) => c.id !== componentId)
                    };
                }
                return comp;
            }).filter((comp: IWorkflowComponentRow | IWorkflowComponent) => {
                // 如果行中没有组件了，删除整行
                if (comp.type === 'row' && (comp as IWorkflowComponentRow).children.length === 0) {
                    return false;
                }
                return true;
            })
        });
    };

    const handleComponentDragStart = (e: React.DragEvent, component: IWorkflowComponent | IWorkflowComponentRow) => {
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
            let sourceComponent: IWorkflowComponent | null = null;
            let sourceRowId: string | null = null;
            let sourceIndex: number = -1;
            let targetIndex: number = -1;

            // 查找源组件
            formSchemaDesignInfo.componentInfoList.forEach((row: IWorkflowComponentRow | IWorkflowComponent) => {
                if (row.type === 'row') {
                    const index = (row as IWorkflowComponentRow).children.findIndex((comp: IWorkflowComponent) => comp.id === data.componentId);
                    if (index !== -1) {
                        sourceComponent = (row as IWorkflowComponentRow).children[index];
                        sourceRowId = row.id;
                        sourceIndex = index;
                    }
                }
            });

            // 查找目标组件
            const targetRow = formSchemaDesignInfo.componentInfoList.find((row: IWorkflowComponentRow | IWorkflowComponent) => row.id === targetRowId);
            if (targetRow && targetRow.type === 'row') {
                targetIndex = (targetRow as IWorkflowComponentRow).children.findIndex((comp: IWorkflowComponent) => comp.id === targetComponentId);
            }

            if (sourceComponent && sourceRowId && sourceIndex !== -1 && targetIndex !== -1) {
                // 检查目标行的span总和是否超过12
                const targetRowData = formSchemaDesignInfo.componentInfoList.find((row: IWorkflowComponentRow | IWorkflowComponent) => row.id === targetRowId);
                if (targetRowData && targetRowData.type === 'row') {
                    const currentSpanSum = (targetRowData as IWorkflowComponentRow).children.reduce((sum: number, comp: IWorkflowComponent) => {
                        // 如果是同一个组件，不计算其span
                        if (comp.id === (sourceComponent as IWorkflowComponent).id) {
                            return sum;
                        }
                        return sum + (comp.layout.span || 12);
                    }, 0);

                    const newSpanSum = currentSpanSum + ((sourceComponent as IWorkflowComponent).layout.span || 12);
                    if (newSpanSum > 12) {
                        console.log('行内组件span总和不能超过12');
                        showMessage('行内组件宽度不得超过1', 'error');
                        onIsMovingChange(false);
                        onMovingComponentChange(null);
                        return;
                    }
                }

                const newComponents = [...formSchemaDesignInfo.componentInfoList];

                // 从源行移除组件
                const sourceRowIndex = newComponents.findIndex(row => row.id === sourceRowId);
                if (sourceRowIndex !== -1) {
                    const sourceRow = newComponents[sourceRowIndex];
                    if (sourceRow.type === 'row') {
                        const newSourceRow = { ...sourceRow, components: [...(sourceRow as IWorkflowComponentRow).children] };
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
                        const newTargetRow = { ...targetRow, components: [...(targetRow as IWorkflowComponentRow).children] };
                        newTargetRow.components.splice(targetIndex, 0, sourceComponent!);
                        newComponents[targetRowIndex] = newTargetRow;
                    }
                }

                updateFormSchema({ ...formSchemaDesignInfo, componentInfoList: newComponents });
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
                let sourceComponent: IWorkflowComponent | null = null;
                let sourceRowId: string | null = null;
                let sourceIndex: number = -1;

                formSchemaDesignInfo.componentInfoList.forEach((row: IWorkflowComponentRow | IWorkflowComponent) => {
                    if (row.type === 'row') {
                        const index = (row as IWorkflowComponentRow).children.findIndex((comp: IWorkflowComponent) => comp.id === parsedData.componentId);
                        if (index !== -1) {
                            sourceComponent = (row as IWorkflowComponentRow).children[index];
                            sourceRowId = row.id;
                            sourceIndex = index;
                        }
                    }
                });

                // 如果找到源组件且不是同一个行
                if (sourceComponent && sourceRowId && sourceRowId !== rowId) {
                    // 检查目标行的span总和是否超过12
                    const targetRowData = formSchemaDesignInfo.componentInfoList.find((row: IWorkflowComponentRow | IWorkflowComponent) => row.id === rowId);
                    if (targetRowData && targetRowData.type === 'row') {
                        const currentSpanSum = (targetRowData as IWorkflowComponentRow).children.reduce((sum: number, comp: IWorkflowComponent) => {
                            return sum + (comp.layout.span || 12);
                        }, 0);

                        const newSpanSum = currentSpanSum + ((sourceComponent as IWorkflowComponent).layout?.span || 12);
                        console.log('newSpanSum', newSpanSum);
                        if (newSpanSum > 12) {
                            console.log('行内组件span总和不能超过12');
                            onIsMovingChange(false);
                            onMovingComponentChange(null);
                            return;
                        }
                    }

                    const newComponents = [...formSchemaDesignInfo.componentInfoList];

                    // 从源行移除组件
                    const sourceRowIndex = newComponents.findIndex(row => row.id === sourceRowId);
                    if (sourceRowIndex !== -1) {
                        const sourceRow = { ...newComponents[sourceRowIndex] };
                        (sourceRow as IWorkflowComponentRow).children = [...(sourceRow as IWorkflowComponentRow).children];
                        (sourceRow as IWorkflowComponentRow).children.splice(sourceIndex, 1);
                        newComponents[sourceRowIndex] = sourceRow;
                    }

                    // 添加到目标行
                    const targetRowIndex = newComponents.findIndex(row => row.id === rowId);
                    if (targetRowIndex !== -1) {
                        const targetRow = newComponents[targetRowIndex];
                        if (targetRow.type === 'row') {
                            const newTargetRow = { ...targetRow, children: [...(targetRow as IWorkflowComponentRow).children] };
                            newTargetRow.children.push(sourceComponent!);
                            newComponents[targetRowIndex] = newTargetRow;
                        }
                    }

                    updateFormSchema({ ...formSchemaDesignInfo, componentInfoList: newComponents });
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
                    key: generateUniqueOptionKey(formSchemaDesignInfo.componentInfoList)
                }));
            }

            const newComponent: IWorkflowComponent = {
                id: generateId(),
                type: template.type,
                componentName: template.componentName || '新字段',
                description: template.defaultProps.description || '',
                componentKey: generateUniqueFieldKey(formSchemaDesignInfo.componentInfoList),
                label: {},
                props: {
                    placeholder: template.defaultProps.placeholder || '',
                    multiple: template.defaultProps.extendedProps?.multiple || false,
                    optionsWithKeys: optionsWithKeys,
                },
                layout: { span: 6 }
            };
            updateFormSchema({
                ...formSchemaDesignInfo,
                componentInfoList: formSchemaDesignInfo.componentInfoList.map(comp => {
                    if (comp.id === rowId && comp.type === 'row') {
                        // 检查行内宽度
                        const currentRowWidth = (comp as IWorkflowComponentRow).children.reduce((sum: number, c: IWorkflowComponent) => sum + (c.layout.span || 12), 0);
                        const componentSpan = newComponent.layout.span || 12;
                        if (currentRowWidth + componentSpan <= 12) {
                            return {
                                ...comp,
                                children: [...(comp as IWorkflowComponentRow).children, newComponent]
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
                {formSchemaDesignInfo.componentInfoList.map((component) => {
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
                                    {(component as IWorkflowComponentRow).children.map((fieldComponent: IWorkflowComponent) => (
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
                                                        {renderFieldComponent(fieldComponent, (updatedComponent) => {
                                                            // 更新组件逻辑
                                                            updateFormSchema({
                                                                ...formSchemaDesignInfo,
                                                                componentInfoList: formSchemaDesignInfo.componentInfoList.map(comp => {
                                                                    if (comp.id === component.id && comp.type === 'row') {
                                                                        return {
                                                                            ...comp,
                                                                            children: (comp as IWorkflowComponentRow).children.map(child =>
                                                                                child.id === updatedComponent.id ? updatedComponent : child
                                                                            )
                                                                        };
                                                                    }
                                                                    return comp;
                                                                })
                                                            });
                                                        })}
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

                                {(component as IWorkflowComponentRow).children.length === 0 && (
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

            {formSchemaDesignInfo.componentInfoList.length === 0 && (
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