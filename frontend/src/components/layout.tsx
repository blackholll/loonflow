import React, { ReactNode } from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { AppBar, Toolbar, Typography, CssBaseline, Drawer, List, ListItem, ListItemText, Box, Menu, MenuItem, IconButton, Dialog, DialogTitle, DialogContent, DialogActions, Button, Select, FormControl, InputLabel, Avatar } from '@mui/material';
import { Link } from 'react-router-dom';
import MenuList from './MenuList';
import Home from './home/HomePage';
import { useTranslation } from 'react-i18next';
import AccountCircle from '@mui/icons-material/AccountCircle';
import { logoutState } from '../store/authSlice';
import { removeCookie } from '../utils/cookie';
import { updateMyProfile, getMyProfile } from '../services/user';
import useSnackbar from '../hooks/useSnackbar';


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

  React.useEffect(() => {
    const fetchUserLanguage = async () => {
      try {
        const response = await getMyProfile();
        if (response.code === 0 && response.data.my_profile.language) {
          setLanguage(response.data.my_profile.language);
          i18n.changeLanguage(response.data.my_profile.language);
        }
      } catch (error) {
        console.error('Failed to fetch user language setting:', error);
      }
    };
    fetchUserLanguage();
  }, []);

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1, backgroundColor: 'white', boxShadow: 'none', borderBottom: (theme) => `1px solid ${theme.palette.divider}` }}>
        <Toolbar sx={{ justifyContent: 'space-between' }}>
          {tenant?.tenantInfo?.logo_path ? (
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <img src={tenant.tenantInfo.logo_path} alt="Logo" style={{ height: '40px', marginRight: '10px' }} />
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
      <Dialog open={openUserInfo} onClose={handleCloseUserInfo}>
        <DialogTitle>{t('common.userInfo')}</DialogTitle>
        <DialogContent>
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
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseUserInfo}>{t('common.close')}</Button>
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
