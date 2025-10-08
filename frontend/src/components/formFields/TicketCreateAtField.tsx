import { Typography } from '@mui/material';
import { formatDate } from '../../utils/dateFormat';



interface TicketCreatorFieldProps {
    value: string | null;
}

export default function TicketCreatedAtField({ value }: TicketCreatorFieldProps) {
    return (<Typography variant="body2" sx={{ whiteSpace: 'pre-line' }}>
        {value ? formatDate(value) : ''}
    </Typography>)
}

