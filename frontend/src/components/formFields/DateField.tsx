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

    // convert date string to display format
    const formatDateForDisplay = (dateValue: string): string => {
        console.log('formatDateForDisplay', dateValue);
        console.log('mode', mode);
        if (!dateValue) return '';

        try {
            // if it is a pure date format(YYYY-MM-DD), return directly
            if (/^\d{4}-\d{2}-\d{2}$/.test(dateValue)) {
                return dateValue;
            }

            // if it is a ISO format, extract the date part
            if (dateValue.includes('T') || dateValue.includes('Z') || dateValue.includes('+') || dateValue.includes('-')) {
                const dateMatch = dateValue.match(/^(\d{4}-\d{2}-\d{2})/);
                if (dateMatch) {
                    return dateMatch[1];
                }
            }

            // other formats return directly
            return dateValue;
        } catch (error) {
            return dateValue;
        }
    };

    // view mode only show value with formatting
    if (mode === 'view') {
        const displayValue = formatDateForDisplay(value);
        console.log('displayValue1111', displayValue);
        return (
            <ViewField type='text' value={displayValue} props={props} />
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

    // get current display value(convert to dayjs object)
    const getCurrentDisplayValue = (): dayjs.Dayjs | null => {
        if (!value) return null;

        try {
            // if it is a pure date format(YYYY-MM-DD), parse directly
            if (/^\d{4}-\d{2}-\d{2}$/.test(value)) {
                return dayjs(value);
            }

            // if it is a ISO format, extract the date part
            if (value.includes('T') || value.includes('Z') || value.includes('+') || value.includes('-')) {
                const dateMatch = value.match(/^(\d{4}-\d{2}-\d{2})/);
                if (dateMatch) {
                    return dayjs(dateMatch[1]);
                }
            }

            // try to parse directly
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
                format={props?.format || 'YYYY-MM-DD'}
                slotProps={{
                    textField: {
                        variant: props?.variant ?? 'outlined',
                        size: props?.size ?? 'small',
                        placeholder: props?.placeholder || t('common.dateTimePicker.dateFormat'),
                        fullWidth: true,
                        error: false,
                        helperText: '',
                    }
                }}
            />
        </FormControl>
    );
}

export default DateField;
