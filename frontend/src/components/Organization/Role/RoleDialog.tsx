import React, { useState, useCallback, useEffect } from 'react';
import { Dialog, DialogActions, DialogContent, DialogTitle, TextField, Button, Radio, RadioGroup, FormControlLabel, FormControl, FormLabel } from '@mui/material';
import { useTranslation } from 'react-i18next';
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import { addRole, updateRole } from '../../../services/role';
import useSnackbar from '../../../hooks/useSnackbar';
import { getRoleDetail } from '../../../services/role';


interface RoleDialogProps {
    open: boolean;
    onClose: () => void;
    roleId?: string;
}

const RoleDialog = (props: RoleDialogProps) => {
    const { t } = useTranslation();
    const { open, onClose, roleId } = props;
    const [name, setName] = useState('');
    const [description, setDescription] = useState('');
    const [loading, setLoading] = useState(false);
    const { showMessage } = useSnackbar();

    const fetchRoleDetail = useCallback(async () => {
        if (roleId) {
            try {
                const result = await getRoleDetail(roleId);
                console.log('1111111');
                console.log(result);
                console.log('11111111');
                if (result.code === -1) {
                    showMessage(`fail to get role info: ${result.message}`, 'error');
                } else {
                    setName(result.data.roleInfo.name);
                    setDescription(result.data.roleInfo.description);
                }
            } catch (error: any) {
                showMessage(`fail to get role info: ${error.message}`, 'error');
            }
        }
    }, [roleId, showMessage]);

    const handleClose = () => {
        onClose();
    };

    useEffect(() => {
        fetchRoleDetail();
    }, [fetchRoleDetail]);

    const handleSubmitRole = async () => {
        try {
            setLoading(true);
            if (!roleId) {
                const result = await addRole(name, description);
                if (result.code === -1) {
                    showMessage(`fail to add role: ${result.message}`, 'error');
                } else {
                    showMessage(`success to add role`, 'success');
                    onClose();
                }
            } else {
                const result = await updateRole(roleId, name, description);
                if (result.code === -1) {
                    showMessage(`fail to update role: ${result.message}`, 'error');
                } else {
                    showMessage(`success to update role`, 'success');
                    onClose();
                }

            }

        } catch (error: any) {
            showMessage(`fail to add role: ${error.message}`, 'error');
        } finally {
            setLoading(false);
        }
    }

    return (
        <Dialog open={open} onClose={handleClose}>
            <DialogTitle>
                {t('common.add')}
                <HelpOutlineIcon sx={{ marginLeft: '10px' }} />
            </DialogTitle>
            <DialogContent>
                <TextField
                    label={t('common.name')}
                    fullWidth
                    value={name}
                    onChange={(event: React.ChangeEvent<HTMLInputElement>) => { setName(event.target.value); }}
                    required />
                <TextField
                    label={t('common.description')}
                    value={description}
                    fullWidth
                    margin="normal"
                    onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
                        setDescription(event.target.value);
                    }}
                />
            </DialogContent>
            <DialogActions>
                <Button autoFocus onClick={onClose}>
                    {t('common.cancel')}
                </Button>
                <Button onClick={() => handleSubmitRole()} disabled={loading}>{t('common.save')}</Button>
            </DialogActions>
        </Dialog>
    );

}

export default RoleDialog;
