import { FormControl, FormControlLabel, Radio, RadioGroup } from '@mui/material';
import React from 'react';
import { FormOption } from '../../types/workflowDesign';
import ViewField from './ViewField';

interface RadioFieldProps {
    value: string | FormOption;
    onChange: (value: string | FormOption) => void;
    mode: 'view' | 'edit';
    props: any;
}

function RadioField({
    value = '',
    onChange,
    mode,
    props,
}: RadioFieldProps) {

    // 获取选项列表
    const options: FormOption[] = props?.optionsWithKeys || [];

    // 处理值的变化
    const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (onChange) {
            const selectedValue = event.target.value;
            onChange(selectedValue);
        }
    };

    // 获取当前选中的值
    const getCurrentValue = (val: any): string => {
        if (!val) return '';

        // 确保 val 是字符串类型
        let stringVal: string;
        if (typeof val === 'string') {
            stringVal = val;
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

        return stringVal.trim();
    };

    // 获取显示值（用于 view 模式）
    const getDisplayValue = (val: any): string => {
        if (!val) return '';

        const stringVal = getCurrentValue(val);
        const option = options.find(opt => opt.key === stringVal || opt.label === stringVal);
        return option ? option.label : stringVal;
    };

    // view mode only show value
    if (mode === 'view') {
        const displayValue = getDisplayValue(value);
        return (
            <ViewField type='radio' value={displayValue} props={props} />
        );
    }

    // edit mode, support edit
    const currentValue = getCurrentValue(value);

    return (
        <FormControl
            fullWidth={true}
        >
            <RadioGroup
                value={currentValue}
                row
                onChange={handleChange}
                sx={{
                    '& .MuiFormControlLabel-root': {
                        marginBottom: 0.5,
                    }
                }}
            >
                {options.map((option) => (
                    <FormControlLabel
                        key={option.id || option.key}
                        value={option.key}
                        control={<Radio size="small" />}
                        label={option.label}
                    />
                ))}
            </RadioGroup>
        </FormControl>
    );
}

export default RadioField;
