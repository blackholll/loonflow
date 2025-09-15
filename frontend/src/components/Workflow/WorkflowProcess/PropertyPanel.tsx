import React, { useState, useEffect } from 'react';
import {
    Box,
    Typography,
    TextField,
    Divider,
    FormControl,
    InputLabel,
    Select,
    MenuItem,
    IconButton,
    Autocomplete,
    Chip,
    CircularProgress,
    FormLabel,
    RadioGroup,
    FormControlLabel,
    Radio,
    Switch
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import { Node, Edge } from '@xyflow/react';
import { IFormSchema } from '../../../types/workflow';
import { getSimpleUsers } from '../../../services/user';
import { getDeptPaths } from '../../../services/dept';
import { getSimpleRoles } from '../../../services/role';
import { ISimpleUser } from '../../../types/user';
import { ISimpleDeptPath } from '../../../types/dept';
import { ISimpleRole } from '../../../types/role';

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

// 类型守卫函数，用于明确区分 Node 和 Edge
function isNode(element: Node | Edge): element is Node {
    return !('source' in element) && !('target' in element);
}

function isEdge(element: Node | Edge): element is Edge {
    return 'source' in element && 'target' in element;
}

// 其他可能的类型检查方法（供参考）
function isNodeAlternative1(element: Node | Edge): element is Node {
    // 方法1：检查是否有 position 属性（Node 特有）
    return 'position' in element;
}

function isNodeAlternative2(element: Node | Edge): element is Node {
    // 方法2：检查是否有 type 属性且不是 'custom'（Edge 的默认类型）
    return 'type' in element && element.type !== 'custom';
}

function isEdgeAlternative1(element: Node | Edge): element is Edge {
    // 方法1：检查是否有 source 和 target 属性
    return 'source' in element && 'target' in element;
}

function isEdgeAlternative2(element: Node | Edge): element is Edge {
    // 方法2：检查是否有 sourceHandle 和 targetHandle 属性（Edge 特有）
    return 'sourceHandle' in element && 'targetHandle' in element;
}

// 最可靠的方法：结合多个属性检查
function isNodeReliable(element: Node | Edge): element is Node {
    return (
        'position' in element &&
        !('source' in element) &&
        !('target' in element)
    );
}

function isEdgeReliable(element: Node | Edge): element is Edge {
    return (
        'source' in element &&
        'target' in element &&
        !('position' in element)
    );
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


    const fetchSimpleUsers = async (searchValue: string = '', userIds: string = '', page = 1, perPage: 1000) => {
        const response = await getSimpleUsers(searchValue, userIds, page, perPage);
        if (response.code === 0) {
            return response.data.userInfoList.map((user) => ({ label: `${user.name}(${user.alias})`, value: user.id })) || [];
        }
        return []
    }
    const fetchDeptPaths = async (searchValue: string = '', userIds: string = '', page = 1, perPage: 1000) => {
        const response = await getDeptPaths(searchValue, userIds, page, perPage);
        if (response.code === 0) {
            return response.data?.deptPathList || [];
        }
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
                    }
                } else if (nodeProperties.assigneeType === 'depts') {
                    if (nodeProperties.assignee) {
                        fetchDeptPaths('', nodeProperties.assignee, 1, 1000).then(data => setSelectedAssignees(data));
                    }
                    setSelectedAssignees([]);
                } else if (nodeProperties.assigneeType === 'roles') {
                    setSelectedAssignees(nodeProperties.assignee || null);
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
        { name: '用户', value: 'users' },
        { name: '部门', value: 'depts' },
        { name: '角色', value: 'roles' },
        { name: '变量', value: 'variables' },
        { name: '工单字段', value: 'ticket_field' },
        { name: '父工单字段', value: 'parent_ticket_field' },
        { name: '外部获取', value: 'external' },
    ];

    const assignmentStrategyOptions = [
        { name: '主动接单', value: 'voluntary' },
        { name: '直接处理', value: 'direct' },
        { name: '随机分配', value: 'random' },
        { name: '全部处理', value: 'all' },
    ];

    // 变量选项
    const variableOptions = [
        { name: '工单创建人', value: 'creator' },
        { name: '部门审批人', value: 'dept_approver' },
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
            console.error('加载用户列表失败:', error);
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
            console.error('加载部门列表失败:', error);
        } finally {
            setLoadingDepts(false);
        }
    };

    // 加载角色列表
    const loadRoles = async (searchValue: string = '') => {
        if (loadingRoles) return;
        setLoadingRoles(true);
        try {
            const response = await getSimpleRoles(searchValue, '', 1, 100);
            if (response.code === 0) {
                setRoles(response.data?.roleList || []);
            }
        } catch (error) {
            console.error('加载角色列表失败:', error);
        } finally {
            setLoadingRoles(false);
        }
    };

    // 处理处理人类型变化
    const handleAssigneeTypeChange = (value: string) => {
        console.log('handleAssigneeTypeChangevalue:', value);
        handlePropertyChange('assigneeType', value);
        // 清空处理人值
        // handlePropertyChange('assignee', '');
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
                                label="选择处理人"
                                placeholder="输入关键词后搜索用户..."
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
                                label="选择部门"
                                placeholder="搜索部门..."
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
                        options={Array.isArray(roles) ? roles : []}
                        getOptionLabel={(option) => option.label}
                        value={Array.isArray(roles) ? roles.find(r => r.value === assigneeValue) || null : null}
                        onChange={(e, value) => handlePropertyChange('assignee', value?.value || '')}
                        onInputChange={(e, value) => {
                            setRoleSearchValue(value);
                            if (value.length > 0) {
                                loadRoles(value);
                            }
                        }}
                        renderInput={(params) => (
                            <TextField
                                {...params}
                                label="选择角色"
                                placeholder="搜索角色..."
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

            case 'variable':
                return (
                    <Autocomplete
                        options={variableOptions}
                        getOptionLabel={(option) => option.name}
                        value={variableOptions.find(v => v.value === assigneeValue) || null}
                        onChange={(e, value) => handlePropertyChange('assignee', value?.value || '')}
                        renderInput={(params) => (
                            <TextField {...params} label="选择变量" placeholder="选择系统变量" />
                        )}
                        size="small"
                        fullWidth
                    />
                );

            case 'ticket_field':
                return (
                    <TextField
                        label="工单字段"
                        value={assigneeValue}
                        onChange={(e) => handlePropertyChange('assignee', e.target.value)}
                        size="small"
                        fullWidth
                        placeholder="输入工单字段标识，如：username, agent"
                        helperText="请输入工单中的字段标识，该字段应包含用户名信息"
                    />
                );

            case 'parent_ticket_field':
                return (
                    <TextField
                        label="父工单字段"
                        value={assigneeValue}
                        onChange={(e) => handlePropertyChange('assignee', e.target.value)}
                        size="small"
                        fullWidth
                        placeholder="输入父工单字段标识，如：po, manager"
                        helperText="请输入父工单中的字段标识，该字段应包含用户名信息"
                    />
                );

            case 'hook':
                return (
                    <TextField
                        label="钩子配置"
                        value={assigneeValue}
                        onChange={(e) => handlePropertyChange('assignee', e.target.value)}
                        size="small"
                        multiline
                        rows={3}
                        fullWidth
                        placeholder='{"hook_url":"http://xxx.com/xxx", "hook_token":"xxxx", "wait":true, "extra_info":"xxx"}'
                        helperText="请输入JSON格式的钩子配置"
                    />
                );

            case 'external':
                return (
                    <TextField
                        label="外部接口"
                        value={assigneeValue}
                        onChange={(e) => handlePropertyChange('assignee', e.target.value)}
                        size="small"
                        fullWidth
                        placeholder="输入外部接口URL"
                        helperText="系统将通过该接口获取处理人信息"
                    />
                );

            default:
                return (
                    <TextField
                        label="处理人"
                        value={assigneeValue}
                        onChange={(e) => handlePropertyChange('assignee', e.target.value)}
                        size="small"
                        fullWidth
                        placeholder="请先选择处理人类型"
                    />
                );
        }
    };

    if (!element) {
        return (
            <Box sx={{ p: 2 }}>
                <Typography variant="h6" gutterBottom>
                    属性面板
                </Typography>
                <Typography variant="body2" color="text.secondary">
                    请选择一个节点或连线来查看和编辑属性
                </Typography>
            </Box>
        );
    }

    const isEdgeElement = isEdge(element);
    const elementType = isEdgeElement ? '连线' : '节点';
    const elementLabel = isEdgeElement ? '连线属性' : (element.data?.label as string) || '节点属性';

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
                        label="名称"
                        value={properties.name || '同意'}
                        onChange={(e) => handlePropertyChange('name', e.target.value)}
                        size="small"
                        fullWidth
                        placeholder="输入连线名称"
                    />

                    <FormControl size="small" fullWidth>
                        <InputLabel>类型</InputLabel>
                        <Select
                            value={properties.type || 'agree'}
                            label="连线类型"
                            onChange={(e) => handlePropertyChange('type', e.target.value)}
                        >
                            <MenuItem value="agree">同意</MenuItem>
                            <MenuItem value="reject">拒绝</MenuItem>
                            <MenuItem value="other">其他</MenuItem>
                        </Select>
                    </FormControl>

                    {properties.type === 'conditional' && (
                        <TextField
                            label="条件表达式"
                            value={properties.condition || ''}
                            onChange={(e) => handlePropertyChange('condition', e.target.value)}
                            size="small"
                            multiline
                            rows={2}
                            fullWidth
                            placeholder="例如: status === 'approved'"
                        />
                    )}
                </Box>
            ) : (
                // 节点属性
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                    <TextField
                        label="节点名称"
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
                                renderInput={(params) => <TextField {...params} label="处理人类型" />}
                                onChange={(e, value) => handleAssigneeTypeChange(value?.value || '')}
                                size="small"
                                fullWidth
                            />
                            {renderAssigneeInput()}
                            <Autocomplete
                                options={assignmentStrategyOptions}
                                getOptionLabel={(option) => option.name}
                                value={properties.assignmentStrategy ? assignmentStrategyOptions.find(option => option.value === properties.assignmentStrategy) || null : null}
                                renderInput={(params) => <TextField {...params} label="分配策略" />}
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
                                    label="允许撤回"
                                    labelPlacement='start'

                                />
                            </Box>
                            <Box sx={{ width: '100%' }}>
                                <FormControlLabel
                                    sx={{ marginLeft: 0 }}
                                    control={
                                        <Switch checked={properties.rememberLastAssignee} onChange={(event: React.ChangeEvent<HTMLInputElement>) => handlePropertyChange('rememberLastAssignee', event.target.checked)} />
                                    }
                                    label="记忆上次处理人"
                                    labelPlacement='start'
                                />
                            </Box>
                        </>
                    )}

                    {/* 网关特定属性 */}
                    {(element.data?.nodeType === 'parallel' || element.data?.nodeType === 'exclusive') && (
                        <>
                            <Divider sx={{ my: 1 }} />
                            <Typography variant="subtitle2" color="primary">
                                网关配置
                            </Typography>

                            <FormControl size="small" fullWidth>
                                <InputLabel>网关类型</InputLabel>
                                <Select
                                    value={properties.gatewayType || element.data?.nodeType}
                                    label="网关类型"
                                    onChange={(e) => handlePropertyChange('gatewayType', e.target.value)}
                                >
                                    <MenuItem value="parallel">并行网关</MenuItem>
                                    <MenuItem value="exclusive">排他网关</MenuItem>
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
                    {element.data?.nodeType !== 'end' && (
                        <>

                            <div style={{ fontSize: '14px', fontWeight: 'bold' }}>字段权限</div>
                            {currentFormSchema.componentInfoList.map((component: any) => {
                                if (component.type === 'row') {
                                    return component.children.map((child: any) => {
                                        return (<Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>

                                            <FormLabel id="demo-controlled-radio-buttons-group" sx={{ width: '80px' }}>{child.componentName}</FormLabel>
                                            <RadioGroup
                                                row
                                                aria-labelledby="demo-controlled-radio-buttons-group"
                                                name="controlled-radio-buttons-group"
                                                value={properties?.fieldPermissions?.[child.componentKey] || 'hidden'}
                                                onChange={(e) => handleFieldPermissionChange(child.componentKey, e.target.value)}
                                            >
                                                <FormControlLabel value="readonly" control={<Radio />} label="只读" />
                                                <FormControlLabel value="optional" control={<Radio />} label="选填" />
                                                <FormControlLabel value="required" control={<Radio />} label="必填" />
                                                <FormControlLabel value="hidden" control={<Radio />} label="隐藏" />
                                            </RadioGroup>
                                        </Box>)
                                    })
                                }
                            })}

                        </>
                    )}
                </Box>
            )}
        </Box>
    );
};

export default PropertyPanel; 