import { ISimpleWorkflowEntity } from '@/types/workflow';
import { Button, CardContent, CardHeader, CircularProgress, Table, TableBody, TableCell, TableContainer, TableHead, TablePagination, TableRow, TextField } from '@mui/material';
import Autocomplete from '@mui/material/Autocomplete';
import Card from '@mui/material/Card';
import React, { useCallback, useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import i18n from '../../../i18n';
import { getTicketList } from '../../../services/ticket';
import { getSimpleUsers } from '../../../services/user';
import { getSimpleWorkflowList } from '../../../services/workflow';

import useSnackbar from '../../../hooks/useSnackbar';
import { formatDate } from '../../../utils/dateFormat';



import { ITicketListResEntity } from '@/types/ticket';
import { ISimpleUser } from '@/types/user';
import Grid from '@mui/material/Grid2';
import MuiLink from '@mui/material/Link';

interface IOption {
  label: string;
  value: string;
}

function TicketList({ category, refreshToken }: { category: string; refreshToken?: number | string | boolean }) {
  const { t } = useTranslation();
  const [workflowList, setWorkflowList] = useState<ISimpleWorkflowEntity[]>([]);
  const [workflowValue, setWorkflowValue] = useState<ISimpleWorkflowEntity | null>(null);
  const [ticketList, setTicketList] = useState<ITicketListResEntity[]>([]);

  const [page, setPage] = useState(0)
  const [perPage, setPerPage] = useState(10)
  const [total, setTotal] = useState(0)
  const [users, setUsers] = useState<IOption[]>([]);
  const [searchValue, setSearchValue] = useState('');
  const [createDateStart, setCreateDateStart] = useState<string>('');
  const [createDateEnd, setCreateDateEnd] = useState<string>('');
  const [showDateStart, setShowDateStart] = useState<boolean>(false);
  const [showDateEnd, setShowDateEnd] = useState<boolean>(false);

  const [loadingUsers, setLoadingUsers] = useState(false);
  const [selectedUser, setSelectedUser] = useState<IOption | null>(null);



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

  const loadUsers = async (searchValue: string = '') => {
    if (loadingUsers) return;
    setLoadingUsers(true);
    try {
      const response = await getSimpleUsers(searchValue);
      if (response.code === 0) {
        setUsers(response.data.userInfoList.map((user: ISimpleUser) => ({ label: `${user.name}(${user.alias})`, value: user.id })) || []);
      }
    } catch (error) {
      console.error('加载用户列表失败:', error);
    } finally {
      setLoadingUsers(false);
    }
  };
  const handleUserSelectChange = (value: IOption | null) => {
    setSelectedUser(value);
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

  const fetchTicketList = useCallback(async (searchValue: string = '') => {
    try {
      const res = await getTicketList({ category, page, perPage, searchValue, creatorId: selectedUser?.value, createDateStart, createDateEnd, workflowId: workflowValue?.id });
      if (res.code === 0) {
        setTicketList(res.data.ticketList);
        setTotal(res.data.total);
      } else {
        showMessage(res.msg, 'error');
      }
    } catch (error: any) {
      showMessage(error.message, 'error');
      console.log(error);
    }
  }, [category, page, perPage, selectedUser?.value, createDateStart, createDateEnd, workflowValue?.id, showMessage]);

  useEffect(() => {
    fetchTicketList();
  }, [fetchTicketList, refreshToken])

  const handleChangePage = (_event: any, newPage: number) => {
    setPage(newPage);
  }

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleTicketSearch = async () => {
    const res = await getTicketList({ category, page, perPage, searchValue, creatorId: selectedUser?.value, createDateStart, createDateEnd, workflowId: workflowValue?.id });
    if (res.code === 0) {
      setTicketList(res.data.ticketList);
    } else {
      showMessage(res.msg, 'error');
    }
  }

  return (
    <React.Fragment>
      <Card>
        <CardHeader title={listTitle} />
        <CardContent>
          <Grid container spacing={1} justifyContent="left" alignItems="center">
            <Grid size={{ xs: 12, sm: 6, md: 2 }}>
              <TextField fullWidth label={t('ticketList.keyword')} size="small" value={searchValue} onChange={(e) => setSearchValue(e.target.value)} />
            </Grid>
            <Grid size={{ xs: 12, sm: 6, md: 2 }}>
              <Autocomplete
                options={users}
                getOptionLabel={(option) => option.label}
                value={selectedUser}
                onChange={(e, value) => handleUserSelectChange(value)}
                onInputChange={(e, value) => {
                  if (value.length > 0) {
                    loadUsers(value);
                  }
                }}
                renderInput={(params) => (
                  <TextField
                    {...params}
                    label={t('ticketList.creator')}
                    placeholder={t('common.userSearchTip')}
                    InputProps={{
                      ...params.InputProps,
                      endAdornment: (
                        <>
                          {loadingUsers ? <CircularProgress color="inherit" size={20} /> : null}
                          {params.InputProps.endAdornment}
                        </>
                      ),
                    }}
                  />
                )}
                loading={loadingUsers}
                size="small"
                fullWidth
              />
            </Grid>
            <Grid size={{ xs: 12, sm: 6, md: 2 }}>
              <TextField
                fullWidth
                label={t('ticketList.createDateStart')}
                type="date"
                slotProps={{
                  inputLabel: { shrink: true },
                  input: {
                    lang: i18n.language,
                    style: { colorScheme: 'light' }
                  }
                }}
                size="small"
                value={createDateStart || (showDateStart ? new Date().toISOString().split('T')[0] : '')}
                onChange={(e) => {
                  setCreateDateStart(e.target.value);
                  setShowDateStart(true);
                }}
                onFocus={() => setShowDateStart(true)}
                onBlur={() => {
                  if (!createDateStart) {
                    setShowDateStart(false);
                  }
                }}
                InputLabelProps={{ shrink: true }}
                sx={{
                  '& input[type="date"]::-webkit-calendar-picker-indicator': {
                    opacity: 1
                  },
                  '& input[type="date"]': {
                    colorScheme: 'light',
                    color: createDateStart ? 'inherit' : (showDateStart ? 'inherit' : 'transparent')
                  }
                }}
                inputProps={{
                  'data-placeholder': '',
                  'data-empty': 'true'
                }}
              />
            </Grid>
            <Grid size={{ xs: 12, sm: 6, md: 2 }}>
              <TextField
                fullWidth
                label={t('ticketList.createDateEnd')}
                type="date"
                slotProps={{
                  inputLabel: { shrink: true },
                  input: {
                    lang: i18n.language,
                    style: { colorScheme: 'light' }
                  }
                }}
                size="small"
                value={createDateEnd || (showDateEnd ? new Date().toISOString().split('T')[0] : '')}
                onChange={(e) => {
                  setCreateDateEnd(e.target.value);
                  setShowDateEnd(true);
                }}
                onFocus={() => setShowDateEnd(true)}
                onBlur={() => {
                  if (!createDateEnd) {
                    setShowDateEnd(false);
                  }
                }}
                InputLabelProps={{ shrink: true }}
                sx={{
                  '& input[type="date"]::-webkit-calendar-picker-indicator': {
                    opacity: 1
                  },
                  '& input[type="date"]': {
                    colorScheme: 'light',
                    color: createDateEnd ? 'inherit' : (showDateEnd ? 'inherit' : 'transparent')
                  }
                }}
                inputProps={{
                  'data-placeholder': '',
                  'data-empty': 'true'
                }}
              />
            </Grid>
            <Grid size={{ xs: 12, sm: 6, md: 2 }}>
              <Autocomplete
                value={workflowValue}
                onChange={(event, newValue) => setWorkflowValue(newValue)}
                getOptionLabel={(option) => option.name}
                disablePortal
                options={workflowList}
                sx={{ marginLeft: 0, marginRight: 0 }}
                renderInput={(params) => <TextField {...params} label={t('ticketList.ticketType')} size="small" />}
              />
            </Grid>
            <Grid size={{ xs: 12, sm: 6, md: 2 }}>
              <Button variant="outlined" sx={{ height: '40px', width: '100px' }} size="small" onClick={handleTicketSearch}>{t('common.search')}</Button>
            </Grid>

          </Grid>

          <TableContainer sx={{ marginTop: '10px', boxShadow: 'none' }}>
            <Table>
              <TableHead>
                <TableRow>
                  {/* <TableCell>Id</TableCell> */}
                  <TableCell>{t('ticketList.ticketTitle')}</TableCell>
                  <TableCell>{t('ticketList.ticketType')}</TableCell>
                  <TableCell>{t('ticketList.approveState')}</TableCell>
                  <TableCell>{t('ticketList.ticketCreator')}</TableCell>
                  <TableCell>{t('ticketList.ticketCreateTime')}</TableCell>
                  <TableCell>{t('actions')}</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {ticketList ? ticketList.map((ticket) => (
                  <TableRow key={ticket.id}>
                    {/* <TableCell>{ticket.id}</TableCell> */}
                    <TableCell>{ticket.title}</TableCell>
                    <TableCell>{ticket.workflowInfo.name}</TableCell>
                    <TableCell>{ticket.actState}</TableCell>
                    <TableCell>{ticket.creatorInfo.alias}</TableCell>
                    <TableCell>{formatDate(ticket.createdAt)}</TableCell>
                    <TableCell align="left">
                      <MuiLink component={Link} to={`/ticket/${ticket.id}`} underline="none" color="primary">
                        {t('common.detail')}
                      </MuiLink>
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