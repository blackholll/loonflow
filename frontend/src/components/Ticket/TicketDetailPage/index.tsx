import { useState } from 'react';
import { useParams } from 'react-router-dom';
import TicketDetail from '../TicketDetail';

function TicketDetailPage() {
    const { ticketId } = useParams();
    const [refreshToken, setRefreshToken] = useState(0);
    console.log('ticketId', ticketId)


    return <TicketDetail ticketId={ticketId} refreshToken={refreshToken} onTicketHandledChange={() => { setRefreshToken(refreshToken + 1) }} />
}

export default TicketDetailPage;