import React, { useEffect, useState } from 'react';
import { Alert, CircularProgress, OutlinedInput, MenuItem, Dialog, DialogTitle, DialogContent, DialogActions, Box, Stack, Grid2, FormLabel, Autocomplete, TextField, Chip, Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@mui/material';
import Grid from '@mui/material/Grid2';
import { getSimpletApplicationList } from '../../../../services/application'
import { ISimpleApplicationResEntity } from '../../../../types/application';
import { v4 as uuidv4 } from 'uuid';
import { ICustomizationInfo, IWorkflowHook } from '../../../../types/workflow';
import useSnackbar from '../../../../hooks/useSnackbar';


interface IHookEvent {
    key: string;
    label: string;
}
interface CustomizeConfigProps {
    onCustomizeConfigChange: (customizationInfo: ICustomizationInfo) => void;
    customizeConfig: ICustomizationInfo;
}

function CustomizeConfig({ onCustomizeConfigChange, customizeConfig }: CustomizeConfigProps) {
    const [customizationInfo, setCustomizationInfo] = useState<ICustomizationInfo>(customizeConfig);
    const [applicationList, setApplicationList] = useState<ISimpleApplicationResEntity[]>([]);
    const [loadingApps, setLoadingApps] = useState(false);
    const [selectedApplications, setSelectedApplications] = useState<ISimpleApplicationResEntity[]>([]);
    const [label, setLabel] = useState({});
    const [labelJson, setLabelJson] = useState(JSON.stringify(label, null, 2));
    const [error, setError] = useState('');
    const [open, setOpen] = useState(false);
    const [selectedHookEvent, setSelectedHookEvent] = useState<IHookEvent[]>([]);
    const [addedHookToken, setAddedHookToken] = useState('');
    const [hooks, setHooks] = useState<IWorkflowHook[]>(customizeConfig.hookInfoList || []);
    const [hookUrl, setHookUrl] = useState('');
    const [appSearchValue, setAppSearchValue] = useState('');
    const [loadingApplications, setLoadingApplications] = useState(false);

    const { showMessage } = useSnackbar();

    useEffect(() => {
        if (customizeConfig.authorizedAppIdList.length > 0) {
            getSimpletApplicationList('', customizeConfig.authorizedAppIdList.join(','), 1, 1000, 'workflow_admin').then((res) => {
                setSelectedApplications(res.data.applicationList.filter((app: ISimpleApplicationResEntity) => customizeConfig.authorizedAppIdList.includes(app.id)));
            });
        }
    }, [customizeConfig]);

    const handleClose = () => {
        setOpen(false);
    };
    const handleAddHook = () => {
        const newToken = uuidv4();
        const newHookId = uuidv4();
        setAddedHookToken(newToken);
        setHooks([...hooks, {
            id: `temp_${newHookId}`,
            url: hookUrl,
            token: newToken,
            eventList: selectedHookEvent.map((event) => event.key as 'pre_start' | 'started' | 'force_closed' | 'nomal_end' | 'rejected' | 'withdrawn')
        }]);
        const newCustomizationInfo = {
            ...customizationInfo, hookInfoList: [...customizationInfo.hookInfoList, {
                id: `temp_${newHookId}`,
                url: hookUrl,
                token: newToken,
                eventList: selectedHookEvent.map((event) => event.key as 'pre_start' | 'started' | 'force_closed' | 'nomal_end' | 'rejected' | 'withdrawn')
            }]
        };
        setCustomizationInfo(newCustomizationInfo);
        onCustomizeConfigChange(newCustomizationInfo);
        setOpen(false);
    }

    const hookEvents = [
        {
            key: 'pre_start',
            label: '创建前'
        },
        {
            key: 'started',
            label: '创建后'
        },
        {
            key: 'force_closed',
            label: '强制关闭'
        },
        {
            key: 'nomal_end',
            label: '正常结束'
        },
        {
            key: 'rejected',
            label: '被拒绝'
        },
        {
            key: 'withdrawn',
            label: '被撤回'
        }
    ]


    const handleLabelChange = (e: React.ChangeEvent<HTMLInputElement>) => {

        setLabelJson(e.target.value);
        try {
            setLabel(JSON.parse(e.target.value));
            const newCustomizationInfo = { ...customizationInfo, label: JSON.parse(e.target.value) };
            setCustomizationInfo(newCustomizationInfo);
            onCustomizeConfigChange(newCustomizationInfo);
            setError('');
        } catch (err) {
            setError('Invalid JSON');
        }
    };


    function copyToClipboardFallback(text: string) {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        document.body.appendChild(textarea);
        textarea.select();

        try {
            const successful = document.execCommand('copy');
            if (successful) {
                showMessage('复制成功', 'success');
            } else {
                showMessage('复制失败', 'error');
            }
            setAddedHookToken('');
            return successful;
        } catch (err: any) {
            showMessage('复制失败', 'error');
            return false;
        } finally {
            document.body.removeChild(textarea);
        }
    }


    const handleCopy = async () => {
        try {
            await navigator.clipboard.writeText(addedHookToken);
            setAddedHookToken('');
            showMessage('复制成功', 'success');
        } catch (err) {
            // 降级方案
            copyToClipboardFallback(addedHookToken);
        }
    };
    const handleAuthorizedAppChange = (value: ISimpleApplicationResEntity[]) => {
        const newCustomizationInfo = { ...customizationInfo, authorizedAppIdList: value.map((v: any) => v.id) };
        setCustomizationInfo(newCustomizationInfo);
        onCustomizeConfigChange(newCustomizationInfo);
        setSelectedApplications(value);
    }

    const loadApplications = async (searchValue: string = '') => {
        if (loadingApps) return;
        setLoadingApps(true);
        try {
            const response = await getSimpletApplicationList(searchValue, '', 1, 1000, 'workflow_admin');
            if (response.code === 0) {
                setApplicationList(response.data.applicationList);
            }
        } catch (error) {
            console.error('加载应用列表失败:', error);
        } finally {
            setLoadingApps(false);
        }
    };


    return (
        <Box>
            <Stack spacing={3}>
                <Grid container alignItems="flex-start" spacing={2}>
                    <Grid size={3} sx={{ minWidth: 100, pt: 1 }}>
                        <FormLabel>应用授权</FormLabel>
                    </Grid>
                    <Grid size={9}>
                        <Autocomplete
                            multiple
                            options={applicationList}
                            getOptionLabel={(option) => option.name}
                            value={selectedApplications}
                            onChange={(e, value) => handleAuthorizedAppChange(value)}
                            onInputChange={(e, value) => {
                                setAppSearchValue(value);
                                if (value.length > 0) {
                                    loadApplications(value);
                                }
                            }}
                            renderInput={(params) => (
                                <TextField
                                    {...params}
                                    label="选择应用"
                                    placeholder="输入关键词后搜索应用..."
                                    InputProps={{
                                        ...params.InputProps,
                                        endAdornment: (
                                            <>
                                                {loadingApplications ? <CircularProgress color="inherit" size={20} /> : null}
                                                {params.InputProps.endAdornment}
                                            </>
                                        ),
                                    }}
                                />
                            )}
                            loading={loadingApplications}
                            size="small"
                            fullWidth
                        />
                    </Grid>
                </Grid>
                <Grid container alignItems="flex-start" spacing={2}>
                    <Grid size={3} sx={{ minWidth: 100, pt: 1 }}>
                        <FormLabel>标签配置</FormLabel>
                    </Grid>
                    <Grid size={9}>
                        <TextField
                            multiline
                            fullWidth
                            minRows={3}
                            value={labelJson}
                            onChange={handleLabelChange}
                            error={!!error}
                            helperText={error}
                            sx={{ fontFamily: 'monospace' }}
                        />
                        <Button onClick={() => setLabelJson(JSON.stringify(label, null, 2))}>
                            Format
                        </Button>
                    </Grid>
                </Grid>
                <Grid container alignItems="flex-start" spacing={2}>
                    <Grid size={12} sx={{ minWidth: 100, pt: 1 }}>
                        <FormLabel>hook配置</FormLabel>
                        <Button onClick={() => setOpen(true)}>
                            新增
                        </Button>
                        {addedHookToken !== "" ? (<Alert severity="info">{addedHookToken} <Button onClick={() => handleCopy()}>复制Token</Button></Alert>) : null}

                    </Grid>
                    <Table sx={{ minWidth: 650 }} aria-label="caption table">
                        <TableHead>
                            <TableRow>
                                <TableCell>HOOK地址</TableCell>
                                <TableCell align="right">事件类型</TableCell>
                                <TableCell align="right">操作</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {customizationInfo.hookInfoList.map((row) => (
                                <TableRow key={row.url}>
                                    <TableCell component="th" scope="row">
                                        {row.url}
                                    </TableCell>
                                    <TableCell align="right">{row.eventList.map((event) => hookEvents.find((e) => e.key === event)?.label).join(',')}</TableCell>
                                    <TableCell align="right"><div><Button disabled>编辑</Button><Button disabled>重置token</Button><Button disabled>删除</Button></div></TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </Grid>
            </Stack>
            <Dialog open={open} onClose={handleClose} fullWidth maxWidth="sm">
                <DialogTitle>新增hook</DialogTitle>
                <DialogContent>
                    <Grid container spacing={2}>
                        <TextField label="HOOK地址" fullWidth value={hookUrl} onChange={(e) => setHookUrl(e.target.value)} />
                        <Autocomplete
                            value={selectedHookEvent}
                            onChange={(event, newValue) => {
                                setSelectedHookEvent(newValue);
                            }}
                            fullWidth
                            multiple
                            id="tags-outlined"
                            options={hookEvents}
                            getOptionLabel={(option) => option.label}
                            filterSelectedOptions
                            renderInput={(params) => (
                                <TextField
                                    {...params}
                                    label="事件类型"
                                    placeholder="Favorites"
                                />
                            )}
                        />
                    </Grid>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleClose}>取消</Button>
                    <Button onClick={handleAddHook}>确定</Button>
                </DialogActions>
            </Dialog>
        </Box >

    );
}

export default CustomizeConfig;