import CloseIcon from '@mui/icons-material/Close';
import {
    Alert,
    Autocomplete,
    Box,
    Button,
    Chip,
    CircularProgress,
    Divider,
    FormControl,
    FormControlLabel,
    FormLabel,
    IconButton,
    InputLabel,
    Link,
    MenuItem,
    Radio,
    RadioGroup,
    Select,
    Snackbar,
    Switch,
    TextField,
    Typography
} from '@mui/material';
import { Edge, Node } from '@xyflow/react';
import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { materialDark } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { v4 as uuidv4 } from 'uuid';
import { getDeptPaths } from '../../../services/dept';
import { getSimpleRoles } from '../../../services/role';
import { getSimpleUsers } from '../../../services/user';
import { ISimpleDeptPath } from '../../../types/dept';
import { ISimpleUser } from '../../../types/user';
import { IFormSchema } from '../../../types/workflow';
import ConditionExpressionEditor from './ConditionExpressionEditor';

interface PropertyPanelProps {
    element: Node | Edge | null;
    formSchema: IFormSchema;
    onUpdateNodeProperties: (nodeId: string, properties: any) => void;
    onUpdateEdgeProperties: (edgeId: string, properties: any) => void;
}

interface IOption {
    label: string;
    value: string;
}

function toCamelCase(input: string): string {
    if (!input) return input;
    return input
        .replace(/[-_ ]+([a-zA-Z0-9])/g, (_, c) => c.toUpperCase())
        .replace(/^[A-Z]/, (c) => c.toLowerCase());
}

function generateToken(): string {
    return uuidv4();
}

// 类型守卫函数，用于明确区分 Node 和 Edge
function isNode(element: Node | Edge): element is Node {
    return !('source' in element) && !('target' in element);
}

function isEdge(element: Node | Edge): element is Edge {
    return 'source' in element && 'target' in element;
}

