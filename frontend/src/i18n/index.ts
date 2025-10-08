import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

import enTranslation from './locales/en-US.json';
import zhTranslation from './locales/zh-CN.json';

console.log('enTranslation:', enTranslation);

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