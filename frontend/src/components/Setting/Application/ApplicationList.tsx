import React, { useEffect, useState, useCallback } from 'react';
import { useTranslation } from 'react-i18next';
import { Card, CardHeader, Button, Dialog, DialogTitle, DialogActions, DialogContent, Autocomplete, Container, TextField, Select, MenuItem, FormControl, InputLabel, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Box, TablePagination, CircularProgress } from '@mui/material';
import Grid from '@mui/material/Grid2';
import { IApplicationResEntity } from '@/types/application';
import useSnackbar from '../../../hooks/useSnackbar';
import { getApplicationList, delApplicationDetail } from '../../../services/application';
import ApplicationDialog from './ApplicationDialog';


export function ApplicationList() {
  const { t } = useTranslation();
  const [applicationDatas, setApplicationDatas] = useState<IApplicationResEntity[]>([]);
  const [applicationListLoading, setApplicationListLoading] = useState<Boolean>(false);
  const [searchKey, setSearchKey] = useState('');
  const [page, setPage] = useState(1);
  const [perPage, setPerPage] = useState(10);
  const [total, setTotal] = useState(0);
  const [openApp, setOpenApp] = useState(false);
  const [openDeleteConfirm, setOpenDeleteConfirm] = useState(false);
  const [openedAppId, setOpenedAppId] = useState('');
  const [delAppId, setDelAppId] = useState('');
  const { showMessage } = useSnackbar();

  const fetchApplicationList = useCallback(async () => {
    try {
      setApplicationListLoading(true);
      const res = await getApplicationList(searchKey, page, perPage);
      if (res.code === 0) {
        setApplicationDatas(res.data.applicationList);
        setTotal(res.data.total);
      } else {
        showMessage(res.msg, 'error');
      }
    } catch (error: any) {
      showMessage(error.message, 'error');
      console.log(error);
    } finally {
      setApplicationListLoading(false);
    }
  }, [searchKey, page, perPage, showMessage]);

  useEffect(() => {
    fetchApplicationList();
  }, [searchKey, page, perPage, fetchApplicationList]);

  const handleConfirmDelete = async (applicationId: string) => {
    const result = await delApplicationDetail(applicationId);
    if (result.code === 0) {
      fetchApplicationList();
      showMessage('deleted', 'success');
      setOpenDeleteConfirm(false);
    } else {
      showMessage(result.msg, 'error');
    }
  }

  const handleConfirmClose = () => {
    setOpenDeleteConfirm(false);
  }
  const handleDeleteClick = (applicationId: string) => {
    setOpenDeleteConfirm(true);
    setDelAppId(applicationId);
  }

  const handleChangePage = (_event: any, newPage: number) => {
    setPage(newPage);
  }
  const handleChangeKeyword = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchKey(event.target.value);
  }
  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setPerPage(parseInt(event.target.value, 10));
    setPage(0);
    fetchApplicationList()
  };

  const handleOpenNewApp = () => {
    setOpenApp(true);
  }
  const handleOpenApp = (applicationId: string) => {
    console.log('applicationIdapplicationId:', applicationId);
    setOpenedAppId(applicationId)
    setOpenApp(true);
  }

  const closeDialog = () => {
    setOpenApp(false);
    setOpenedAppId('');
  }

  return (
    <Card>
      <CardHeader title={t('setting.application.applicationList')} />
      <Grid container spacing={4} justifyContent="left" alignItems="center" sx={{ 'marginLeft': '10px' }}>
        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <TextField fullWidth label={t('ticketList.searchWithKeyword')} onChange={handleChangeKeyword} />
        </Grid>
        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Button variant="outlined" size={'large'} sx={{ width: '150px' }} onClick={handleOpenNewApp}>{t('common.new')}</Button>
        </Grid>
      </Grid>

      <TableContainer component={Paper} sx={{ marginTop: '10px' }}>
        {applicationListLoading ? (<div><CircularProgress /></div>) : (
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
              {applicationDatas ? applicationDatas.map((application) => (
                <TableRow key={application.id}>
                  <TableCell>{application.name}</TableCell>
                  <TableCell>{application.description}</TableCell>
                  <TableCell>{t(`common.${application.type}`)}</TableCell>
                  <TableCell>
                    <div><Button onClick={() => handleOpenApp(application.id)}>edit</Button><Button onClick={() => handleDeleteClick(application.id)}>delete</Button>{application.type === 'workflowAdmin' ? <Button >{t('common.workflowPermission')}</Button> : null}</div>
                  </TableCell>
                </TableRow>
              )) : null}
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
      <ApplicationDialog open={openApp} applicationId={openedAppId} onClose={() => closeDialog()} />
      <Dialog open={openDeleteConfirm} onClose={handleConfirmClose}>
        <DialogTitle>{t('common.confirm')}</DialogTitle>
        <DialogContent>
          <p>{t('common.wantDeleteRecord')}</p>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleConfirmClose} color="primary">
            {t('common.cancel')}
          </Button>
          <Button onClick={() => handleConfirmDelete(delAppId)} color="error">
            {t('common.confirm')}
          </Button>
        </DialogActions>

      </Dialog>
    </Card>
  )

}