import React, { useEffect, useState, useCallback } from 'react';
import { useTranslation } from 'react-i18next';
import { Card, CardHeader, Button, Dialog, DialogTitle, DialogActions, DialogContent, Autocomplete, Container, TextField, Select, MenuItem, FormControl, InputLabel, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Box, TablePagination, CircularProgress } from '@mui/material';
import Grid from '@mui/material/Grid2';
import { INotificationResEntity } from '@/types/notification';
import useSnackbar from '../../../hooks/useSnackbar';
import { getNotificationList, delNotification } from '../../../services/notification';
import NotificationDialog from './NotificationDialog';


export const NotificationList=()=> {
  const { t } = useTranslation();
  const [ notificationDatas, setNotificationDatas ] = useState<INotificationResEntity[]>([]);
  const [ notificationListLoading, setNotificationListLoading ] = useState<Boolean>(false);
  const [ searchKey, setSearchKey ] = useState('');
  const [ page, setPage ] = useState(1);
  const [ perPage, setPerPage ] = useState(10);
  const [ total, setTotal ] = useState(0);
  const [ openNotification, setOpenNotification ] = useState(false);
  const [ openDeleteConfirm, setOpenDeleteConfirm ] = useState(false);
  const [ openedNotificationId, setOpenedAppId ] = useState('');
  const [ delNotificationId, setDelAppId] = useState('');
  const { showMessage } = useSnackbar();
  
  const fetchNotificationList = useCallback(async()=>{
    try{
      setNotificationListLoading(true);
      const res = await getNotificationList(searchKey, page, perPage);
      if (res.code === 0){
        setNotificationDatas(res.data.notification_list);
        setTotal(res.data.total);
      } else {
        showMessage(res.msg, 'error');
      }
    } catch (error:any) {
      showMessage(error.message, 'error');
      console.log(error);
    } finally {
      setNotificationListLoading(false);
    }
  }, [searchKey, page, perPage, showMessage]);
  
  useEffect(() => {
      fetchNotificationList();
  }, [searchKey, page, perPage, fetchNotificationList]);

  const handleConfirmDelete = async(notificationId:string) => {
    const result = await delNotification(notificationId);
    if (result.code === 0) {
      fetchNotificationList();
      showMessage('deleted', 'success');
      setOpenDeleteConfirm(false);
    } else {
      showMessage(result.msg, 'error');
    }
  }

  const handleConfirmClose = () => {
    setOpenDeleteConfirm(false);
  }
  const handleDeleteClick = (notificationId:string) => {
    setOpenDeleteConfirm(true);
    setDelAppId(notificationId);
  }
  
  const handleChangePage = (_event:any, newPage:number) => {
    setPage(newPage);
  }
  const handleChangeKeyword = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchKey(event.target.value);
  }
  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setPerPage(parseInt(event.target.value, 10));
    setPage(0);
    fetchNotificationList()
  };
  
  const handleOpenNewNotifacation = () => {
    setOpenNotification(true);
  }
  const handleOpenNotification = (notificationId:string) => {
    console.log('notificationIdnotificationId:', notificationId);
    setOpenedAppId(notificationId)
    setOpenNotification(true);
  }

  const closeDialog = () => {
    setOpenNotification(false);
    setOpenedAppId('');
  }
  
  return (
    <Card>
      <CardHeader title={t('setting.notification.notificationList')}/>
        <Grid container spacing={4} justifyContent="left" alignItems="center" sx={{'marginLeft': '10px'}}>
          <Grid size={{xs:12, sm:6, md:3}}>
            <TextField fullWidth label={t('ticketList.searchWithKeyword')} onChange={handleChangeKeyword}/>
          </Grid>
          <Grid size={{xs:12, sm:6, md:3}}>
            <Button variant="outlined" size={'large'} sx={{width:'150px'}} onClick={handleOpenNewNotifacation}>{t('common.new')}</Button>
          </Grid>
        </Grid>
      
        <TableContainer component={Paper} sx={{ marginTop: '10px' }}>
        {notificationListLoading?(<div><CircularProgress/></div>) : (
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>{t('common.name')}</TableCell>
              <TableCell>{t('common.description')}</TableCell>
              <TableCell>{t('common.type')}</TableCell>
              <TableCell>{t('common.actions')}</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {notificationDatas?notificationDatas.map((notification) => (
              <TableRow key={notification.id}>
                <TableCell>{notification.name}</TableCell>
                <TableCell>{notification.description}</TableCell>
                <TableCell>{t(`common.${notification.type}`)}</TableCell>
                <TableCell>
                  <div><Button onClick={()=>handleOpenNotification(notification.id)}>edit</Button><Button onClick={()=>handleDeleteClick(notification.id)}>delete</Button>{notification.type === 'workflowAdmin'?<Button >{t('common.workflowPermission')}</Button>:null}</div>
                  </TableCell>
              </TableRow>
            )):null}
          </TableBody>
        </Table>)}
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
      <NotificationDialog open={openNotification} notificationId={openedNotificationId} onClose={()=>closeDialog()}/>
      <Dialog open={openDeleteConfirm} onClose={handleConfirmClose}>
        <DialogTitle>{t('common.confirm')}</DialogTitle>
        <DialogContent>
          <p>{t('common.wantDeleteRecord')}</p>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleConfirmClose} color="primary">
            {t('common.cancel')}
          </Button>
          <Button onClick={()=> handleConfirmDelete(delNotificationId)} color="error">
          {t('common.confirm')}
          </Button>
        </DialogActions>

      </Dialog>
      </Card>
  )

}