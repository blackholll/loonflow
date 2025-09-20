import React, { useCallback, useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { Box, Card, CardHeader, Dialog, DialogTitle, DialogContent, DialogActions, TextField, Button, Paper, Table, TableBody, TableRow, TableCell, TableContainer, TableHead, TablePagination, CircularProgress } from '@mui/material'
import GroupIcon from '@mui/icons-material/Group';
import Grid from '@mui/material/Grid2';
import useSnackbar from '../../../hooks/useSnackbar';
import { getRoleList, deleteRole } from '../../../services/role';
import { IRoleResEntity } from '@/types/role';
import RoleDialog from './RoleDialog';
import RoleMember from './RoleMember';
import { Edit as EditIcon, Delete as DeleteIcon } from '@mui/icons-material';




export function Role() {
    const { t } = useTranslation();
    const [roleDatas, setRoleDatas] = useState<IRoleResEntity[]>([]);
    const [roleLoading, setRoleLoading] = useState<boolean>(false);
    const [searchKey, setSearchKey] = useState<string>('');
    const [page, setPage] = useState<number>(0);
    const [perPage, setPerPage] = useState<number>(10);
    const [openedRoleId, setOpenedRoleId] = useState('');
    const [total, setTotal] = useState<number>(0);
    const [openRole, setOpenRole] = useState<boolean>(false);
    const [openDeleteConfirm, setOpenDeleteConfirm] = useState<boolean>(false);
    const [deleteRoleId, setDeleteRoleId] = useState('');
    const [openRoleMember, setOpenRoleMember] = useState<boolean>(false);
    const [selectedRoleId, setSelectedRoleId] = useState('');
    const [selectedRoleName, setSelectedRoleName] = useState('');
    const { showMessage } = useSnackbar();

    const fetchRoleList = useCallback(async () => {
        try {
            setRoleLoading(true);
            const res = await getRoleList(searchKey, page, perPage);
            setRoleDatas(res.data.roleList);
            setTotal(res.data.total)
        } catch (error: any) {
            showMessage(error.message, 'error');
        } finally {
            setRoleLoading(false);
        }
    }, [searchKey, page, perPage, showMessage]);

    useEffect(() => {
        fetchRoleList();
    }, [searchKey, page, perPage, fetchRoleList]);

    const handleConfirmDelete = async () => {
        try {
            await deleteRole(deleteRoleId);
            showMessage(t('common.deleteSuccess'), 'success');
            setOpenDeleteConfirm(false);
            setDeleteRoleId('');
        } catch (error: any) {
            showMessage(error.message, 'error');
        }
    };

    const closeDialog = () => {
        setOpenRole(false);
        setOpenedRoleId('');
    }
    const handleOpenRole = (RoleId: string) => {
        setOpenedRoleId(RoleId)
        setOpenRole(true);
    }
    const handleDeleteClick = (roleId: string) => {
        setOpenDeleteConfirm(true);
        setDeleteRoleId(roleId);
    }

    const handleRoleMemberClick = (roleId: string, roleName: string) => {
        setSelectedRoleId(roleId);
        setSelectedRoleName(roleName);
        setOpenRoleMember(true);
    }

    return (
        <Card>
            <CardHeader title={t('role.roleList')} />
            <Grid container spacing={4} justifyContent="left" alignItems="center" sx={{ 'marginLeft': '10px' }}>
                <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                    <TextField fullWidth label={t('common.searchWithKeyword')} onChange={(e) => setSearchKey(e.target.value)} />
                </Grid>
                <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                    <Button variant="outlined" size={'large'} sx={{ width: '150px' }} onClick={() => setOpenRole(true)}>{t('common.new')}</Button>
                </Grid>
            </Grid>

            <TableContainer component={Paper} sx={{ marginTop: '10px' }}>
                {roleLoading ? (<div><CircularProgress /></div>) : (
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell>{t('common.name')}</TableCell>
                                <TableCell>{t('common.description')}</TableCell>
                                <TableCell>{t('common.actions')}</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {roleDatas ? roleDatas.map((roleData) => (
                                <TableRow key={roleData.id}>
                                    <TableCell>{roleData.name}</TableCell>
                                    <TableCell>{roleData.description}</TableCell>
                                    <TableCell>
                                        <Box sx={{ display: 'flex', gap: 1 }}>
                                            <Button size="small" startIcon={<EditIcon />} onClick={() => handleOpenRole(roleData.id)}>{t('common.edit')}</Button>
                                            <Button size="small" startIcon={<GroupIcon />} color="warning" onClick={() => handleRoleMemberClick(roleData.id, roleData.name)}>{t('role.roleMember')}</Button>
                                            <Button size="small" startIcon={<DeleteIcon />} color="error" onClick={() => handleDeleteClick(roleData.id)}>{t('common.delete')}</Button>
                                        </Box>
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
                onPageChange={(_e, newPage) => { setPage(newPage) }}
                onRowsPerPageChange={(e) => {
                    setPage(0);
                    setPerPage(parseInt(e.target.value, 10))
                }}
            />
            <RoleDialog open={openRole} roleId={openedRoleId} onClose={() => closeDialog()} />
            <RoleMember
                open={openRoleMember}
                roleId={selectedRoleId}
                roleName={selectedRoleName}
                onClose={() => setOpenRoleMember(false)}
            />
            <Dialog open={openDeleteConfirm} onClose={() => setOpenDeleteConfirm(false)}>
                <DialogTitle>{t('common.confirm')}</DialogTitle>
                <DialogContent>
                    <p>{t('common.wantDeleteRecord')}</p>
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setOpenDeleteConfirm(false)} color="primary">
                        {t('common.cancel')}
                    </Button>
                    <Button onClick={() => handleConfirmDelete()} color="error">
                        {t('common.confirm')}
                    </Button>
                </DialogActions>

            </Dialog>
        </Card>
    )
}

export default Role;