
import { defineConfig } from "umi";

export default defineConfig({
  plugins: ['@umijs/plugins/dist/react-query', '@umijs/plugins/dist/antd', '@umijs/plugins/dist/locale'],
  reactQuery: {},
  routes: [
    {
        path: '/workbench',
        title: 'menu.workbench',
        component: '@/pages/Workbench',
    },
    {
      path: '/user',
      routes: [
        {
          title: 'login',
          layout: false,
          path: '/user/login',
          component: '@/pages/User/Login',
        },
      ],
    },
    {
      path: "/tickets",
      title: "menu.ticket.manager",
      routes: [
        {
          path: "/tickets/duty",
          title: "menu.ticket.duty",
          component: 'index',
          // "component": '../../src/pages/Ticket/DutyTicket',
        },
        {
          path: "/tickets/owner",
          title: "menu.ticket.owner",
          component: 'index',
          // "component": '../../src/pages/Ticket/OwnerTicket',

        },
        {
          path: "/tickets/relation",
          title: "menu.ticket.related",
          component: 'index',
          // "component": '../../src/pages/Ticket/RelatedTicket',

        },
        {
          path: "/tickets/view",
          title: "menu.ticket.view",
          component: 'index',
          // "component": '../../src/pages/Ticket/ViewTicket',

        },
        {
          path: "/tickets/intervene",
          title: "menu.ticket.intervene",
          component: 'index',
          // "component": '../../src/pages/Ticket/InterveneTicket',

        },
        {
          path: "/tickets/all",
          access: 'admin',
          title: "menu.ticket.all",
          component: 'index',
          // "component": '../../src/pages/Ticket/AllTicket',

        }
      ]
    },
    {
      path: '/workflows',
      title: 'menu.workflow.manager',
      component: 'index',
      // component: '../../src/pages/Workflow/WorkflowList',
    },
    {
      path: '/workflows/detail',
      component: 'index',
      // component: '../../src/pages/Workflow/WorkflowDetail',
    },
    {
      path: "/users",
      title: "menu.organization",
      routes: [
        {
          path: "/users/user",
          title: "menu.organization.department_and_user",
          component: 'index',
          // "component": '../../src/pages/User/User/UserList',

        },
        {
          path: "/users/role",
          title: "menu.organization.role",
          component: 'index',
          // "component": '../../src/pages/User/Role/RoleList',

        }
      ],
    },
    {
      path: '/manage',
      title: 'menu.settings',
      routes: [
        {
          path: "users/role",
          title: "menu.settings.tenant",
          component: 'index',
          // "component": '../../src/pages/User/Role/RoleList',
        },
        {
          path: "users/role",
          title: "menu.settings.application",
          component: 'index',
          // "component": '../../src/pages/User/Role/RoleList',
        },
        {
          path: "users/role",
          title: "menu.settings.notification",
          component: 'index',
          // "component": '../../src/pages/User/Role/RoleList',
        }
      ]
    },
    {
      path: 'account/changepwd',
      component: 'index',
      // component: './Account/ChangePwd',
    }      
  ],
  locale: {
    title: true,
    antd: true,
    baseNavigator: true,
    baseSeparator: '-',
  },
  npmClient: 'yarn',
  proxy: {
    '/api': {
      'target': 'http://127.0.0.1:6060/',
      'changeOrigin': true,
      'pathRewrite': { '^/api' : 'api' },
    },
  },
});
