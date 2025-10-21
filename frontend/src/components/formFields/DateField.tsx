import { FormControl } from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import dayjs from 'dayjs';
import { useTranslation } from 'react-i18next';
import ViewField from './ViewField';

interface DateFieldProps {
    value: string;
    onChange: (value: string) => void;
    mode: 'view' | 'edit';
    props: any;
}

function DateField({
    value = '',
    onChange,
    mode,
    props,
}: DateFieldProps) {
    const { t } = useTranslation();

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

    // view mode only show value with formatting
    if (mode === 'view') {
        const displayValue = formatDateForDisplay(value);
        return (
            <ViewField type='date' value={displayValue} props={props} />
        );
    }

    // edit mode
    const handleDateChange = (newValue: dayjs.Dayjs | null) => {
        if (onChange) {
            if (newValue) {
                // 保存为纯日期格式 YYYY-MM-DD
                const formattedValue = newValue.format('YYYY-MM-DD');
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
            // 如果是纯日期格式（YYYY-MM-DD），直接解析
            if (/^\d{4}-\d{2}-\d{2}$/.test(value)) {
                return dayjs(value);
            }

            // 如果是ISO格式，提取日期部分
            if (value.includes('T') || value.includes('Z') || value.includes('+') || value.includes('-')) {
                const dateMatch = value.match(/^(\d{4}-\d{2}-\d{2})/);
                if (dateMatch) {
                    return dayjs(dateMatch[1]);
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
            <DatePicker
                value={getCurrentDisplayValue()}
                onChange={handleDateChange}
                slotProps={{
                    textField: {
                        variant: props?.variant ?? 'outlined',
                        size: props?.size ?? 'small',
                        placeholder: props?.placeholder || t('common.dateTimePicker.placeholder'),
                        fullWidth: true,
                    }
                }}
            />
        </FormControl>
    );
}

export default DateField;
