import {
    Edit as EditIcon,
    Visibility as PreviewIcon
} from '@mui/icons-material';
import {
    Box,
    Card,
    Divider,
    Paper,
    Tab,
    Tabs,
    Typography
} from '@mui/material';
import React, { useCallback, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { v4 as uuidv4 } from 'uuid';
import { IFormSchema, IWorkflowComponent, IWorkflowComponentRow } from '../../../types/workflow';
import { ComponentTemplate } from '../../../types/workflowDesign';
import getComponentCategories from './ComponentCategories';
import ComponentProperties from './ComponentProperties';
import FormDesign from './FormDesign';
import FormPreview from './FormPreview';
import RenderFormComponent from './RenderFormComponent';


interface WorkflowFormProps {
    onFormSchemaChange: (newFormSchema: IFormSchema) => void;
    formSchema: { componentInfoList: (IWorkflowComponent | IWorkflowComponentRow)[]; }
}


function WorkflowForm({ onFormSchemaChange, formSchema }: WorkflowFormProps) {
    const { t } = useTranslation();
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
    const generateUniqueFieldKey = (existingComponents: (IWorkflowComponent | IWorkflowComponentRow)[], type: string) => {
        if (['title', 'creator_info', 'created_at', 'ticket_node_infos', 'act_state', 'workflow_info', 'current_assignee_infos'].includes(type)) {
            return type;
        }
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
        // 创建一个不包含React组件的纯数据对象
        const templateData = {
            type: template.type,
            componentName: template.componentName,
            defaultProps: template.defaultProps
        };
        e.dataTransfer.setData('application/json', JSON.stringify(templateData));
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


    return (
        <Box sx={{ display: 'flex', height: 'calc(100vh - 100px)', gap: 2, p: 2 }}>
            {/* 左侧组件库 */}
            <Paper sx={{ width: 250, p: 2, overflow: 'auto' }}>
                <Typography variant="h6" gutterBottom>
                    {t('workflow.componentLibrary')}
                </Typography>
                <Divider sx={{ mb: 2 }} />

                {Object.entries(getComponentCategories(t)).map(([categoryKey, category]) => (
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
                            label={t('workflow.design')}
                            iconPosition="start"
                        />
                        <Tab
                            icon={<PreviewIcon />}
                            label={t('workflow.preview')}
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
                        renderFieldComponent={(component, handleComponentUpdate) => <RenderFormComponent component={component} handleComponentUpdate={handleComponentUpdate} />}
                    />
                ) : (
                    <FormPreview
                        formSchemaInfo={formSchemaInfo}
                        renderFieldComponent={(component, handleComponentUpdate) => <RenderFormComponent component={component} handleComponentUpdate={handleComponentUpdate || (() => { })} />}
                    />
                )}
            </Box>

            {/* 右侧属性面板 */}
            <Paper sx={{ width: 350, p: 2, overflow: 'auto' }}>
                <Typography variant="h6" gutterBottom>
                    {t('workflow.componentProperties.componentProperties')}
                </Typography>
                <Divider sx={{ mb: 2 }} />

                {selectedComponent ? (
                    <ComponentProperties
                        component={selectedComponent}
                        onUpdate={handleComponentUpdate}
                        formSchema={formSchemaInfo}
                    />
                ) : (
                    <Typography variant="body2" color="text.secondary">
                        {t('workflow.componentProperties.selectComponentToEditProperties')}
                    </Typography>
                )}
            </Paper>
        </Box>
    );
}



export default WorkflowForm; 