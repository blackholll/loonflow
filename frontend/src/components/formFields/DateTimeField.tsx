import React from 'react';
import { FormControl, TextField as MuiTextField } from '@mui/material';
import ViewField from './ViewField';

interface DateTimeFieldProps {
    value: string;
    fieldRequired: boolean;
    onChange: (value: string) => void;
    mode: 'view' | 'edit';
    props: any;
}

function DateTimeField({
    value = '',
    fieldRequired,
    onChange,
    mode,
    props,
}: DateTimeFieldProps) {

    // 获取显示格式配置，默认为 'YYYY-MM-DD HH:mm:ss'
    const format = props?.format || 'YYYY-MM-DD HH:mm:ss'; // 'YYYY-MM-DD HH:mm', 'YYYY-MM-DD HH:mm:ss'
    const includeSeconds = format.includes('HH:mm:ss');

    // 获取用户时区
    const getUserTimezone = () => {
        return Intl.DateTimeFormat().resolvedOptions().timeZone;
    };

    // 将日期时间字符串转换为本地日期时间显示
    const formatDateTimeForDisplay = (dateTimeValue: string): string => {
        if (!dateTimeValue) return '';

        try {
            const date = new Date(dateTimeValue);
            if (isNaN(date.getTime())) return dateTimeValue;

            // 根据配置格式化日期时间
            const options: Intl.DateTimeFormatOptions = {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit',
                hour12: false,
                timeZone: getUserTimezone()
            };

            if (includeSeconds) {
                options.second = '2-digit';
            }

            return date.toLocaleString(undefined, options);
        } catch (error) {
            return dateTimeValue;
        }
    };

    // 将本地日期时间转换为带时区信息的ISO字符串
    const formatDateTimeForSave = (dateTimeValue: string): string => {
        if (!dateTimeValue) return '';

        try {
            const date = new Date(dateTimeValue);
            if (isNaN(date.getTime())) return dateTimeValue;

            // 返回带时区信息的ISO字符串
            return date.toISOString();
        } catch (error) {
            return dateTimeValue;
        }
    };

    // view mode only show value with formatting
    if (mode === 'view') {
        const displayValue = formatDateTimeForDisplay(value);
        return (
            <ViewField type='datetime' value={displayValue} props={props} />
        );
    }

    // edit mode
    const handleDateTimeChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const newValue = event.target.value;
        if (onChange) {
            // 保存时带上时区信息
            const formattedValue = formatDateTimeForSave(newValue);
            onChange(formattedValue);
        }
    };

    // 获取当前显示值（从ISO字符串中提取日期时间部分）
    const getCurrentDisplayValue = (): string => {
        if (!value) return '';

        try {
            const date = new Date(value);
            if (isNaN(date.getTime())) return '';

            const year = date.getFullYear();
            const month = (date.getMonth() + 1).toString().padStart(2, '0');
            const day = date.getDate().toString().padStart(2, '0');
            const hours = date.getHours().toString().padStart(2, '0');
            const minutes = date.getMinutes().toString().padStart(2, '0');
            const seconds = date.getSeconds().toString().padStart(2, '0');

            if (includeSeconds) {
                return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}`;
            } else {
                return `${year}-${month}-${day}T${hours}:${minutes}`;
            }
        } catch (error) {
            return '';
        }
    };

    // 获取占位符
    const getPlaceholder = (): string => {
        return includeSeconds ? 'YYYY-MM-DD HH:mm:ss' : 'YYYY-MM-DD HH:mm';
    };

    return (
        <FormControl fullWidth={true}>
            <MuiTextField
                type="datetime-local"
                value={getCurrentDisplayValue()}
                onChange={handleDateTimeChange}
                required={fieldRequired}
                variant={props?.variant ?? 'outlined'}
                size={props?.size ?? 'small'}
                placeholder={props?.placeholder || getPlaceholder()}
                inputProps={{
                    step: includeSeconds ? 1 : 60, // 秒级精度或分钟级精度
                }}
                InputLabelProps={{
                    shrink: true,
                }}
            />
        </FormControl>
    );
}

export default DateTimeField;
