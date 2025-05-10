import React, { useState, useEffect, useCallback } from 'react';
import { ISimpleDept } from '../../../types/dept';
import { Tabs, Tab, Button, TableContainer, Table, TableHead, TableBody, TableRow, TableCell, Box, Modal, TextField, Paper, DialogTitle, DialogContent, DialogActions, FormControl, FormLabel, FormHelperText, CircularProgress, Dialog } from '@mui/material';
import { RichTreeView } from '@mui/x-tree-view';
import { TreeViewBaseItem } from '@mui/x-tree-view/models';
import { Add as AddIcon, Edit as EditIcon, Delete as DeleteIcon, ExpandMore as ExpandMoreIcon, ChevronRight as ChevronRightIcon } from '@mui/icons-material';
import { useSelector } from 'react-redux';
import { RootState } from '../../../store';
import { getDeptTree, getDeptDetail } from '../../../services/dept';
import useSnackbar from '../../../hooks/useSnackbar';
import DeptDialog from './DeptDialog';
import DeptParentDialog from './DeptParentDialog';
import { getUsers } from '../../../services/user';
import { IUser, ISimpleUserListRes } from '@/types/user';
import { IDept } from '@/types/dept';
import User from './User';
import { useTranslation } from 'react-i18next';
import { deleteDept } from '../../../services/dept';


interface Department {
    id: string;
    name: string;
    label: string;
    leader_info: basicUser;
    children?: Department[];
    has_children?: boolean;
}

