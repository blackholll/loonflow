import React, { useState } from 'react';
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
  const navigate = useNavigate();
  const location = useLocation(); // 获取当前路径
  const menuItems = useMenuItems();

  const handleClick = (text: string) => {
    setOpen((prev) => ({ ...prev, [text]: !prev[text] }));
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
            {item.icon && <ListItemIcon sx={{ minWidth: 24, marginRight: 1 }}><item.icon/></ListItemIcon>}
            <ListItemText primary={item.text} />
          </ListItemButton>
          {item.children && (
            <Collapse in={open[item.text]} timeout="auto" unmountOnExit>
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
