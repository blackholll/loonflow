import AccountCircle from '@mui/icons-material/AccountCircle';
import { AppBar, Box, Button, CssBaseline, Dialog, DialogActions, DialogContent, DialogTitle, Drawer, FormControl, IconButton, InputLabel, Menu, MenuItem, Select, Tab, Tabs, TextField, Toolbar, Typography } from '@mui/material';
import React, { ReactNode } from 'react';
import { useTranslation } from 'react-i18next';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import useSnackbar from '../hooks/useSnackbar';
import { changePassword, getMyProfile, updateMyProfile } from '../services/user';
import { logoutState } from '../store/authSlice';
import { removeCookie } from '../utils/cookie';
import MenuList from './MenuList';


const drawerWidth = 240;

interface LayoutProps {
  children: ReactNode;
}

const Layout = ({ children }: LayoutProps) => {
  const { t, i18n } = useTranslation();
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const [openUserInfo, setOpenUserInfo] = React.useState(false);
  const [language, setLanguage] = React.useState(i18n.language);
  const [tabValue, setTabValue] = React.useState(0);
  const [passwordForm, setPasswordForm] = React.useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  });
  const [passwordErrors, setPasswordErrors] = React.useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  });
  const user = useSelector((state: any) => state.auth.user);
  const tenant = useSelector((state: any) => state.tenant);
  const { showMessage } = useSnackbar();
  const handleMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    dispatch(logoutState());
    removeCookie('jwtToken');
    navigate('/signin');
    handleClose();
  };

  const handleOpenUserInfo = () => {
    setOpenUserInfo(true);
    handleClose();
  };

  const handleCloseUserInfo = () => {
    setOpenUserInfo(false);
    setTabValue(0);
    setPasswordForm({
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    });
    setPasswordErrors({
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    });
  };

  const handleLanguageChange = async (event: any) => {
    const newLang = event.target.value;
    try {
      await updateMyProfile(newLang);
      setLanguage(newLang);
      i18n.changeLanguage(newLang);
      showMessage(t('layout.updateProfileSuccess'), 'success');
    } catch (error) {
      showMessage(t('layout.updateProfileFail'), 'error');
      console.error('Failed to update language setting:', error);
    }
  };

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handlePasswordInputChange = (field: string) => (event: React.ChangeEvent<HTMLInputElement>) => {
    const value = event.target.value;
    setPasswordForm(prev => ({
      ...prev,
      [field]: value
    }));

    // 清除错误信息
    setPasswordErrors(prev => ({
      ...prev,
      [field]: ''
    }));
  };

  const validatePasswordForm = () => {
    const errors = {
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    };

    if (!passwordForm.currentPassword) {
      errors.currentPassword = t('layout.currentPasswordRequired');
    }
    if (!passwordForm.newPassword) {
      errors.newPassword = t('layout.newPasswordRequired');
    }
    if (!passwordForm.confirmPassword) {
      errors.confirmPassword = t('layout.confirmPasswordRequired');
    }
    if (passwordForm.newPassword && passwordForm.confirmPassword && passwordForm.newPassword !== passwordForm.confirmPassword) {
      errors.confirmPassword = t('layout.passwordsNotMatch');
    }

    setPasswordErrors(errors);
    return !Object.values(errors).some(error => error !== '');
  };

  const handleChangePassword = async () => {
    if (!validatePasswordForm()) {
      return;
    }

    try {
      const result = await changePassword(passwordForm.currentPassword, passwordForm.newPassword, passwordForm.confirmPassword);
      if (result.code === -1) {
        showMessage(result.msg, 'error');
        return;
      }
      showMessage(t('layout.changePasswordSuccess'), 'success');
      setPasswordForm({
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      });
      setPasswordErrors({
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      });
    } catch (error: any) {
      const errorMessage = error.response?.data?.msg || t('layout.changePasswordFail');
      showMessage(errorMessage, 'error');
      console.error('Failed to change password:', error);
    }
  };

  React.useEffect(() => {
    const fetchUserLanguage = async () => {
      try {
        const response = await getMyProfile();
        if (response.code === 0 && response.data.myProfile.language) {
          setLanguage(response.data.myProfile.language);
          i18n.changeLanguage(response.data.myProfile.language);
        }
      } catch (error) {
        console.error('Failed to fetch user language setting:', error);
      }
    };
    fetchUserLanguage();
  }, [i18n]);

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1, backgroundColor: 'white', boxShadow: 'none', borderBottom: (theme) => `1px solid ${theme.palette.divider}` }}>
        <Toolbar sx={{ justifyContent: 'space-between' }}>
          {tenant?.tenantInfo?.logoPath ? (
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <img src={tenant.tenantInfo.logoPath} alt="Logo" style={{ height: '40px', marginRight: '10px' }} />
            </Box>
          ) : (
            <Typography variant="h6" noWrap component="div" sx={{ color: 'gray' }}>
              Loonflow
            </Typography>
          )}
          <div>
            <IconButton
              size="large"
              aria-label="account of current user"
              aria-controls="menu-appbar"
              aria-haspopup="true"
              onClick={handleMenu}
              color="inherit"
              sx={{ color: 'gray' }}
            >
              <AccountCircle />
              <Typography variant="body1" sx={{ ml: 1, color: 'gray' }}>
                {user?.alias || user?.name}
              </Typography>
            </IconButton>
            <Menu
              id="menu-appbar"
              anchorEl={anchorEl}
              anchorOrigin={{
                vertical: 'bottom',
                horizontal: 'right',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              open={Boolean(anchorEl)}
              onClose={handleClose}
            >
              <MenuItem onClick={handleOpenUserInfo}>{t('common.userInfo')}</MenuItem>
              <MenuItem onClick={handleLogout}>{t('common.logout')}</MenuItem>
            </Menu>
          </div>
        </Toolbar>
      </AppBar>
      <Dialog open={openUserInfo} onClose={handleCloseUserInfo} maxWidth="sm" fullWidth>
        <DialogTitle>{t('common.userInfo')}</DialogTitle>
        <DialogContent>
          <Box sx={{ mt: 2 }}>
            <Tabs value={tabValue} onChange={handleTabChange} aria-label="user info tabs">
              <Tab label={t('common.userInfo')} />
              <Tab label={t('layout.changePassword')} />
            </Tabs>

            {tabValue === 0 && (
              <Box sx={{ mt: 2 }}>
                <Typography variant="subtitle1">{t('layout.name')}: {user?.name}</Typography>
                <Typography variant="subtitle1">{t('common.alias')}: {user?.alias}</Typography>
                <Typography variant="subtitle1">{t('common.email')}: {user?.email}</Typography>
                <FormControl fullWidth sx={{ mt: 2 }}>
                  <InputLabel>{t('common.language')}</InputLabel>
                  <Select
                    value={language}
                    label={t('common.language')}
                    onChange={handleLanguageChange}
                  >
                    <MenuItem value="zh-CN">简体中文</MenuItem>
                    <MenuItem value="en-US">American English</MenuItem>
                  </Select>
                </FormControl>
              </Box>
            )}

            {tabValue === 1 && (
              <Box sx={{ mt: 2 }}>
                <TextField
                  fullWidth
                  label={t('layout.currentPassword')}
                  type="password"
                  value={passwordForm.currentPassword}
                  onChange={handlePasswordInputChange('currentPassword')}
                  error={!!passwordErrors.currentPassword}
                  helperText={passwordErrors.currentPassword}
                  sx={{ mb: 2 }}
                />
                <TextField
                  fullWidth
                  label={t('layout.newPassword')}
                  type="password"
                  value={passwordForm.newPassword}
                  onChange={handlePasswordInputChange('newPassword')}
                  error={!!passwordErrors.newPassword}
                  helperText={passwordErrors.newPassword}
                  sx={{ mb: 2 }}
                />
                <TextField
                  fullWidth
                  label={t('layout.confirmPassword')}
                  type="password"
                  value={passwordForm.confirmPassword}
                  onChange={handlePasswordInputChange('confirmPassword')}
                  error={!!passwordErrors.confirmPassword}
                  helperText={passwordErrors.confirmPassword}
                  sx={{ mb: 2 }}
                />
              </Box>
            )}
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseUserInfo}>{t('common.close')}</Button>
          {tabValue === 1 && (
            <Button onClick={handleChangePassword} variant="contained" color="primary">
              {t('layout.changePassword')}
            </Button>
          )}
        </DialogActions>
      </Dialog>
      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: drawerWidth,
            boxSizing: 'border-box',
          },
        }}
      >
        <Toolbar />
        <MenuList />
      </Drawer>
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          bgcolor: 'background.default',
          p: 3,
        }}
      >
        <Toolbar />
        {children}
      </Box>
    </Box>
  );
};

export default Layout;
