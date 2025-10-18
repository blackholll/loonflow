import { Autocomplete, CircularProgress, FormControl, TextField } from '@mui/material';
import { useCallback, useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { getDeptPaths } from '../../services/dept';
import { ISimpleDeptPath } from '../../types/dept';
import ViewField from './ViewField';

interface DeptFieldProps {
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

function DepartmentField({
    value = '',
    onChange,
    mode,
    props,
}: DeptFieldProps) {
    const [loading, setLoading] = useState(false);
    const [depts, setDepts] = useState<IOption[]>([]);
    const [selectedDepts, setSelectedDepts] = useState<IOption[]>([]);
    const [selectedDept, setSelectedDept] = useState<IOption | null>(null);
    const { t } = useTranslation();

    const isMultiple = props.multiple || false;

    const loadDepts = useCallback(async (searchValue: string = '') => {
        if (loading) return;
        setLoading(true);
        try {
            const response = await getDeptPaths(searchValue, '', 1, 1000);
            if (response.code === 0) {
                setDepts(response.data.deptPathList.map((dept: ISimpleDeptPath) => ({ label: `${dept.path}`, value: dept.id })) || []);
            }
        } catch (error) {
            console.error('加载部门列表失败:', error);
        } finally {
            setLoading(false);
        }
    }, [loading]);


    const fetchDeptByIds = async (deptIds: string | string[]) => {
        if (!deptIds || (Array.isArray(deptIds) && deptIds.length === 0)) {
            return [];
        }

        const ids = Array.isArray(deptIds) ? deptIds.join(',') : deptIds;
        try {
            const response = await getDeptPaths('', ids, 1, 1000);
            if (response.code === 0) {
                return response.data.deptPathList.map((dept: ISimpleDeptPath) => ({
                    label: `${dept.path}`,
                    value: dept.id
                }));
            }
        } catch (error) {
            console.error('获取部门信息失败:', error);
        }
        return [];
    };

    // 处理值变化
    const handleChange = (newValue: IOption | IOption[] | null) => {
        let strValue = '';

        if (isMultiple) {
            setSelectedDepts(newValue as IOption[]);
            strValue = newValue ? (newValue as IOption[]).map(item => item.value).join(',') : '';
        } else {
            setSelectedDept(newValue as IOption);
            strValue = newValue ? (newValue as IOption).value : '';
        }
        onChange(strValue);
        console.log('🔍 UserField handleChange:', { newValue, strValue });

    };


    useEffect(() => {
        if (value) {
            fetchDeptByIds(value).then(deptsFetched => {
                if (isMultiple) {
                    setSelectedDepts(deptsFetched);
                } else {
                    setSelectedDept(deptsFetched[0] || null);
                }
            });
        } else {
            // 清空时同步受控值
            if (isMultiple) {
                setSelectedDepts([]);
            } else {
                setSelectedDept(null);
            }
        }
    }, [value, isMultiple]);



    if (mode === 'view') {
        return <ViewField type='department' value={value || ''} props={props} />;
    }

    // 编辑模式
    return (
        <FormControl fullWidth error={false}>
            <Autocomplete
                multiple={isMultiple}
                options={depts}
                getOptionLabel={(option) => (option as IOption).label}
                isOptionEqualToValue={(option, val) => {
                    if (isMultiple) {
                        return Array.isArray(val) && val.some((v: IOption) => v.value === (option as IOption).value);
                    } else {
                        return (option as IOption).value === (val as IOption)?.value;
                    }
                }}
                value={isMultiple ? selectedDepts : selectedDept}
                onChange={(_e, value) => handleChange(value as IOption | IOption[])}
                onInputChange={(_e, value) => {
                    if (value.length > 0) {
                        loadDepts(value);
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

export default DepartmentField;
