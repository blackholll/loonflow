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

    // get display format configuration, default is 'YYYY-MM-DD HH:mm:ss'



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
                // save as ISO string with timezone information
                const formattedValue = newValue.toISOString();
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
            // try to parse directly to dayjs object
            const parsed = dayjs(value);
            return parsed.isValid() ? parsed : null;
        } catch (error) {
            return null;
        }
    };


    return (
        <FormControl fullWidth={true}>
            <DateTimePicker
                value={getCurrentDisplayValue()}
                onChange={handleDateTimeChange}
                format={props?.format}
                slotProps={{
                    textField: {
                        variant: props?.variant ?? 'outlined',
                        size: props?.size ?? 'small',
                        placeholder: props?.placeholder || t('common.dateTimePicker.dateTimeFormatHourMinSec'),
                        fullWidth: true,
                        error: false,
                        helperText: '',
                    }
                }}
            />
        </FormControl>
    );
}

export default DateTimeField;
