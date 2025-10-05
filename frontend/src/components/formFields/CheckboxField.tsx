import React from 'react';
import { FormControl, FormLabel, FormGroup, FormControlLabel, Checkbox, FormHelperText } from '@mui/material';
import ViewField from './ViewField';
import { FormOption } from '../../types/workflowDesign';

interface CheckboxFieldProps {
    value: string | string[] | FormOption | FormOption[];
    fieldRequired: boolean;
    onChange: (value: string | string[] | FormOption | FormOption[]) => void;
    mode: 'view' | 'edit';
    props: any;
}

function CheckboxField({
    value = [],
    fieldRequired,
    onChange,
    mode,
    props,
}: CheckboxFieldProps) {

    // 获取选项列表
    const options: FormOption[] = props?.optionsWithKeys || [];

    // 处理值的变化
    const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (onChange) {
            const selectedValue = event.target.value;
            const checked = event.target.checked;

            // 获取当前选中的值数组
            const currentValues = getCurrentValues(value);

            let newValues: string[];
            if (checked) {
                // 添加选中的值
                newValues = [...currentValues, selectedValue];
            } else {
                // 移除取消选中的值
                newValues = currentValues.filter(val => val !== selectedValue);
            }

            onChange(newValues);
        }
    };

    // 获取当前选中的值数组
    const getCurrentValues = (val: any): string[] => {
        if (!val) return [];

        // 确保 val 是数组类型
        let stringArray: string[];
        if (Array.isArray(val)) {
            stringArray = val.map(item => {
                if (typeof item === 'string') {
                    return item;
                } else if (typeof item === 'object' && item !== null) {
                    return item.key || item.label || String(item);
                } else {
                    return String(item);
                }
            });
        } else if (typeof val === 'string') {
            // 如果是逗号分隔的字符串，转换为数组
            stringArray = val.split(',').map(str => str.trim()).filter(str => str);
        } else if (typeof val === 'object' && val !== null) {
            // 如果是单个对象，转换为数组
            const singleValue = val.key || val.label || String(val);
            stringArray = [singleValue];
        } else {
            stringArray = [];
        }

        return stringArray;
    };

    // 获取显示值（用于 view 模式）
    const getDisplayValue = (val: any): string => {
        if (!val) return '';

        const stringArray = getCurrentValues(val);
        return stringArray.map(str => {
            const option = options.find(opt => opt.key === str || opt.label === str);
            return option ? option.label : str;
        }).join(', ');
    };

    // 检查某个选项是否被选中
    const isChecked = (optionKey: string): boolean => {
        const currentValues = getCurrentValues(value);
        return currentValues.includes(optionKey);
    };

    // view mode only show value
    if (mode === 'view') {
        const displayValue = getDisplayValue(value);
        return (
            <ViewField type='checkbox' value={displayValue} props={props} />
        );
    }

    // edit mode, support edit
    const currentValues = getCurrentValues(value);
    const hasSelection = currentValues.length > 0;

    return (
        <FormControl
            fullWidth={true}
            error={fieldRequired && !hasSelection}
        >
            <FormLabel component="legend" sx={{ fontSize: '0.875rem', color: 'text.secondary', mb: 1 }}>
            </FormLabel>
            <FormGroup
                row
                sx={{
                    '& .MuiFormControlLabel-root': {
                        marginBottom: 0.5,
                    }
                }}
            >
                {options.map((option) => (
                    <FormControlLabel
                        key={option.id || option.key}
                        control={
                            <Checkbox
                                size="small"
                                checked={isChecked(option.key)}
                                onChange={handleChange}
                                value={option.key}
                            />
                        }
                        label={option.label}
                    />
                ))}
            </FormGroup>
            {fieldRequired && !hasSelection && (
                <FormHelperText error>
                    此字段为必填项
                </FormHelperText>
            )}
        </FormControl>
    );
}

export default CheckboxField;
