import React, { useState, useEffect, useCallback } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField, FormControl, FormLabel, RadioGroup, FormControlLabel, Radio, Icon, Box, Tooltip, InputAdornment } from '@mui/material';
import { useTranslation } from 'react-i18next';
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import { addApplication } from '../../../services/application';
import useSnackbar from '../../../hooks/useSnackbar';
import { getApplicationDetail } from '../../../services/application';


interface ApplicationDetailProps {
  open: boolean
  onClose: () => void
  applicationId?: string
}

const ApplicationDialog = ({ open, onClose, applicationId }: ApplicationDetailProps) => {
  const { t } = useTranslation();
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [type, setType] = useState('');
  const [token, setToken] = useState('');
  const [loading, setLoading] = useState(false);
  const { showMessage } = useSnackbar();


  const getAppDetail = useCallback(async () => {
    if (applicationId) {
      try {
        const result = await getApplicationDetail(applicationId);
        if (result.code === -1) {
          showMessage(`fail to get application detail: ${result.message}`, 'error');
        } else {
          setName(result.data.applicationInfo.name);
          setDescription(result.data.applicationInfo.description);
          setToken(result.data.applicationInfo.token);
          setType(result.data.applicationInfo.type);
        }
      } catch (error: any) {
        showMessage(`fail to get application detail: ${error.message}`, 'error');
      }
    }
  }, [applicationId])

  useEffect(() => {
    getAppDetail();
  }, [applicationId, getAppDetail]);

  const handelSubmit = async () => {
    console.log('submit');
    try {
      setLoading(true);
      const result = await addApplication(name, description, type);
      if (result.code === -1) {
        showMessage(result.msg, 'error');
      } else {
        showMessage(t('common.addRecordSuccess'), 'success');
        setName('');
        setDescription('');
        setToken('');
        onClose();
      }
    } catch (error: any) {
      showMessage('Internel Server Error', 'error');
    } finally {
      setLoading(false);
    }
  }

  return (
    <Dialog open={open} onClose={onClose}>
      <DialogTitle>{applicationId ? t('common.edit') : t('common.new')}</DialogTitle>
      <DialogContent>
        <TextField
          label="Name"
          value={name}
          required
          fullWidth
          margin="normal"
          onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
            setName(event.target.value);
          }}

        />
        <TextField
          label="Description"
          value={description}
          fullWidth
          margin="normal"
          onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
            setDescription(event.target.value);
          }}
        />
        {applicationId ? <TextField
          label="token"
          type="password"
          disabled
          value={token}
          fullWidth
          margin="normal"
          slotProps={{
            input: {
              endAdornment: <InputAdornment position="end"><Button onClick={() => {
                navigator.clipboard.writeText(token).then(() => {
                  showMessage(t('settings.application.tokenCopied'), 'success');
                });
              }}>COPY</Button></InputAdornment>,
            },
          }}
        /> : null}

        {/* <Button variant="contained" color="primary">
        Copy
      </Button> */}
        <FormControl component="fieldset" required margin="normal">
          <FormLabel component="legend" sx={{ display: 'flex', alignItems: 'center' }}>
            <Box display="flex" alignItems="center" justifyContent="center">
              {t('common.type')}<Tooltip title={t('setting.application.appTypeDescription')}><HelpOutlineIcon /></Tooltip>
            </Box>
          </FormLabel>
          <RadioGroup
            aria-label="option"
            name="option"
            value={type}
            row
            onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
              setType(event.target.value);
            }}
          // value={formData.option}
          // onChange={handleRadioChange}
          >
            <FormControlLabel value="admin" control={<Radio />} label={t('common.admin')} />
            <FormControlLabel value="workflowAdmin" control={<Radio />} label={t('common.workflow_admin')} />
          </RadioGroup>
        </FormControl>
      </DialogContent>
      <DialogActions>
        <Button autoFocus onClick={onClose}>
          {t('common.cancel')}
        </Button>
        <Button onClick={() => handelSubmit()} disabled={loading}>{t('common.save')}</Button>
      </DialogActions>
    </Dialog>
  )
}

export default ApplicationDialog;