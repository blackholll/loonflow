import { ISimpleWorkflowEntity } from '@/types/workflow';
import { Link } from '@mui/material';
import Autocomplete from '@mui/material/Autocomplete';
import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Dialog from '@mui/material/Dialog';
import DialogContent from '@mui/material/DialogContent';
import Grid from '@mui/material/Grid2';
import TextField from '@mui/material/TextField';
import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import useSnackbar from '../hooks/useSnackbar';
import { getSimpleWorkflowList } from '../services/workflow';
import TicketDetail from './Ticket/TicketDetail';
import TicketList from './Ticket/TicketList';


function Workbench() {
  const [workflowList, setWorkflowList] = useState<ISimpleWorkflowEntity[]>([]);
  const [workflowValue, setWorkflowValue] = useState<ISimpleWorkflowEntity | null>(null);
  const [openTicketDetail, setOpenTicketDetail] = useState(false);
  const [openedTicketId, setOpenedTicketId] = useState<string | null>(null);
  const [newTicketWorkflowId, setNewTicketWorkflowId] = useState<string | null>(null);
  const [ticketListRefreshToken, setTicketListRefreshToken] = useState<number>(0);

  const { showMessage } = useSnackbar();
  const { t } = useTranslation();


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

  }, [showMessage])

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
    // 触发 TicketList 刷新
    setTicketListRefreshToken((prev) => prev + 1);
  }

  return (
    <React.Fragment>
      <Card>
        <CardContent>
          <Grid container spacing={1} justifyContent="left" alignItems="center">
            {/* 搜索部分 */}
            <Grid size={{ xs: 8, sm: 6, md: 4 }}>
              <Autocomplete
                value={workflowValue}
                onChange={(event, newValue) => setWorkflowValue(newValue)}
                getOptionLabel={(option) => option.name}
                disablePortal
                options={workflowList}
                sx={{ marginLeft: 0, marginRight: 0 }}
                renderInput={(params) => <TextField {...params} label={t("common.pleaseSelectTicketType")} />}
              />
            </Grid>
            <Grid size={{ xs: 4, sm: 3, md: 2 }} justifyContent="left" >
              <Button
                variant="outlined"
                sx={{ marginLeft: 0, marginRight: 0, height: '55px' }}
                disabled={!workflowValue}
                onClick={() => {
                  if (!workflowValue) return;
                  setNewTicketWorkflowId(workflowValue?.workflowId ?? '');
                  setOpenTicketDetail(true);
                }}
              >
                New Ticket
              </Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      <TicketList category="duty" refreshToken={ticketListRefreshToken} />
      <Dialog
        maxWidth="lg"
        fullWidth
        open={openTicketDetail}
        onClose={handleClose}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogContent>
          <TicketDetail workflowId={newTicketWorkflowId ?? ''} ticketId={openedTicketId ?? ''} onTicketHandledChange={handleTicketHandledChange} />
        </DialogContent>
      </Dialog>


    </React.Fragment>
  )
}

export default Workbench;
