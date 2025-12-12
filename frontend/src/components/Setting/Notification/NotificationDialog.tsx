import { Box, Button, Dialog, DialogActions, DialogContent, DialogTitle, FormControl, FormControlLabel, FormHelperText, FormLabel, Radio, RadioGroup, TextField } from '@mui/material';
import React, { useCallback, useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import * as Yup from 'yup';
import useSnackbar from '../../../hooks/useSnackbar';
import { addNotification, getNotificationDetail, updateNotification } from '../../../services/notification';


const validationSchema = Yup.object({
  name: Yup.string().required('Name is required'),
  description: Yup.string().required('Description is required'),
  type: Yup.string().required('Type is required'),
  hookUrl: Yup.string().test('is-hook-url-required', 'Hook URL is required', function (value) {
    const { type } = this.parent;
    if (type === 'hook') {
      console.log('1111111111');
      return Yup.string().url('Invalid URL').required('Hook URL is required').isValidSync(value);
    }
    return true;
  }),
  hookToken: Yup.string().test('is-hook-token-required', 'Hook Token is required', function (value) {
    const { type } = this.parent;
    if (type === 'hook') {
      console.log('2222222');
      return Yup.string().required('Hook Token is required').isValidSync(value);
    }
    return true;
  })
});


interface NotificationDetailProps {
  open: boolean
  onClose: () => void
  notificationId?: string
}

const NotificationDialog = ({ open, onClose, notificationId }: NotificationDetailProps) => {
  const { t } = useTranslation();
  const [errors, setErrors] = useState<{ [key: string]: string }>({});
  const initialFormData = {
    name: '',
    description: '',
    type: '',
    dtAppKey: '',
    dtAppSecret: '',
    wcCorpId: '',
    wcCorpSecret: '',
    fsAppId: '',
    fsAppSecret: '',
    hookUrl: '',
    hookToken: ''
  };
  const [formData, setFormData] = useState(initialFormData);
  const [loading, setLoading] = useState(false);

  const { showMessage } = useSnackbar();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };



  const getNotificationDetailR = useCallback(async () => {
    if (notificationId) {
      try {
        const result = await getNotificationDetail(notificationId);
        if (result.code === -1) {
          showMessage(`fail to get notification detail: ${result.message}`, 'error');
        } else {
          const notificationType = result.data.notificationInfo.type;
          const notificationDetail: any = {
            name: result.data.notificationInfo.name,
            description: result.data.notificationInfo.description,
            type: notificationType,
          }
          if (notificationType === 'hook') {
            notificationDetail.hookUrl = result.data.notificationInfo.extra.hookUrl;
            notificationDetail.hookToken = result.data.notificationInfo.extra.hookToken;
          } else if (notificationType === 'dingtalk') {
            notificationDetail.dtAppKey = result.data.notificationInfo.extra.dtAppKey;
            notificationDetail.dtAppSecret = result.data.notificationInfo.extra.dtAppSecret;
          } else if (notificationType === 'wecom') {
            notificationDetail.wcCorpId = result.data.notificationInfo.extra.wcCorpId;
            notificationDetail.wcCorpSecret = result.data.notificationInfo.extra.wcCorpSecret;
          } else if (notificationType === 'feishu') {
            notificationDetail.fsAppId = result.data.notificationInfo.extra.fsAppId;
            notificationDetail.fsAppSecret = result.data.notificationInfo.extra.fsAppSecret
          }
          setFormData((prev) => ({ ...prev, ...notificationDetail }));
        }
      } catch (error: any) {
        showMessage(`fail to get notification detail: ${error.message}`, 'error');
      }
    }
  }, [notificationId, showMessage])

  useEffect(() => {
    getNotificationDetailR();
  }, [notificationId, getNotificationDetailR]);

  useEffect(() => {
    const validate = async () => {
      try {
        await validationSchema.validate(formData, { abortEarly: false });
        setErrors({});
      } catch (err) {
        if (err instanceof Yup.ValidationError) {
          const newErrors: { [key: string]: string } = {};
          err.inner.forEach((error) => {
            if (error.path) {
              newErrors[error.path] = error.message;
            }
          });
          setErrors(newErrors);
        }
      }
    };
    validate();
  }, [formData]);

  const clearExtra = () => {
    setFormData(initialFormData);
  }
  const handelSubmit = async () => {
    if (Object.keys(errors).length === 0) {
      try {
        setLoading(true);
        const requestData: any = {}
        requestData.name = formData.name;
        formData.description && (requestData.description = formData.description);
        requestData.type = formData.type;
        if (formData.type === 'hook') {
          requestData.extra = {
            hookUrl: formData.hookUrl,
            hookToken: formData.hookToken
          }
        }
        if (formData.type === 'dingtalk') {
          requestData.extra = {
            dtAppKey: formData.dtAppKey,
            dtAppSecret: formData.dtAppSecret
          }
        }
        if (formData.type === 'wecom') {
          requestData.extra = {
            wcCorpId: formData.wcCorpId,
            wcCorpSecret: formData.wcCorpSecret
          }
        }
        if (formData.type === 'feishu') {
          requestData.extra = {
            fsAppId: formData.fsAppId,
            fsAppSecret: formData.fsAppSecret
          }
        }
        let result: any = {};
        if (notificationId) {
          result = await updateNotification(notificationId, requestData);
        } else {
          result = await addNotification(requestData);
        }
        if (result.code === -1) {
          showMessage(result.msg, 'error');
        } else {
          showMessage(t('common.addRecordSuccess'), 'success');
          setFormData(initialFormData);
          onClose();
        }
      } catch (error: any) {
        showMessage('Internel Server Error', 'error');
      } finally {
        setLoading(false);
      }
    }
  }

  return (
    <Dialog open={open} onClose={onClose}>
      <DialogTitle>{notificationId ? t('setting.notification.notificationDetial') : t('setting.notification.newNotification')}</DialogTitle>
      <DialogContent>
        <TextField
          label={t('common.name')}
          name="name"
          value={formData.name}
          required
          fullWidth
          margin="normal"
          onChange={handleChange}
          error={!!errors.name}
          helperText={errors.name}
        />
        <TextField
          label={t('common.description')}
          name="description"
          value={formData.description}
          fullWidth
          margin="normal"
          onChange={handleChange}
          error={!!errors.description}
          helperText={errors.description}
        />

        <FormControl component="fieldset" error={!!errors.radio} required margin="normal">
          <FormLabel component="legend" sx={{ display: 'flex', alignItems: 'center' }}>
            <Box display="flex" alignItems="center" justifyContent="center">
              {t('common.type')}
            </Box>
          </FormLabel>
          <RadioGroup
            aria-label="option"
            name="type"
            value={formData.type}
            row
            onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
              clearExtra();
              handleChange(event);
            }}
          >
            <FormControlLabel value="hook" control={<Radio />} label={t('common.hook')} />
            <FormControlLabel value="dingtalk" control={<Radio />} label={t('common.dingtalk')} disabled />
            <FormControlLabel value="wecom" control={<Radio />} label={t('common.wecom')} disabled />
            <FormControlLabel value="feishu" control={<Radio />} label={t('common.feishu')} disabled />
          </RadioGroup>
          {errors.type && <FormHelperText style={{ "color": "red" }}>{errors.type}</FormHelperText>}
        </FormControl>
        {formData.type === 'hook' ?
          <React.Fragment>
            <TextField
              label="URL"
              name="hookUrl"
              value={formData.hookUrl}
              required
              fullWidth
              error={!!errors.hookUrl}
              helperText={errors.hookUrl}
              margin="normal"
              onChange={handleChange}
            /><TextField
              label="Token"
              name="hookToken"
              value={formData.hookToken}
              required
              fullWidth
              margin="normal"
              onChange={handleChange}
            /></React.Fragment> : null}
        {formData.type === 'dingtalk' ?
          <React.Fragment>
            <TextField
              label="app Key"
              name="appKey"
              value={formData.dtAppKey}
              required
              fullWidth
              margin="normal"
              onChange={handleChange}
            /><TextField
              label="app secret"
              name="dtAppSecret"
              value={formData.dtAppSecret}
              required
              fullWidth
              margin="normal"
              onChange={handleChange}
            /></React.Fragment> : null}
        {formData.type === 'wecom' ?
          <React.Fragment>
            <TextField
              label="corp id"
              name="wcCorpId"
              value={formData.wcCorpId}
              required
              fullWidth
              margin="normal"
              onChange={handleChange}
            /><TextField
              label="corp secret"
              name="wcCorpSecret"
              value={formData.wcCorpSecret}
              required
              fullWidth
              margin="normal"
              onChange={handleChange}
            /></React.Fragment> : null}
        {formData.type === 'feishu' ?
          <React.Fragment>
            <TextField
              label="app id"
              name="fsAppId"
              value={formData.fsAppId}
              required
              fullWidth
              margin="normal"
              onChange={handleChange}
            /><TextField
              label="app secret"
              name="fsAppSecret"
              value={formData.fsAppSecret}
              required
              fullWidth
              margin="normal"
              onChange={handleChange}
            /></React.Fragment> : null}
      </DialogContent>
      <DialogActions>
        <Button autoFocus onClick={onClose}>
          {t('common.cancel')}
        </Button>
        <Button onClick={() => handelSubmit()} disabled={loading || Object.keys(errors).length > 0}>{t('common.save')}</Button>
      </DialogActions>
    </Dialog>
  )
}

export default NotificationDialog;