interface basicUser {
    id: string;
    alias: string;
}
function Dept() {
    const [selectedDeptId, setSelectedDeptId] = useState<string>('00000000-0000-0000-0000-000000000000');
    const [selectedDeptName, setSelectedDeptName] = useState<string>('');
    const [expandedItems, setExpandedItems] = useState<string[]>(['00000000-0000-0000-0000-000000000000']);
    const [departments, setDepartments] = useState<Department[]>([]);
    const [deptList, setDeptList] = useState<IDept[]>([]);
    const [openDept, setOpenDept] = useState<boolean>(false);
    const [openParentDept, setOpenParentDept] = useState<boolean>(false);
    const [openedDeptId, setOpenedDeptId] = useState<string>('');
    const [openedParentDeptId, setOpenedParentDeptId] = useState<string>('');
    const [loading, setLoading] = useState<boolean>(false);
    const [deptloading, setDeptLoading] = useState<boolean>(false);
    const { showMessage } = useSnackbar();

    const { t } = useTranslation();

    const [openDeleteConfirm, setOpenDeleteConfirm] = useState<boolean>(false);
    const [deptToDelete, setDeptToDelete] = useState<string>('');

    const handleOpenDept = () => {
        setOpenDept(true);
    }

    const handleOpenDeptEdit = (deptId: string) => {
        setOpenedDeptId(deptId);
        setOpenDept(true);
    }
    const handleOpenParentDeptEdit = (deptId: string, parentDeptId: string) => {
        console.log('parent dept id: ', parentDeptId);
        setOpenedDeptId(deptId);
        setOpenedParentDeptId(parentDeptId);
        setOpenParentDept(true);
    }

    const handleConfirmDelete = (deptId: string) => {
        setDeptToDelete(deptId);
        setOpenDeleteConfirm(true);
    }

    const handleDeleteDept = async () => {
        try {
            await deleteDept(deptToDelete);
            setDeptList([]);
            setOpenDeleteConfirm(false);
            showMessage('部门删除成功', 'success');
        } catch (error: any) {
            showMessage(error.message || '删除部门失败', 'error');
            console.error('删除部门失败:', error);
        } finally {
            fetchDepartmentTree();
            fetchDeptDetail();
        }
    }

    const closeDialog = (needRefresh: boolean) => {
        setOpenDept(false);
        setOpenParentDept(false);
        setOpenedDeptId('');
        if (needRefresh) {
            fetchDepartmentTree();
            fetchDeptDetail();
        }
    }
    const renderTreeItem = (dept: Department): TreeViewBaseItem => {
        return {
            id: dept.id,
            label: dept.name,
            expandable: dept.has_children || false,
            children: dept.children?.map(child => renderTreeItem(child)) || []
        };
    };

    const handleItemSelectionChange = (_event: React.SyntheticEvent, itemId: string | null) => {
        if (!itemId) {
            setSelectedDeptId('00000000-0000-0000-0000-000000000000');
            setSelectedDeptName('无')
            return;
        }
        setSelectedDeptId(itemId);
        console.log('Selected department ID:', itemId);
    };

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

    const fetchDepartmentTree = async () => {
        try {
            setLoading(true);
            const response = await getDeptTree(true);
            if (response.code === 0) {
                const transformedData = transformDeptData(response.data.dept_list);
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
    const transformDeptData = (deptList: any[]): Department[] => {
        return deptList.map(dept => ({
            id: dept.id.toString(),
            name: dept.name,
            label: dept.name,
            leader_info: dept.leader_info,
            has_children: dept.has_children || false,
            children: dept.children ? transformDeptData(dept.children) : undefined
        }));
    };

    // 在组件加载时获取部门树数据
    useEffect(() => {
        fetchDepartmentTree();
    }, []);


    const fetchDeptDetail = useCallback(async () => {
        try {
            if (selectedDeptId === '00000000-0000-0000-0000-000000000000') {
                setDeptList([])
                setSelectedDeptName('无')
                return
            }
            setDeptLoading(true);
            const response = await getDeptDetail(selectedDeptId ?? '');
            if (response.code === 0) {
                setDeptList([response.data.dept_info])
                setSelectedDeptName(response.data.dept_info.name)
            }
            setDeptLoading(false);
        } catch (error: any) {
            showMessage(error.message || '获取用户列表失败', 'error');
            console.error('获取用户列表失败:', error);
        }
    }, [showMessage, selectedDeptId]);

    //get dept detail
    useEffect(() => {
        if (selectedDeptId) {
            fetchDeptDetail();
        }
    }, [fetchDeptDetail, selectedDeptId]);

    // 更新部门树中特定节点的子节点
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


    const handleNodeToggle = async (event: React.SyntheticEvent, nodeIds: string[]) => {
        // 找出新展开的节点ID
        const newExpandedIds = nodeIds.filter(id => !expandedItems.includes(id));

        // 对于每个新展开的节点，如果它有子节点标记但没有加载子节点，则加载其子节点
        for (const nodeId of newExpandedIds) {
            const dept = findDepartmentById(departments, nodeId);
            if (dept && dept.has_children && (!dept.children || dept.children.length === 0)) {
                try {
                    setLoading(true);
                    // 调用API获取子节点
                    const response = await getDeptTree(true);
                    if (response.code === 0) {
                        // 将获取到的子节点数据转换并添加到当前节点
                        const childrenData = transformDeptData(response.data.dept_list);
                        // 更新departments状态，将子节点添加到对应的父节点
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


    return (<div style={{ display: 'flex', marginTop: '20px' }}>
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
                    selectedItems={selectedDeptId}
                    multiSelect={false}
                />
            )}
        </div>
        <div style={{ flex: 1, paddingLeft: '20px' }}>
            <h3>{t('common.dept')}</h3>
            <Box display="flex" justifyContent="flex-end" sx={{ marginRight: '10px' }}>
                <Button variant="outlined" size={'large'} sx={{ width: '150px' }} onClick={handleOpenDept}>新增部门</Button>
            </Box>
            {deptloading ? (
                <Box display="flex" justifyContent="center" alignItems="center" height="200px">
                    <CircularProgress />
                </Box>
            ) : (
                <TableContainer component={Paper}>
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell>{t('common.name')}</TableCell>
                                <TableCell>{t('common.leader')}</TableCell>
                                <TableCell>{t('common.actions')}</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {deptList.map((dept: IDept) => (
                                <TableRow key={dept.id}>
                                    <TableCell>{dept.name}</TableCell>
                                    <TableCell>{dept.leader_info.alias}</TableCell>
                                    <TableCell>
                                        <Box sx={{ display: 'flex', gap: 1 }}>
                                            <Button size="small" startIcon={<EditIcon />} onClick={() => handleOpenDeptEdit(dept.id)}>编辑</Button>
                                            <Button size="small" startIcon={<EditIcon />} onClick={() => handleOpenParentDeptEdit(dept.id, dept.parent_dept_info?.id ?? '')}>修改父部门</Button>
                                            <Button size="small" startIcon={<DeleteIcon />} onClick={() => handleConfirmDelete(dept.id)} color="error">删除</Button>
                                        </Box>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>)}
        </div>
        <Dialog
            open={openDeleteConfirm}
            onClose={() => setOpenDeleteConfirm(false)}
            aria-labelledby="alert-dialog-title"
            aria-describedby="alert-dialog-description"
        >
            <DialogTitle id="alert-dialog-title">
                确认删除
            </DialogTitle>
            <DialogContent>
                确定要删除这个部门吗？此操作不可撤销。
            </DialogContent>
            <DialogActions>
                <Button onClick={() => setOpenDeleteConfirm(false)}>取消</Button>
                <Button onClick={handleDeleteDept} color="error" autoFocus>
                    确认删除
                </Button>
            </DialogActions>
        </Dialog>
        <DeptDialog open={openDept} deptId={openedDeptId} selectedDeptId={selectedDeptId} selectedDeptName={selectedDeptName} onClose={closeDialog} />
        <DeptParentDialog open={openParentDept} deptId={openedDeptId} parentDeptId={openedParentDeptId} onClose={closeDialog} />
    </div>)
}

export default Dept;