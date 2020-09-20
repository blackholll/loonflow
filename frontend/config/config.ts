// https://umijs.org/config/
import { defineConfig } from 'umi';
import defaultSettings from './defaultSettings';
import proxy from './proxy';
import UserList from "@/pages/user/User";

const { REACT_APP_ENV } = process.env;

export default defineConfig({
  hash: true,
  antd: {},
  dva: {
    hmr: true,
  },
  layout: {
    name: 'Ant Design Pro',
    locale: true,
    siderWidth: 208,
  },
  locale: {
    // default zh-CN
    default: 'zh-CN',
    // default true, when it is true, will use `navigator.language` overwrite default
    antd: true,
    baseNavigator: true,
  },
  dynamicImport: {
    loading: '@/components/PageLoading/index',
  },
  targets: {
    ie: 11,
  },
  // umi routes: https://umijs.org/docs/routing
  routes: [
    {
      path: '/user',
      layout: false,
      routes: [
        {
          name: 'login',
          path: '/user/login',
          component: './user/login',
        },
      ],
    },
    {
      path: '/workbench',
      name: '工作台',
      icon: 'ScheduleOutlined',
      component: './Workbench',
    },
    {
      "path": "/tickets",
      "name": "工单管理",
      "icon": "SolutionOutlined",
      routes: [
        {
          "path": "/tickets/duty",
          "name": "我的待办",
          "component": '../../src/pages/ticket/DutyTicket',
        },
        {
          "path": "/tickets/owner",
          "name": "我的申请",
          "component": '../../src/pages/ticket/OwnerTicket',

        },
        {
          "path": "/tickets/relation",
          "name": "与我相关",
          "component": '../../src/pages/ticket/RelatedTicket',

        },
        {
          "path": "/tickets/view",
          "name": "工单查看",
          "component": '../../src/pages/ticket/ViewTicket',

        },
        {
          "path": "/tickets/intervene",
          "name": "工单干预",
          "component": '../../src/pages/ticket/InterfereTicket',

        },
        {
          "path": "/tickets/all",
          "name": "所有工单",
          "component": '../../src/pages/ticket/AllTicket',

        }
      ]
    },
    {
      path: '/workflows',
      name: '工作流管理',
      icon: 'DeploymentUnitOutlined',
      component: './Workbench',
    },
    {
      "path": "/users",
      "name": "用户及权限",
      // "icon": "dashboard",
      "icon": "ApartmentOutlined",
      routes: [
        {
          "path": "/users/user",
          "name": "用户管理",
          "component": '../../src/pages/user/User/UserList',

        },
        {
          "path": "/users/rule",
          "name": "角色管理"
        },
        {
          "path": "/users/dept",
          "name": "部门管理"
        },
        {
          "path": "/users/app",
          "name": "调用权限"
        }
      ],
    },
    {
      path: '/manage',
      name: '系统配置',
      icon: 'ToolOutlined',
      component: './Manage',
    },
    {
      path: '/',
      redirect: '/workbench',
    },
    {
      component: './404',
    },
  ],
  // Theme for antd: https://ant.design/docs/react/customize-theme-cn
  theme: {
    // ...darkTheme,
    'primary-color': defaultSettings.primaryColor,
  },
  // @ts-ignore
  title: false,
  ignoreMomentLocale: true,
  proxy: proxy[REACT_APP_ENV || 'dev'],
  manifest: {
    basePath: '/',
  },
});