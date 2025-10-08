import { Typography } from '@mui/material';

interface TicketActStateFieldProps {
    value: string;
}

const stateMap: Record<string, string> = {
    'in-draft': '草稿中',
    'on-going': '进行中',
    'rejected': '被拒绝',
    'withdrawn': '被撤回',
    'finished': '已完成',
    'closed': '已关闭',
}
export default function TicketActStateField({ value }: TicketActStateFieldProps) {
    return (<Typography variant="body2" sx={{ whiteSpace: 'pre-line' }}>
        {stateMap[value] ? stateMap[value] : ''}
    </Typography>)
}