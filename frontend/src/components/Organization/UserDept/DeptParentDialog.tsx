import { Autocomplete, Button, Dialog, DialogActions, DialogContent, DialogTitle, InputAdornment, TextField } from '@mui/material';
import { debounce } from 'lodash';
import { useCallback, useEffect, useMemo, useState } from 'react';
import { useTranslation } from 'react-i18next';
import useSnackbar from '../../../hooks/useSnackbar';
import { getDeptPath, getDeptPaths, updateDeptParentDept } from '../../../services/dept';


interface IDeptPath {
    id: string;
    path: string;
    name: string;
}
const DeptParentDialog = ({ open, deptId, parentDeptId, onClose }: {
    open: boolean,
    deptId: string,
    parentDeptId: string,
    onClose: (needRefresh: boolean) => void
}) => {
    const { t } = useTranslation();
    const [deptPathList, setDeptPathList] = useState<IDeptPath[]>([]);
    const [deptPath, setDeptPath] = useState<IDeptPath | null>(null);
    const [parentDeptInputValue, setParentDeptInputValue] = useState('');

    const [loading, setLoading] = useState(false);
    const { showMessage } = useSnackbar();


    const fetchDeptPathList = useCallback(async (keyword: string) => {
        try {
            setLoading(true);
            const result = await getDeptPaths(keyword, '', 1, 1000);
            if (result.code === 0) {
                setDeptPathList(result.data.deptPathList);
            } else {
                showMessage(result.msg, 'error');
            }
        } catch (error: any) {
            showMessage('搜索deptpath失败', 'error');
        } finally {
            setLoading(false);
        }
    }, [showMessage]);

    const debouncedFetchDeptPaths = useMemo(
        () => debounce((keyword: string) => {
            fetchDeptPathList(keyword);
        }, 500),
        [fetchDeptPathList]
    );


    const handelSubmit = async () => {
        console.log('submit')
        try {
            await updateDeptParentDept(deptId, deptPath?.id ?? '')
            showMessage('update parent dept successfully', 'success');
        } catch (error: any) {
            showMessage(error.message, 'error');
        }
        onClose(true);
    }

    useEffect(() => {
        if (parentDeptId) {
            setLoading(true);
            getDeptPath(parentDeptId).then((res) => {
                setDeptPath(res.data.deptPath);
                setLoading(false);
            }).catch((err) => {
                showMessage('error', err.message);
                setLoading(false);
            });
        } else {
            setDeptPath(null);
        }

    }, [open, parentDeptId, showMessage]);

    return (
        <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth style={{ maxWidth: 600, margin: '0 auto' }}>
            <DialogTitle>{t('user.changeParentDept')}</DialogTitle>
            <DialogContent>
                <Autocomplete
                    value={deptPath}
                    onChange={(_event, newValue) => {
                        setDeptPath(newValue)
                    }}
                    inputValue={parentDeptInputValue}
                    onInputChange={(_event, newValue) => {
                        setParentDeptInputValue(newValue);
                        debouncedFetchDeptPaths(newValue)

                    }}
                    getOptionLabel={(option) => {
                        if (!option) return '';
                        return `${option.path}`;
                    }}
                    isOptionEqualToValue={(option, value) => option.id === value.id}
                    disablePortal
                    options={deptPathList}
                    loading={loading}
                    noOptionsText={parentDeptInputValue.length < 1 ? t('common.pleaseEnterToSearch') : t('common.noData')}
                    sx={{ marginTop: 2, marginBottom: 2 }}
                    renderInput={(params) => (
                        <TextField
                            {...params}
                            label='上级部门'
                            slotProps={{
                                input: {
                                    ...params.InputProps,
                                    endAdornment: (
                                        <>
                                            {loading ? <InputAdornment position="end">{t('common.searching')}</InputAdornment> : null}
                                            {params.InputProps.endAdornment}
                                        </>
                                    ),
                                }
                            }}
                        />
                    )}
                />

            </DialogContent>
            <DialogActions>
                <Button autoFocus onClick={() => onClose(false)}>
                    {t('common.cancel')}
                </Button>
                <Button onClick={() => handelSubmit()} disabled={loading}>{t('common.save')}</Button>
            </DialogActions>
        </Dialog>
    )
}

export default DeptParentDialog;