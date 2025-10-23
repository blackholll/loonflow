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

    const format = props?.format || 'HH:mm'; // 'HH:mm' 或 'HH:mm:ss'
    const includeSeconds = format === 'HH:mm:ss';


    // view mode only show value with formatting
    if (mode === 'view') {
        console.log('TimeField value', value);
        return (
            <ViewField type='time' value={value} props={props} />
        );
    }

    // edit mode
    const handleTimeChange = (newValue: dayjs.Dayjs | null) => {
        if (onChange) {
            if (newValue) {
                const formattedValue = newValue.format(format);
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
            // if it is a pure time format(HH:mm or HH:mm:ss), create dayjs object
            if (/^\d{2}:\d{2}(:\d{2})?$/.test(value)) {
                return dayjs(value, includeSeconds ? 'HH:mm:ss' : 'HH:mm');
            }

            // if it is a ISO format, extract the time part
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

            // try to parse directly
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
                format={props?.format}
                slotProps={{
                    textField: {
                        variant: props?.variant ?? 'outlined',
                        size: props?.size ?? 'small',
                        placeholder: props?.placeholder || (includeSeconds ? t('common.dateTimePicker.timeFormatHourMinSec') : t('common.dateTimePicker.timeFormatHourMin')),
                        fullWidth: true,
                        error: false,
                        helperText: '',
                    }
                }}
            />
        </FormControl>
    );
}

export default TimeField;
