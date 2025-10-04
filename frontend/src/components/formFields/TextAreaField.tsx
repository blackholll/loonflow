import React from 'react';
import { TextField as MuiTextField, FormControl } from '@mui/material';
import ViewField from './ViewField';

interface TextAreaFieldProps {
    value: string;
    fieldRequired: boolean;
    onChange: (value: string) => void;
    mode: 'view' | 'edit';
    props: any;
}

function TextAreaField({
    value = '',
    fieldRequired,
    onChange,
    mode,
    props,
}: TextAreaFieldProps) {

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
                multiline={true}
                rows={3}
                onChange={handleChange}
                required={fieldRequired}
                variant="outlined"
                fullWidth={true}
                size="small"
                type={props.type ?? 'text'}
                placeholder={props.placeholder}
            />
        </FormControl>
    );

};

export default TextAreaField; 