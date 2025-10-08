import React, { useState, useEffect } from 'react';
import { List, ListItemButton, ListItemText, ListItemIcon, Collapse } from '@mui/material';
import { useNavigate, useLocation } from 'react-router-dom'; // 引入 useLocation
import useMenuItems from './MenuItem';

interface IMenuItem {
  text: string;
  path: string; // 添加 path 属性
  component?: React.ComponentType;
  isSingleLayout?: boolean;
  isVisibleInMenu?: boolean;
  children?: IMenuItem[];
}

const MenuList = () => {
  const [open, setOpen] = useState<{ [key: string]: boolean }>({});
  const [lastPath, setLastPath] = useState<string>('');
  const navigate = useNavigate();
  const location = useLocation(); // 获取当前路径
  const menuItems = useMenuItems();

  // 根据当前路由自动展开对应的父菜单，并收起其他父菜单
  useEffect(() => {
    const findParentMenu = (items: IMenuItem[], currentPath: string): string | null => {
      for (const item of items) {
        if (item.children) {
          for (const child of item.children) {
            if (child.path === currentPath) {
              return item.text;
            }
          }
        }
      }
      return null;
    };

    const parentMenuText = findParentMenu(menuItems, location.pathname);

    // 只有当路径真正改变时才重置菜单状态
    if (location.pathname !== lastPath) {
      setLastPath(location.pathname);

      // 重置所有菜单状态，只展开当前需要的父菜单
      const newOpenState: { [key: string]: boolean } = {};
      if (parentMenuText) {
        newOpenState[parentMenuText] = true;
      }
      setOpen(newOpenState);
    }
  }, [location.pathname, menuItems, lastPath]);

  const handleClick = (text: string) => {
    setOpen((prev) => {
      const isCurrentlyOpen = prev[text] || false;
      // 如果当前菜单是关闭的，则关闭所有其他菜单，只打开当前菜单
      if (!isCurrentlyOpen) {
        const newState: { [key: string]: boolean } = {};
        newState[text] = true;
        return newState;
      } else {
        // 如果当前菜单是打开的，则关闭它
        return { ...prev, [text]: false };
      }
    });
  };

  const handleItemClick = (item: IMenuItem) => {
    if (item.children) {
      handleClick(item.text);
    } else {
      navigate(`${item.path}`);
    }
  };

  // 检查是否为当前选中的菜单项
  const isSelected = (path: string) => location.pathname === path;

  return (
    <List>
      {menuItems.filter((item) => item.isVisibleInMenu).map((item) => (
        <div key={item.text}>
          <ListItemButton
            onClick={() => handleItemClick(item)}
            selected={isSelected(item.path)} // 判断是否选中
            sx={{ backgroundColor: isSelected(item.path) ? '#f0f0f0' : 'inherit' }} // 选中时背景色变化
          >
            {item.icon && <ListItemIcon sx={{ minWidth: 24, marginRight: 1 }}><item.icon /></ListItemIcon>}
            <ListItemText primary={item.text} />
          </ListItemButton>
          {item.children && (
            <Collapse in={!!open[item.text]} timeout="auto" unmountOnExit>
              <List component="div" disablePadding>
                {item.children.map((child) => (
                  <ListItemButton
                    key={child.text}
                    onClick={() => handleItemClick(child)}
                    selected={isSelected(child.path)} // 判断二级菜单是否选中
                    sx={{
                      paddingLeft: 4, // 二级菜单缩进
                      backgroundColor: isSelected(child.path) ? '#f0f0f0' : 'inherit', // 选中时背景色变化
                    }}
                  >
                    <ListItemText primary={child.text} />
                  </ListItemButton>
                ))}
              </List>
            </Collapse>
          )}
        </div>
      ))}
    </List>
  );
};

export default MenuList;
