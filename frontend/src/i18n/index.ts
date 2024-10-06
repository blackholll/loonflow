import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

// 导入语言资源
import enTranslation from './locales/en.json';
import zhTranslation from './locales/zh.json';

console.log('enTranslation:', enTranslation);

// 定义语言资源
const resources = {
  en: {
    translation: enTranslation,
    // translation: {
    //   welcomeMessage: 'Welcome to React!',
    // },
  },
  zh: {
    translation: zhTranslation,
  },
};

// 初始化 i18next
i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources,
    // lng: "zh",
    // fallbackLng: 'en', // 默认语言
    fallbackLng: 'zh', // 默认语言
    interpolation: {
      escapeValue: false, // 不转义变量值
    },
  });

export default i18n;