import { useState, useEffect, useCallback, useMemo } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';


import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogActions from '@mui/material/DialogActions';
import DialogContentText from '@mui/material/DialogContentText';
import Tooltip from '@mui/material/Tooltip';
import TextField from '@mui/material/TextField';
import Alert from '@mui/material/Alert';
import ArrowBackIosNewOutlinedIcon from '@mui/icons-material/ArrowBackIosNewOutlined';
import WorkflowBasic from '../WorkflowBasic';
import WorkflowForm from '../WorkflowForm';
import WorkflowProcess from '../WorkflowProcess';
import WorkflowAdvanced from '../WorkflowAdvanced';
import { IWorkflowFullDefinition, createEmptyWorkflowFullDefinition, IFormSchema, IProcessSchema, IAdvancedSchema } from '../../../types/workflow';
import { getWorkflowDetail, addWorkflow, updateWorkflow } from '../../../services/workflow';
import useSnackbar from '../../../hooks/useSnackbar';
import { useSearchParams } from 'react-router-dom';
import checkWorkflowCompatibility from './checkWorkflowCompatibility';
import { checkWorkflowProblems } from './WorkflowValidation';

function WorkflowDetail() {
    const { t } = useTranslation();
    const [searchParams] = useSearchParams();
    const { workflowId } = useParams();
    const [activeTab, setActiveTab] = useState('basicInfo');
    const [workflowDetailInfo, setWorkflowDetailInfo] = useState<IWorkflowFullDefinition>(createEmptyWorkflowFullDefinition());
    const [workflowSourceDetailInfo, setWorkflowSourceDetailInfo] = useState<IWorkflowFullDefinition | null>(null);
    const [showConfirmDialog, setShowConfirmDialog] = useState(false);
    const [hasCheckedDraft, setHasCheckedDraft] = useState(false);
    const [isInitialized, setIsInitialized] = useState(false);
    const [problems, setProblems] = useState<string[]>([]);
    const [showVersionDialog, setShowVersionDialog] = useState(false);
    const [versionName, setVersionName] = useState('');
    const [isCheckingCompatibility, setIsCheckingCompatibility] = useState(false);
    const [isCompatible, setIsCompatible] = useState(true);
    const [compatibilityMessages, setCompatibilityMessages] = useState<string[]>([]);

    const { showMessage } = useSnackbar();
    const navigate = useNavigate();
    const versionPathName = searchParams.get('version_name') || '';

    const NEW_WORKFLOW_ID = '00000000-0000-0000-0000-000000000000';
    const STORAGE_KEY = 'workflow_draft';

    // 保存到 localStorage
    const saveToLocalStorage = useCallback((data: IWorkflowFullDefinition) => {
        localStorage.setItem(STORAGE_KEY, JSON.stringify({
            data,
            timestamp: Date.now()
        }));
    }, []);

    // 从 localStorage 加载
    const loadFromLocalStorage = useCallback((): IWorkflowFullDefinition | null => {
        const stored = localStorage.getItem(STORAGE_KEY);
        if (stored) {
            try {
                const parsed = JSON.parse(stored);
                return parsed.data;
            } catch (error) {
                console.error('Failed to parse localStorage data:', error);
                return null;
            }
        }
        return null;
    }, []);

    // 清空 localStorage
    const clearLocalStorage = useCallback(() => {
        localStorage.removeItem(STORAGE_KEY);
    }, []);

    const fetchWorkflowFromAPI = useCallback(async (id: string, versionName?: string): Promise<IWorkflowFullDefinition | null> => {
        try {
            const response = await getWorkflowDetail(id, versionName);
            if (response.code === 0) {
                const data = response.data.workflowFullDefination;
                saveToLocalStorage(data);
                return data;
            } else {
                throw new Error(response.msg);
            }
        } catch (error) {
            console.error('Failed to fetch workflow:', error);
            showMessage(t('common.fetchWorkflowFailed'), 'error');
            return null;
        }
    }, [showMessage, t, saveToLocalStorage]);

    // 处理确认对话框
    const handleConfirmLoad = useCallback(() => {
        const storedData = loadFromLocalStorage();
        if (storedData) {
            setWorkflowDetailInfo(storedData);
        }
        setIsInitialized(true);
        setShowConfirmDialog(false);
    }, [loadFromLocalStorage]);

    const handleConfirmClear = useCallback(() => {
        clearLocalStorage();
        setIsInitialized(true);
        setShowConfirmDialog(false);
    }, [clearLocalStorage]);

    // 初始化数据
    useEffect(() => {
        const initializeWorkflow = async () => {
            if (workflowId === NEW_WORKFLOW_ID) {
                // 新增工作流 - 只在第一次检查草稿
                if (!hasCheckedDraft) {
                    const storedData = loadFromLocalStorage();
                    if (storedData && Object.keys(storedData).length > 0) {
                        setShowConfirmDialog(true);
                    } else {
                        // 如果没有草稿，设置初始化完成标记
                        setIsInitialized(true);
                    }
                    setHasCheckedDraft(true);
                }
            } else {
                // 查看现有工作流
                const data = await fetchWorkflowFromAPI(workflowId!, versionPathName);

                if (data) {
                    console.log('data2222:', data);
                    setWorkflowDetailInfo(data);
                    setWorkflowSourceDetailInfo(data);
                }
                setIsInitialized(true);
            }
        };
        initializeWorkflow();
    }, [workflowId, fetchWorkflowFromAPI, hasCheckedDraft, loadFromLocalStorage, versionPathName]);

    // 当 workflowId 变化时重置草稿检查状态
    useEffect(() => {
        setHasCheckedDraft(false);
        setIsInitialized(false);
        setWorkflowSourceDetailInfo(null); // 重置原始数据
    }, [workflowId]);

    // 当 workflowDetailInfo 变化时保存到 localStorage（延迟保存，避免频繁更新）
    useEffect(() => {
        if (workflowId === NEW_WORKFLOW_ID && isInitialized && Object.keys(workflowDetailInfo).length > 0) {
            const timeoutId = setTimeout(() => {
                saveToLocalStorage(workflowDetailInfo);
            }, 1000); // 延迟1秒保存，避免频繁更新

            return () => clearTimeout(timeoutId);
        }
    }, [workflowDetailInfo, workflowId, isInitialized, saveToLocalStorage]);

    const handleTabChange = useCallback((event: React.SyntheticEvent, newValue: string) => {
        console.log(newValue);
        setActiveTab(newValue);
    }, []);

    const checkProblems = useCallback((workflowData: IWorkflowFullDefinition) => {
        const result = checkWorkflowProblems(workflowData);
        setProblems(result.problems);
    }, []);

    // 更新基础信息的回调函数
    const onBasicChange = useCallback((name: string, description: string) => {
        setWorkflowDetailInfo(prev => ({
            ...prev,
            basicInfo: {
                ...prev.basicInfo,
                name: name,
                description: description
            }
        }));
    }, []);

    // 更新表单架构的回调函数
    const onFormSchemaChange = useCallback((formSchema: IFormSchema) => {
        setWorkflowDetailInfo(prev => ({
            ...prev,
            formSchema: formSchema
        }));
    }, []);

    // 更新流程架构的回调函数
    const onProcessSchemaChange = useCallback((processSchema: IProcessSchema) => {
        console.log(processSchema);
        setWorkflowDetailInfo(prev => ({
            ...prev,
            processSchema: processSchema
        }));
    }, []);

    const onAdvancedSchemaChange = useCallback((advancedSchema: IAdvancedSchema) => {
        setWorkflowDetailInfo(prev => ({
            ...prev,
            advancedSchema: advancedSchema
        }));
    }, []);

    // 监听workflowDetailInfo变化，自动检查问题
    useEffect(() => {
        if (isInitialized) {
            checkProblems(workflowDetailInfo);
        }
    }, [workflowDetailInfo, isInitialized, checkProblems]);

    const handleReleaseWorkflow = useCallback(async () => {
        if (workflowId === NEW_WORKFLOW_ID) {
            const response = await addWorkflow({ ...workflowDetailInfo, basicInfo: { ...workflowDetailInfo.basicInfo, version: versionName } })
            if (response.code === 0) {
                showMessage(t('common.releaseWorkflowSuccess'), 'success');
                setShowVersionDialog(false);
                handleConfirmClear();
                const newWorkflowId = response.data.workflowId;
                navigate(`/workflow/${newWorkflowId}?version_name=${versionName}`)
            } else {
                showMessage(t('workflow.releaseWorkflowFailed'), 'error');
            }
        } else {
            // update workflow
            const response = await updateWorkflow(workflowId!, { ...workflowDetailInfo, basicInfo: { ...workflowDetailInfo.basicInfo, version: versionName } })
            if (response.code === 0) {
                showMessage(t('workflow.releaseWorkflowSuccess'), 'success');
                setShowVersionDialog(false);
                handleConfirmClear();
                navigate(`/workflow/${workflowId}?version_name=${versionName}`)
            } else {
                showMessage(t('common.releaseWorkflowFailed'), 'error');
            }
        }

    }, [showMessage, t, workflowDetailInfo, versionName, handleConfirmClear, navigate, workflowId]);

    const handleCheckCompatibility = useCallback(async () => {
        setIsCheckingCompatibility(true);
        console.log('checkWorkflowCompatibility:', workflowSourceDetailInfo);
        const response = await checkWorkflowCompatibility(workflowDetailInfo, workflowSourceDetailInfo);
        setIsCompatible(response.isCompatible);
        setCompatibilityMessages(response.messages);
        setIsCheckingCompatibility(false);
    }, [workflowDetailInfo, workflowSourceDetailInfo]);

    const handleReleaseClick = useCallback(() => {
        // todo: check if need create a new version
        // todo: check if have issues
        if (workflowId !== NEW_WORKFLOW_ID) {
            handleCheckCompatibility();
        }
        setShowVersionDialog(true);
    }, [workflowId, handleCheckCompatibility]);

    const handleUseCurrentVersion = useCallback(() => {
        if (versionPathName) {
            setVersionName(versionPathName);
        }
    }, [versionPathName]);

    // 使用 useMemo 优化子组件渲染，避免不必要的重新渲染
    const basicComponent = useMemo(() => (
        <WorkflowBasic
            onBasicChange={onBasicChange}
            basicInfo={workflowDetailInfo.basicInfo}
            key="workflow-basic"
        />
    ), [workflowDetailInfo.basicInfo, onBasicChange]);

    const formComponent = useMemo(() => (
        <WorkflowForm
            onFormSchemaChange={onFormSchemaChange}
            formSchema={workflowDetailInfo.formSchema}
            key="workflow-form"
        />
    ), [workflowDetailInfo.formSchema, onFormSchemaChange]);

    const processComponent = useMemo(() => (
        <WorkflowProcess
            onProcessSchemaChange={onProcessSchemaChange}
            processSchema={workflowDetailInfo.processSchema}
            formSchema={workflowDetailInfo.formSchema}
            key="workflow-process" />
    ), [workflowDetailInfo.processSchema, workflowDetailInfo.formSchema, onProcessSchemaChange]);

    const advancedComponent = useMemo(() => (
        <WorkflowAdvanced
            formSchema={workflowDetailInfo.formSchema}
            onAdvancedChange={onAdvancedSchemaChange}
            advancedSchema={workflowDetailInfo.advancedSchema}
            key="workflow-advanced"
        />
    ), [workflowDetailInfo.advancedSchema, onAdvancedSchemaChange, workflowDetailInfo.formSchema]);

    return (
        <Box sx={{ width: '100%' }} >
            <Box sx={{
                borderBottom: 1,
                borderColor: 'divider',
                display: 'flex',
                alignItems: 'center',
                height: '64px',
                padding: '0 16px',
                position: 'relative'
            }}>
                <ArrowBackIosNewOutlinedIcon style={{ marginRight: '16px' }} onClick={() => navigate(`/workflow`)} />
                {workflowDetailInfo?.basicInfo?.name || t('workflow.unnamed')}
                <Box sx={{
                    position: 'absolute',
                    left: '50%',
                    transform: 'translateX(-50%)'
                }}>
                    <Tabs
                        value={activeTab}
                        onChange={handleTabChange}
                        centered
                    >
                        <Tab label={t('workflow.basicInfo')} value="basicInfo" />
                        <Tab label={t('workflow.formDesign')} value="formDesign" />
                        <Tab label={t('workflow.processDesign')} value="processDesign" />
                        <Tab label={t('workflow.advancedSetting')} value="advancedSetting" />
                    </Tabs>
                </Box>
                {problems.length > 0 && (
                    <Tooltip
                        title={
                            <Box>
                                <Box sx={{ fontWeight: 'bold', mb: 1 }}>发现以下问题：</Box>
                                {problems.map((problem, index) => (
                                    <Box key={index} sx={{ mb: 0.5 }}>
                                        • {problem}
                                    </Box>
                                ))}
                            </Box>
                        }
                        arrow
                        placement="bottom"
                    >
                        <Box
                            style={{ color: 'red', cursor: 'pointer' }}
                            sx={{
                                position: 'absolute',
                                left: '85%',
                                transform: 'translateX(-50%)',
                                '&:hover': {
                                    textDecoration: 'underline'
                                }
                            }}
                        >
                            存在{problems.length}个问题,请修改后再发布
                        </Box>
                    </Tooltip>
                )}

                <Button
                    variant="contained"
                    color="primary"
                    disabled={problems.length > 0}
                    sx={{ marginLeft: 'auto' }}
                    onClick={handleReleaseClick}
                >
                    {t('workflow.release')}
                </Button>
            </Box>
            <Box>
                {activeTab === 'basicInfo' && basicComponent}
                {activeTab === 'formDesign' && formComponent}
                {activeTab === 'processDesign' && processComponent}
                {activeTab === 'advancedSetting' && advancedComponent}
            </Box>

            {/* 确认对话框 */}
            <Dialog
                open={showConfirmDialog}
                onClose={() => setShowConfirmDialog(false)}
            >
                <DialogTitle>{t('workflow.draftFound')}</DialogTitle>
                <DialogContent>
                    <DialogContentText>
                        {t('workflow.loadDraftDescription')}
                    </DialogContentText>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleConfirmClear} color="primary">
                        {t('workflow.clearDraft')}
                    </Button>
                    <Button onClick={handleConfirmLoad} color="primary" variant="contained">
                        {t('workflow.loadDraft')}
                    </Button>
                </DialogActions>
            </Dialog>
            <Dialog
                open={showVersionDialog}
                onClose={() => setShowVersionDialog(false)}
                fullWidth
            >
                <DialogTitle>{t('workflow.setVersion')} ({versionPathName ? `${t('workflow.currentVersion')} : ${versionPathName}` : null})</DialogTitle>
                <DialogContent>
                    <DialogContentText>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }} style={{ marginTop: '10px' }}>
                            <TextField
                                fullWidth
                                label={t('workflow.versionName')}
                                required
                                value={versionName}
                                onChange={(e) => setVersionName(e.target.value)}
                            />
                            {versionPathName && (
                                <Button
                                    variant="text"
                                    size="small"
                                    onClick={handleUseCurrentVersion}
                                    sx={{
                                        minWidth: 'auto',
                                        whiteSpace: 'nowrap',
                                        textDecoration: 'underline',
                                        color: 'primary.main',
                                        '&:hover': {
                                            backgroundColor: 'transparent',
                                            textDecoration: 'underline'
                                        }
                                    }}
                                >
                                    {t('workflow.useCurrentVersion')}
                                </Button>
                            )}
                        </Box>
                        {!versionName && <Alert severity="error">{t('workflow.setVersionDescription')}</Alert>}
                        <Alert severity="info">{t('workflow.setVersionDescription2')}</Alert>
                        {isCheckingCompatibility && <Alert severity="info">{t('workflow.checkCompatibilityDescription')}</Alert>}
                        {!isCompatible && <Alert severity="error">{t('workflow.compatibilityMessages', { compatibilityMessages: compatibilityMessages.join(', ') })}</Alert>}

                    </DialogContentText>
                </DialogContent>
                <DialogActions>
                    <Button onClick={(e) => setShowVersionDialog(false)} color="primary">
                        {t('common.cancel')}
                    </Button>
                    <Button onClick={handleReleaseWorkflow} color="primary" variant="contained" disabled={!versionName}>
                        {t('common.confirm')}
                    </Button>
                </DialogActions>
            </Dialog>
        </Box>
    )
}

export default WorkflowDetail;
