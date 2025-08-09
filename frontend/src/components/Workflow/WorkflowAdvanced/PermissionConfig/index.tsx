import React, { useState, useEffect } from 'react';
import { Autocomplete, CircularProgress, Box, Paper, Typography, Button, TextField, FormControl, FormLabel, RadioGroup, FormControlLabel, Radio, Icon, Tooltip, InputAdornment, Stack, Chip, Grid2 } from '@mui/material';
import Grid from '@mui/material/Grid2';
import { getSimpleUsers } from '../../../../services/user';
import { getDeptPaths } from '../../../../services/dept';
import { ISimpleUser } from '../../../../types/user';
import { ISimpleDeptPath } from '../../../../types/dept';
import { IpermissionInfo } from '../../../../types/workflow';

interface PermissionConfigProps {
    onPermissionConfigChange: (permissionConfig: IpermissionInfo) => void;
    permissionConfig: IpermissionInfo;
}

interface IOption {
    label: string;
    value: string;
}

function PermissionConfig({ onPermissionConfigChange, permissionConfig }: PermissionConfigProps) {
    const [permissionConfigInfo, setPermissionConfigInfo] = useState(permissionConfig);
    const [loadingAdminUsers, setLoadingAdminUsers] = React.useState(false);
    const [loadingDispatcherUsers, setLoadingDispatcherUsers] = React.useState(false);
    const [loadingViewerUsers, setLoadingViewerUsers] = React.useState(false);
    const [loadingViewerDepts, setLoadingViewerDepts] = React.useState(false);
    const [selectedAdmins, setSelectedAdmins] = useState<{ label: string, value: string }[]>([]);
    const [selectedDispatchers, setSelectedDispatchers] = useState<{ label: string, value: string }[]>([]);
    const [selectedViewers, setSelectedViewers] = useState<{ label: string, value: string }[]>([]);
    const [selectedViewerDepts, setSelectedViewerDepts] = useState<{ label: string, value: string }[]>([]);


    // 为不同的权限配置创建独立的状态变量
    const [adminUsers, setAdminUsers] = React.useState<IOption[]>([]);
    const [dispatcherUsers, setDispatcherUsers] = React.useState<IOption[]>([]);
    const [viewerUsers, setViewerUsers] = React.useState<IOption[]>([]);
    const [viewerDepts, setViewerDepts] = React.useState<IOption[]>([]);

    const handleAdminSelectChange = (value: { label: string, value: string }[]) => {
        const newPermissionConfig = { ...permissionConfigInfo, adminIdList: value.map((v: any) => v.value) };
        setPermissionConfigInfo(newPermissionConfig);
        onPermissionConfigChange(newPermissionConfig);
        setSelectedAdmins(value);
    }

    const handleDispatcherSelectChange = (value: { label: string, value: string }[]) => {
        const newPermissionConfig = { ...permissionConfigInfo, dispatcherIdList: value.map((v: any) => v.value) };
        setPermissionConfigInfo(newPermissionConfig);
        onPermissionConfigChange(newPermissionConfig);
        setSelectedDispatchers(value);
    }

    const handleViewerSelectChange = (value: { label: string, value: string }[]) => {
        const newPermissionConfig = { ...permissionConfigInfo, viewerIdList: value.map((v: any) => v.value) };
        setPermissionConfigInfo(newPermissionConfig);
        onPermissionConfigChange(newPermissionConfig);
        setSelectedViewers(value);
    }

    const handleViewerDeptSelectChange = (value: { label: string, value: string }[]) => {
        const newPermissionConfig = { ...permissionConfigInfo, viewDepartmentIdList: value.map((v: any) => v.value) };
        setPermissionConfigInfo(newPermissionConfig);
        onPermissionConfigChange(newPermissionConfig);
        setSelectedViewerDepts(value);
    }

    const loadAdminUsers = async (searchValue: string = '') => {
        if (loadingAdminUsers) return;
        setLoadingAdminUsers(true);
        try {
            const response = await getSimpleUsers(searchValue);
            if (response.code === 0) {
                setAdminUsers(response.data.userInfoList.map((user: ISimpleUser) => ({ label: `${user.name}(${user.alias})`, value: user.id })) || []);
            }
        } catch (error) {
            console.error('加载用户列表失败:', error);
        } finally {
            setLoadingAdminUsers(false);
        }
    };
    const loadDispatcherUsers = async (searchValue: string = '') => {
        if (loadingDispatcherUsers) return;
        setLoadingDispatcherUsers(true);
        try {
            const response = await getSimpleUsers(searchValue);
            if (response.code === 0) {
                setDispatcherUsers(response.data.userInfoList.map((user: ISimpleUser) => ({ label: `${user.name}(${user.alias})`, value: user.id })) || []);
            }
        } catch (error) {
            console.error('加载用户列表失败:', error);
        } finally {
            setLoadingDispatcherUsers(false);
        }
    }
    const loadViewerUsers = async (searchValue: string = '') => {
        if (loadingViewerUsers) return;
        setLoadingViewerUsers(true);
        try {
            const response = await getSimpleUsers(searchValue);
            if (response.code === 0) {
                setViewerUsers(response.data.userInfoList.map((user: ISimpleUser) => ({ label: `${user.name}(${user.alias})`, value: user.id })) || []);
            }
        } catch (error) {
            console.error('加载用户列表失败:', error);
        } finally {
            setLoadingViewerUsers(false);
        }
    }

    const loadViewerDepts = async (searchValue: string = '') => {
        if (loadingViewerDepts) return;
        setLoadingViewerDepts(true);
        try {
            const response = await getDeptPaths(searchValue, '', 1, 10);
            if (response.code === 0) {
                setViewerDepts(response.data.deptPathList.map((dept: ISimpleDeptPath) => ({ label: dept.name, value: dept.id })) || []);
            }
        } catch (error) {
            console.error('加载部门列表失败:', error);
        } finally {
            setLoadingViewerDepts(false);
        }
    }

    const fetchSimpleUsers = async (searchValue: string = '', userIds: string = '', page = 1, perPage: 1000) => {
        const response = await getSimpleUsers(searchValue, userIds, page, perPage);
        if (response.code === 0) {
            return response.data.userInfoList.map((user: ISimpleUser) => ({ label: `${user.name}(${user.alias})`, value: user.id })) || [];
        }
        return []
    }
    const fetchDeptPaths = async (searchValue: string = '', deptIds: string = '', page = 1, perPage: 1000) => {
        const response = await getDeptPaths(searchValue, deptIds, page, perPage);
        if (response.code === 0) {
            return response.data.deptPathList.map((dept: ISimpleDeptPath) => ({ label: dept.name, value: dept.id })) || [];
        }
        return []
    }

    useEffect(() => {
        if (permissionConfigInfo.adminIdList.length > 0) {
            fetchSimpleUsers('', permissionConfig.adminIdList.join(','), 1, 1000).then(data => setSelectedAdmins(data));
        }
        if (permissionConfigInfo.dispatcherIdList.length > 0) {
            fetchSimpleUsers('', permissionConfig.dispatcherIdList.join(','), 1, 1000).then(data => setSelectedDispatchers(data));
        }
        if (permissionConfigInfo.viewerIdList.length > 0) {
            fetchSimpleUsers('', permissionConfig.viewerIdList.join(','), 1, 1000).then(data => setSelectedViewers(data));
        }
        if (permissionConfigInfo.viewerDeptIdList.length > 0) {
            fetchDeptPaths('', permissionConfig.viewerDeptIdList.join(','), 1, 1000).then(data => setSelectedViewerDepts(data));
        }
    }, [permissionConfigInfo]);

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
                            options={adminUsers}
                            getOptionLabel={(option) => option.label}
                            value={selectedAdmins}
                            onChange={(e, value) => handleAdminSelectChange(value)}
                            onInputChange={(e, value) => {
                                if (value.length > 0) {
                                    loadAdminUsers(value);
                                }
                            }}
                            renderInput={(params) => (
                                <TextField
                                    {...params}
                                    label="选择管理员"
                                    placeholder="输入关键词后搜索用户..."
                                    InputProps={{
                                        ...params.InputProps,
                                        endAdornment: (
                                            <>
                                                {loadingAdminUsers ? <CircularProgress color="inherit" size={20} /> : null}
                                                {params.InputProps.endAdornment}
                                            </>
                                        ),
                                    }}
                                />
                            )}
                            loading={loadingAdminUsers}
                            size="small"
                            fullWidth
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
                            options={dispatcherUsers}
                            getOptionLabel={(option) => option.label}
                            value={selectedDispatchers}
                            onChange={(e, value) => handleDispatcherSelectChange(value)}
                            onInputChange={(e, value) => {
                                if (value.length > 0) {
                                    loadDispatcherUsers(value);
                                }
                            }}
                            renderInput={(params) => (
                                <TextField
                                    {...params}
                                    label="选择调度员"
                                    placeholder="输入关键词后搜索用户..."
                                    InputProps={{
                                        ...params.InputProps,
                                        endAdornment: (
                                            <>
                                                {loadingAdminUsers ? <CircularProgress color="inherit" size={20} /> : null}
                                                {params.InputProps.endAdornment}
                                            </>
                                        ),
                                    }}
                                />
                            )}
                            loading={loadingAdminUsers}
                            size="small"
                            fullWidth
                        />
                    </Grid>
                </Grid>
                <Grid container alignItems="flex-start" spacing={2}>
                    <Grid size={3} sx={{ minWidth: 100, pt: 1 }}>
                        <FormLabel>查看者</FormLabel>
                    </Grid>
                    <Grid size={9}>
                        <Autocomplete
                            multiple
                            options={viewerUsers}
                            getOptionLabel={(option) => option.label}
                            value={selectedViewers}
                            onChange={(e, value) => handleViewerSelectChange(value)}
                            onInputChange={(e, value) => {
                                if (value.length > 0) {
                                    loadViewerUsers(value);
                                }
                            }}
                            renderInput={(params) => (
                                <TextField
                                    {...params}
                                    label="选择处理人"
                                    placeholder="输入关键词后搜索用户..."
                                    InputProps={{
                                        ...params.InputProps,
                                        endAdornment: (
                                            <>
                                                {loadingAdminUsers ? <CircularProgress color="inherit" size={20} /> : null}
                                                {params.InputProps.endAdornment}
                                            </>
                                        ),
                                    }}
                                />
                            )}
                            loading={loadingAdminUsers}
                            size="small"
                            fullWidth
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
                            options={viewerDepts}
                            getOptionLabel={(option) => option.label}
                            value={selectedViewerDepts}
                            onChange={(e, value) => handleViewerDeptSelectChange(value)}
                            onInputChange={(e, value) => {
                                if (value.length > 0) {
                                    loadViewerDepts(value);
                                }
                            }}
                            renderInput={(params) => (
                                <TextField
                                    {...params}
                                    label="选择查看部门"
                                    placeholder="输入关键词后搜索用户..."
                                    InputProps={{
                                        ...params.InputProps,
                                        endAdornment: (
                                            <>
                                                {loadingViewerDepts ? <CircularProgress color="inherit" size={20} /> : null}
                                                {params.InputProps.endAdornment}
                                            </>
                                        ),
                                    }}
                                />
                            )}
                            loading={loadingAdminUsers}
                            size="small"
                            fullWidth
                        />
                    </Grid>
                </Grid>
            </Stack>
        </Box>
    );
}

export default PermissionConfig;