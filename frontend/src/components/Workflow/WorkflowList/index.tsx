import React, { useCallback, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { Card, CardHeader, Button, Dialog, DialogTitle, DialogActions, DialogContent, Autocomplete, Container, TextField, Select, MenuItem, FormControl, InputLabel, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Box, TablePagination, CircularProgress } from '@mui/material';
import { Link } from 'react-router-dom';
import Grid from '@mui/material/Grid2';
import { IWorkflowEntity } from '../../../types/workflow';
import useSnackbar from '../../../hooks/useSnackbar';
import { getWorkflowList, } from '../../../services/workflow';


export function WorkflowList() {
    const { t } = useTranslation();
    const [workflowDatas, setWorkflowDatas] = React.useState<IWorkflowEntity[]>([]);
    const [workflowListLoading, setWorkflowListLoading] = React.useState<boolean>(false);
    const [searchKey, setSearchKey] = React.useState<string>('')
    const [openWorkflow, setOpenWorkflow] = React.useState<boolean>(false);
    const [openedWorkflowId, setOpenedWorkflowId] = React.useState<string>('')
    const [total, setTotal] = React.useState<number>(0)
    const [page, setPage] = React.useState<number>(1)
    const [perPage, setPerPage] = React.useState<number>(10)
    const { showMessage } = useSnackbar();

    const fetchWorkflowList = useCallback(async () => {
        try {
            setWorkflowListLoading(true);
            const res = await getWorkflowList(searchKey, page, perPage,);
            if (res.code === 0) {
                setWorkflowDatas(res.data.workflowInfoList);
                setTotal(res.data.total);
            }
        } catch (error: any) {
            showMessage(error.msg, 'error');
        } finally {
            setWorkflowListLoading(false);
        }
    }, [searchKey, page, perPage, showMessage]);

    useEffect(() => {
        fetchWorkflowList();
    }, [searchKey, page, perPage, fetchWorkflowList]);


    const handleOpenWorkflow = (workflowId: string) => {
        setOpenWorkflow(true);
        setOpenedWorkflowId(workflowId);
    }

    return (
        <Card>
            <CardHeader title={t('workflow.workflowList')} />
            <Grid container spacing={4} justifyContent="left" alignItems="center" sx={{ 'marginLeft': '10px' }}>
                <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                    <TextField fullWidth label={t('ticketList.searchWithKeyword')} onChange={(event: React.ChangeEvent<HTMLInputElement>) => { setSearchKey(event.target.value) }} />
                </Grid>
                <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                    <Link to="/workflow/00000000-0000-0000-0000-000000000000">
                        <Button variant="outlined" size={'large'} sx={{ width: '150px' }} onClick={() => setOpenWorkflow(true)}>{t('common.new')}</Button>
                    </Link>
                </Grid>
            </Grid>

            <TableContainer component={Paper} sx={{ marginTop: '10px' }}>
                {workflowListLoading ? (<div><CircularProgress /></div>) : (
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell>{t('common.name')}</TableCell>
                                <TableCell>{t('common.description')}</TableCell>
                                <TableCell>{t('common.actions')}</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {workflowDatas ? workflowDatas.map((workflowData) => (
                                <TableRow key={workflowData.id}>
                                    <TableCell>{workflowData.name}</TableCell>
                                    <TableCell>{workflowData.description}</TableCell>
                                    <TableCell>
                                        <div><Button onClick={() => handleOpenWorkflow(workflowData.id)}>edit</Button></div>
                                        {/* <div><Button onClick={() => handleOpenWorkflow(workflowData.id)}>edit</Button><Button onClick={() => handleDeleteClick(workflowData.id)}>delete</Button>{application.type === 'workflowAdmin' ? <Button >{t('common.workflowPermission')}</Button> : null}</div> */}
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
                onPageChange={(_event: any, newPage) => setPage(newPage)}
                onRowsPerPageChange={(event: React.ChangeEvent<HTMLInputElement>) => { setPerPage(parseInt(event.target.value, 10)); setPage(1); fetchWorkflowList() }}
            />
        </Card>
    );
}
