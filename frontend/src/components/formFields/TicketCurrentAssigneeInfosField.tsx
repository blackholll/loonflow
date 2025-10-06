import { Typography } from '@mui/material';

interface TicketCurrentAssigneeInfosFieldProps {
    value: any;
}

export default function TicketCurrentAssigneeInfosField({ value }: TicketCurrentAssigneeInfosFieldProps) {
    return (<Typography variant="body2" sx={{ whiteSpace: 'pre-line' }}>
        {value ? value.map((item: any) => item.assignee).join(',') : ''}
    </Typography>)
}