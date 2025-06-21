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
import {
    Visibility as PreviewIcon,
    Edit as EditIcon
} from '@mui/icons-material';
import useSnackbar from '../../../hooks/useSnackbar';
import { FormStructure, FormComponent, RowContainer, ComponentTemplate, FormDesignProps } from '../../../types/workflowDesign';
import componentCategories from './ComponentCategories';
import ComponentProperties from './ComponentProperties';
import FormDesign from './FormDesign';
import FormPreview from './FormPreview';


function WorkflowForm({ fieldInfoList }: FormDesignProps) {
    const [formStructure, setFormStructure] = useState<FormStructure>({
        type: 'form',
        layout: { type: 'vertical', gutter: 16 },
        components: []
    });
    const [selectedComponent, setSelectedComponent] = useState<FormComponent | RowContainer | null>(null);
    const [isDragging, setIsDragging] = useState(false);
    const [dragOver, setDragOver] = useState(false);
    const [isMoving, setIsMoving] = useState(false);
    const [movingComponent, setMovingComponent] = useState<string | null>(null);
    const [activeTab, setActiveTab] = useState(0); // 0: 设计, 1: 预览
    const generateId = () => `component_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

    const handleDragStart = (e: React.DragEvent, template: ComponentTemplate) => {
        setIsDragging(true);
        e.dataTransfer.setData('application/json', JSON.stringify(template));
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
                {activeTab === 0 ? (
                    <FormDesign
                        formStructure={formStructure}
                        selectedComponent={selectedComponent}
                        isDragging={isDragging}
                        dragOver={dragOver}
                        isMoving={isMoving}
                        movingComponent={movingComponent}
                        onFormStructureChange={setFormStructure}
                        onSelectedComponentChange={setSelectedComponent}
                        onIsDraggingChange={setIsDragging}
                        onDragOverChange={setDragOver}
                        onIsMovingChange={setIsMoving}
                        onMovingComponentChange={setMovingComponent}
                        generateId={generateId}
                        renderFieldComponent={renderFieldComponent}
                    />
                ) : (
                    <FormPreview
                        formStructure={formStructure}
                        renderFieldComponent={renderFieldComponent}
                    />
                )}
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



export default WorkflowForm; 