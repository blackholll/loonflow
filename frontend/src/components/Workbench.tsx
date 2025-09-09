import React, { useEffect, useState } from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import DialogTitle from '@mui/material/DialogTitle';
import Dialog from '@mui/material/Dialog';
import DialogContent from '@mui/material/DialogContent';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid2';
import { ISimpleWorkflowEntity } from '@/types/workflow';
import { getSimpleWorkflowList } from '../services/workflow';
import TicketList from './Ticket/TicketList';
import useSnackbar from '../hooks/useSnackbar';
import TicketDetail from './Ticket/TicketDetail';
import { Link } from '@mui/material';


function Workbench() {
  const [workflowList, setWorkflowList] = useState<ISimpleWorkflowEntity[]>([]);
  const [workflowValue, setWorkflowValue] = useState<ISimpleWorkflowEntity | null>(null);
  const [openTicketDetail, setOpenTicketDetail] = useState(false);
  const [openedTicketId, setOpenedTicketId] = useState<string | null>(null);
  const [newTicketWorkflowId, setNewTicketWorkflowId] = useState<string | null>(null);

  const { showMessage } = useSnackbar();

  useEffect(() => {
    const fetchSimpleWorkflow = async () => {
      try {
        const res = await getSimpleWorkflowList('', 1, 10000);
        if (res.code === 0) {
          console.log('res.data.wokflow_info_listres.data.wokflow_info_list:', res)
          setWorkflowList(res.data.workflowInfoList);
        } else {
          showMessage(res.msg, 'error');
        }
      } catch (error: any) {
        showMessage(error.message, 'error');
        console.log(error);
      }

    };
    fetchSimpleWorkflow();

  }, [])

  const handleClose = () => {
    setOpenTicketDetail(false);
    setOpenedTicketId(null);
    setNewTicketWorkflowId(null);
  }

  const handleTicketHandledChange = (ticketId: string) => {
    if (openedTicketId) {
      // handle ticket
      showMessage('工单已处理', 'success')
    } else {
      // new ticket
      const messageWithLink = (
        <>
          工单已创建
          <Link
            component="button"
            variant="body2"
            onClick={() => {
              setOpenedTicketId(ticketId);
              setNewTicketWorkflowId(null);
              setOpenTicketDetail(true);
            }}
            sx={{
              ml: 1,
              color: 'inherit',
              textDecoration: 'underline',
              cursor: 'pointer',
              '&:hover': {
                textDecoration: 'underline'
              }
            }}
          >
            查看工单详情
          </Link>
        </>
      );
      showMessage(messageWithLink, 'success');
    }
    setOpenTicketDetail(false);
    setOpenedTicketId('');
    setNewTicketWorkflowId(null);
    // todo: trigger ticket list refresh
  }

  return (
    <React.Fragment>
      <Card>
        <CardContent>
          <Grid container spacing={1} justifyContent="left" alignItems="center">
            {/* 搜索部分 */}
            <Grid size={{ xs: 12, sm: 6, md: 3 }}>
              <Autocomplete
                value={workflowValue}
                onChange={(event, newValue) => setWorkflowValue(newValue)}
                getOptionLabel={(option) => option.name}
                disablePortal
                options={workflowList}
                sx={{ margeLeft: 0, margeRight: 0 }}
                renderInput={(params) => <TextField {...params} label="Select Ticke Type" />}
              />
            </Grid>
            <Grid size={{ xs: 12, sm: 6, md: 3 }} justifyContent="left" >
              <Button variant="outlined" sx={{ margeLeft: 0, margeRight: 0, height: '55px' }} onClick={() => { setNewTicketWorkflowId(workflowValue?.workflowId ?? ''); setOpenTicketDetail(true) }}>New Ticket</Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      <TicketList category="duty" />
      <Dialog
        maxWidth="lg"
        fullWidth
        open={openTicketDetail}
        onClose={handleClose}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">
          {newTicketWorkflowId ? 'New Ticket' : 'Ticket Detail'}
        </DialogTitle>
        <DialogContent>
          <TicketDetail workflowId={newTicketWorkflowId ?? ''} ticketId={openedTicketId ?? ''} onTicketHandledChange={handleTicketHandledChange} />
        </DialogContent>
      </Dialog>


    </React.Fragment>
  )
}

export default Workbench;
