import { Box, Typography } from '@mui/material';
import { useEffect, useMemo } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import useSnackbar from '../../../hooks/useSnackbar';
import TicketDetail from '../TicketDetail';

function NewTicketPage() {
  const [searchParams] = useSearchParams();
  const workflowId = useMemo(() => searchParams.get('workflow_id') || '', [searchParams]);
  const workflowVersionName = useMemo(() => searchParams.get('version_name') || undefined, [searchParams]);
  const { showMessage } = useSnackbar();
  const navigate = useNavigate();

  useEffect(() => {
    if (!workflowId) {
      showMessage('缺少 workflow_id 参数，无法创建工单', 'error');
    }
  }, [workflowId, showMessage]);

  const handleTicketCreated = (ticketId: string) => {
    showMessage('工单创建成功', 'success');
    navigate(`/ticket/${ticketId}`);
  };

  if (!workflowId) {
    return (
      <Box sx={{ p: 3 }}>
        <Typography color="error">缺少 workflow_id 参数，无法创建工单。</Typography>
      </Box>
    );
  }

  return (
    <TicketDetail
      workflowId={workflowId}
      workflowVersionName={workflowVersionName}
      onTicketHandledChange={handleTicketCreated}
    />
  );
}

export default NewTicketPage;
