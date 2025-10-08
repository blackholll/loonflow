import React from 'react';
import { FormControl, TextField as MuiTextField } from '@mui/material';
import ViewField from './ViewField';
import { NumericFormat, NumericFormatProps } from 'react-number-format';

interface NumberFieldProps {
    value: number | string;
    fieldRequired: boolean;
    onChange: (value: number | string) => void;
    mode: 'view' | 'edit';
    props: any;
}

function NumberField({
    value = '',
    fieldRequired,
    onChange,
    mode,
    props,
}: NumberFieldProps) {

    // view mode only show value with formatting
    if (mode === 'view') {
        const allowDecimal: boolean = props?.allowDecimal !== false;
        const decimalScale: number | undefined = allowDecimal ? (props?.precision ?? undefined) : 0;
        const fixedDecimalScale: boolean = props?.fixedPrecision === true;
        const thousandSeparator: boolean = props?.thousandSeparator ?? true;
        const suffix: string | undefined = props?.unitSuffix;
        const prefix: string | undefined = props?.unitPrefix;

        const formatNumberForView = (raw: number | string | undefined | null): string => {
            if (raw === undefined || raw === null || raw === '') return '';
            const num = typeof raw === 'number' ? raw : Number(raw);
            if (Number.isNaN(num)) return String(raw);
            const minimumFractionDigits = fixedDecimalScale ? (decimalScale ?? 0) : undefined;
            const maximumFractionDigits = typeof decimalScale === 'number' ? decimalScale : (allowDecimal ? undefined : 0);
            const formatter = new Intl.NumberFormat(undefined, {
                useGrouping: thousandSeparator,
                minimumFractionDigits,
                maximumFractionDigits,
            });
            const core = formatter.format(num);
            return `${prefix ?? ''}${core}${suffix ?? ''}`;
        };

        const displayValue = formatNumberForView(value as any);
        return (
            <ViewField type='number' value={displayValue} props={props} />
        );
    }

    const allowDecimal: boolean = props?.allowDecimal !== false; // 默认允许小数
    const decimalScale: number | undefined = allowDecimal ? (props?.precision ?? undefined) : 0;
    const fixedDecimalScale: boolean = props?.fixedPrecision === true;

    const suffix: string | undefined = props?.unitSuffix; // 例如 'kg', '%'
    const prefix: string | undefined = props?.unitPrefix; // 例如 '¥', '$'

    const thousandSeparator: boolean = props?.thousandSeparator ?? true;

    const min = props?.min;
    const max = props?.max;

    const handleValueChange: NumericFormatProps['onValueChange'] = (values) => {
        const { floatValue, value: strVal } = values;
        if (strVal === '') {
            onChange('');
            return;
        }
        // 边界限制
        let next = floatValue as number | undefined;
        if (typeof next === 'number') {
            if (typeof min === 'number' && next < min) next = min;
            if (typeof max === 'number' && next > max) next = max;
            onChange(next);
        } else {
            onChange(strVal);
        }
    };

    return (
        <FormControl fullWidth={true}>
            <NumericFormat
                value={value === undefined || value === null ? '' : value}
                onValueChange={handleValueChange}
                thousandSeparator={thousandSeparator}
                allowNegative={props?.allowNegative ?? true}
                decimalScale={decimalScale}
                fixedDecimalScale={fixedDecimalScale}
                allowLeadingZeros={false}
                suffix={suffix}
                prefix={prefix}
                placeholder={props?.placeholder}
                inputMode={allowDecimal ? 'decimal' : 'numeric'}
                customInput={MuiTextField}
                // 传递给 TextField，确保样式与 TextField 一致
                fullWidth={true}
                required={fieldRequired}
                variant={props?.variant ?? 'outlined'}
                size={props?.size ?? 'small'}
            />
        </FormControl>
    );

};

export default NumberField;
