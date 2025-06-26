import react, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
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
import ArrowBackIosNewOutlinedIcon from '@mui/icons-material/ArrowBackIosNewOutlined';
import WorkflowBasic from '../WorkflowBasic';
import WorkflowForm from '../WorkflowForm';


interface WorkflowDetailInfo {
    basicInfo?: {
        name: string;
        description: string;
    };
    noticeInfo?: any;
    fieldInfoList?: any[];
    [key: string]: any;
}

function WorkflowDetail() {
    const { t } = useTranslation();

    const { workflowId } = useParams();
    const [activeTab, setActiveTab] = useState('basicInfo');
    const [lastSavedTimestamp, setLastSavedTimestamp] = useState<number | null>(null);
    const [lastSavedTimeValue, setLastSavedTimeValue] = useState<number | null>(1);
    const [lastSavedTimeUnit, setLastSavedTimeUnit] = useState('common.second')
    const [workflowDetailInfo, setWorkflowDetailInfo] = useState<WorkflowDetailInfo>({});
    const [showConfirmDialog, setShowConfirmDialog] = useState(false);

    const NEW_WORKFLOW_ID = '00000000-0000-0000-0000-000000000000';
    const STORAGE_KEY = 'workflow_draft';

    // 保存到 localStorage
    const saveToLocalStorage = (data: WorkflowDetailInfo) => {
        localStorage.setItem(STORAGE_KEY, JSON.stringify({
            data,
            timestamp: Date.now()
        }));
    };

    // 从 localStorage 加载
    const loadFromLocalStorage = (): WorkflowDetailInfo | null => {
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
    };

    // 清空 localStorage
    const clearLocalStorage = () => {
        localStorage.removeItem(STORAGE_KEY);
    };

    // 从 API 获取工作流信息
    const fetchWorkflowFromAPI = async (id: string): Promise<WorkflowDetailInfo> => {
        try {
            // 这里替换为实际的 API 调用
            const response = await fetch(`/api/workflow/${id}`);
            const data = await response.json();

            // 保存到 localStorage
            saveToLocalStorage(data);

            return data;
        } catch (error) {
            console.error('Failed to fetch workflow:', error);
            return {};
        }
    };

    // 处理确认对话框
    const handleConfirmLoad = () => {
        const storedData = loadFromLocalStorage();
        if (storedData) {
            setWorkflowDetailInfo(storedData);
        }
        setShowConfirmDialog(false);
    };

    const handleConfirmClear = () => {
        clearLocalStorage();
        setWorkflowDetailInfo({});
        setShowConfirmDialog(false);
    };

    // 初始化数据
    useEffect(() => {
        const initializeWorkflow = async () => {
            if (workflowId === NEW_WORKFLOW_ID) {
                // 新增工作流
                const storedData = loadFromLocalStorage();
                if (storedData && Object.keys(storedData).length > 0) {
                    setShowConfirmDialog(true);
                } else {
                    setWorkflowDetailInfo({});
                }
            } else {
                // 查看现有工作流
                const data = await fetchWorkflowFromAPI(workflowId!);
                setWorkflowDetailInfo(data);
            }
        };

        initializeWorkflow();
    }, [workflowId]);

    // 当 workflowDetailInfo 变化时保存到 localStorage
    useEffect(() => {
        if (workflowId === NEW_WORKFLOW_ID && Object.keys(workflowDetailInfo).length > 0) {
            saveToLocalStorage(workflowDetailInfo);
        }
    }, [workflowDetailInfo, workflowId]);

    const handleTabChange = (event: React.SyntheticEvent, newValue: string) => {
        console.log(newValue);
        setActiveTab(newValue);
    };

    function onBasicChange(name: string, description: string) {
        console.log(name);
        console.log(description)
        setWorkflowDetailInfo({
            ...workflowDetailInfo,
            basicInfo: {
                name: name,
                description: description
            }
        })
    }

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
                <ArrowBackIosNewOutlinedIcon style={{ marginRight: '16px' }} />
                {workflowDetailInfo?.basicInfo?.name || '未命名1'} {lastSavedTimeValue ? <div style={{ fontSize: 12, color: 'gray' }}> ( {t('common.lastSavedTime') + ': ' + t(`${lastSavedTimeValue}`) + ' ' + t(`${lastSavedTimeUnit}`) + t('common.ago')} )</div> : ''}
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
                        <Tab label="基本信息" value="basicInfo" />
                        <Tab label="表单设计" value="formDesign" />
                        <Tab label="流程设计" value="worflowDesign" />
                        <Tab label="高级设置" value="advancedSetting" />
                    </Tabs>
                </Box>
                <Button
                    variant="contained"
                    color="primary"
                    sx={{ marginLeft: 'auto' }}
                >
                    保存
                </Button>
            </Box>
            <Box>
                {activeTab === 'basicInfo' && <WorkflowBasic onBasicChange={onBasicChange} basicInfo={workflowDetailInfo.basicInfo} />}
                {activeTab === 'formDesign' && <WorkflowForm />}
                {activeTab === 'workflowDesign' && <div>workflowDesign</div>}
                {activeTab === 'advancedSetting' && <div>advancedSetting - noticeInfo: {JSON.stringify(workflowDetailInfo.noticeInfo)}</div>}
            </Box>

            {/* 确认对话框 */}
            <Dialog
                open={showConfirmDialog}
                onClose={() => setShowConfirmDialog(false)}
            >
                <DialogTitle>发现草稿</DialogTitle>
                <DialogContent>
                    <DialogContentText>
                        发现本地保存的草稿，是否要加载？
                    </DialogContentText>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleConfirmClear} color="primary">
                        清空草稿
                    </Button>
                    <Button onClick={handleConfirmLoad} color="primary" variant="contained">
                        加载草稿
                    </Button>
                </DialogActions>
            </Dialog>
        </Box>
    )
}

export default WorkflowDetail;
