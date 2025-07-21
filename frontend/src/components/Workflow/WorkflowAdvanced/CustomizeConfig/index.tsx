import React, { useEffect, useState } from 'react';
import { Alert, OutlinedInput, MenuItem, Dialog, DialogTitle, DialogContent, DialogActions, Box, Stack, Grid2, FormLabel, Autocomplete, TextField, Chip, Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@mui/material';
import Grid from '@mui/material/Grid2';
import { getSimpletApplicationList } from '../../../../services/application'
import { ISimpleApplicationResEntity } from '../../../../types/application';
import { v4 as uuidv4 } from 'uuid';
import useSnackbar from '../../../../hooks/useSnackbar';

interface IHook {
    id: string;
    url: string;
    token: string;
    events: IHookEvent[];
}

interface IHookEvent {
    key: string;
    label: string;
}

function CustomizeConfig() {
    const [applicationList, setApplicationList] = useState<ISimpleApplicationResEntity[]>([]);
    const [selectedApplications, setSelectedApplications] = useState<ISimpleApplicationResEntity[]>([]);
    const [label, setLabel] = useState({});
    const [labelJson, setLabelJson] = useState(JSON.stringify(label, null, 2));
    const [error, setError] = useState('');
    const [open, setOpen] = useState(false);
    const [selectedHookEvent, setSelectedHookEvent] = useState<IHookEvent[]>([]);
    const [addedHookToken, setAddedHookToken] = useState('');
    const [hooks, setHooks] = useState<IHook[]>([]);
    const [hookUrl, setHookUrl] = useState('');
    const { showMessage } = useSnackbar();


    const handleClose = () => {
        setOpen(false);
    };
    const handleAddHook = () => {
        const newToken = uuidv4();
        setAddedHookToken(newToken);
        setHooks([...hooks, {
            id: '00000000-0000-0000-0000-000000000000',
            url: hookUrl,
            token: newToken,
            events: selectedHookEvent
        }]);
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


    useEffect(() => {
        getSimpletApplicationList('', 1, 1000, 'workflow_admin').then((res) => {
            setApplicationList(res.data.applicationList);
        });
    }, []);
    const handleLabelChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setLabelJson(e.target.value);
        try {
            setLabel(JSON.parse(e.target.value));
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
                            disablePortal
                            options={applicationList || []}
                            value={selectedApplications}
                            onChange={(event, newValue) => {
                                setSelectedApplications(newValue);
                            }}
                            getOptionLabel={(option) => option.name || ''}
                            isOptionEqualToValue={(option, value) => option.id === value.id}
                            sx={{ width: 300 }}
                            renderInput={(params) => <TextField {...params} label="应用授权" />}
                            renderOption={(props, option) => (
                                <li {...props}>
                                    <div>
                                        <div>{option.name || '未命名'}</div>
                                        <div style={{ fontSize: '0.8em', color: '#666' }}>
                                            {option.description || '无描述'}
                                        </div>
                                    </div>
                                </li>
                            )}
                            renderTags={(value, getTagProps) =>
                                value.map((option, index) => (
                                    <Chip
                                        label={option.name}
                                        size="small"
                                        {...getTagProps({ index })}
                                    />
                                ))
                            }
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
                            {hooks.map((row) => (
                                <TableRow key={row.url}>
                                    <TableCell component="th" scope="row">
                                        {row.url}
                                    </TableCell>
                                    <TableCell align="right">{row.events.map((event) => event.label).join(',')}</TableCell>
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