import { Typography } from '@mui/material';

interface WorkflowInfoFieldProps {
    value: any;
}

export default function WorkflowInfoField({ value }: WorkflowInfoFieldProps) {
    return (<Typography variant="body2" sx={{ whiteSpace: 'pre-line' }}>
        {value?.name ? value.name : ''}
    </Typography>)
}