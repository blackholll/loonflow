import { useEffect, useState, useCallback } from 'react';
import { useTranslation } from 'react-i18next';

import { getWorkflowVersionList } from '../../../../services/workflow';
import { SelectChangeEvent, Card, CardHeader, Button, Dialog, DialogTitle, DialogActions, DialogContent, Autocomplete, Container, TextField, Select, MenuItem, FormControl, InputLabel, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Box, TablePagination, CircularProgress } from '@mui/material';
import Grid from '@mui/material/Grid2';
import useSnackbar from '../../../../hooks/useSnackbar';


function WorkflowVersion({ workflowId }: { workflowId: string }) {
    const { t } = useTranslation();

    const [workflowVersionList, setWorkflowVersionList] = useState<any[]>([]);
    const [workflowVersionListLoading, setWorkflowVersionListLoading] = useState(false);
    const [page, setPage] = useState(1);
    const [perPage, setPerPage] = useState(10);
    const [total, setTotal] = useState(0);
    const [searchValue, setSearchValue] = useState('');
    const [openedVersionId, setOpenedVersionId] = useState('');
    const [versionName, setVersionName] = useState('');
    const [versionDescription, setVersionDescription] = useState('');
    const [versionType, setVersionType] = useState('default');
    const { showMessage } = useSnackbar();


    const fetchWorkflowVersionList = useCallback(async () => {
        if (!workflowId) {
            return;
        }
        try {
            setWorkflowVersionListLoading(true);
            const res = await getWorkflowVersionList(workflowId, searchValue, page, perPage);
            if (res.code === 0) {
                setWorkflowVersionList(res.data.versionInfoList);
                setTotal(res.data.total);
            } else {
                showMessage(res.msg, 'error');
            }
        } catch (error: any) {
            showMessage(error.message, 'error');
        } finally {
            setWorkflowVersionListLoading(false);
        }
    }, [workflowId, searchValue, page, perPage, showMessage]);



    useEffect(() => {
        fetchWorkflowVersionList();
    }, [fetchWorkflowVersionList]);

    const handleChangeKeyword = (event: React.ChangeEvent<HTMLInputElement>) => {
        setSearchValue(event.target.value);
    };

    const handleChangePage = (event: React.MouseEvent<HTMLButtonElement> | null, newPage: number) => {
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
        setPerPage(parseInt(event.target.value, 10));
    };

    const handleWorkflowVersionClose = () => {
        setOpenedVersionId('');
    };

    const handleEditVersion = (workflowVersion: any) => {
        console.log('workflowVersionworkflowVersion:', workflowVersion)
        setOpenedVersionId(workflowVersion.id);
        setVersionName(workflowVersion.name);
        setVersionDescription(workflowVersion.description);
        setVersionType(workflowVersion.type);
    };

    return (
        <div>
            <Grid container spacing={4} justifyContent="left" alignItems="center" sx={{ 'marginLeft': '10px' }}>
                <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                    <TextField fullWidth label={t('ticketList.searchWithKeyword')} onChange={handleChangeKeyword} />
                </Grid>
            </Grid>

            <TableContainer component={Paper} sx={{ marginTop: '10px' }}>
                {workflowVersionListLoading ? (<div><CircularProgress /></div>) : (
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell>{t('common.name')}</TableCell>
                                <TableCell>{t('common.description')}</TableCell>
                                <TableCell>{t('common.type')}</TableCell>
                                <TableCell>{t('common.createdAt')}</TableCell>
                                <TableCell>{t('common.actions')}</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {workflowVersionList ? workflowVersionList.map((workflowVersion) => (
                                <TableRow key={workflowVersion.id}>
                                    <TableCell>{workflowVersion.name}</TableCell>
                                    <TableCell>{workflowVersion.description}</TableCell>
                                    <TableCell>{workflowVersion.type}</TableCell>
                                    <TableCell>{new Date(workflowVersion.createdAt).toLocaleString()}</TableCell>
                                    <TableCell>
                                        <div><Button onClick={() => handleEditVersion(workflowVersion)}>编辑版本</Button><Button >编辑工作流</Button></div>
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
            <Dialog
                open={openedVersionId !== ''}
                keepMounted
                onClose={handleWorkflowVersionClose}
                aria-describedby="alert-dialog-slide-description"
                fullWidth
            >
                <DialogTitle>{"编辑版本"}</DialogTitle>
                <DialogContent>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                        <TextField
                            label="名称"
                            value={versionName}
                            fullWidth
                            margin="normal"
                            onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
                                setVersionName(event.target.value);
                            }}
                        />
                        <TextField
                            label="描述"
                            value={versionDescription}
                            fullWidth
                            margin="normal"
                            onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
                                setVersionDescription(event.target.value);
                            }}
                        />
                        <Select
                            value={versionType}
                            label="版本类型"
                            onChange={(event: SelectChangeEvent) => {
                                setVersionType(event.target.value);
                            }}
                        >
                            <MenuItem value={'default'}>default</MenuItem>
                            <MenuItem value={'archived'}>archived</MenuItem>
                            <MenuItem value={'candidate'}>candidate</MenuItem>
                        </Select>
                        <div style={{ display: 'flex', flexDirection: 'row', gap: '10px' }}>
                            <Button variant="outlined" size={'large'} sx={{ width: '150px' }} >{t('common.save')}</Button>
                            <Button variant="outlined" size={'large'} sx={{ width: '150px' }} >{t('common.cancel')}</Button>
                        </div>
                    </div>

                </DialogContent>
            </Dialog>
        </div>
    );
}

export default WorkflowVersion;