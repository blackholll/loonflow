import i18n from 'i18next';
import LanguageDetector from 'i18next-browser-languagedetector';
import { initReactI18next } from 'react-i18next';

// 导入中文翻译模块
import zhCommon from './locales/zh-CN/common.json';
import zhDepartment from './locales/zh-CN/department.json';
import zhLayout from './locales/zh-CN/layout.json';
import zhMenu from './locales/zh-CN/menu.json';
import zhRole from './locales/zh-CN/role.json';
import zhSetting from './locales/zh-CN/setting.json';
import zhSignIn from './locales/zh-CN/signIn.json';
import zhTicket from './locales/zh-CN/ticket.json';
import zhUser from './locales/zh-CN/user.json';
import zhWorkflow from './locales/zh-CN/workflow.json';
import zhWorkflowValidation from './locales/zh-CN/workflowValidation.json';

// 导入英文翻译模块
import enCommon from './locales/en-US/common.json';
import enDepartment from './locales/en-US/department.json';
import enLayout from './locales/en-US/layout.json';
import enMenu from './locales/en-US/menu.json';
import enRole from './locales/en-US/role.json';
import enSetting from './locales/en-US/setting.json';
import enSignIn from './locales/en-US/signIn.json';
import enTicket from './locales/en-US/ticket.json';
import enUser from './locales/en-US/user.json';
import enWorkflow from './locales/en-US/workflow.json';
import enWorkflowValidation from './locales/en-US/workflowValidation.json';

// 合并翻译资源
const resources = {
  'en-US': {
    translation: {
      layout: enLayout,
      common: enCommon,
      user: enUser,
      department: enDepartment,
      role: enRole,
      signIn: enSignIn,
      menu: enMenu,
      ticket: enTicket,
      workflow: enWorkflow,
      workflowValidation: enWorkflowValidation,
      setting: enSetting,
    },
  },
  'zh-CN': {
    translation: {
      layout: zhLayout,
      common: zhCommon,
      user: zhUser,
      department: zhDepartment,
      role: zhRole,
      signIn: zhSignIn,
      menu: zhMenu,
      ticket: zhTicket,
      workflow: zhWorkflow,
      workflowValidation: zhWorkflowValidation,
      setting: zhSetting,
    },
  },
};

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources,
    fallbackLng: 'en-US',
    interpolation: {
      escapeValue: false,
    },
  });

export default i18n;