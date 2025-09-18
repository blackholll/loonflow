import React, { useEffect, useState } from 'react';
import { Button, TextField, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TablePagination, CardContent } from '@mui/material';
import Card from '@mui/material/Card';
import { CardHeader } from '@mui/material';
import { Link } from 'react-router-dom';
import Autocomplete from '@mui/material/Autocomplete';
import { useTranslation } from 'react-i18next';
import { ISimpleWorkflowEntity } from '@/types/workflow';
import { getTicketList } from '../../../services/ticket';
import { getSimpleWorkflowList } from '../../../services/workflow';
import useSnackbar from '../../../hooks/useSnackbar';



import Grid from '@mui/material/Grid2';
import { ITicketListResEntity } from '@/types/ticket';


function TicketList({ category, refreshToken }: { category: string; refreshToken?: number | string | boolean }) {
  const { t } = useTranslation();
  const [workflowList, setWorkflowList] = useState<ISimpleWorkflowEntity[]>([]);
  const [workflowValue, setWorkflowValue] = useState<ISimpleWorkflowEntity | null>(null);
  const [ticketList, setTicketList] = useState<ITicketListResEntity[]>([]);

  const [page, setPage] = useState(1)
  const [perPage, setPerPage] = useState(10)
  const [total] = useState(0)

  const { showMessage } = useSnackbar();
  let listTitle = t('ticketList.allTickets');
  if (category === 'owner') {
    listTitle = t('ticketList.owerTickets');
  } else if (category === 'view') {
    listTitle = t('ticketList.viewTickets');
  } else if (category === 'duty') {
    listTitle = t('ticketList.dutyTickets');
  } else if (category === 'relation') {
    listTitle = t('ticketList.relationTickets');
  } else if (category === 'intervene') {
    listTitle = t('ticketList.interveneTickets')
  }

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
  }, [showMessage]);

  useEffect(() => {
    const fetchTicketList = async () => {
      try {
        const res = await getTicketList({ category, page, perPage });
        if (res.code === 0) {
          setTicketList(res.data.ticketList);
        } else {
          showMessage(res.msg, 'error');
        }
      } catch (error: any) {
        showMessage(error.message, 'error');
        console.log(error);
      }
    };
    fetchTicketList();
  }, [category, page, perPage, refreshToken, showMessage])

  const handleChangePage = (_event: any, newPage: number) => {
    setPage(newPage);
  }

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  return (
    <React.Fragment>
      <Card>
        <CardHeader title={listTitle} />
        <CardContent>
          <Grid container spacing={1} justifyContent="left" alignItems="center">
            <Grid size={{ xs: 12, sm: 6, md: 2 }}>
              <TextField fullWidth label={t('ticketList.keyword')} />
            </Grid>
            <Grid size={{ xs: 12, sm: 6, md: 2 }}>
              <TextField fullWidth label={t('ticketList.creator')} />
            </Grid>
            <Grid size={{ xs: 12, sm: 6, md: 2 }}>
              <TextField fullWidth label={t('ticketList.createDateStart')} type="date" slotProps={{ inputLabel: { shrink: true } }} />
            </Grid>
            <Grid size={{ xs: 12, sm: 6, md: 2 }}>
              <TextField fullWidth label={t('ticketList.createDateEnd')} type="date" slotProps={{ inputLabel: { shrink: true } }} />
            </Grid>
            <Grid size={{ xs: 12, sm: 6, md: 2 }}>
              <Autocomplete
                value={workflowValue}
                onChange={(event, newValue) => setWorkflowValue(newValue)}
                getOptionLabel={(option) => option.name}
                disablePortal
                options={workflowList}
                sx={{ marginLeft: 0, marginRight: 0 }}
                renderInput={(params) => <TextField {...params} label={t('ticketList.ticketType')} />}
              />
            </Grid>
            <Grid size={{ xs: 12, sm: 6, md: 2 }}>
              <Button variant="outlined" size={'large'} sx={{ height: '55px', width: '150px' }}>{t('common.search')}</Button>
            </Grid>

          </Grid>

          <TableContainer sx={{ marginTop: '10px', boxShadow: 'none' }}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Id</TableCell>
                  <TableCell>{t('ticketList.ticketTitle')}</TableCell>
                  <TableCell>审批状态</TableCell>
                  <TableCell>{t('ticketList.ticketCreator')}</TableCell>
                  <TableCell>{t('ticketList.ticketCreateTime')}</TableCell>
                  <TableCell>{t('actions')}</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {ticketList ? ticketList.map((ticket) => (
                  <TableRow key={ticket.id}>
                    <TableCell>{ticket.id}</TableCell>
                    <TableCell>{ticket.title}</TableCell>
                    <TableCell>{ticket.actState}</TableCell>
                    <TableCell>{ticket.creatorInfo.alias}</TableCell>
                    <TableCell>{new Date(ticket.createdAt).toLocaleString()}</TableCell>
                    <TableCell>
                      <div>
                        <Link to={`/ticket/${ticket.id}`}>
                          <Button variant="text" size={'large'} sx={{ width: '150px' }}>详情</Button>
                        </Link>
                      </div>
                    </TableCell>
                  </TableRow>
                )) : null}
              </TableBody>
            </Table>
          </TableContainer>
          <TablePagination
            rowsPerPageOptions={[10, 25, 100]}
            component="div"
            count={total}
            rowsPerPage={perPage}
            page={page}
            onPageChange={handleChangePage}
            onRowsPerPageChange={handleChangeRowsPerPage}
          />
        </CardContent>

      </Card>
    </React.Fragment >
  );
}

export default TicketList;