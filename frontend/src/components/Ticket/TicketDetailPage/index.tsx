import { useParams, useNavigate } from 'react-router-dom';
import TicketDetail from '../TicketDetail';

function TicketDetailPage() {
    const { ticketId } = useParams();
    console.log('ticketId', ticketId)

    return <TicketDetail ticketId={ticketId} />
}

export default TicketDetailPage;