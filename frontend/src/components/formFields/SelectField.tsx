import React from 'react';
import { Autocomplete, FormControl, TextField as MuiTextField } from '@mui/material';
import ViewField from './ViewField';
import { FormOption } from '../../types/workflowDesign';

interface SelectFieldProps {
    value: string | string[] | FormOption | FormOption[];
    fieldRequired: boolean;
    onChange: (value: string | string[] | FormOption | FormOption[]) => void;
    mode: 'view' | 'edit';
    props: any;
}

function SelectField({
    value = '',
    fieldRequired,
    onChange,
    mode,
    props,
}: SelectFieldProps) {

    // 获取选项列表
    const options: FormOption[] = props?.optionsWithKeys || [];

    // 判断是否为多选
    const isMultiple = props?.multiple || false;

    // 处理值的变化
    const handleChange = (event: any, newValue: FormOption | FormOption[] | null) => {
        if (onChange) {
            if (isMultiple) {
                // 多选模式：返回字符串数组
                const stringArray = Array.isArray(newValue)
                    ? newValue.map(option => option.key || option.label)
                    : [];
                onChange(stringArray);
            } else {
                // 单选模式：返回字符串
                const stringValue = newValue ? (newValue as FormOption).key || (newValue as FormOption).label : '';
                onChange(stringValue);
            }
        }
    };

    // 将字符串值转换为选项对象
    const getValueFromString = (val: any): FormOption | FormOption[] | null => {
        if (!val) return isMultiple ? [] : null;

        // 确保 val 是字符串类型
        let stringVal: string;
        if (typeof val === 'string') {
            stringVal = val;
        } else if (Array.isArray(val)) {
            // 如果是数组，转换为逗号分隔的字符串
            stringVal = val.join(',');
        } else if (typeof val === 'object' && val !== null) {
            // 如果是对象（FormOption），提取 key 或 label
            if ('key' in val) {
                stringVal = val.key;
            } else if ('label' in val) {
                stringVal = val.label;
            } else {
                stringVal = String(val);
            }
        } else {
            stringVal = String(val);
        }

        if (isMultiple) {
            const stringArray = stringVal.split(',');
            return stringArray.map(str => {
                const trimmedStr = str.trim();
                const option = options.find(opt => opt.key === trimmedStr || opt.label === trimmedStr);
                return option || { id: trimmedStr, key: trimmedStr, label: trimmedStr };
            });
        } else {
            const trimmedStr = stringVal.trim();
            const option = options.find(opt => opt.key === trimmedStr || opt.label === trimmedStr);
            return option || { id: trimmedStr, key: trimmedStr, label: trimmedStr };
        }
    };

    // 获取显示值（用于 view 模式）
    const getDisplayValue = (val: any): string => {
        if (!val) return '';

        // 确保 val 是字符串类型
        let stringVal: string;
        if (typeof val === 'string') {
            stringVal = val;
        } else if (Array.isArray(val)) {
            // 如果是数组，转换为逗号分隔的字符串
            stringVal = val.join(',');
        } else if (typeof val === 'object' && val !== null) {
            // 如果是对象（FormOption），提取 key 或 label
            if ('key' in val) {
                stringVal = val.key;
            } else if ('label' in val) {
                stringVal = val.label;
            } else {
                stringVal = String(val);
            }
        } else {
            stringVal = String(val);
        }

        if (isMultiple) {
            const stringArray = stringVal.split(',');
            return stringArray.map(str => {
                const trimmedStr = str.trim();
                const option = options.find(opt => opt.key === trimmedStr || opt.label === trimmedStr);
                return option ? option.label : trimmedStr;
            }).join(', ');
        } else {
            const trimmedStr = stringVal.trim();
            const option = options.find(opt => opt.key === trimmedStr || opt.label === trimmedStr);
            return option ? option.label : trimmedStr;
        }
    };

    // view mode only show value
    if (mode === 'view') {
        const displayValue = getDisplayValue(value);
        return (
            <ViewField type='select' value={displayValue} props={props} />
        );
    }

    // edit mode, support edit
    const currentValue = getValueFromString(value);

    return (
        <FormControl fullWidth={true}>
            <Autocomplete
                multiple={isMultiple}
                value={currentValue}
                onChange={handleChange}
                getOptionLabel={(option) => option.label}
                isOptionEqualToValue={(option, value) => option.key === value.key}
                disablePortal
                options={options}
                sx={{ marginLeft: 0, marginRight: 0 }}
                renderInput={(params) => (
                    <MuiTextField
                        {...params}
                        label={props?.placeholder || '请选择'}
                        required={fieldRequired}
                        variant="outlined"
                        size="small"
                    />
                )}
            />
        </FormControl>
    );
};

export default SelectField; 