function PropertyPanel(props: PropertyPanelProps) {
    const { element, formSchema, onUpdateNodeProperties, onUpdateEdgeProperties } = props;
    const [currentElement, setCurrentElement] = useState<Node | Edge | null>(element);
    const [properties, setProperties] = useState<any>({});
    const [currentFormSchema, setCurrentFormSchema] = useState<IFormSchema>(formSchema);
    // const [assigneeType, setAssigneeType] = useState<string>('');
    const [selectedAssignees, setSelectedAssignees] = useState<{ label: string, value: string }[]>([]);
    // const [inputedAssignee, setInputedAssignee] = useState<string>('');

    const [loadingUsers, setLoadingUsers] = useState(false);
    const [loadingDepts, setLoadingDepts] = useState(false);
    const [loadingRoles, setLoadingRoles] = useState(false);
    const [userSearchValue, setUserSearchValue] = useState('');
    const [deptSearchValue, setDeptSearchValue] = useState('');
    const [roleSearchValue, setRoleSearchValue] = useState('');

    const [users, setUsers] = useState<IOption[]>([]);
    const [departments, setDepartments] = useState<IOption[]>([]);
    const [roles, setRoles] = useState<IOption[]>([]);
    const [copySuccess, setCopySuccess] = useState(false);
    const [showSignatureSample, setShowSignatureSample] = useState(false);
    const { t } = useTranslation();


    const fetchSimpleUsers = async (searchValue: string = '', userIds: string = '', page = 1, perPage: 1000) => {
        const response = await getSimpleUsers(searchValue, userIds, page, perPage);
        if (response.code === 0) {
            return response.data.userInfoList.map((user) => ({ label: `${user.name}(${user.alias})`, value: user.id })) || [];
        }
        return []
    }
    const fetchDeptPaths = async (searchValue: string = '', deptIds: string = '', page = 1, perPage: 1000) => {
        const response = await getDeptPaths(searchValue, deptIds, page, perPage);
        if (response.code === 0) {
            return (response.data?.deptPathList || []).map((dept: ISimpleDeptPath) => ({ label: dept.name, value: dept.id }));
        }
        return [];
    }

    useEffect(() => {
        setCurrentFormSchema(formSchema);
        setCurrentElement(element);
        console.log('formSchema11111', formSchema);
    }, [formSchema, element]);


    useEffect(() => {
        console.log('currentElement', currentElement);
        if (currentElement) {
            if (isEdge(currentElement)) {
                setProperties(currentElement.data?.properties || {});
            } else if (isNode(currentElement)) {
                const nodeProperties = { ...(currentElement.data?.properties || {}) } as any;
                setProperties(nodeProperties);
                if (nodeProperties.assigneeType === 'users') {
                    if (nodeProperties.assignee) {
                        fetchSimpleUsers('', nodeProperties.assignee, 1, 1000).then(data => setSelectedAssignees(data));
                    } else {
                        setSelectedAssignees([]);
                    }
                } else if (nodeProperties.assigneeType === 'depts') {
                    if (nodeProperties.assignee) {
                        fetchDeptPaths('', nodeProperties.assignee, 1, 1000).then(data => setSelectedAssignees(data));
                    } else {
                        setSelectedAssignees([]);
                    }
                } else if (nodeProperties.assigneeType === 'roles') {
                    if (nodeProperties.assignee) {
                        loadRoles('', nodeProperties.assignee).then(data => setSelectedAssignees(data));
                    } else {
                        setSelectedAssignees([]);
                    }
                } else if (nodeProperties.assigneeType === 'variables') {
                    if (nodeProperties.assignee) {
                        const selectedValues = nodeProperties.assignee.split(',');
                        const selectedOptions = selectedValues.map((value: string) => {
                            const option = variableOptions.find((opt: any) => opt.value === value);
                            return { label: option?.name || value, value };
                        }).filter((opt: any) => opt.label);
                        setSelectedAssignees(selectedOptions);
                    } else {
                        setSelectedAssignees([]);
                    }
                }
            }
        }
    }, [currentElement]);

    const handlePropertyChange = (key: string, value: any) => {
        console.log('handlePropertyChange', key, value);
        const newProperties = { ...properties, [key]: value };
        setProperties(newProperties);
        console.log('newProperties', key, newProperties);

        if (currentElement) {
            if (isEdge(currentElement)) {
                // 更新边属性
                onUpdateEdgeProperties(currentElement.id, newProperties);
            } else if (isNode(currentElement)) {
                // 更新节点属性
                onUpdateNodeProperties(currentElement.id, newProperties);
            }
        }
    };

    // 支持一次性合并更新多个属性，避免连续更新时的状态覆盖问题
    const updateProperties = (partial: Record<string, any>) => {
        const newProperties = { ...properties, ...partial };
        setProperties(newProperties);

        if (currentElement) {
            if (isEdge(currentElement)) {
                onUpdateEdgeProperties(currentElement.id, newProperties);
            } else if (isNode(currentElement)) {
                onUpdateNodeProperties(currentElement.id, newProperties);
            }
        }
    };

    // 特殊处理节点名称修改，同时更新节点的 label
    const handleNodeNameChange = (value: string) => {
        const newProperties = { ...properties, name: value };
        setProperties(newProperties);

        if (element && isNode(element)) {
            // 更新节点属性
            onUpdateNodeProperties(element.id, newProperties);
            // 同时更新节点的 label
            onUpdateNodeProperties(element.id, { ...newProperties, label: value });
        }
    };


    const handleFieldPermissionChange = (key: string, value: any) => {
        const newFieldPermissions = { ...properties.fieldPermissions, [key]: value };
        console.log('newFieldPermissions', newFieldPermissions);
        handlePropertyChange('fieldPermissions', newFieldPermissions);
    };

    // 处理人类型选项
    const assigneeTypeOptions = [
        { name: t('workflow.propertyPanelLabel.assigneeTypeOptions.users'), value: 'users' },
        { name: t('workflow.propertyPanelLabel.assigneeTypeOptions.depts'), value: 'depts' },
        { name: t('workflow.propertyPanelLabel.assigneeTypeOptions.roles'), value: 'roles' },
        { name: t('workflow.propertyPanelLabel.assigneeTypeOptions.variables'), value: 'variables' },
        // { name: t('workflow.propertyPanelLabel.assigneeTypeOptions.ticket_field'), value: 'ticket_field' },
        // { name: t('workflow.propertyPanelLabel.assigneeTypeOptions.parent_ticket_field'), value: 'parent_ticket_field' },
        { name: t('workflow.propertyPanelLabel.assigneeTypeOptions.external'), value: 'external' },
    ];

    const assignmentStrategyOptions = [
        { name: t('workflow.propertyPanelLabel.assignmentStrategyOptions.voluntary'), value: 'voluntary' },
        { name: t('workflow.propertyPanelLabel.assignmentStrategyOptions.direct'), value: 'direct' },
        { name: t('workflow.propertyPanelLabel.assignmentStrategyOptions.random'), value: 'random' },
        { name: t('workflow.propertyPanelLabel.assignmentStrategyOptions.all'), value: 'whole' },
    ];

    // 变量选项
    const variableOptions = [
        { name: t('workflow.propertyPanelLabel.assigneeTypeVariableOptions.creator'), value: 'creator' },
        { name: t('workflow.propertyPanelLabel.assigneeTypeVariableOptions.dept_approver'), value: 'dept_approver' },
    ];

    // 加载用户列表
    const loadUsers = async (searchValue: string = '') => {
        if (loadingUsers) return;
        setLoadingUsers(true);
        try {
            const response = await getSimpleUsers(searchValue);
            if (response.code === 0) {
                setUsers(response.data.userInfoList.map((user: ISimpleUser) => ({ label: `${user.name}(${user.alias})`, value: user.id })) || []);
            }
        } catch (error) {
            console.error(t('workflow.propertyPanelLabel.loadUsersFailed'), error);
        } finally {
            setLoadingUsers(false);
        }
    };

    // 加载部门列表
    const loadDepartments = async (searchValue: string = '') => {
        if (loadingDepts) return;
        setLoadingDepts(true);
        try {
            const response = await getDeptPaths(searchValue, '', 1, 1000);
            if (response.code === 0) {
                setDepartments(response.data?.deptPathList.map((dept: ISimpleDeptPath) => ({ label: dept.name, value: dept.id })) || []);
            }
        } catch (error) {
            console.error(t('workflow.propertyPanelLabel.loadDeptsFailed'), error);
        } finally {
            setLoadingDepts(false);
        }
    };

    // 加载角色列表
    const loadRoles = async (searchValue: string = '', roleIds: string = '') => {
        if (loadingRoles) return [];
        setLoadingRoles(true);
        try {
            const response = await getSimpleRoles(searchValue, roleIds, 1, 100);
            if (response.code === 0) {
                const rawList = response.data?.roleList || response.data?.role_list || [];
                const fetched = rawList.map((role: any) => ({ label: role.name, value: String(role.id) }));
                setRoles((prev) => {
                    const map = new Map<string, { label: string, value: string }>();
                    [...prev, ...fetched].forEach(item => map.set(item.value, item));
                    return Array.from(map.values());
                });
                return fetched;
            }
            return [];
        } catch (error) {
            console.error(t('workflow.propertyPanelLabel.loadRolesFailed'), error);
            return [];
        } finally {
            setLoadingRoles(false);
        }
    };

    // 处理处理人类型变化
    const handleAssigneeTypeChange = (value: string) => {
        console.log('handleAssigneeTypeChangevalue:', value);
        // 一次性更新类型并清空处理人，避免连续 set 覆盖
        updateProperties({ assigneeType: value, assignee: '' });
        // 同步清空已选的处理人选项
        setSelectedAssignees([]);
    };

    const handleAssigneeSelectChange = (value: { label: string, value: string }[]) => {
        console.log('handleAssigneeSelectChangevalue:', value);
        console.log('handleAssigneeSelectChangevaluestr:', value.map((v: any) => v.value).join(',') || '');
        handlePropertyChange('assignee', value.map((v: any) => v.value).join(',') || '');
        setSelectedAssignees(value);

        // todo: setSelectedAssignees
    }

    const handleAssigneeInputChange = (value: string) => {
        handlePropertyChange('assignee', value);
    }

    const handleAssignmentStrategyChange = (value: string) => {
        console.log('handleAssignmentStrategyChangevalue:', value);
        handlePropertyChange('assignmentStrategy', value);
    }

    // 渲染处理人输入组件
    const renderAssigneeInput = () => {
        const assigneeType = properties.assigneeType;
        const assigneeValue = properties.assignee || '';
        const externalToken = properties.externalToken || '';

        switch (assigneeType) {
            case 'users':
                return (
                    <Autocomplete
                        multiple
                        options={users}
                        getOptionLabel={(option) => option.label}
                        value={selectedAssignees}
                        onChange={(e, value) => handleAssigneeSelectChange(value)}
                        onInputChange={(e, value) => {
                            setUserSearchValue(value);
                            if (value.length > 0) {
                                loadUsers(value);
                            }
                        }}
                        renderInput={(params) => (
                            <TextField
                                {...params}
                                required
                                label={t('workflow.propertyPanelLabel.assigneeTypeUsersLabel.label')}
                                placeholder={t('workflow.propertyPanelLabel.assigneeTypeUsersLabel.placeholder')}
                                InputProps={{
                                    ...params.InputProps,
                                    endAdornment: (
                                        <>
                                            {loadingUsers ? <CircularProgress color="inherit" size={20} /> : null}
                                            {params.InputProps.endAdornment}
                                        </>
                                    ),
                                }}
                            />
                        )}
                        loading={loadingUsers}
                        size="small"
                        fullWidth
                    />
                );



            case 'depts':
                return (
                    <Autocomplete
                        multiple
                        options={Array.isArray(departments) ? departments : []}
                        getOptionLabel={(option) => option.label}
                        value={selectedAssignees ? selectedAssignees : []}
                        onChange={(e, value) => handleAssigneeSelectChange(value)}
                        onInputChange={(e, value) => {
                            setDeptSearchValue(value);
                            if (value.length > 0) {
                                loadDepartments(value);
                            }
                        }
                        }
                        renderInput={(params) => (
                            <TextField
                                {...params}
                                required
                                label={t('workflow.propertyPanelLabel.assigneeTypeDeptsLabel.label')}
                                placeholder={t('workflow.propertyPanelLabel.assigneeTypeDeptsLabel.placeholder')}
                                InputProps={{
                                    ...params.InputProps,
                                    endAdornment: (
                                        <>
                                            {loadingDepts ? <CircularProgress color="inherit" size={20} /> : null}
                                            {params.InputProps.endAdornment}
                                        </>
                                    ),
                                }}
                            />
                        )}
                        loading={loadingDepts}
                        size="small"
                        fullWidth
                    />
                );

            case 'roles':
                return (
                    <Autocomplete
                        multiple
                        options={Array.isArray(roles) ? roles : []}
                        getOptionLabel={(option) => option.label}
                        value={selectedAssignees ? selectedAssignees : []}
                        onChange={(e, value) => handleAssigneeSelectChange(value)}
                        onInputChange={(e, value) => {
                            setRoleSearchValue(value);
                            if (value && value.length > 0) {
                                loadRoles(value);
                            }
                        }}
                        renderInput={(params) => (
                            <TextField
                                {...params}
                                required
                                label={t('workflow.propertyPanelLabel.assigneeTypeRolesLabel.label')}
                                placeholder={t('workflow.propertyPanelLabel.assigneeTypeRolesLabel.placeholder')}
                                InputProps={{
                                    ...params.InputProps,
                                    endAdornment: (
                                        <>
                                            {loadingRoles ? <CircularProgress color="inherit" size={20} /> : null}
                                            {params.InputProps.endAdornment}
                                        </>
                                    ),
                                }}
                            />
                        )}
                        loading={loadingRoles}
                        size="small"
                        fullWidth
                    />
                );

            case 'variables':
                return (
                    <FormControl size="small" fullWidth>
                        <InputLabel>{t('workflow.propertyPanelLabel.assigneeTypeVariablesLabel.label')}</InputLabel>
                        <Select
                            multiple
                            required
                            value={assigneeValue ? assigneeValue.split(',') : []}
                            label={t('workflow.propertyPanelLabel.assigneeTypeVariablesLabel.label')}
                            onChange={(e) => handlePropertyChange('assignee', Array.isArray(e.target.value) ? e.target.value.join(',') : '')}
                            renderValue={(selected) => (
                                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                                    {selected.map((value: string) => {
                                        const option = variableOptions.find((opt: any) => opt.value === value);
                                        return (
                                            <Chip
                                                key={value}
                                                label={option?.name || value}
                                                size="small"
                                            />
                                        );
                                    })}
                                </Box>
                            )}
                        >
                            {variableOptions.map((option) => (
                                <MenuItem key={option.value} value={option.value}>
                                    {option.name}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                );

            case 'ticket_field':
                return (
                    <TextField
                        required
                        label={t('workflow.propertyPanelLabel.assigneeTypeTicketFieldLabel.label')}
                        value={assigneeValue}
                        onChange={(e) => handlePropertyChange('assignee', e.target.value)}
                        size="small"
                        fullWidth
                        placeholder={t('workflow.propertyPanelLabel.assigneeTypeTicketFieldLabel.placeholder')}
                        helperText={t('workflow.propertyPanelLabel.assigneeTypeTicketFieldLabel.helperText')}
                    />
                );

            case 'parent_ticket_field':
                return (
                    <TextField
                        required
                        label={t('workflow.propertyPanelLabel.assigneeTypeParentTicketFieldLabel.label')}
                        value={assigneeValue}
                        onChange={(e) => handlePropertyChange('assignee', e.target.value)}
                        size="small"
                        fullWidth
                        placeholder={t('workflow.propertyPanelLabel.assigneeTypeParentTicketFieldLabel.placeholder')}
                        helperText={t('workflow.propertyPanelLabel.assigneeTypeParentTicketFieldLabel.helperText')}
                    />
                );

            case 'hook':
                return (
                    <>
                        <TextField
                            required
                            label={t('workflow.propertyPanelLabel.assigneeTypeHookLabel.label')}
                            value={assigneeValue}
                            onChange={(e) => handlePropertyChange('assignee', e.target.value)}
                            size="small"
                            multiline
                            rows={3}
                            fullWidth
                            placeholder={t('workflow.propertyPanelLabel.assigneeTypeHookLabel.placeholder')}
                            helperText={t('workflow.propertyPanelLabel.assigneeTypeHookLabel.helperText')}
                        />
                    </>
                );

            case 'external':
                return (
                    <>
                        <TextField
                            label="外部接口"
                            required
                            value={assigneeValue}
                            onChange={(e) => handlePropertyChange('assignee', e.target.value)}
                            size="small"
                            fullWidth
                            placeholder={t('workflow.propertyPanelLabel.assigneeTypeExternalLabel.placeholder')}
                            helperText={t('workflow.propertyPanelLabel.assigneeTypeExternalLabel.helperText')}
                        />
                        <TextField
                            required
                            label="Token"
                            value={externalToken}
                            onChange={(e) => handlePropertyChange('externalToken', e.target.value)}
                            size="small"
                            fullWidth
                            placeholder={t('workflow.propertyPanelLabel.assigneeTypeExternalLabel.tokenPlaceholder')}
                            helperText={t('workflow.propertyPanelLabel.assigneeTypeExternalLabel.tokenHelperText')}
                        />
                        <Link
                            component="button"
                            variant="body2"
                            onClick={() => setShowSignatureSample(!showSignatureSample)}
                        >
                            {showSignatureSample ? 'Hide Signature Sample' : 'Show Signature Sample'}
                        </Link>
                        {showSignatureSample && (
                            <SyntaxHighlighter language="python" style={materialDark} showLineNumbers
                                customStyle={{ margin: 0, borderRadius: '4px' }}>
                                {`# This is Django View example code, you can refer to this code to write your own code
import hashlib
from django.http import JsonResponse
from django.views import View

class externalAssigneeView(View):
    def post(self, request, *args, **kwargs):
        """
        external assignee
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        token = "the token you configured in loonflow"
        signature = request.META.get('HTTP_SIGNATURE')
        timestamp = request.META.get('HTTP_TIMESTAMP')
        ori_str = timestamp + token
        new_str = hashlib.md5(ori_str.encode(encoding='utf-8')).hexdigest()
        if new_str == signature:
            # add you logic to get the real assignee email list
            return JsonResponse(dict(code=0, data={"assignee_email_list": ["blackholll@loonapp.com"]}, msg=""))
        else:
            return JsonResponse(dict(code=-1, data={}, msg="signature is invalid"))
`}
                            </SyntaxHighlighter>
                        )}


                    </>
                );
        }
    };

    if (!element) {
        return (
            <Box sx={{ p: 2 }}>
                <Typography variant="h6" gutterBottom>
                    {t('workflow.propertyPanelLabel.propertyPanel')}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                    {t('workflow.propertyPanelLabel.pleaseSelectNodeOrEdge')}
                </Typography>
            </Box>
        );
    }

    const isEdgeElement = isEdge(element);
    const elementType = isEdgeElement ? t('workflow.propertyPanelLabel.edge') : t('workflow.propertyPanelLabel.node');
    const elementLabel = isEdgeElement ? t('workflow.propertyPanelLabel.edgeProperties') : (element.data?.label as string) || t('workflow.propertyPanelLabel.nodeProperties');

    return (
        <Box sx={{ p: 2, height: '100%', overflow: 'auto' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
                <Typography variant="h6">
                    {elementLabel}
                </Typography>
                <IconButton size="small">
                    <CloseIcon />
                </IconButton>
            </Box>

            <Divider sx={{ mb: 2 }} />

            {isEdgeElement ? (
                // 边属性
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                    <TextField
                        label={t('workflow.propertyPanelLabel.name')}
                        value={properties.name || t('workflow.propertyPanelLabel.edgeNameAccept')}
                        onChange={(e) => handlePropertyChange('name', e.target.value)}
                        size="small"
                        fullWidth
                        placeholder={t('workflow.propertyPanelLabel.inputEdgeName')}
                    />

                    <FormControl size="small" fullWidth>
                        <InputLabel>{t('workflow.propertyPanelLabel.edgeType')}</InputLabel>
                        <Select
                            value={properties.type || 'agree'}
                            label={t('workflow.propertyPanelLabel.edgeType')}
                            onChange={(e) => handlePropertyChange('type', e.target.value)}
                            disabled={properties.type === 'condition'}
                        >
                            <MenuItem value="agree">{t('workflow.propertyPanelLabel.edgeNameAccept')}</MenuItem>
                            <MenuItem value="reject">{t('workflow.propertyPanelLabel.edgeNameReject')}</MenuItem>
                            <MenuItem value="condition">{t('workflow.propertyPanelLabel.edgeNameCondition')}</MenuItem>
                            <MenuItem value="other">{t('workflow.propertyPanelLabel.edgeNameOther')}</MenuItem>
                        </Select>
                    </FormControl>

                    {properties.type === 'condition' && (
                        <ConditionExpressionEditor
                            value={properties.conditionGroups || properties.condition || []}
                            onChange={(groups) => handlePropertyChange('conditionGroups', groups)}
                            formSchema={formSchema}
                        />
                    )}
                </Box>
            ) : (
                // 节点属性
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                    <TextField
                        required
                        label={t('workflow.propertyPanelLabel.nodeLabel')}
                        value={properties.name || ''}
                        disabled={properties.type === 'start' || properties.type === 'end'}
                        onChange={(e) => handleNodeNameChange(e.target.value)}
                        size="small"
                        fullWidth
                    />

                    {properties.type === 'normal' && (
                        <>
                            <Autocomplete
                                options={assigneeTypeOptions}
                                getOptionLabel={(option) => option.name}
                                value={properties.assigneeType ? assigneeTypeOptions.find(option => option.value === properties.assigneeType) || null : null}
                                renderInput={(params) => <TextField {...params} required label={t('workflow.propertyPanelLabel.assigneeType')} />}
                                onChange={(e, value) => handleAssigneeTypeChange(value?.value || '')}
                                size="small"
                                fullWidth
                            />
                            {renderAssigneeInput()}
                            <Autocomplete
                                options={assignmentStrategyOptions}
                                getOptionLabel={(option) => option.name}
                                value={properties.assignmentStrategy ? assignmentStrategyOptions.find(option => option.value === properties.assignmentStrategy) || null : null}
                                renderInput={(params) => <TextField {...params} required label={t('workflow.propertyPanelLabel.assignmentStrategy')} />}
                                onChange={(e, value) => handleAssignmentStrategyChange(value?.value || '')}
                                size="small"
                                fullWidth
                            />
                            <Box sx={{ width: '100%' }}>
                                <FormControlLabel
                                    sx={{ marginLeft: 0 }}
                                    control={
                                        <Switch checked={properties.allowWithdraw} onChange={(event: React.ChangeEvent<HTMLInputElement>) => handlePropertyChange('allowWithdraw', event.target.checked)} />
                                    }
                                    label={t('workflow.propertyPanelLabel.allowWithdraw')}
                                    labelPlacement='start'

                                />
                            </Box>
                            <Box sx={{ width: '100%' }}>
                                <FormControlLabel
                                    sx={{ marginLeft: 0 }}
                                    control={
                                        <Switch checked={properties.rememberLastAssignee} onChange={(event: React.ChangeEvent<HTMLInputElement>) => handlePropertyChange('rememberLastAssignee', event.target.checked)} />
                                    }
                                    label={t('workflow.propertyPanelLabel.rememberLastAssignee')}
                                    labelPlacement='start'
                                />
                            </Box>
                        </>
                    )}

                    {properties.type === 'hook' && (
                        <>
                            <TextField
                                label={t('workflow.propertyPanelLabel.hookUrl')}
                                value={properties.hookUrl || ''}
                                onChange={(e) => handlePropertyChange('hookUrl', e.target.value)}
                                size="small"
                                fullWidth
                                required
                                placeholder="https://example.com/webhook"
                            />
                            <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
                                <TextField
                                    label={t('workflow.propertyPanelLabel.hookToken')}
                                    value={properties.hookToken || ''}
                                    onChange={(e) => handlePropertyChange('hookToken', e.target.value)}
                                    size="small"
                                    fullWidth
                                    required
                                    placeholder="Hook访问令牌"
                                />
                                <Button
                                    variant="outlined"
                                    size="small"
                                    onClick={() => {
                                        const token = generateToken();
                                        handlePropertyChange('hookToken', token);
                                    }}
                                    sx={{ minWidth: 'auto', px: 2 }}
                                >
                                    {t('workflow.propertyPanelLabel.generateToken')}
                                </Button>
                                <Button
                                    variant="outlined"
                                    size="small"
                                    onClick={async () => {
                                        if (properties.hookToken) {
                                            try {
                                                await navigator.clipboard.writeText(properties.hookToken);
                                                setCopySuccess(true);
                                            } catch (error) {
                                                console.error('复制失败:', error);
                                            }
                                        }
                                    }}
                                    disabled={!properties.hookToken}
                                    sx={{ minWidth: 'auto', px: 2 }}
                                >
                                    {t('workflow.propertyPanelLabel.copyToken')}
                                </Button>
                            </Box>
                        </>
                    )}

                    {/* 网关特定属性 */}
                    {(element.data?.nodeType === 'parallel' || element.data?.nodeType === 'exclusive') && (
                        <>
                            <Divider sx={{ my: 1 }} />
                            <Typography variant="subtitle2" color="primary">
                                {t('workflow.propertyPanelLabel.gatewayConfig')}
                            </Typography>

                            <FormControl size="small" fullWidth>
                                <InputLabel>{t('workflow.propertyPanelLabel.gatewaytype')}</InputLabel>
                                <Select
                                    value={properties.gatewayType || element.data?.nodeType}
                                    label={t('workflow.propertyPanelLabel.gatewaytype')}
                                    onChange={(e) => handlePropertyChange('gatewayType', e.target.value)}
                                >
                                    <MenuItem value="parallel">{t('workflow.propertyPanelLabel.gatewaytypeOptions.parallel')}</MenuItem>
                                    <MenuItem value="exclusive">{t('workflow.propertyPanelLabel.gatewaytypeOptions.exclusive')}</MenuItem>
                                </Select>
                            </FormControl>

                            {properties.gatewayType === 'exclusive' && (
                                <TextField
                                    label="默认分支"
                                    value={properties.defaultBranch || ''}
                                    onChange={(e) => handlePropertyChange('defaultBranch', e.target.value)}
                                    size="small"
                                    fullWidth
                                    placeholder="默认分支的连线ID"
                                />
                            )}
                        </>
                    )}
                    {['end', 'hook', 'timer', 'exclusive', 'parallel'].indexOf(element.type as string) === -1 && (
                        <>

                            <div style={{ fontSize: '14px', fontWeight: 'bold' }}>{t('workflow.propertyPanelLabel.fieldPermission')}</div>
                            {currentFormSchema.componentInfoList.map((component: any) => {
                                if (component.type === 'row') {
                                    return component.children.map((child: any) => {
                                        return (<Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>

                                            <FormLabel id="demo-controlled-radio-buttons-group" sx={{ width: '80px' }}>{child.componentName}</FormLabel>
                                            <RadioGroup
                                                row
                                                aria-labelledby="demo-controlled-radio-buttons-group"
                                                name="controlled-radio-buttons-group"
                                                value={properties?.fieldPermissions?.[toCamelCase(child.componentKey)] || 'hidden'}
                                                onChange={(e) => handleFieldPermissionChange(toCamelCase(child.componentKey), e.target.value)}
                                            >
                                                <FormControlLabel value="readonly" control={<Radio />} label={t('workflow.propertyPanelLabel.fieldPermissionOptions.readonly')} />
                                                <FormControlLabel value="optional" control={<Radio />} label={t('workflow.propertyPanelLabel.fieldPermissionOptions.optional')} />
                                                <FormControlLabel value="required" control={<Radio />} label={t('workflow.propertyPanelLabel.fieldPermissionOptions.required')} />
                                                <FormControlLabel value="hidden" control={<Radio />} label={t('workflow.propertyPanelLabel.fieldPermissionOptions.hidden')} />
                                            </RadioGroup>
                                        </Box>)
                                    })
                                }
                                return null;
                            })}

                        </>
                    )}
                </Box>
            )}

            <Snackbar
                open={copySuccess}
                autoHideDuration={2000}
                onClose={() => setCopySuccess(false)}
                anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
            >
                <Alert onClose={() => setCopySuccess(false)} severity="success" sx={{ width: '100%' }}>
                    {t('workflow.propertyPanelLabel.copySuccess')}
                </Alert>
            </Snackbar>
        </Box>
    );
};

export default PropertyPanel; 