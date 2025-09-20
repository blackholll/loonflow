import React, { useState, useEffect, useCallback, useMemo } from 'react';
import {
    Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField,
    Autocomplete, CircularProgress, Checkbox, FormControlLabel, Box, InputAdornment, RadioGroup, Radio
} from '@mui/material';
import { useTranslation } from 'react-i18next';
import useSnackbar from '../../../hooks/useSnackbar';
import { debounce } from 'lodash';
import { getUserDetail, addUser, updateUser } from '../../../services/user'; // 假设的API服务
import { getDeptPaths } from '../../../services/dept';
import Grid from '@mui/material/Grid2';


interface ISimpleDept {
    id: string;
    name: string;
    path: string;
}

interface IUserFormData {
    name: string;
    alias: string;
    email: string;
    phone: string;
    password?: string;
    password1?: string;
    isActive: boolean;
    type: string;
}

interface UserDialogProps {
    open: boolean;
    onClose: (refresh?: boolean) => void;
    userId?: string | null;
    selectedDeptId?: string | null;
}

const UserDialog: React.FC<UserDialogProps> = ({ open, onClose, userId, selectedDeptId }) => {
    const { t } = useTranslation();
    const { showMessage } = useSnackbar();

    const [loading, setLoading] = useState(false);
    const [formLoading, setFormLoading] = useState(false);
    const initialFormData = useMemo<IUserFormData>(() => ({
        name: '',
        alias: '',
        email: '',
        phone: '',
        password: '',
        password1: '',
        type: '',
        isActive: true,
    }), []);

    const [formData, setFormData] = useState<IUserFormData>(initialFormData);
    const [selectedDeptPaths, setSelectedDeptPaths] = useState<ISimpleDept[]>([]);
    const [deptPathList, setDeptPathList] = useState<ISimpleDept[]>([]);
    const [deptSearchLoading, setDeptSearchLoading] = useState(false);
    const [deptInputValue, setDeptInputValue] = useState('');
    const [passwordError, setPasswordError] = useState('');

    useEffect(() => {
        if (open) {
            if (userId) {
                setFormLoading(true);
                getUserDetail(userId).then(result => {
                    if (result.code === 0) {
                        const userData = result.data.userInfo;
                        setFormData({
                            name: userData.name,
                            alias: userData.alias,
                            email: userData.email,
                            phone: userData.phone,
                            type: userData.type,
                            isActive: userData.isActive,
                            // password 通常不回显
                        });
                        setSelectedDeptPaths(userData.deptInfoList || []);
                    } else {
                        showMessage(result.msg || 'failed to get user details', 'error');
                    }
                }).catch(error => {
                    showMessage(error.message || 'failed to get user details', 'error');
                }).finally(() => {
                    setFormLoading(false);
                });
            } else {
                setFormData(initialFormData);
                setSelectedDeptPaths([]);
            }
        }
    }, [userId, open, selectedDeptId, initialFormData]);


    const fetchDeptPaths = useCallback(async (inputValue: string) => {
        try {
            setDeptSearchLoading(true);
            await getDeptPaths(inputValue, '', 1, 1000).then(result => {
                if (result.code === 0) {
                    setDeptPathList(result.data.deptPathList);
                }
            })
            setDeptSearchLoading(false);
        } catch (error: any) {
            showMessage(error.message || t('common.loadingFail'), 'error');
        }
    }, [showMessage, t]);

    const handleChange = (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>, field: string) => {
        const { value } = event.target;
        setFormData(prev => {
            const newFormData = { ...prev, [field]: value };
            if (field === 'password' || field === 'password1') {
                if (field === 'password' && newFormData.password1 && newFormData.password !== newFormData.password1) {
                    setPasswordError(t('common.passwordNotMatch'));
                } else if (field === 'password1' && newFormData.password && newFormData.password !== value) {
                    setPasswordError(t('common.passwordNotMatch'));
                } else {
                    setPasswordError('');
                }
            }
            return newFormData;
        });
    };

    const handleCheckboxChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const { name, checked } = event.target;
        setFormData(prev => ({ ...prev, [name]: checked }));
    };

    const debouncedFetchDeptPaths = useMemo(
        () => debounce(async (inputValue: string) => {
            fetchDeptPaths(inputValue);
        }, 500),
        [fetchDeptPaths]
    )

    const handleSubmit = async () => {
        try {
            const payload = {
                ...formData,
                deptIdList: selectedDeptPaths.map(d => d.id),
            };
            if (!userId && payload.password !== payload.password1) {
                showMessage(t('common.passwordNotMatch'), 'error');
                return;
            }
            if (!userId && !payload.password) {
                showMessage(t('common.passwordCannotBeEmpty'), 'error');
                return;
            }
            if (!payload.name || !payload.email) {
                showMessage(t('nameAndEmailCannotBeEmpty'), 'error');
                return;
            }


            let result;
            setLoading(true);
            if (userId) {
                result = await updateUser(userId, payload);
            } else {
                result = await addUser(payload);
            }
            setLoading(false);
            if (result.code === 0) {
                showMessage(userId ? t('common.updateUserSuccess') : t('common.addUserSuccess'), 'success');
                onClose(true);
            } else {
                showMessage(result.msg || (userId ? t('common.updateUserFail') : t('common.addUserFail')), 'error');
            }
        } catch (error: any) {
            showMessage(error.message || t('common.actionFail'), 'error');
        } finally {
            setLoading(false);
        }
    };

    const handleDialogClose = () => {
        onClose(false);
    }



    return (
        <Dialog open={open} onClose={handleDialogClose} maxWidth="md" fullWidth>
            <DialogTitle>{userId ? t('common.edit') : t('common.new')}</DialogTitle>
            <DialogContent>
                {formLoading ? (
                    <Box display="flex" justifyContent="center" alignItems="center" sx={{ minHeight: 300 }}>
                        <CircularProgress />
                    </Box>
                ) : (
                    <Grid container spacing={2} size={12}>
                        <Grid size={12}>
                            <TextField
                                label={t('common.name')}
                                name="name"
                                value={formData.name}
                                onChange={(e) => handleChange(e, "name")}
                                fullWidth
                                required
                            />
                        </Grid>
                        <Grid size={12}>
                            <TextField
                                label={t('common.alias')}
                                name="alias"
                                value={formData.alias}
                                onChange={(e) => handleChange(e, "alias")}
                                fullWidth
                            />
                        </Grid>
                        <Grid size={12}>
                            <TextField
                                label={t('common.email')}
                                name="email"
                                type="email"
                                value={formData.email}
                                onChange={(e) => handleChange(e, "email")}
                                fullWidth
                                required
                            />
                        </Grid>
                        <Grid size={12}>
                            <TextField
                                label={t('common.phone')}
                                name="phone"
                                value={formData.phone}
                                onChange={(e) => handleChange(e, "phone")}
                                fullWidth
                            />
                        </Grid>
                        {
                            !userId && (
                                <Grid size={12}>
                                    <TextField
                                        label={t('common.password')}
                                        name="password"
                                        type="password"
                                        value={formData.password}
                                        onChange={(e) => handleChange(e, "password")}
                                        fullWidth
                                        helperText={userId ? t('organization.passwordEditHint') : ''}
                                        required={!userId}
                                    />
                                </Grid>
                            )
                        }
                        {
                            !userId && (
                                <Grid size={12}>
                                    <TextField
                                        label={t('common.password1')}
                                        name="password1"
                                        type="password"
                                        error={!!passwordError}
                                        helperText={passwordError}
                                        value={formData.password1 || ''}
                                        onChange={(e) => handleChange(e, "password1")}
                                        fullWidth
                                        required
                                    />
                                </Grid>
                            )
                        }
                        <Grid size={12}>
                            <Autocomplete
                                multiple
                                options={deptPathList}
                                value={selectedDeptPaths}
                                getOptionLabel={(option) => option.path}
                                isOptionEqualToValue={(option, value) => option.id === value.id}
                                onChange={(_event, newValue) => {
                                    setSelectedDeptPaths(newValue);
                                    setDeptPathList(newValue);
                                }}
                                inputValue={deptInputValue}
                                onInputChange={(_event, newInputValue) => {
                                    setDeptInputValue(newInputValue);
                                    debouncedFetchDeptPaths(newInputValue);
                                }}
                                loading={deptSearchLoading}
                                loadingText={t('common.loading')}
                                noOptionsText={deptInputValue.length < 1 ? t('common.pleaseEnterToSearch') : t('common.noOptions')}
                                renderInput={(params) => (
                                    <TextField
                                        {...params}
                                        label={t('common.dept')}
                                        helperText={t('user.userDeptHelpText')}
                                        slotProps={{
                                            input: {
                                                ...params.InputProps,
                                                endAdornment: (
                                                    <>
                                                        {deptSearchLoading ? <InputAdornment position="end">t('common.searching')...</InputAdornment> : null}
                                                        {params.InputProps.endAdornment}
                                                    </>
                                                ),
                                            }
                                        }}
                                    />
                                )}
                                fullWidth
                            />
                        </Grid>
                        <Grid size={12} marginLeft={1}>
                            <FormControlLabel
                                control={
                                    <RadioGroup
                                        row
                                        name="type"
                                        value={formData.type}
                                        onChange={(e) => handleChange(e, "type")}
                                    >
                                        <FormControlLabel value="admin" control={<Radio />} label={t('common.admin')} />
                                        <FormControlLabel value="workflow_admin" control={<Radio />} label={t('common.workflow_admin')} />
                                        <FormControlLabel value="normal" control={<Radio />} label={t('common.normal')} />
                                    </RadioGroup>
                                }
                                label={''}
                            />
                        </Grid>
                        <Grid size={12}>
                            <FormControlLabel
                                control={
                                    <Checkbox
                                        checked={formData.isActive}
                                        onChange={handleCheckboxChange}
                                        name="isActive"
                                    />
                                }
                                label={t('common.isActive')}
                            />
                        </Grid>
                    </Grid>
                )}
            </DialogContent>
            <DialogActions>
                <Button onClick={handleDialogClose}>{t('common.cancel')}</Button>
                <Button onClick={handleSubmit} color="primary" disabled={loading || formLoading}>
                    {loading ? <CircularProgress size={24} /> : t('common.save')}
                </Button>
            </DialogActions>
        </Dialog>
    );
};

export default UserDialog;