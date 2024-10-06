import React, { ReactNode } from 'react';
import { Outlet } from 'react-router-dom';

import { AppBar, Toolbar, Typography, CssBaseline, Drawer, List, ListItem, ListItemText, Box } from '@mui/material';
import { Link } from 'react-router-dom';
import MenuList from './MenuList'; // 引入 MenuList 组件
import Home from './home/HomePage';

const drawerWidth = 240;

interface LayoutProps {
  children: ReactNode; // 定义 children 的类型
}

const Layout = ({ children }: LayoutProps) => {

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
        <Toolbar sx={{ justifyContent: 'space-between' }}>
          <Typography variant="h6" noWrap component="div">
            Loonflow
          </Typography>
          <Typography variant="body1">用户信息</Typography>
        </Toolbar>
      </AppBar>
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
        <Toolbar /> {/* 留出顶部空间 */}
        <MenuList />
      </Drawer>
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          bgcolor: 'background.default',
          p: 3,
          marginLeft: `${drawerWidth}px`,
          marginTop: '64px', // 确保内容不被 AppBar 遮挡
        }}
      >
        <Toolbar />
        {children}
      </Box>
    </Box>
  );
};

export default Layout;
