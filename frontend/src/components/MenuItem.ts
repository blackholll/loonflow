// src/components/MenuItem.ts
import { useTranslation } from 'react-i18next';
import Home from './home/HomePage';
import Home2 from './home2/HomePage';
import SignIn from '../SignIn';
import { Home as HomeIcon, AccountTree as AccountTreeIcon, Assignment as AssignmentIcon, Schema as SchemaIcon, Settings as SettingsIcon } from '@mui/icons-material';


export interface IMenuItem {
  text: string;
  path: string;
  icon?: React.ComponentType;
  component?: React.ComponentType;
  isSingleLayout?: boolean; // 是否使用单独的布局，即不显示菜单和顶栏
  isVisibleInMenu?: boolean;// 是否显示在菜单中
  requireAuth?: boolean; // 是否需要登录
  children?: IMenuItem[];
}

const useMenuItems=():IMenuItem[] => {
  const { t } = useTranslation();
  return [
    // { text: t('menu.workbench'), path: '', component: Home, isVisibleInMenu: true, icon: HomeIcon },
    { text: t('menu.workbench'), path: '/', component: Home, isVisibleInMenu: true, icon: HomeIcon },
    {
      text: t('menu.ticketManagement'),
      path: '/ticket',
      icon: AssignmentIcon,
      isVisibleInMenu: true,
      children: [
        { text: t('menu.ticketDuty'), path: '/ticket/duty', component: Home },
        { text: t('menu.ticketOwner'), path: '/ticket/owner', component: Home2 },
        { text: t('menu.ticketRelation'), path: '/ticket/relation', component: Home },
        { text: t('menu.ticketView'), path: '/ticket/view', component: Home },
        { text: t('menu.ticketIntervene'), path: '/ticket/intervene', component: Home },
        { text: t('menu.ticketAll'), path: '/ticket/all', component: Home },
      ],
    },
    {
      text: t('menu.workflowManagement'),
      path: '/workflow',
      icon: SchemaIcon,
      isVisibleInMenu: true,
      component: Home
    },
    {
      text: t('menu.organization'),
      path: '/organization',
      icon: AccountTreeIcon,
      isVisibleInMenu: true,
      children: [
        { text: t('menu.userAndDept'), path: '/organization/userdept', component: Home },
        { text: t('menu.role'), path: '/organization/role', component: Home },
      ],
    },
    {
      text: t('menu.settings'),
      path: '/settings',
      icon: SettingsIcon,
      isVisibleInMenu: true,
      children: [
        { text: t('menu.tenant'), path: '/settings/tenant', component: Home },
        { text: t('menu.app'), path: '/settings/app', component: Home },
        { text: t('menu.notice'), path: '/settings/notice', component: Home },
      ]
    },
    { text: t('menu.signin'), path: 'signin', component: SignIn, isSingleLayout: true, isVisibleInMenu: false },
  ];
};

export default useMenuItems;
