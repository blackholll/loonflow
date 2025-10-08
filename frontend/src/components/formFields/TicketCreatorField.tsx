import { Typography, Tooltip } from '@mui/material';


interface TicketCreatorFieldProps {
    value: any | null;
}

export default function TicketCreatorField({ value }: TicketCreatorFieldProps) {
    return (<Typography variant="body2" sx={{ whiteSpace: 'pre-line' }}>
        <Tooltip title={value?.email}><span>{value ? `${value.name}(${value.alias})` : ''}</span></Tooltip>
    </Typography>)
}

