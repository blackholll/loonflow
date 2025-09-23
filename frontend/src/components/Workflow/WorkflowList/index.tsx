import React, { useCallback, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { Card, CardHeader, Button, Dialog, DialogTitle, DialogActions, DialogContent, Autocomplete, Container, TextField, Select, MenuItem, FormControl, InputLabel, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Box, TablePagination, CircularProgress } from '@mui/material';
import { Link } from 'react-router-dom';
import Grid from '@mui/material/Grid2';
import { IWorkflowEntity } from '../../../types/workflow';
import useSnackbar from '../../../hooks/useSnackbar';
import { getWorkflowList, } from '../../../services/workflow';
import WorkflowVersion from './workflowVersion';


export function WorkflowList() {
    const { t } = useTranslation();
    const [workflowDatas, setWorkflowDatas] = React.useState<IWorkflowEntity[]>([]);
    const [workflowListLoading, setWorkflowListLoading] = React.useState<boolean>(false);
    const [searchKey, setSearchKey] = React.useState<string>('')
    const [total, setTotal] = React.useState<number>(0)
    const [page, setPage] = React.useState<number>(0)
    const [perPage, setPerPage] = React.useState<number>(10)
    const [openedWorkflowIdVersion, setOpenedWorkflowIdVersion] = React.useState<string>('')

    useEffect(() => {
        const maxPage = Math.ceil(total / perPage);
        if (page > maxPage - 1 && maxPage >= 1) {
            setPage(maxPage);
        }
    }, [total, perPage]);

    const { showMessage } = useSnackbar();

    const fetchWorkflowList = useCallback(async () => {
        try {
            setWorkflowListLoading(true);
            const res = await getWorkflowList(searchKey, page + 1, perPage,);
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

    const handleWorkflowVersionClose = () => {
        setOpenedWorkflowIdVersion('');
    }

    return (
        <Card>
            <CardHeader title={t('workflow.workflowList')} />
            <Grid container spacing={4} justifyContent="left" alignItems="center" sx={{ 'marginLeft': '10px' }}>
                <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                    <TextField fullWidth label={t('common.searchWithKeyword')} onChange={(event: React.ChangeEvent<HTMLInputElement>) => { setSearchKey(event.target.value) }} />
                </Grid>
                <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                    <Link to="/workflow/00000000-0000-0000-0000-000000000000">
                        <Button variant="outlined" size={'large'} sx={{ width: '150px' }}>{t('common.new')}</Button>
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
                                <TableCell>{t('workflow.activeVersion')}</TableCell>
                                <TableCell>{t('common.actions')}</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {workflowDatas ? workflowDatas.map((workflowData) => (
                                <TableRow key={workflowData.id}>
                                    <TableCell>{workflowData.name}</TableCell>
                                    <TableCell>{workflowData.description}</TableCell>
                                    <TableCell>{workflowData.version}</TableCell>
                                    <TableCell>
                                        <div><Button onClick={() => setOpenedWorkflowIdVersion(workflowData.workflowId)}>{t('common.edit')}</Button></div>
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
                page={total === 0 ? 0 : page}
                onPageChange={(_event: any, newPage) => setPage(newPage)}
                onRowsPerPageChange={(event: React.ChangeEvent<HTMLInputElement>) => {
                    setPerPage(parseInt(event.target.value, 10));
                    setPage(0);
                }}
            />
            <Dialog
                maxWidth="md"
                open={openedWorkflowIdVersion !== ''}
                keepMounted
                onClose={handleWorkflowVersionClose}
                aria-describedby="alert-dialog-slide-description"
                fullWidth
            >
                <DialogTitle>{t('workflow.versionList')}</DialogTitle>
                <DialogContent>
                    <WorkflowVersion workflowId={openedWorkflowIdVersion} />
                </DialogContent>
            </Dialog>
        </Card>

    );
}
