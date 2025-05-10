import React, { useState } from 'react';
import { Tabs, Tab } from '@mui/material';
import { useTranslation } from 'react-i18next';
import User from './User';
import Dept from './Dept';


interface Department {
    id: string;
    name: string;
    label: string;
    leader_info: basicUser;
    children?: Department[];
    has_children?: boolean;
}

interface basicUser {
    id: string;
    alias: string;
}


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