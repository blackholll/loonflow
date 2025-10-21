import { FormControl } from '@mui/material';
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';
import dayjs from 'dayjs';
import { useTranslation } from 'react-i18next';
import ViewField from './ViewField';

interface DateTimeFieldProps {
    value: string;
    onChange: (value: string) => void;
    mode: 'view' | 'edit';
    props: any;
}

function DateTimeField({
    value = '',
    onChange,
    mode,
    props,
}: DateTimeFieldProps) {
    const { t } = useTranslation();

    // 获取显示格式配置，默认为 'YYYY-MM-DD HH:mm:ss'
    const format = props?.format || 'YYYY-MM-DD HH:mm:ss'; // 'YYYY-MM-DD HH:mm', 'YYYY-MM-DD HH:mm:ss'
    const includeSeconds = format.includes('HH:mm:ss');



    // view mode only show value with formatting
    if (mode === 'view') {
        const displayValue = value ? dayjs(value).format('YYYY-MM-DD HH:mm:ss') : '';
        return (
            <ViewField type='datetime' value={displayValue} props={props} />
        );
    }

    // edit mode
    const handleDateTimeChange = (newValue: dayjs.Dayjs | null) => {
        if (onChange) {
            if (newValue) {
                // 保存为带时区信息的ISO字符串
                const formattedValue = newValue.toISOString();
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
            // 尝试直接解析为 dayjs 对象
            const parsed = dayjs(value);
            return parsed.isValid() ? parsed : null;
        } catch (error) {
            return null;
        }
    };

    // 获取占位符
    const getPlaceholder = (): string => {
        return includeSeconds ? t('common.dateTimePicker.dateTimeFormat') : 'YYYY-MM-DD HH:mm';
    };

    return (
        <FormControl fullWidth={true}>
            <DateTimePicker
                value={getCurrentDisplayValue()}
                onChange={handleDateTimeChange}
                slotProps={{
                    textField: {
                        variant: props?.variant ?? 'outlined',
                        size: props?.size ?? 'small',
                        placeholder: props?.placeholder || getPlaceholder(),
                        fullWidth: true,
                    }
                }}
            />
        </FormControl>
    );
}

export default DateTimeField;
