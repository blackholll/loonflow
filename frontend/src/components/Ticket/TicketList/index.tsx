import React,  { useEffect, useState }  from 'react';
import { Container, TextField, Select, MenuItem, FormControl, InputLabel, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Box, TablePagination } from '@mui/material';
import Card from '@mui/material/Card';
import { CardContent, CardHeader } from '@mui/material';

import Autocomplete from '@mui/material/Autocomplete';
import { useTranslation } from 'react-i18next';
import { ISimpleWorkflowEntity } from '@/types/workflow';
import { getTicketList } from '../../../services/ticket';
import { getSimpleWorkflowList } from '../../../services/workflow';
import useSnackbar from '../../../hooks/useSnackbar';



import Grid from '@mui/material/Grid2';
import { ITicketListResEntity } from '@/types/ticket';


function TicketList({category}:{category:string}) {
  const { t } = useTranslation();
  const [ workflowList, setWorkflowList] = useState<ISimpleWorkflowEntity[]>([]);
  const [ workflowValue, setWorkflowValue ] = useState<ISimpleWorkflowEntity|null>(null);
  const [ ticketList, setTicketList ] = useState<ITicketListResEntity[]>([]);
  const [ticketListLoading, setTicketListLoading ] = useState<Boolean>(false);
  
  const [page, setPage] = useState(1)
  const [perPage, setPerPage] = useState(10)
  const [total, setTotal] = useState(0)
  
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
    const fetchSimpleWorkflow = async()=>{
      try {
        const res = await getSimpleWorkflowList('', 1, 10000);
        if (res.code ===0){
          console.log('res.data.wokflow_info_listres.data.wokflow_info_list:', res)
          setWorkflowList(res.data.workflow_info_list);
        } else {
          showMessage(res.msg, 'error');
        }
      } catch (error:any) {
        showMessage( error.message, 'error');
        console.log(error);
      }
    };
    fetchSimpleWorkflow();
  }, []);
  
  useEffect(() => {
    const fetchTicketList = async()=> {
      try {
        setTicketListLoading(true);
        const res = await getTicketList({category, page, perPage});
        if (res.code === 0) {
          setTicketList(res.data.ticket_list);
        } else {
          showMessage(res.msg, 'error');
        }
        setTicketListLoading(false);
      } catch (error:any) {
        showMessage(error.message, 'error');
        console.log(error);
      }
    };
    fetchTicketList();
  }, [category, page, perPage])
  
  const handleChangePage = (_event:any, newPage:number) => {
    setPage(newPage);
  }
  
  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };
  
  return (
    <Card>
      <CardHeader title={listTitle}/>
        <Grid container spacing={2} justifyContent="center" alignItems="center">
          <Grid size={{xs:12, sm:6, md:3}}>
            <TextField fullWidth label={t('ticketList.searchWithKeyword')} />
          </Grid>
          <Grid size={{xs:12, sm:6, md:3}}>
            <TextField fullWidth label={t('ticketList.searchWithCreator')}/>
          </Grid>
          <Grid size={{xs:12, sm:6, md:3}}>
            <TextField fullWidth label={t('ticketList.searchWithTimeRange')} type="date" />
          </Grid>
          <Grid size={{xs:12, sm:6, md:3}}>
            <Autocomplete
                value={workflowValue}
                onChange={ (event, newValue) => setWorkflowValue(newValue)}
                getOptionLabel={(option) => option.name}
                disablePortal
                options={workflowList}
                sx={{ margeLeft:0, margeRight:0 }}
                renderInput={(params) => <TextField {...params} label={t('ticketList.ticketType')} />}
              />
          </Grid>
        </Grid>

      <TableContainer component={Paper} sx={{ marginTop: '10px' }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Id</TableCell>
              <TableCell>{t('ticketList.ticketTitle')}</TableCell>
              <TableCell>{t('ticketList.ticketCreator')}</TableCell>
              <TableCell>{t('ticketList.ticketCreateTime')}</TableCell>
              <TableCell>{t('ticketList.ticketStatus')}</TableCell>
              <TableCell>{t('actions')}</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {ticketList?ticketList.map((ticket) => (
              <TableRow key={ticket.id}>
                <TableCell>{ticket.title}</TableCell>
                <TableCell>{ticket.creator.alias}</TableCell>
                <TableCell>{ticket.create_time}</TableCell>
                <TableCell>{ticket.node.name}</TableCell>
                <TableCell>{'actions'}</TableCell>
              </TableRow>
            )):null}
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
      </Card>
  );
}

export default TicketList;