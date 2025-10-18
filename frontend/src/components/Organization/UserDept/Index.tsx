import { Tab, Tabs } from '@mui/material';
import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import Dept from './Dept';
import User from './User';



function UserDept() {
    const [activeTab, setActiveTab] = useState('users');
    const { t } = useTranslation();

    return (
        <div style={{ padding: '20px' }}>
            <Tabs
                value={activeTab}
                onChange={(_, newValue) => setActiveTab(newValue)}
            >
                <Tab value="users" label={t('common.user')} />
                <Tab value="depts" label={t('common.dept')} />
            </Tabs>

            {activeTab === 'users' ? (
                <User />
            ) : (
                <div><Dept /></div>
            )}
        </div>
    );
}

export default UserDept;