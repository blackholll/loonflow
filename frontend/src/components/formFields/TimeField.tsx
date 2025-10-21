import { FormControl } from '@mui/material';
import { TimePicker } from '@mui/x-date-pickers/TimePicker';
import dayjs from 'dayjs';
import { useTranslation } from 'react-i18next';
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
    const { t } = useTranslation();

    // 获取显示格式配置，默认为 'HH:mm'
    const format = props?.format || 'HH:mm'; // 'HH:mm' 或 'HH:mm:ss'
    const includeSeconds = format === 'HH:mm:ss';


    // view mode only show value with formatting
    if (mode === 'view') {
        const displayValue = value ? dayjs(value).format(includeSeconds ? 'HH:mm:ss' : 'HH:mm') : '';
        return (
            <ViewField type='time' value={displayValue} props={props} />
        );
    }

    // edit mode
    const handleTimeChange = (newValue: dayjs.Dayjs | null) => {
        if (onChange) {
            if (newValue) {
                // 保存为纯时间格式 HH:mm 或 HH:mm:ss
                const formattedValue = includeSeconds ? newValue.format('HH:mm:ss') : newValue.format('HH:mm');
                onChange(formattedValue);
            } else {
                onChange('');
            }
        }
    };

    // 获取当前显示值（转换为 dayjs 对象）
    const getCurrentDisplayValue = (): dayjs.Dayjs | null => {
        if (!value) return null;

        try {
            // 如果是纯时间格式（HH:mm 或 HH:mm:ss），创建 dayjs 对象
            if (/^\d{2}:\d{2}(:\d{2})?$/.test(value)) {
                return dayjs(value, includeSeconds ? 'HH:mm:ss' : 'HH:mm');
            }

            // 如果是ISO格式，提取时间部分
            if (value.includes('T') || value.includes('Z') || value.includes('+') || value.includes('-')) {
                const timeMatch = value.match(/T(\d{2}):(\d{2})(:(\d{2}))?/);
                if (timeMatch) {
                    const hours = timeMatch[1];
                    const minutes = timeMatch[2];
                    const seconds = timeMatch[4] || '00';

                    const timeString = includeSeconds ? `${hours}:${minutes}:${seconds}` : `${hours}:${minutes}`;
                    return dayjs(timeString, includeSeconds ? 'HH:mm:ss' : 'HH:mm');
                }
            }

            // 尝试直接解析
            const parsed = dayjs(value);
            return parsed.isValid() ? parsed : null;
        } catch (error) {
            return null;
        }
    };

    return (
        <FormControl fullWidth={true}>
            <TimePicker
                value={getCurrentDisplayValue()}
                onChange={handleTimeChange}
                slotProps={{
                    textField: {
                        variant: props?.variant ?? 'outlined',
                        size: props?.size ?? 'small',
                        placeholder: props?.placeholder || (includeSeconds ? t('common.dateTimePicker.timeFormat') + ':ss' : t('common.dateTimePicker.timeFormat')),
                        fullWidth: true,
                    }
                }}
            />
        </FormControl>
    );
}

export default TimeField;
