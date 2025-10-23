import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import dayjs from 'dayjs';
import 'dayjs/locale/en';
import 'dayjs/locale/zh-cn';
import React from 'react';
import { useTranslation } from 'react-i18next';

interface DynamicLocalizationProviderProps {
    children: React.ReactNode;
}

function DynamicLocalizationProvider({ children }: DynamicLocalizationProviderProps) {
    const { i18n } = useTranslation();

    // 根据当前语言设置 dayjs locale
    const getDayjsLocale = React.useCallback(() => {
        switch (i18n.language) {
            case 'zh-CN':
                return 'zh-cn';
            case 'en-US':
            default:
                return 'en';
        }
    }, [i18n.language]);

    // 设置 dayjs locale
    React.useEffect(() => {
        const locale = getDayjsLocale();
        dayjs.locale(locale);
    }, [getDayjsLocale]);

    return (
        <LocalizationProvider
            dateAdapter={AdapterDayjs}
            adapterLocale={getDayjsLocale()}
        >
            {children}
        </LocalizationProvider>
    );
}

export default DynamicLocalizationProvider;
