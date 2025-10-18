import { Autocomplete, CircularProgress, FormControl, TextField } from '@mui/material';
import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { getSimpleUsers } from '../../services/user';
import { ISimpleUser } from '../../types/user';
import ViewField from './ViewField';

interface UserFieldProps {
    value: string | null;
    onChange: (value: string) => void;
    mode: 'view' | 'edit';
    props: {
        multiple?: boolean;
        placeholder?: string;
        [key: string]: any;
    };
}

interface IOption {
    label: string;
    value: string;
}

function UserField({
    value = '',
    onChange,
    mode,
    props,
}: UserFieldProps) {
    const [loading, setLoading] = useState(false);
    const [users, setUsers] = useState<IOption[]>([]);
    const [selectedUsers, setSelectedUsers] = useState<IOption[]>([]);
    const [selectedUser, setSelectedUser] = useState<IOption | null>(null);
    const { t } = useTranslation();

    const isMultiple = props.multiple || false;

    const loadUsers = async (searchValue: string = '') => {
        if (loading) return;
        setLoading(true);
        try {
            const response = await getSimpleUsers(searchValue);
            if (response.code === 0) {
                setUsers(response.data.userInfoList.map((user: ISimpleUser) => ({ label: `${user.name}(${user.alias})`, value: user.id })) || []);
            }
        } catch (error) {
            console.error('加载用户列表失败:', error);
        } finally {
            setLoading(false);
        }
    };


    const fetchUsersByIds = async (userIds: string | string[]) => {
        if (!userIds || (Array.isArray(userIds) && userIds.length === 0)) {
            return [];
        }

        const ids = Array.isArray(userIds) ? userIds.join(',') : userIds;
        try {
            const response = await getSimpleUsers('', ids, 1, 1000);
            if (response.code === 0) {
                return response.data.userInfoList.map((user: ISimpleUser) => ({
                    label: `${user.name}(${user.alias})`,
                    value: user.id
                }));
            }
        } catch (error) {
            console.error('获取用户信息失败:', error);
        }
        return [];
    };

    // 处理值变化
    const handleChange = (newValue: IOption | IOption[] | null) => {
        let strValue = '';

        if (isMultiple) {
            setSelectedUsers(newValue as IOption[]);
            strValue = newValue ? (newValue as IOption[]).map(item => item.value).join(',') : '';
        } else {
            setSelectedUser(newValue as IOption);
            strValue = newValue ? (newValue as IOption).value : '';
        }
        onChange(strValue);
        console.log('🔍 UserField handleChange:', { newValue, strValue });

    };

    useEffect(() => {
        if (value) {
            fetchUsersByIds(value).then(users => {
                if (isMultiple) {
                    setSelectedUsers(users);
                } else {
                    setSelectedUser(users[0]);
                }
            });
        }
    }, [value, isMultiple]);


    // 监控selectedUsers变化
    useEffect(() => {
        console.log('🔍 UserField selectedUsers changed:', selectedUsers);
    }, [selectedUsers]);

    if (mode === 'view') {
        return <ViewField type='user' value={value || ''} props={props} />;
    }

    // 编辑模式
    return (
        <FormControl fullWidth error={false}>
            <Autocomplete
                multiple={isMultiple}
                options={users}
                getOptionLabel={(option) => (option as IOption).label}
                isOptionEqualToValue={(option, val) => {
                    if (isMultiple) {
                        return Array.isArray(val) && val.some((v: IOption) => v.value === (option as IOption).value);
                    } else {
                        return (option as IOption).value === (val as IOption)?.value;
                    }
                }}
                value={isMultiple ? selectedUsers : selectedUser}
                onChange={(e, value) => handleChange(value as IOption | IOption[])}
                onInputChange={(e, value) => {
                    if (value.length > 0) {
                        loadUsers(value);
                    }
                }}
                renderInput={(params) => (
                    <TextField
                        {...params}
                        placeholder={t('common.searchWithKeyword')}
                        InputProps={{
                            ...params.InputProps,
                            endAdornment: (
                                <>
                                    {loading ? <CircularProgress color="inherit" size={20} /> : null}
                                    {params.InputProps.endAdornment}
                                </>
                            ),
                        }}
                    />
                )}
                loading={loading}
                size="small"
                fullWidth
            />
        </FormControl>
    );
}

export default UserField;
