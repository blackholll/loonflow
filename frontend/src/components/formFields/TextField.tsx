import React from 'react';
import { TextField as MuiTextField, FormControl, FormHelperText, InputLabel } from '@mui/material';
import ViewField from './ViewField';

interface TextFieldProps {
    value: string;
    fieldRequired: boolean;
    onChange: (value: string) => void;
    mode: 'view' | 'edit';
    props: any;
}

function TextField({
    value = '',
    fieldRequired,
    onChange,
    mode,
    props,
}: TextFieldProps) {

    const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (onChange) {
            onChange(event.target.value);
        }
    };

    // view mode only show value
    if (mode === 'view') {
        return (
            <ViewField type={props.type} value={value} props={props} />
        );
    }

    // edit mode, support edit
    return (
        <FormControl fullWidth={true}>
            <MuiTextField
                value={value}
                onChange={handleChange}
                required={fieldRequired}
                variant="outlined"
                fullWidth={true}
                multiline={props.multiline}
                size="small"
                rows={props.rows}
                type={props.type ?? 'text'}
                placeholder={props.placeholder}
            />
        </FormControl>
    );

};

export default TextField; 