import React from 'react';
import { FormControl, TextField as MuiTextField } from '@mui/material';
import ViewField from './ViewField';

interface DateFieldProps {
    value: string;
    fieldRequired: boolean;
    onChange: (value: string) => void;
    mode: 'view' | 'edit';
    props: any;
}

function DateField({
    value = '',
    fieldRequired,
    onChange,
    mode,
    props,
}: DateFieldProps) {

    // 将日期字符串转换为显示格式
    const formatDateForDisplay = (dateValue: string): string => {
        if (!dateValue) return '';

        try {
            // 如果是纯日期格式（YYYY-MM-DD），直接返回
            if (/^\d{4}-\d{2}-\d{2}$/.test(dateValue)) {
                return dateValue;
            }

            // 如果是ISO格式，提取日期部分
            if (dateValue.includes('T') || dateValue.includes('Z') || dateValue.includes('+') || dateValue.includes('-')) {
                const dateMatch = dateValue.match(/^(\d{4}-\d{2}-\d{2})/);
                if (dateMatch) {
                    return dateMatch[1];
                }
            }

            // 其他格式直接返回
            return dateValue;
        } catch (error) {
            return dateValue;
        }
    };

    // 将日期值保存为纯日期格式
    const formatDateForSave = (dateValue: string): string => {
        if (!dateValue) return '';

        try {
            // 直接返回日期格式字符串，不包含时间和时区信息
            // 格式：YYYY-MM-DD
            return dateValue;
        } catch (error) {
            return dateValue;
        }
    };

    // view mode only show value with formatting
    if (mode === 'view') {
        const displayValue = formatDateForDisplay(value);
        return (
            <ViewField type='date' value={displayValue} props={props} />
        );
    }

    // edit mode
    const handleDateChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const newValue = event.target.value;
        if (onChange) {
            // 保存为纯日期格式
            const formattedValue = formatDateForSave(newValue);
            onChange(formattedValue);
        }
    };

    // 获取当前显示值
    const getCurrentDisplayValue = (): string => {
        if (!value) return '';

        try {
            // 如果是纯日期格式（YYYY-MM-DD），直接返回
            if (/^\d{4}-\d{2}-\d{2}$/.test(value)) {
                return value;
            }

            // 如果是ISO格式，提取日期部分
            if (value.includes('T') || value.includes('Z') || value.includes('+') || value.includes('-')) {
                const dateMatch = value.match(/^(\d{4}-\d{2}-\d{2})/);
                if (dateMatch) {
                    return dateMatch[1];
                }
            }

            return value;
        } catch (error) {
            return '';
        }
    };

    return (
        <FormControl fullWidth={true}>
            <MuiTextField
                type="date"
                value={getCurrentDisplayValue()}
                onChange={handleDateChange}
                required={fieldRequired}
                variant={props?.variant ?? 'outlined'}
                size={props?.size ?? 'small'}
                placeholder={props?.placeholder || 'YYYY-MM-DD'}
                InputLabelProps={{
                    shrink: true,
                }}
            />
        </FormControl>
    );
}

export default DateField;
