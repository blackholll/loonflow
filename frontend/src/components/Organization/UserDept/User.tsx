import { IUser } from '@/types/user';
import { Add as AddIcon, Delete as DeleteIcon, Edit as EditIcon } from '@mui/icons-material';
import LockResetIcon from '@mui/icons-material/LockReset';
import { Box, Button, Card, CardHeader, Chip, CircularProgress, Dialog, DialogActions, DialogContent, DialogTitle, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TablePagination, TableRow, TextField, Typography } from '@mui/material';
import Grid from '@mui/material/Grid2';
import { RichTreeView } from '@mui/x-tree-view';
import { TreeViewBaseItem } from '@mui/x-tree-view/models';
import React, { useCallback, useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import useSnackbar from '../../../hooks/useSnackbar';
import { getDeptTree } from '../../../services/dept';
import { deleteUser, getUsers, resetUserPassword } from '../../../services/user';
import UserDialog from './UserDialog';


interface Department {
    id: string;
    name: string;
    label: string;
    leaderInfo: basicUser;
    children?: Department[];
    hasChildren?: boolean;
}

interface basicUser {
    id: string;
    alias: string;
}


function User() {
    const [selectedDept, setSelectedDept] = useState<string>('00000000-0000-0000-0000-000000000000');
    const [page, setPage] = useState(1);
    const [perPage, setPerPage] = useState(10);
    const [selectedItems, setSelectedItems] = useState<string | null>(null);
    const [expandedItems, setExpandedItems] = useState<string[]>(['00000000-0000-0000-0000-000000000000']);
    const [departments, setDepartments] = useState<Department[]>([]);
    const [userList, setUserList] = useState<IUser[]>([]);
    const [loading, setLoading] = useState<boolean>(false);
    const [total, setTotal] = useState(0);
    const { showMessage } = useSnackbar();

    const { t } = useTranslation();

    const [openUserDialog, setOpenUserDialog] = useState<boolean>(false);
    const [editingUserId, setEditingUserId] = useState<string | null>(null);
    const [openDeleteConfirm, setOpenDeleteConfirm] = useState(false);
    const [userToDelete, setUserToDelete] = useState<IUser | null>(null);
    const [userToResetPassword, setUserToResetPassword] = useState<IUser | null>(null);

    const [openResetPasswordConfirm, setOpenResetPasswordConfirm] = useState(false);


    const handleChangePage = (_event: any, newPage: number) => {
        setPage(newPage + 1);
    };

    const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
        setPerPage(parseInt(event.target.value, 10));
        setPage(1);
    };

    const fetchDepartmentTree = async () => {
        try {
            setLoading(true);
            const response = await getDeptTree(true);
            if (response.code === 0) {
                const transformedData = transformDeptData(response.data.deptList);
                setDepartments(transformedData);
            } else {
                showMessage(response.msg || '获取部门树失败', 'error');
            }
        } catch (error: any) {
            showMessage(error.message || '获取部门树失败', 'error');
            console.error('获取部门树失败:', error);
        } finally {
            setLoading(false);
        }
    };

    const fetchUsers = useCallback(async () => {
        try {
            setLoading(true);
            const response = await getUsers('', selectedItems ?? '', page, perPage);
            if (response.code === 0) {
                setUserList(response.data.userInfoList);
                setTotal(response.data.total);
            } else {
                showMessage(response.msg || '获取用户列表失败', 'error');
            }
        } catch (error: any) {
            showMessage(error.message || '获取用户列表失败', 'error');
            console.error('获取用户列表失败:', error);
        } finally {
            setLoading(false);
        }
    }, [showMessage, selectedItems, page, perPage]);

    useEffect(() => {
        fetchUsers();
    }, [selectedItems, fetchUsers]);


    const transformDeptData = (deptList: any[]): Department[] => {
        return deptList.map(dept => ({
            id: dept.id.toString(),
            name: dept.name,
            label: dept.name,
            leaderInfo: dept.leaderInfo,
            hasChildren: dept.hasChildren || false,
            children: dept.children ? transformDeptData(dept.children) : undefined
        }));
    };

    useEffect(() => {
        fetchDepartmentTree();
    }, [fetchDepartmentTree]);


    useEffect(() => {
        // get use info when selected department changed
        if (selectedDept) {
            // fetchDepartmentTree();
            console.log('Selected department ID:', selectedDept);
        }
    }, [selectedDept]);



    const handleOpenAddUserDialog = () => {
        setEditingUserId(null);
        setOpenUserDialog(true);
    };

    const handleOpenEditUserDialog = (userId: string) => {
        setEditingUserId(userId);
        setOpenUserDialog(true);
    };

    const handleCloseUserDialog = (refresh?: boolean) => {
        setOpenUserDialog(false);
        setEditingUserId(null);
        if (refresh) {
            fetchUsers();
        }
    };

    const handleDeleteUserClick = (user: IUser) => {
        setUserToDelete(user);
        setOpenDeleteConfirm(true);
    };
    const handleResetPasswordClick = (user: IUser) => {
        setUserToResetPassword(user);
        setOpenResetPasswordConfirm(true);
    };

    const handleConfirmRestPassword = async () => {
        if (!userToResetPassword) return;
        try {
            const result = await resetUserPassword(userToResetPassword.id);
            if (result.code === 0) {
                showMessage(t('user.resetPasswordSuccess'), 'success');
            }
        } catch (error: any) {
            console.error(t('resetPasswordSuccess'), error);
        } finally {
            setOpenResetPasswordConfirm(false);
            setUserToResetPassword(null);
        }
    }
    const handleConfirmDeleteUser = async () => {
        if (!userToDelete) return;
        try {
            const result = await deleteUser(userToDelete.id); // 假设的 deleteUser API
            if (result.code === 0) {
                showMessage(t('user.deleteUserSuccess'), 'success');
                fetchUsers();
            } else {
                showMessage(t('user.deleteUserSuccess'), 'error');
            }
        } catch (error: any) {
            showMessage(t('user.deleteUserSuccess'), 'error');
        } finally {
            setOpenDeleteConfirm(false);
            setUserToDelete(null);
        }
    };

    const handleItemSelectionChange = (_: React.SyntheticEvent, itemId: string | null) => {
        setSelectedItems(itemId);
        if (itemId) {
            setSelectedDept(itemId);
        }
    };

    const handleNodeToggle = async (_: React.SyntheticEvent, nodeIds: string[]) => {
        const newExpandedIds = nodeIds.filter(id => !expandedItems.includes(id));

        for (const nodeId of newExpandedIds) {
            const dept = findDepartmentById(departments, nodeId);
            if (dept && dept.hasChildren && (!dept.children || dept.children.length === 0)) {
                try {
                    setLoading(true);
                    const response = await getDeptTree(true);
                    if (response.code === 0) {
                        const childrenData = transformDeptData(response.data.deptList);
                        setDepartments(prevDepts => updateDepartmentChildren(prevDepts, nodeId, childrenData));
                    } else {
                        showMessage(response.msg || '获取部门子节点失败', 'error');
                    }
                } catch (error: any) {
                    showMessage(error.message || '获取部门子节点失败', 'error');
                    console.error('获取部门子节点失败:', error);
                } finally {
                    setLoading(false);
                }
            }
        }

        setExpandedItems(nodeIds);
    };

    // 根据ID查找部门节点
    const findDepartmentById = (depts: Department[], id: string): Department | undefined => {
        for (const dept of depts) {
            if (dept.id === id) {
                return dept;
            }
            if (dept.children && dept.children.length > 0) {
                const found = findDepartmentById(dept.children, id);
                if (found) {
                    return found;
                }
            }
        }
        return undefined;
    };

    const handleChangeKeyword = async (event: React.ChangeEvent<HTMLInputElement>) => {
        const keyword = event.target.value;
        try {
            const response = await getUsers(keyword, selectedItems ?? '', page, perPage);
            if (response.code === 0) {
                setUserList(response.data.userInfoList);
                setTotal(response.data.total);
            }
        } catch (error: any) {
            showMessage(error.message || '获取用户列表失败', 'error');
        }
    };

    const updateDepartmentChildren = (depts: Department[], parentId: string, children: Department[]): Department[] => {
        return depts.map(dept => {
            if (dept.id === parentId) {
                return { ...dept, children };
            }
            if (dept.children && dept.children.length > 0) {
                return { ...dept, children: updateDepartmentChildren(dept.children, parentId, children) };
            }
            return dept;
        });
    };

    const renderTreeItem = (dept: Department): TreeViewBaseItem => {
        return {
            id: dept.id,
            label: dept.name,
            children: dept.children?.map(child => renderTreeItem(child)) || []
        };
    };

    return (
        <div style={{ display: 'flex', marginTop: '20px' }}>
            <div style={{ width: '300px', borderRight: '1px solid #eee', paddingRight: '20px' }}>
                {loading ? (
                    <Box display="flex" justifyContent="center" alignItems="center" height="200px">
                        <CircularProgress />
                    </Box>
                ) : (
                    <RichTreeView
                        items={departments.map(dept => renderTreeItem(dept))}
                        onSelectedItemsChange={handleItemSelectionChange}
                        onExpandedItemsChange={handleNodeToggle}
                        expandedItems={expandedItems}
                        selectedItems={selectedDept}
                        multiSelect={false}
                    />
                )}
            </div>
            <div style={{ flex: 1, paddingLeft: '20px' }}>
                <Card>
                    <CardHeader title={t('common.users')} />
                    <Grid container spacing={2} sx={{ mb: 2, paddingLeft: 2, paddingRight: 2, alignItems: 'center' }}>
                        <Grid size={{ xs: 4, sm: 6, md: 3 }}>
                            <TextField size="small" fullWidth label={t('common.searchWithKeyword')} onChange={handleChangeKeyword} />
                        </Grid>
                        <Grid size={{ xs: 8, sm: 6, md: 9 }} sx={{ display: 'flex', justifyContent: 'flex-end' }}>
                            <Button variant="outlined" onClick={handleOpenAddUserDialog} startIcon={<AddIcon />}>{t('common.new')}</Button>
                        </Grid>
                    </Grid> {/* 确保 Grid container 包裹了 TableContainer */}

                    <TableContainer component={Paper}>
                        {loading && ( // 根据列表加载状态显示
                            <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 200 }}>
                                <CircularProgress />
                            </Box>
                        )}
                        {!loading && userList.length === 0 && (
                            <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 100 }}>
                                <Typography>{t('common.noData')}</Typography>
                            </Box>
                        )}
                        {!loading && userList.length > 0 && (
                            <Table>
                                <TableHead>
                                    <TableRow>
                                        <TableCell>{t('common.name')}</TableCell>
                                        <TableCell>{t('common.email')}</TableCell>
                                        <TableCell>{t('common.dept')}</TableCell>
                                        <TableCell>{t('common.type')}</TableCell>
                                        <TableCell>{t('common.status')}</TableCell>
                                        <TableCell>{t('common.actions')}</TableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {userList.map((user: IUser) => (
                                        <TableRow key={user.id}>
                                            <TableCell>{user.name}</TableCell>
                                            <TableCell>{user.email}</TableCell>
                                            <TableCell>{user.deptInfoList?.map(dept => dept.name).join(', ') || '-'}</TableCell>
                                            <TableCell>{t(`common.${user.type}`)}</TableCell>
                                            <TableCell>
                                                {user.isActive ? (
                                                    <Chip
                                                        label="active"
                                                        color="success"
                                                        size="small"
                                                    />
                                                ) : (
                                                    <Chip
                                                        label="inactive"
                                                        color="error"
                                                        size="small"
                                                    />
                                                )}
                                            </TableCell>
                                            <TableCell>
                                                <Box sx={{ display: 'flex', gap: 1 }}>
                                                    <Button size="small" startIcon={<EditIcon />} onClick={() => handleOpenEditUserDialog(user.id)}>{t('common.edit')}</Button>
                                                    <Button size="small" startIcon={<LockResetIcon />} color="warning" onClick={() => handleResetPasswordClick(user)}>{t('user.resetPassword')}</Button>
                                                    <Button size="small" startIcon={<DeleteIcon />} color="error" onClick={() => handleDeleteUserClick(user)}>{t('common.delete')}</Button>
                                                </Box>
                                            </TableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        )}
                    </TableContainer>
                    <TablePagination
                        rowsPerPageOptions={[10, 25, 100]}
                        component="div"
                        count={total}
                        rowsPerPage={perPage}
                        page={page - 1}
                        onPageChange={handleChangePage}
                        onRowsPerPageChange={handleChangeRowsPerPage}
                    />
                </Card>

            </div>
            <UserDialog
                open={openUserDialog}
                onClose={handleCloseUserDialog}
                userId={editingUserId}
                selectedDeptId={selectedItems}
            />
            <Dialog open={openDeleteConfirm} onClose={() => setOpenDeleteConfirm(false)}>
                <DialogTitle>{t('common.confirmDeletion')}</DialogTitle>
                <DialogContent>
                    <Typography>
                        {t('common.confirmDeleteMsg', { userName: userToDelete?.name || '' })}
                    </Typography>
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setOpenDeleteConfirm(false)}>{t('common.cancel')}</Button>
                    <Button onClick={handleConfirmDeleteUser} color="error" autoFocus>
                        {t('common.delete')}
                    </Button>
                </DialogActions>
            </Dialog>
            <Dialog open={openResetPasswordConfirm} onClose={() => setOpenResetPasswordConfirm(false)}>
                <DialogTitle>{t('user.confirmResetPassword')}</DialogTitle>
                <DialogContent>
                    <Typography>
                        {t('user.confirmResetPasswordMsg')}
                    </Typography>
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setOpenResetPasswordConfirm(false)}>{t('common.cancel')}</Button>
                    <Button onClick={handleConfirmRestPassword} color="error" autoFocus>
                        {t('user.resetPassword')}
                    </Button>
                </DialogActions>
            </Dialog>

        </div>
    );
}

export default User;

