import { Typography } from '@mui/material';
import { useTranslation } from 'react-i18next';

interface TicketActStateFieldProps {
    value: string;
}

export default function TicketActStateField({ value }: TicketActStateFieldProps) {
    const { t } = useTranslation();

    return (<Typography variant="body2" sx={{ whiteSpace: 'pre-line' }}>
        {t(`ticket.state.${value}`)}
    </Typography>)
}