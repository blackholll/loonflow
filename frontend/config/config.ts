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
          "component": '../../src/pages/Ticket/DutyTicket',
        },
        {
          "path": "/tickets/owner",
          "name": "我的申请",
          "component": '../../src/pages/Ticket/OwnerTicket',

        },
        {
          "path": "/tickets/relation",
          "name": "与我相关",
          "component": '../../src/pages/Ticket/RelatedTicket',

        },
        {
          "path": "/tickets/view",
          "name": "工单查看",
          "component": '../../src/pages/Ticket/ViewTicket',

        },
        {
          "path": "/tickets/intervene",
          "name": "工单干预",
          "access": 'workflowAdmin',
          "component": '../../src/pages/Ticket/InterveneTicket',

        },
        {
          "path": "/tickets/all",
          "access": 'superAdmin',
          "name": "所有工单",
          "component": '../../src/pages/Ticket/AllTicket',

        }
      ]
    },
    {
      path: '/workflows',
      name: '工作流管理',
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
      "name": "用户及权限",
      // "icon": "dashboard",
      "icon": "ApartmentOutlined",
      access: 'superAdmin',
      routes: [
        {
          "path": "/users/user",
          "name": "用户管理",
          "component": '../../src/pages/User/User/UserList',

        },
        {
          "path": "/users/role",
          "name": "角色管理",
          "component": '../../src/pages/User/Role/RoleList',

        },
        {
          "path": "/users/dept",
          "name": "部门管理",
          "component": '../../src/pages/User/Dept/DeptList',

        },
        {
          "path": "/users/app",
          "name": "调用权限",
          "component": '../../src/pages/User/Token/TokenList',
        }
      ],
    },
    {
      path: '/manage',
      name: '系统配置',
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
