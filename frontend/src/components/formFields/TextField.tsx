import { FormControl, TextField as MuiTextField } from '@mui/material';
import React from 'react';
import ViewField from './ViewField';

interface TextFieldProps {
    value: string;
    onChange: (value: string) => void;
    mode: 'view' | 'edit';
    props: any;
}

function TextField({
    value = '',
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
            <ViewField type='text' value={value} props={props} />
        );
    }

    // edit mode, support edit
    return (
        <FormControl fullWidth={true}>
            <MuiTextField
                value={value}
                onChange={handleChange}
                variant="outlined"
                fullWidth={true}
                size="small"
                type={props.type ?? 'text'}
                placeholder={props.placeholder}
            />
        </FormControl>
    );

};

export default TextField; 