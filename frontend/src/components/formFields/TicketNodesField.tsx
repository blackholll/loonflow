import { useEffect, useState } from 'react';
import { Typography } from '@mui/material';

interface TicketNodesFieldProps {
    value: any | null;
}

export default function TicketNodesField({ value }: TicketNodesFieldProps) {
    return (<Typography variant="body2" sx={{ whiteSpace: 'pre-line' }}>
        {value ? value.map((item: any) => item.name).join(',') : ''}
    </Typography>)
}