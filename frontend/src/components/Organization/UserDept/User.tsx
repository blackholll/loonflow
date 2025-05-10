import React, { useState, useEffect, useCallback } from 'react';
import { Tabs, Tab, Button, TableContainer, Table, TableHead, TableBody, TableRow, TableCell, Box, Modal, TextField, Paper, DialogTitle, DialogContent, DialogActions, FormControl, FormLabel, FormHelperText, CircularProgress } from '@mui/material';
import { RichTreeView } from '@mui/x-tree-view';
import { TreeViewBaseItem } from '@mui/x-tree-view/models';
import { Add as AddIcon, Edit as EditIcon, Delete as DeleteIcon, ExpandMore as ExpandMoreIcon, ChevronRight as ChevronRightIcon } from '@mui/icons-material';
import { useSelector } from 'react-redux';
import { RootState } from '../../../store';
import { useTranslation } from 'react-i18next';
import { getDeptTree } from '../../../services/dept';
import useSnackbar from '../../../hooks/useSnackbar';
import DeptDialog from './DeptDialog';
import { getUsers } from '../../../services/user';
import { IUser, ISimpleUserListRes } from '@/types/user';


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


function User() {
    const [activeTab, setActiveTab] = useState('users');
    const [selectedDept, setSelectedDept] = useState<string>('00000000-0000-0000-0000-000000000000');
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [modalType, setModalType] = useState<'add' | 'edit' | 'delete'>('add');
    const [departmentName, setDepartmentName] = useState('');
    const [selectedItems, setSelectedItems] = useState<string | null>(null);
    const [expandedItems, setExpandedItems] = useState<string[]>(['00000000-0000-0000-0000-000000000000']);
    const [departments, setDepartments] = useState<Department[]>([]);
    const [userList, setUserList] = useState<IUser[]>([]);
    const [openDept, setOpenDept] = useState<boolean>(false);
    const [openedDeptId, setOpenedDeptId] = useState<string>('');
    const [loading, setLoading] = useState<boolean>(false);
    const tenant = useSelector((state: RootState) => state.tenant);
    const { showMessage } = useSnackbar();

    const { t } = useTranslation();


    const fetchDepartmentTree = async () => {
        try {
            setLoading(true);
            const response = await getDeptTree(true);
            if (response.code === 0) {
                // 将后端返回的部门树数据转换为组件需要的格式
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

    const fetchUsers = useCallback(async () => {
        try {

            const response = await getUsers('', selectedItems ?? '');
            if (response.code === 0) {
                setUserList(response.data.user_info_list)
            }
        } catch (error: any) {
            showMessage(error.message || '获取用户列表失败', 'error');
            console.error('获取用户列表失败:', error);
        }
    }, [showMessage, selectedItems]);

    useEffect(() => {
        fetchUsers();
    }, [selectedItems, fetchUsers]);


    // 将后端返回的部门树数据转换为组件需要的格式
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


    useEffect(() => {
        // get use info when selected department changed
        if (selectedDept) {
            // fetchDepartmentTree();
            console.log('Selected department ID:', selectedDept);
        }
    }, [selectedDept]);



    const handleDeptAdd = () => {
        setOpenDept(true);
        setOpenedDeptId('');
    };

    const handleDepartmentAction = (type: 'add' | 'edit' | 'delete') => {
        setModalType(type);
        setIsModalVisible(true);
    };

    const handleModalOk = () => {
        // 处理表单提交
        setIsModalVisible(false);
        setDepartmentName('');
    };

    const handleModalClose = () => {
        setIsModalVisible(false);
        setDepartmentName('');
    };

    const handleItemSelectionChange = (event: React.SyntheticEvent, itemId: string | null) => {
        setSelectedItems(itemId);
        if (itemId) {
            // 更新选中的部门
            setSelectedDept(itemId);
            // 这里可以根据选中的部门ID加载相应的用户列表
            console.log('Selected department ID:', itemId);
        }
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

    // 递归渲染树形结构项，支持任意层级
    const renderTreeItem = (dept: Department): TreeViewBaseItem => {
        return {
            id: dept.id,
            label: dept.name,
            expandable: dept.has_children || false,
            children: dept.children?.map(child => renderTreeItem(child)) || []
        };
    };


    const departmentColumns = [
        { field: 'name', headerName: '部门名称', flex: 1 },
        {
            field: 'actions',
            headerName: '操作',
            flex: 1,
            renderCell: (params: any) => (
                <Box sx={{ display: 'flex', gap: 1 }}>
                    <Button
                        size="small"
                        startIcon={<EditIcon />}
                        onClick={() => handleDepartmentAction('edit')}
                    >
                        编辑
                    </Button>
                    <Button
                        size="small"
                        startIcon={<DeleteIcon />}
                        color="error"
                        onClick={() => handleDepartmentAction('delete')}
                    >
                        删除
                    </Button>
                </Box>
            ),
        },
    ];

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
                <h3>{t('common.users')}</h3>
                <TableContainer component={Paper}>
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell>{t('common.name')}</TableCell>
                                <TableCell>{t('common.email')}</TableCell>
                                <TableCell>{t('common.department')}</TableCell>
                                <TableCell>{t('common.actions')}</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {userList.map((user: IUser) => (
                                <TableRow key={user.id}>
                                    <TableCell>{user.name}</TableCell>
                                    <TableCell>{user.email}</TableCell>
                                    <TableCell>{user.dept_info_list.map(dept => dept.name).join(',')}</TableCell>
                                    <TableCell>
                                        <Box sx={{ display: 'flex', gap: 1 }}>
                                            <Button size="small" startIcon={<EditIcon />}>编辑</Button>
                                            <Button size="small" startIcon={<DeleteIcon />} color="error">删除</Button>
                                        </Box>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
            </div>
        </div>
    );
}

export default User;