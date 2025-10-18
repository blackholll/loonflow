import { FormControl, TextField as MuiTextField } from '@mui/material';
import React from 'react';
import ViewField from './ViewField';

interface TimeFieldProps {
    value: string;
    onChange: (value: string) => void;
    mode: 'view' | 'edit';
    props: any;
}

function TimeField({
    value = '',
    onChange,
    mode,
    props,
}: TimeFieldProps) {

    // 获取显示格式配置，默认为 'HH:mm'
    const format = props?.format || 'HH:mm'; // 'HH:mm' 或 'HH:mm:ss'
    const includeSeconds = format === 'HH:mm:ss';

    // 将时间字符串转换为显示格式
    const formatTimeForDisplay = (timeValue: string): string => {
        if (!timeValue) return '';

        try {
            // 如果是纯时间格式（HH:mm 或 HH:mm:ss），直接返回
            if (/^\d{2}:\d{2}(:\d{2})?$/.test(timeValue)) {
                return timeValue;
            }

            // 如果值包含时区信息，提取时间部分（不进行时区转换）
            if (timeValue.includes('T') || timeValue.includes('Z') || timeValue.includes('+') || timeValue.includes('-')) {
                // 使用正则表达式直接提取时间部分，避免时区转换
                const timeMatch = timeValue.match(/T(\d{2}):(\d{2})(:(\d{2}))?/);
                if (timeMatch) {
                    const hours = timeMatch[1];
                    const minutes = timeMatch[2];
                    const seconds = timeMatch[4] || '00';

                    if (includeSeconds) {
                        return `${hours}:${minutes}:${seconds}`;
                    } else {
                        return `${hours}:${minutes}`;
                    }
                }
            }

            // 其他格式直接返回
            return timeValue;
        } catch (error) {
            return timeValue;
        }
    };

    // 将时间值保存为纯时间格式
    const formatTimeForSave = (timeValue: string): string => {
        if (!timeValue) return '';

        try {
            // 直接返回时间格式字符串，不包含日期和时区信息
            // 格式：HH:mm 或 HH:mm:ss
            return timeValue;
        } catch (error) {
            return timeValue;
        }
    };

    // view mode only show value with formatting
    if (mode === 'view') {
        const displayValue = formatTimeForDisplay(value);
        return (
            <ViewField type='time' value={displayValue} props={props} />
        );
    }

    // edit mode
    const handleTimeChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const newValue = event.target.value;
        if (onChange) {
            // 保存时带上时区信息
            const formattedValue = formatTimeForSave(newValue);
            onChange(formattedValue);
        }
    };

    // 获取当前显示值
    const getCurrentDisplayValue = (): string => {
        if (!value) return '';

        try {
            // 如果是纯时间格式（HH:mm 或 HH:mm:ss），直接返回
            if (/^\d{2}:\d{2}(:\d{2})?$/.test(value)) {
                // 根据配置决定是否显示秒
                if (includeSeconds && value.split(':').length === 2) {
                    return value + ':00';
                } else if (!includeSeconds && value.split(':').length === 3) {
                    return value.substring(0, 5); // 去掉秒部分
                }
                return value;
            }

            // 如果是ISO格式，提取时间部分（不进行时区转换）
            if (value.includes('T') || value.includes('Z') || value.includes('+') || value.includes('-')) {
                // 使用正则表达式直接提取时间部分，避免时区转换
                const timeMatch = value.match(/T(\d{2}):(\d{2})(:(\d{2}))?/);
                if (timeMatch) {
                    const hours = timeMatch[1];
                    const minutes = timeMatch[2];
                    const seconds = timeMatch[4] || '00';

                    if (includeSeconds) {
                        return `${hours}:${minutes}:${seconds}`;
                    } else {
                        return `${hours}:${minutes}`;
                    }
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
                type={includeSeconds ? 'time' : 'time'}
                value={getCurrentDisplayValue()}
                onChange={handleTimeChange}
                variant={props?.variant ?? 'outlined'}
                size={props?.size ?? 'small'}
                placeholder={props?.placeholder || (includeSeconds ? 'HH:mm:ss' : 'HH:mm')}
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

export default TimeField;
