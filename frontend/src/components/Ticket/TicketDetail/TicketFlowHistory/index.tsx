import React, { useEffect, useState } from 'react';
import { Box, Paper, Typography, List, ListItem, Divider } from '@mui/material';
import { getTicketFlowHistory } from '../../../../services/ticket';
import { ITicketFlowHistoryItem } from '../../../../types/ticket';

interface TicketHistoryProps {
    ticketId: string;
    refreshToken?: number;
}

function TicketFlowHistory({ ticketId, refreshToken }: TicketHistoryProps) {
    const [items, setItems] = useState<ITicketFlowHistoryItem[]>([]);

    useEffect(() => {
        if (!ticketId) return;
        (async () => {
            const res = await getTicketFlowHistory(ticketId);
            if (res.code === 0) {
                const rawList = (res.data as any)?.ticketFlowHistoryList || [];
                setItems(rawList);
            }
        })();
    }, [ticketId, refreshToken]);

    return (
        <Paper sx={{ mt: 2, p: 2, border: '1px solid', borderColor: 'divider' }}>
            <Typography variant="h6" sx={{ mb: 1 }}>操作记录</Typography>
            <List>
                {items.map((it, idx) => (
                    <React.Fragment key={it.id}>
                        <ListItem alignItems="flex-start" disableGutters>
                            <Box sx={{ width: '100%' }}>
                                <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                                    <Typography variant="body2"><strong>处理人</strong>：{it.processorInfo?.processorAlias || it.processorInfo?.processor || '-'}</Typography>
                                    <Typography variant="body2"><strong>操作类型</strong>：{it.actionName || it.actionType || '-'}</Typography>
                                </Box>
                                {it.comment && (
                                    <Typography variant="body2" sx={{ mt: 0.5 }}><strong>留言</strong>：{it.comment}</Typography>
                                )}
                                <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 0.5 }}><strong>操作时间</strong>：{new Date(it.createdAt).toLocaleString()}</Typography>
                            </Box>
                        </ListItem>
                        {idx < items.length - 1 && <Divider component="li" />}
                    </React.Fragment>
                ))}
                {items.length === 0 && (
                    <Typography variant="body2" color="text.secondary" sx={{ px: 2, py: 1 }}>暂无记录</Typography>
                )}
            </List>
        </Paper>
    );
}

export default TicketFlowHistory;


