import AccountCircle from '@mui/icons-material/AccountCircle';
import ContentCopy from '@mui/icons-material/ContentCopy';
import {
  Alert,
  AppBar,
  Box,
  Button,
  Chip,
  CssBaseline,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Drawer,
  FormControl,
  IconButton,
  InputAdornment,
  InputLabel,
  Menu,
  MenuItem,
  Select,
  Stack,
  Tab,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Tabs,
  TextField,
  Toolbar,
  Typography,
} from '@mui/material';
import React, { ReactNode } from 'react';
import { useTranslation } from 'react-i18next';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import useSnackbar from '../hooks/useSnackbar';
import {
  changePassword,
  createPersonalAccessToken,
  getMyProfile,
  listPersonalAccessTokens,
  revokePersonalAccessToken,
  updateMyProfile,
} from '../services/user';
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
  const [patTokens, setPatTokens] = React.useState<
    { id: string; label: string; maskedToken: string; expiresAt: string; lastUsedAt: string; revoked: boolean }[]
  >([]);
  const [patLoading, setPatLoading] = React.useState(false);
  const [patLabel, setPatLabel] = React.useState('');
  const [patExpiresDays, setPatExpiresDays] = React.useState<number>(90);
  const [patCreatedToken, setPatCreatedToken] = React.useState<string | null>(null);
  const [patCreatedDialogOpen, setPatCreatedDialogOpen] = React.useState(false);
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
    setPatTokens([]);
    setPatLabel('');
    setPatExpiresDays(90);
    setPatCreatedToken(null);
    setPatCreatedDialogOpen(false);
  };

  const loadPersonalAccessTokens = React.useCallback(async () => {
    setPatLoading(true);
    try {
      const res = await listPersonalAccessTokens();
      if (res.code === 0) {
        setPatTokens(res.data?.personalAccessTokenList ?? []);
      } else {
        setPatTokens([]);
        showMessage(res.msg || t('layout.patLoadFailed'), 'error');
      }
    } catch (e) {
      showMessage(t('layout.patLoadFailed'), 'error');
      setPatTokens([]);
    } finally {
      setPatLoading(false);
    }
  }, [showMessage, t]);

  const handleGeneratePat = async () => {
    try {
      const res = await createPersonalAccessToken({
        label: patLabel.trim(),
        expiresInDays: patExpiresDays,
      });
      if (res.code === 0 && res.data?.token) {
        setPatCreatedToken(res.data.token);
        setPatCreatedDialogOpen(true);
        setPatLabel('');
        await loadPersonalAccessTokens();
        showMessage(t('common.addSuccess'), 'success');
      } else {
        showMessage(res.msg || t('layout.patCreateFailed'), 'error');
      }
    } catch (e) {
      showMessage(t('layout.patCreateFailed'), 'error');
    }
  };

  const handleRevokePat = async (tokenId: string) => {
    if (!window.confirm(t('layout.patRevokeConfirm'))) {
      return;
    }
    try {
      const res = await revokePersonalAccessToken(tokenId);
      if (res.code === 0) {
        showMessage(t('layout.patRevokeSuccess'), 'success');
        await loadPersonalAccessTokens();
      } else {
        showMessage(res.msg || t('layout.patRevokeFailed'), 'error');
      }
    } catch (e) {
      showMessage(t('layout.patRevokeFailed'), 'error');
    }
  };

  const handleCopyPat = async (value: string) => {
    try {
      await navigator.clipboard.writeText(value);
      showMessage(t('layout.patCopied'), 'success');
    } catch {
      showMessage(t('layout.patCopyFailed'), 'error');
    }
  };

  React.useEffect(() => {
    if (openUserInfo && tabValue === 2) {
      void loadPersonalAccessTokens();
    }
  }, [openUserInfo, tabValue, loadPersonalAccessTokens]);

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
      <Dialog open={openUserInfo} onClose={handleCloseUserInfo} maxWidth="md" fullWidth>
        <DialogTitle>{t('common.userInfo')}</DialogTitle>
        <DialogContent>
          <Box sx={{ mt: 2 }}>
            <Tabs value={tabValue} onChange={handleTabChange} aria-label="user info tabs">
              <Tab label={t('common.userInfo')} />
              <Tab label={t('layout.changePassword')} />
              <Tab label={t('layout.personalAccessToken')} />
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

            {tabValue === 2 && (
              <Box sx={{ mt: 2 }}>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  {t('layout.patTabDescription')}
                </Typography>
                <Stack spacing={2} direction={{ xs: 'column', sm: 'row' }} sx={{ mb: 2 }}>
                  <TextField
                    fullWidth
                    label={t('layout.patLabelOptional')}
                    value={patLabel}
                    onChange={(e) => setPatLabel(e.target.value)}
                  />
                  <FormControl fullWidth sx={{ minWidth: 200 }}>
                    <InputLabel>{t('layout.patExpiresIn')}</InputLabel>
                    <Select
                      label={t('layout.patExpiresIn')}
                      value={patExpiresDays}
                      onChange={(e) => setPatExpiresDays(Number(e.target.value))}
                    >
                      <MenuItem value={0}>{t('layout.patExpiresNever')}</MenuItem>
                      <MenuItem value={7}>{t('layout.patExpiresDays', { count: 7 })}</MenuItem>
                      <MenuItem value={30}>{t('layout.patExpiresDays', { count: 30 })}</MenuItem>
                      <MenuItem value={90}>{t('layout.patExpiresDays', { count: 90 })}</MenuItem>
                      <MenuItem value={180}>{t('layout.patExpiresDays', { count: 180 })}</MenuItem>
                      <MenuItem value={365}>{t('layout.patExpiresDays', { count: 365 })}</MenuItem>
                    </Select>
                  </FormControl>
                  <Button variant="contained" onClick={handleGeneratePat} sx={{ alignSelf: { sm: 'center' } }}>
                    {t('layout.patGenerate')}
                  </Button>
                </Stack>
                {patLoading ? (
                  <Typography>{t('layout.patLoading')}</Typography>
                ) : patTokens.length === 0 ? (
                  <Typography color="text.secondary">{t('layout.patListEmpty')}</Typography>
                ) : (
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell>{t('common.description')}</TableCell>
                        <TableCell>{t('layout.personalAccessToken')}</TableCell>
                        <TableCell>{t('layout.patExpiresIn')}</TableCell>
                        <TableCell>{t('common.actions')}</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {patTokens.map((row) => (
                        <TableRow key={row.id}>
                          <TableCell>{row.label || '—'}</TableCell>
                          <TableCell sx={{ fontFamily: 'monospace', wordBreak: 'break-all' }}>
                            {row.maskedToken}
                          </TableCell>
                          <TableCell>{row.expiresAt || t('layout.patExpiresNever')}</TableCell>
                          <TableCell>
                            {row.revoked ? (
                              <Chip size="small" label={t('layout.patRevoked')} />
                            ) : (
                              <Button size="small" color="error" onClick={() => handleRevokePat(row.id)}>
                                {t('layout.patRevoke')}
                              </Button>
                            )}
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                )}
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
      <Dialog
        open={patCreatedDialogOpen}
        onClose={() => {
          setPatCreatedDialogOpen(false);
          setPatCreatedToken(null);
        }}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>{t('layout.patCreatedTitle')}</DialogTitle>
        <DialogContent>
          <Alert severity="warning" sx={{ mb: 2 }}>
            {t('layout.patCreatedWarning')}
          </Alert>
          <TextField
            fullWidth
            multiline
            minRows={3}
            value={patCreatedToken || ''}
            InputProps={{
              readOnly: true,
              endAdornment: (
                <InputAdornment position="end">
                  <IconButton
                    aria-label="copy token"
                    onClick={() => patCreatedToken && void handleCopyPat(patCreatedToken)}
                    edge="end"
                  >
                    <ContentCopy />
                  </IconButton>
                </InputAdornment>
              ),
            }}
          />
        </DialogContent>
        <DialogActions>
          <Button
            onClick={() => {
              setPatCreatedDialogOpen(false);
              setPatCreatedToken(null);
            }}
          >
            {t('common.close')}
          </Button>
          <Button variant="contained" onClick={() => patCreatedToken && void handleCopyPat(patCreatedToken)}>
            {t('layout.patCopy')}
          </Button>
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
