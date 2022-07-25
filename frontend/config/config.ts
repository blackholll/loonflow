// https://umijs.org/config/
import { defineConfig } from 'umi';
import defaultSettings from './defaultSettings';
import proxy from './proxy';
import UserList from "@/pages/User/User";
import RoleList from "@/pages/User/Role/RoleList";
import DeptList from "@/pages/User/Dept/DeptList";
import TokenList from "@/pages/User/Token/TokenList";

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
          component: './User/login',
        },
      ],
    },
    {
      path: '/workbench',
      name: 'workbench',
      icon: 'ScheduleOutlined',
      component: './Workbench',
    },
    {
      "path": "/tickets",
      "name": "tickets",
      "icon": "SolutionOutlined",
      routes: [
        {
          "path": "/tickets/duty",
          "name": "My to do",
          "component": '../../src/pages/Ticket/DutyTicket',
        },
        {
          "path": "/tickets/owner",
          "name": "My application",
          "component": '../../src/pages/Ticket/OwnerTicket',

        },
        {
          "path": "/tickets/relation",
          "name": "Related to me",
          "component": '../../src/pages/Ticket/RelatedTicket',

        },
        {
          "path": "/tickets/view",
          "name": "Work order view",
          "component": '../../src/pages/Ticket/ViewTicket',

        },
        {
          "path": "/tickets/intervene",
          "name": "work order intervention",
          "access": 'workflowAdmin',
          "component": '../../src/pages/Ticket/InterveneTicket',

        },
        {
          "path": "/tickets/all",
          "access": 'superAdmin',
          "name": "All work orders",
          "component": '../../src/pages/Ticket/AllTicket',

        }
      ]
    },
    {
      path: '/workflows',
      name: 'Workflow Management',
      access: 'workflowAdmin',
      icon: 'DeploymentUnitOutlined',
      component: '../../src/pages/Workflow/WorkflowList',
    },
    {
      path: '/workflows/detail',
      component: '../../src/pages/Workflow/WorkflowDetail',

    },
    {
      "path": "/users",
      "name": "Users and permissions",
      // "icon": "dashboard",
      "icon": "ApartmentOutlined",
      access: 'superAdmin',
      routes: [
        {
          "path": "/users/user",
          "name": "User Management",
          "component": '../../src/pages/User/User/UserList',

        },
        {
          "path": "/users/role",
          "name": "Role management",
          "component": '../../src/pages/User/Role/RoleList',

        },
        {
          "path": "/users/dept",
          "name": "Department management",
          "component": '../../src/pages/User/Dept/DeptList',

        },
        {
          "path": "/users/app",
          "name": "Call permission",
          "component": '../../src/pages/User/Token/TokenList',
        }
      ],
    },
    {
      path: '/manage',
      name: 'System Configuration',
      icon: 'ToolOutlined',
      access: 'superAdmin',
      component: './Manage',
    },
    {
      path: 'account/changepwd',
      layout: false,
      icon: 'ToolOutlined',
      component: './Account/ChangePwd',
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
