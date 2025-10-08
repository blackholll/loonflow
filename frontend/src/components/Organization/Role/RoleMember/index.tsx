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
    PersonAdd as PersonAddIcon
} from '@mui/icons-material';
import useSnackbar from '../../../../hooks/useSnackbar';
import { getSimpleUsers } from '../../../../services/user';
import { addRoleUser, deleteRoleUser, getRoleUserList } from '../../../../services/role';
import { ISimpleUser } from '../../../../types/user';

interface RoleMemberProps {
    open: boolean;
    roleId: string;
    roleName: string;
    onClose: () => void;
}

export function RoleMember({ open, roleId, roleName, onClose }: RoleMemberProps) {
    const { t } = useTranslation();
    const { showMessage } = useSnackbar();

    // 状态管理
    const [memberList, setMemberList] = useState<ISimpleUser[]>([]);
    const [allUsers, setAllUsers] = useState<ISimpleUser[]>([]);
    const [loading, setLoading] = useState<boolean>(false);
    const [searchKey, setSearchKey] = useState<string>('');
    const [page, setPage] = useState<number>(0);
    const [perPage, setPerPage] = useState<number>(10);
    const [total, setTotal] = useState<number>(0);

    // 新增成员相关状态
    const [showAddDialog, setShowAddDialog] = useState<boolean>(false);
    const [addSearchKey, setAddSearchKey] = useState<string>('');
    const [addPage, setAddPage] = useState<number>(0);
    const [addPerPage, setAddPerPage] = useState<number>(10);
    const [addTotal, setAddTotal] = useState<number>(0);
    const [selectedUsers, setSelectedUsers] = useState<string[]>([]);
    const [addLoading, setAddLoading] = useState<boolean>(false);

    // 删除确认对话框状态
    const [showDeleteDialog, setShowDeleteDialog] = useState<boolean>(false);
    const [memberToDelete, setMemberToDelete] = useState<ISimpleUser | null>(null);

    // 获取角色成员列表
    const fetchMemberList = useCallback(async () => {
        if (!roleId) return;

        try {
            setLoading(true);
            // 这里需要根据实际API调整，假设有一个获取角色成员的API
            // 暂时使用getSimpleUsers，实际应该调用获取角色成员的API
            const res = await getRoleUserList(roleId, '', page + 1, perPage);
            setMemberList(res.data.userInfoList);
            setTotal(res.data.total);
        } catch (error: any) {
            showMessage(error.message || '获取角色成员失败', 'error');
        } finally {
            setLoading(false);
        }
    }, [roleId, page, perPage, showMessage]);



    useEffect(() => {
        const handleSearchMemberList = async () => {
            if (!roleId) return;
            const res = await getRoleUserList(roleId, searchKey, page + 1, perPage);
            setMemberList(res.data.userInfoList);
            setTotal(res.data.total);
        };
        handleSearchMemberList();
    }, [roleId, searchKey, page, perPage]);


    // 获取所有用户列表（用于添加成员）
    const fetchAllUsers = useCallback(async () => {
        try {
            setAddLoading(true);
            const res = await getSimpleUsers(addSearchKey, '', addPage + 1, addPerPage);
            setAllUsers(res.data.userInfoList);
            setAddTotal(res.data.total);
        } catch (error: any) {
            showMessage(error.message || '获取用户列表失败', 'error');
        } finally {
            setAddLoading(false);
        }
    }, [addSearchKey, addPage, addPerPage, showMessage]);

    // 初始化数据
    useEffect(() => {
        if (open && roleId) {
            fetchMemberList();
        }
    }, [open, roleId, fetchMemberList]);

    useEffect(() => {
        if (showAddDialog) {
            fetchAllUsers();
        }
    }, [showAddDialog, fetchAllUsers]);

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
    const handleDeleteMember = (member: ISimpleUser) => {
        setMemberToDelete(member);
        setShowDeleteDialog(true);
    };

    // 确认删除角色成员
    const handleConfirmDeleteMember = async () => {
        if (!memberToDelete) return;

        try {
            await deleteRoleUser(roleId, [memberToDelete.id]);
            showMessage(t('role.deleteMemberSuccess'), 'success');
            fetchMemberList(); // 刷新列表
        } catch (error: any) {
            showMessage(error.message || t('role.deleteMemberFail'), 'error');
        } finally {
            setShowDeleteDialog(false);
            setMemberToDelete(null);
        }
    };

    // 取消删除
    const handleCancelDelete = () => {
        setShowDeleteDialog(false);
        setMemberToDelete(null);
    };

    // 处理用户选择
    const handleUserSelect = (userId: string, checked: boolean) => {
        if (checked) {
            setSelectedUsers(prev => [...prev, userId]);
        } else {
            setSelectedUsers(prev => prev.filter(id => id !== userId));
        }
    };

    // 处理全选
    const handleSelectAll = (checked: boolean) => {
        if (checked) {
            const currentPageUserIds = allUsers.map(user => user.id);
            setSelectedUsers(prev => Array.from(new Set([...prev, ...currentPageUserIds])));
        } else {
            const currentPageUserIds = allUsers.map(user => user.id);
            setSelectedUsers(prev => prev.filter(id => !currentPageUserIds.includes(id)));
        }
    };

    // 添加角色成员
    const handleAddMembers = async () => {
        if (selectedUsers.length === 0) {
            showMessage('请选择要添加的用户', 'warning');
            return;
        }

        try {
            await addRoleUser(roleId, selectedUsers);
            showMessage(t('common.addSuccess'), 'success');
            setShowAddDialog(false);
            setSelectedUsers([]);
            fetchMemberList(); // 刷新成员列表
        } catch (error: any) {
            showMessage(error.message || '添加成员失败', 'error');
        }
    };

    // 关闭对话框
    const handleClose = () => {
        setSearchKey('');
        setPage(0);
        setPerPage(10);
        setMemberList([]);
        setTotal(0);
        onClose();
    };

    const handleCloseAddDialog = () => {
        setShowAddDialog(false);
        setAddSearchKey('');
        setAddPage(0);
        setAddPerPage(10);
        setSelectedUsers([]);
        setAllUsers([]);
        setAddTotal(0);
    };

    return (
        <>
            {/* 角色成员列表对话框 */}
            <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
                <DialogTitle>
                    {t('role.roleMember')} - {roleName}
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
                                    startIcon={<PersonAddIcon />}
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
                                        <TableCell>{t('common.alias')}</TableCell>
                                        <TableCell>{t('common.email')}</TableCell>
                                        <TableCell>{t('common.actions')}</TableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {memberList.map((member) => (
                                        <TableRow key={member.id}>
                                            <TableCell>{member.name}</TableCell>
                                            <TableCell>{member.alias}</TableCell>
                                            <TableCell>{member.email}</TableCell>
                                            <TableCell>
                                                <IconButton
                                                    color="error"
                                                    onClick={() => handleDeleteMember(member)}
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

            {/* 添加成员对话框 */}
            <Dialog open={showAddDialog} onClose={handleCloseAddDialog} maxWidth="md" fullWidth>
                <DialogTitle>
                    {t('common.add')} {t('role.roleMember')}
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
                                                indeterminate={selectedUsers.length > 0 && selectedUsers.length < allUsers.length}
                                                checked={allUsers.length > 0 && selectedUsers.length === allUsers.length}
                                                onChange={(e) => handleSelectAll(e.target.checked)}
                                            />
                                        </TableCell>
                                        <TableCell>{t('common.name')}</TableCell>
                                        <TableCell>{t('common.alias')}</TableCell>
                                        <TableCell>{t('common.email')}</TableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {allUsers.map((user) => (
                                        <TableRow key={user.id}>
                                            <TableCell padding="checkbox">
                                                <Checkbox
                                                    checked={selectedUsers.includes(user.id)}
                                                    onChange={(e) => handleUserSelect(user.id, e.target.checked)}
                                                />
                                            </TableCell>
                                            <TableCell>{user.name}</TableCell>
                                            <TableCell>{user.alias}</TableCell>
                                            <TableCell>{user.email}</TableCell>
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

                    {selectedUsers.length > 0 && (
                        <Box sx={{ mt: 2 }}>
                            <Chip
                                label={`已选择 ${selectedUsers.length} 个用户`}
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
                    <Button onClick={handleAddMembers} color="primary" variant="contained">
                        {t('common.confirm')}
                    </Button>
                </DialogActions>
            </Dialog>

            {/* 删除确认对话框 */}
            <Dialog open={showDeleteDialog} onClose={handleCancelDelete} maxWidth="sm" fullWidth>
                <DialogTitle>
                    {t('role.deleteMemberConfirm')}
                </DialogTitle>
                <DialogContent>
                    <Box sx={{ pt: 2 }}>
                        {memberToDelete && (
                            <Box>
                                <p>{t('role.deleteMemberConfirmMsg')}</p>
                                <Box sx={{ mt: 2, p: 2, bgcolor: 'grey.100', borderRadius: 1 }}>
                                    <strong>{t('common.name')}:</strong> {memberToDelete.name}<br />
                                    <strong>{t('common.alias')}:</strong> {memberToDelete.alias}<br />
                                    <strong>{t('common.email')}:</strong> {memberToDelete.email}
                                </Box>
                            </Box>
                        )}
                    </Box>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleCancelDelete} color="primary">
                        {t('common.cancel')}
                    </Button>
                    <Button onClick={handleConfirmDeleteMember} color="error" variant="contained">
                        {t('common.confirm')}
                    </Button>
                </DialogActions>
            </Dialog>
        </>
    );
}

export default RoleMember;
