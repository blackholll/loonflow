import React, { useCallback, useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import {
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    TextField,
    Button,
    Paper,
    Table,
    TableBody,
    TableRow,
    TableCell,
    TableContainer,
    TableHead,
    TablePagination,
    CircularProgress,
    Box,
    Chip,
    IconButton,
    Checkbox,
} from '@mui/material';
import Grid from '@mui/material/Grid2';
import {
    Delete as DeleteIcon,
    Search as SearchIcon,
    Add as AddIcon
} from '@mui/icons-material';
import useSnackbar from '../../../hooks/useSnackbar';
import { getSimpleWorkflowList } from '../../../services/workflow';
import { getApplicationWorkflowList, addApplicationWorkflowPermission, deleteApplicationWorkflowPermission } from '../../../services/application';
import { ISimpleWorkflowEntity } from '../../../types/workflow';

interface ApplicationWorkflowPermissionDialogProps {
    open: boolean;
    applicationId: string;
    applicationName: string;
    onClose: () => void;
}

export function ApplicationWorkflowPermissionDialog({
    open,
    applicationId,
    applicationName,
    onClose
}: ApplicationWorkflowPermissionDialogProps) {
    const { t } = useTranslation();
    const { showMessage } = useSnackbar();

    // 状态管理
    const [workflowList, setWorkflowList] = useState<ISimpleWorkflowEntity[]>([]);
    const [allWorkflows, setAllWorkflows] = useState<ISimpleWorkflowEntity[]>([]);
    const [loading, setLoading] = useState<boolean>(false);
    const [searchKey, setSearchKey] = useState<string>('');
    const [page, setPage] = useState<number>(0);
    const [perPage, setPerPage] = useState<number>(10);
    const [total, setTotal] = useState<number>(0);

    // 新增工作流权限相关状态
    const [showAddDialog, setShowAddDialog] = useState<boolean>(false);
    const [addSearchKey, setAddSearchKey] = useState<string>('');
    const [addPage, setAddPage] = useState<number>(0);
    const [addPerPage, setAddPerPage] = useState<number>(10);
    const [addTotal, setAddTotal] = useState<number>(0);
    const [selectedWorkflows, setSelectedWorkflows] = useState<string[]>([]);
    const [addLoading, setAddLoading] = useState<boolean>(false);

    // 删除确认对话框状态
    const [showDeleteDialog, setShowDeleteDialog] = useState<boolean>(false);
    const [workflowToDelete, setWorkflowToDelete] = useState<ISimpleWorkflowEntity | null>(null);

    // 获取应用工作流权限列表
    const fetchWorkflowList = useCallback(async () => {
        if (!applicationId) return;

        try {
            setLoading(true);
            const res = await getApplicationWorkflowList(applicationId, searchKey, page, perPage);
            if (res.code === 0) {
                setWorkflowList(res.data.workflowInfoList);
                setTotal(res.data.total);
            } else {
                showMessage(res.msg, 'error');
            }
        } catch (error: any) {
            showMessage(error.message || '获取工作流权限失败', 'error');
        } finally {
            setLoading(false);
        }
    }, [applicationId, searchKey, page, perPage, showMessage]);

    // 获取所有工作流列表（用于添加权限）
    const fetchAllWorkflows = useCallback(async () => {
        try {
            setAddLoading(true);
            const res = await getSimpleWorkflowList(addSearchKey, addPage + 1, addPerPage);
            if (res.code === 0) {
                setAllWorkflows(res.data.workflowInfoList);
                setAddTotal(res.data.total);
            } else {
                showMessage(res.msg, 'error');
            }
        } catch (error: any) {
            showMessage(error.message || '获取工作流列表失败', 'error');
        } finally {
            setAddLoading(false);
        }
    }, [addSearchKey, addPage, addPerPage, showMessage]);

    // 初始化数据
    useEffect(() => {
        if (open && applicationId) {
            fetchWorkflowList();
        }
    }, [open, applicationId, fetchWorkflowList]);

    useEffect(() => {
        if (showAddDialog) {
            fetchAllWorkflows();
        }
    }, [showAddDialog, fetchAllWorkflows]);

    // 处理分页变化
    const handleChangePage = (event: React.MouseEvent<HTMLButtonElement> | null, newPage: number) => {
        setPage(newPage);
    };

    const handleAddChangePage = (event: React.MouseEvent<HTMLButtonElement> | null, newPage: number) => {
        setAddPage(newPage);
    };

    // 处理每页显示数量变化
    const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
        setPerPage(parseInt(event.target.value, 10));
        setPage(0);
    };

    const handleAddChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
        setAddPerPage(parseInt(event.target.value, 10));
        setAddPage(0);
    };

    // 显示删除确认对话框
    const handleDeleteWorkflow = (workflow: ISimpleWorkflowEntity) => {
        setWorkflowToDelete(workflow);
        setShowDeleteDialog(true);
    };

    // 确认删除工作流权限
    const handleConfirmDeleteWorkflow = async () => {
        if (!workflowToDelete) return;

        try {
            const res = await deleteApplicationWorkflowPermission(applicationId, workflowToDelete.id);
            if (res.code === 0) {
                showMessage('删除工作流权限成功', 'success');
                fetchWorkflowList(); // 刷新列表
            } else {
                showMessage(res.msg || '删除工作流权限失败', 'error');
            }
        } catch (error: any) {
            showMessage(error.message || '删除工作流权限失败', 'error');
        } finally {
            setShowDeleteDialog(false);
            setWorkflowToDelete(null);
        }
    };

    // 取消删除
    const handleCancelDelete = () => {
        setShowDeleteDialog(false);
        setWorkflowToDelete(null);
    };

    // 处理工作流选择
    const handleWorkflowSelect = (workflowId: string, checked: boolean) => {
        if (checked) {
            setSelectedWorkflows(prev => [...prev, workflowId]);
        } else {
            setSelectedWorkflows(prev => prev.filter(id => id !== workflowId));
        }
    };

    // 处理全选
    const handleSelectAll = (checked: boolean) => {
        if (checked) {
            const currentPageWorkflowIds = allWorkflows.map(workflow => workflow.id);
            setSelectedWorkflows(prev => Array.from(new Set([...prev, ...currentPageWorkflowIds])));
        } else {
            const currentPageWorkflowIds = allWorkflows.map(workflow => workflow.id);
            setSelectedWorkflows(prev => prev.filter(id => !currentPageWorkflowIds.includes(id)));
        }
    };

    // 添加工作流权限
    const handleAddWorkflows = async () => {
        if (selectedWorkflows.length === 0) {
            showMessage('请选择要添加的工作流', 'warning');
            return;
        }

        try {
            const res = await addApplicationWorkflowPermission(applicationId, selectedWorkflows);
            if (res.code === 0) {
                showMessage('添加工作流权限成功', 'success');
                setShowAddDialog(false);
                setSelectedWorkflows([]);
                fetchWorkflowList(); // 刷新权限列表
            } else {
                showMessage(res.msg || '添加工作流权限失败', 'error');
            }
        } catch (error: any) {
            showMessage(error.message || '添加工作流权限失败', 'error');
        }
    };

    // 关闭对话框
    const handleClose = () => {
        setSearchKey('');
        setPage(0);
        setPerPage(10);
        setWorkflowList([]);
        setTotal(0);
        onClose();
    };

    const handleCloseAddDialog = () => {
        setShowAddDialog(false);
        setAddSearchKey('');
        setAddPage(0);
        setAddPerPage(10);
        setSelectedWorkflows([]);
        setAllWorkflows([]);
        setAddTotal(0);
    };

    return (
        <>
            {/* 工作流权限列表对话框 */}
            <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
                <DialogTitle>
                    {t('common.workflowPermission')} - {applicationName}
                </DialogTitle>
                <DialogContent>
                    <Box sx={{ mb: 2 }}>
                        <Grid container spacing={2} alignItems="center">
                            <Grid size={{ xs: 8, sm: 6, md: 9 }}>
                                <TextField
                                    fullWidth
                                    style={{ marginTop: '10px' }}
                                    label={t('common.searchWithKeyword')}
                                    value={searchKey}
                                    onChange={(e) => setSearchKey(e.target.value)}
                                    InputProps={{
                                        startAdornment: <SearchIcon sx={{ mr: 1 }} />
                                    }}
                                />
                            </Grid>
                            <Grid size={{ xs: 4, sm: 4, md: 2 }}>
                                <Button
                                    variant="outlined"
                                    startIcon={<AddIcon />}
                                    onClick={() => setShowAddDialog(true)}
                                    fullWidth
                                    style={{ height: '45px' }}
                                >
                                    {t('common.add')}
                                </Button>
                            </Grid>
                        </Grid>
                    </Box>

                    <TableContainer component={Paper}>
                        {loading ? (
                            <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
                                <CircularProgress />
                            </Box>
                        ) : (
                            <Table>
                                <TableHead>
                                    <TableRow>
                                        <TableCell>{t('common.name')}</TableCell>
                                        <TableCell>{t('common.description')}</TableCell>
                                        <TableCell>{t('common.actions')}</TableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {workflowList.map((workflow) => (
                                        <TableRow key={workflow.id}>
                                            <TableCell>{workflow.name}</TableCell>
                                            <TableCell>{workflow.description}</TableCell>
                                            <TableCell>
                                                <IconButton
                                                    color="error"
                                                    onClick={() => handleDeleteWorkflow(workflow)}
                                                    size="small"
                                                >
                                                    <DeleteIcon />
                                                </IconButton>
                                            </TableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        )}
                    </TableContainer>

                    <TablePagination
                        rowsPerPageOptions={[10, 25, 50]}
                        component="div"
                        count={total}
                        rowsPerPage={perPage}
                        page={page}
                        onPageChange={handleChangePage}
                        onRowsPerPageChange={handleChangeRowsPerPage}
                    />
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleClose} color="primary">
                        {t('common.close')}
                    </Button>
                </DialogActions>
            </Dialog>

            {/* 添加工作流权限对话框 */}
            <Dialog open={showAddDialog} onClose={handleCloseAddDialog} maxWidth="md" fullWidth>
                <DialogTitle>
                    {t('common.add')} {t('common.workflowPermission')}
                </DialogTitle>
                <DialogContent>
                    <Box sx={{ mb: 2 }}>
                        <TextField
                            fullWidth
                            style={{ marginTop: '10px' }}
                            label={t('common.searchWithKeyword')}
                            value={addSearchKey}
                            onChange={(e) => setAddSearchKey(e.target.value)}
                            InputProps={{
                                startAdornment: <SearchIcon sx={{ mr: 1 }} />
                            }}
                        />
                    </Box>

                    <TableContainer component={Paper}>
                        {addLoading ? (
                            <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
                                <CircularProgress />
                            </Box>
                        ) : (
                            <Table>
                                <TableHead>
                                    <TableRow>
                                        <TableCell padding="checkbox">
                                            <Checkbox
                                                indeterminate={selectedWorkflows.length > 0 && selectedWorkflows.length < allWorkflows.length}
                                                checked={allWorkflows.length > 0 && selectedWorkflows.length === allWorkflows.length}
                                                onChange={(e) => handleSelectAll(e.target.checked)}
                                            />
                                        </TableCell>
                                        <TableCell>{t('common.name')}</TableCell>
                                        <TableCell>{t('common.description')}</TableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {allWorkflows.map((workflow) => (
                                        <TableRow key={workflow.id}>
                                            <TableCell padding="checkbox">
                                                <Checkbox
                                                    checked={selectedWorkflows.includes(workflow.id)}
                                                    onChange={(e) => handleWorkflowSelect(workflow.id, e.target.checked)}
                                                />
                                            </TableCell>
                                            <TableCell>{workflow.name}</TableCell>
                                            <TableCell>{workflow.description}</TableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        )}
                    </TableContainer>

                    <TablePagination
                        rowsPerPageOptions={[10, 25, 50]}
                        component="div"
                        count={addTotal}
                        rowsPerPage={addPerPage}
                        page={addPage}
                        onPageChange={handleAddChangePage}
                        onRowsPerPageChange={handleAddChangeRowsPerPage}
                    />

                    {selectedWorkflows.length > 0 && (
                        <Box sx={{ mt: 2 }}>
                            <Chip
                                label={`已选择 ${selectedWorkflows.length} 个工作流`}
                                color="primary"
                                variant="outlined"
                            />
                        </Box>
                    )}
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleCloseAddDialog} color="primary">
                        {t('common.cancel')}
                    </Button>
                    <Button onClick={handleAddWorkflows} color="primary" variant="contained">
                        {t('common.confirm')}
                    </Button>
                </DialogActions>
            </Dialog>

            {/* 删除确认对话框 */}
            <Dialog open={showDeleteDialog} onClose={handleCancelDelete} maxWidth="sm" fullWidth>
                <DialogTitle>
                    确认删除工作流权限
                </DialogTitle>
                <DialogContent>
                    <Box sx={{ pt: 2 }}>
                        {workflowToDelete && (
                            <Box>
                                <p>确定要删除此工作流权限吗？</p>
                                <Box sx={{ mt: 2, p: 2, bgcolor: 'grey.100', borderRadius: 1 }}>
                                    <strong>{t('common.name')}:</strong> {workflowToDelete.name}<br />
                                    <strong>{t('common.description')}:</strong> {workflowToDelete.description}
                                </Box>
                            </Box>
                        )}
                    </Box>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleCancelDelete} color="primary">
                        {t('common.cancel')}
                    </Button>
                    <Button onClick={handleConfirmDeleteWorkflow} color="error" variant="contained">
                        {t('common.confirm')}
                    </Button>
                </DialogActions>
            </Dialog>
        </>
    );
}

export default ApplicationWorkflowPermissionDialog;
