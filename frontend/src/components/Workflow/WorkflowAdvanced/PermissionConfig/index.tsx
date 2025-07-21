import React from 'react';
import { Autocomplete, Box, Paper, Typography, Button, TextField, FormControl, FormLabel, RadioGroup, FormControlLabel, Radio, Icon, Tooltip, InputAdornment, Stack, Chip, Grid2 } from '@mui/material';
import Grid from '@mui/material/Grid2';
import { getSimpleUser } from '../../../../services/user';
import { getDeptPaths } from '../../../../services/dept';

// 定义用户和部门的类型
interface User {
    id: number;
    name: string;
}

interface Department {
    id: number;
    name: string;
    path: string;
}

function PermissionConfig() {
    const [userList, setUserList] = React.useState<User[]>([]);
    const [deptList, setDeptList] = React.useState<Department[]>([]);

    // 为不同的权限配置创建独立的状态变量
    const [adminUsers, setAdminUsers] = React.useState<User[]>([]);
    const [dispatcherUsers, setDispatcherUsers] = React.useState<User[]>([]);
    const [viewerUsers, setViewerUsers] = React.useState<User[]>([]);
    const [viewerDepts, setViewerDepts] = React.useState<Department[]>([]);

    // 加载用户列表
    React.useEffect(() => {
        const loadUsers = async () => {
            try {
                const response = await getSimpleUser('');
                // API 返回的数据结构是 { code: 0, msg: "", data: { user_list: [...] } }
                const users = response?.data?.userList || [];
                setUserList(users);
            } catch (error) {
                console.error('加载用户列表失败:', error);
                setUserList([]);
            }
        };
        loadUsers();
    }, []);

    // 加载部门列表
    React.useEffect(() => {
        const loadDepts = async () => {
            try {
                const response = await getDeptPaths('');
                // API 返回的数据结构可能是 { code: 0, msg: "", data: [...] }
                if (response.code === 0) {
                    setDeptList(response.data.deptPathList);
                }
            } catch (error) {
                console.error('加载部门列表失败:', error);
                setDeptList([]);
            }
        };
        loadDepts();
    }, []);

    return (
        <Box>
            <Stack spacing={3}>
                <Grid container alignItems="flex-start" spacing={2}>
                    <Grid size={3} sx={{ minWidth: 100, pt: 1 }}>
                        <FormLabel>管理员</FormLabel>
                    </Grid>
                    <Grid size={9}>
                        <Autocomplete
                            multiple
                            disablePortal
                            options={userList || []}
                            value={adminUsers}
                            onChange={(event, newValue) => {
                                setAdminUsers(newValue);
                            }}
                            getOptionLabel={(option) => option.name || ''}
                            isOptionEqualToValue={(option, value) => option.id === value.id}
                            sx={{ width: 300 }}
                            renderInput={(params) => <TextField {...params} label="选择管理员" />}
                        />
                    </Grid>
                </Grid>
                <Grid container alignItems="flex-start" spacing={2}>
                    <Grid size={3} sx={{ minWidth: 100, pt: 1 }}>
                        <FormLabel>调度员</FormLabel>
                    </Grid>
                    <Grid size={9}>
                        <Autocomplete
                            multiple
                            disablePortal
                            options={userList || []}
                            value={dispatcherUsers}
                            onChange={(event, newValue) => {
                                setDispatcherUsers(newValue);
                            }}
                            getOptionLabel={(option) => option.name || ''}
                            isOptionEqualToValue={(option, value) => option.id === value.id}
                            sx={{ width: 300 }}
                            renderInput={(params) => <TextField {...params} label="选择调度员" />}
                        />
                    </Grid>
                </Grid>
                <Grid container alignItems="flex-start" spacing={2}>
                    <Grid size={3} sx={{ minWidth: 100, pt: 1 }}>
                        <FormLabel>查看人</FormLabel>
                    </Grid>
                    <Grid size={9}>
                        <Autocomplete
                            multiple
                            disablePortal
                            options={userList || []}
                            value={viewerUsers}
                            onChange={(event, newValue) => {
                                setViewerUsers(newValue);
                            }}
                            getOptionLabel={(option) => option.name || ''}
                            isOptionEqualToValue={(option, value) => option.id === value.id}
                            sx={{ width: 300 }}
                            renderInput={(params) => <TextField {...params} label="选择查看人" />}
                        />
                    </Grid>
                </Grid>
                <Grid container alignItems="flex-start" spacing={2}>
                    <Grid size={3} sx={{ minWidth: 100, pt: 1 }}>
                        <FormLabel>查看部门</FormLabel>
                    </Grid>
                    <Grid size={9}>
                        <Autocomplete
                            multiple
                            disablePortal
                            options={deptList || []}
                            value={viewerDepts}
                            onChange={(event, newValue) => {
                                setViewerDepts(newValue);
                            }}
                            getOptionLabel={(option) => option.path || ''}
                            isOptionEqualToValue={(option, value) => option.id === value.id}
                            sx={{ width: 300 }}
                            renderInput={(params) => <TextField {...params} label="选择查看部门" />}
                        />
                    </Grid>
                </Grid>
            </Stack>
        </Box>
    );
}

export default PermissionConfig;