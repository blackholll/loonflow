import AddIcon from '@mui/icons-material/Add';
import DeleteIcon from '@mui/icons-material/Delete';
import {
    Alert,
    Box,
    Button,
    FormControl,
    IconButton,
    InputLabel,
    MenuItem,
    Paper,
    Select,
    TextField,
    Typography
} from '@mui/material';
import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { getSimpleUsers } from '../../../services/user';
import { ISimpleUser } from '../../../types/user';
import { IFormSchema } from '../../../types/workflow';

export interface ConditionGroup {
    id: string;
    conditions: Condition[];
}

export interface Condition {
    id: string;
    fieldType: 'text' | 'number' | 'select' | 'creator';
    fieldName: string;
    operator: string;
    value: string;
}

interface ConditionExpressionEditorProps {
    value: ConditionGroup[] | string;
    onChange: (value: ConditionGroup[]) => void;
    formSchema: IFormSchema;
}

const ConditionExpressionEditor: React.FC<ConditionExpressionEditorProps> = ({
    value,
    onChange,
    formSchema
}) => {
    const { t } = useTranslation();
    const [conditionGroups, setConditionGroups] = useState<ConditionGroup[]>([]);
    const [userOptions, setUserOptions] = useState<{ label: string; value: string }[]>([]);
    const [loadingUsers, setLoadingUsers] = useState(false);

    // 解析现有值（优先当作结构化的条件组数组）
    useEffect(() => {
        if (!value) {
            setConditionGroups([]);
            return;
        }
        try {
            if (Array.isArray(value)) {
                setConditionGroups(value as ConditionGroup[]);
            } else {
                setConditionGroups([]);
            }
        } catch (error) {
            console.error('解析条件失败:', error);
            setConditionGroups([]);
        }
    }, [value]);



    // 返回结构化条件组（不做Python语法转换）
    const emitConditionGroups = (groups: ConditionGroup[]) => {
        onChange(groups);
    };

    // 添加条件组
    const addConditionGroup = () => {
        const newGroup: ConditionGroup = {
            id: `group-${Date.now()}`,
            conditions: [{
                id: `condition-${Date.now()}`,
                fieldType: 'text',
                fieldName: '',
                operator: '==',
                value: ''
            }]
        };

        const newGroups = [...conditionGroups, newGroup];
        setConditionGroups(newGroups);
        emitConditionGroups(newGroups);
    };

    // 删除条件组
    const removeConditionGroup = (groupId: string) => {
        const newGroups = conditionGroups.filter(group => group.id !== groupId);
        setConditionGroups(newGroups);
        emitConditionGroups(newGroups);
    };

    // 添加条件
    const addCondition = (groupId: string) => {
        const newGroups = conditionGroups.map(group => {
            if (group.id === groupId) {
                return {
                    ...group,
                    conditions: [...group.conditions, {
                        id: `condition-${Date.now()}`,
                        fieldType: 'text',
                        fieldName: '',
                        operator: '==',
                        value: ''
                    }]
                };
            }
            return group;
        });

        setConditionGroups(newGroups as ConditionGroup[]);
        emitConditionGroups(newGroups as ConditionGroup[]);
    };

    // 删除条件
    const removeCondition = (groupId: string, conditionId: string) => {
        const newGroups = conditionGroups.map(group => {
            if (group.id === groupId) {
                const newConditions = group.conditions.filter(condition => condition.id !== conditionId);
                return { ...group, conditions: newConditions };
            }
            return group;
        }).filter(group => group.conditions.length > 0);

        setConditionGroups(newGroups);
        emitConditionGroups(newGroups);
    };

    // 更新条件
    const updateCondition = (groupId: string, conditionId: string, field: keyof Condition, value: string) => {
        const newGroups = conditionGroups.map(group => {
            if (group.id === groupId) {
                return {
                    ...group,
                    conditions: group.conditions.map(condition => {
                        if (condition.id === conditionId) {
                            const updatedCondition = { ...condition, [field]: value };
                            // 如果更新的是字段名，需要重置操作符
                            if (field === 'fieldName') {
                                console.log('-----------------value', value);
                                const fieldType = getFieldType(value);
                                const operatorOptions = getOperatorOptions(fieldType);
                                updatedCondition.operator = operatorOptions[0]?.value || '==';
                                // 同步更新条件内的字段类型，避免始终为 'text'
                                updatedCondition.fieldType = fieldType;
                                console.log('-----------------fieldType', fieldType);
                                console.log('-----------------operatorOptions', operatorOptions);
                                console.log('-----------------updatedCondition', updatedCondition);
                            }
                            return updatedCondition;
                        }
                        return condition;
                    })
                };
            }
            return group;
        });

        setConditionGroups(newGroups);
        emitConditionGroups(newGroups);
    };

    // 获取字段类型
    const getFieldType = (fieldName: string): 'text' | 'number' | 'select' => {
        if (fieldName === 'creator') return 'text';

        // 在row的children中查找字段
        let field = null;
        if (formSchema.componentInfoList) {
            for (const row of formSchema.componentInfoList) {
                if (row.type === 'row' && row.children) {
                    field = row.children.find((f: any) => f.componentKey === fieldName);
                    if (field) break;
                } else if (row.componentKey === fieldName) {
                    field = row;
                    break;
                }
            }
        }
        console.log('-----------------field', field);
        if (!field) return 'text';

        switch (field.type) {
            case 'number':
                return 'number';
            case 'select':
            case 'radio':
            case 'checkbox':
            case 'user':
            case 'department':
            default:
                return 'text';
        }
    };

    // 获取操作符选项
    const getOperatorOptions = (fieldType: 'text' | 'number' | 'select') => {
        switch (fieldType) {
            case 'text':
                return [
                    { value: '==', label: t('workflow.propertyPanelLabel.equals') },
                    { value: '!=', label: t('workflow.propertyPanelLabel.notEquals') },
                    { value: 'contains', label: t('workflow.propertyPanelLabel.contains') },
                    { value: 'not_contains', label: t('workflow.propertyPanelLabel.notContains') }
                ];
            case 'number':
                return [
                    { value: '==', label: t('workflow.propertyPanelLabel.equals') },
                    { value: '!=', label: t('workflow.propertyPanelLabel.notEquals') },
                    { value: '>', label: t('workflow.propertyPanelLabel.greaterThan') },
                    { value: '>=', label: t('workflow.propertyPanelLabel.greaterThanOrEqual') },
                    { value: '<', label: t('workflow.propertyPanelLabel.lessThan') },
                    { value: '<=', label: t('workflow.propertyPanelLabel.lessThanOrEqual') }
                ];
            case 'select':
                return [
                    { value: '==', label: t('workflow.propertyPanelLabel.selected') },
                    { value: '!=', label: t('workflow.propertyPanelLabel.notSelected') }
                ];
            default:
                return [];
        }
    };

    // 获取字段选项
    const getFieldOptions = () => {
        const options: { value: string; label: string }[] = [];

        if (formSchema.componentInfoList) {
            formSchema.componentInfoList.forEach((row: any) => {
                if (row.type === 'row' && row.children) {
                    // only support number for now
                    row.children.forEach((field: any) => {
                        if (['number'].includes(field.type)) {
                            options.push({
                                value: field.componentKey,
                                label: field.componentName || field.componentKey
                            });
                        }
                    });
                }
            });
        }

        return options;
    };

    return (
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <Typography variant="subtitle2" sx={{ mb: 1 }}>
                {t('workflow.propertyPanelLabel.conditionExpression')}
            </Typography>

            {conditionGroups.map((group, groupIndex) => (
                <React.Fragment key={group.id}>
                    {groupIndex > 0 && (
                        <Box sx={{ display: 'flex', justifyContent: 'center', my: 1 }}>
                            <Typography variant="body2" color="primary" sx={{ fontWeight: 'bold' }}>
                                或
                            </Typography>
                        </Box>
                    )}
                    <Paper sx={{ p: 2, border: '1px solid #e0e0e0' }}>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                            <Typography variant="subtitle2">
                                {t('workflow.propertyPanelLabel.conditionGroup')} {groupIndex + 1}
                            </Typography>
                            <IconButton
                                size="small"
                                onClick={() => removeConditionGroup(group.id)}
                                color="error"
                            >
                                <DeleteIcon />
                            </IconButton>
                        </Box>

                        {group.conditions.map((condition, conditionIndex) => {
                            const fieldType = getFieldType(condition.fieldName);
                            const operatorOptions = getOperatorOptions(fieldType);
                            console.log('-----------------fieldType', fieldType);
                            console.log('-----------------operatorOptions', operatorOptions);
                            return (
                                <React.Fragment key={condition.id}>
                                    {conditionIndex > 0 && (
                                        <Box sx={{ display: 'flex', justifyContent: 'center', my: 1 }}>
                                            <Typography variant="body2" color="secondary" sx={{ fontWeight: 'bold' }}>
                                                且
                                            </Typography>
                                        </Box>
                                    )}
                                    <Box sx={{ display: 'flex', gap: 1, mb: 2, alignItems: 'center' }}>
                                        {/* 字段选择 */}
                                        <FormControl size="small" sx={{ minWidth: 120 }}>
                                            <InputLabel>{t('workflow.propertyPanelLabel.field')}</InputLabel>
                                            <Select
                                                value={condition.fieldName}
                                                onChange={(e) => updateCondition(group.id, condition.id, 'fieldName', e.target.value)}
                                                label={t('workflow.propertyPanelLabel.field')}
                                            >
                                                {getFieldOptions().map(option => (
                                                    <MenuItem key={option.value} value={option.value}>
                                                        {option.label}
                                                    </MenuItem>
                                                ))}
                                            </Select>
                                        </FormControl>

                                        {/* 操作符选择 */}
                                        <FormControl size="small" sx={{ minWidth: 100 }}>
                                            <InputLabel>{t('workflow.propertyPanelLabel.operator')}</InputLabel>
                                            <Select
                                                value={condition.operator}
                                                onChange={(e) => updateCondition(group.id, condition.id, 'operator', e.target.value)}
                                                label={t('workflow.propertyPanelLabel.operator')}
                                            >
                                                {operatorOptions.map(option => (
                                                    <MenuItem key={option.value} value={option.value}>
                                                        {option.label}
                                                    </MenuItem>
                                                ))}
                                            </Select>
                                        </FormControl>


                                        <TextField
                                            size="small"
                                            type="number"
                                            value={condition.value}
                                            onChange={(e) => updateCondition(group.id, condition.id, 'value', e.target.value)}
                                            placeholder={t('workflow.propertyPanelLabel.inputValue')}
                                            sx={{ minWidth: 120 }}
                                        />

                                        {/* 删除条件按钮 */}
                                        <IconButton
                                            size="small"
                                            onClick={() => removeCondition(group.id, condition.id)}
                                            color="error"
                                        >
                                            <DeleteIcon />
                                        </IconButton>
                                    </Box>
                                </React.Fragment>
                            );
                        })}

                        <Button
                            size="small"
                            startIcon={<AddIcon />}
                            onClick={() => addCondition(group.id)}
                            variant="outlined"
                        >
                            {t('workflow.propertyPanelLabel.addCondition')}
                        </Button>
                        <Alert severity="info"> only support number for now</Alert>
                    </Paper>
                </React.Fragment>
            ))}

            <Button
                startIcon={<AddIcon />}
                onClick={addConditionGroup}
                variant="outlined"
                fullWidth
            >
                {t('workflow.propertyPanelLabel.addConditionGroup')}

            </Button>

        </Box>
    );
};

export default ConditionExpressionEditor;
