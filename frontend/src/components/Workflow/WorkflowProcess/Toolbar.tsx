import React from 'react';
import {
    Box,
    Toolbar as MuiToolbar,
    IconButton,
    Tooltip,
    Divider,
    Typography,
} from '@mui/material';
import {
    Clear as ClearIcon,
    Undo as UndoIcon,
    Redo as RedoIcon,
    Delete as DeleteIcon,
    ContentCopy as CopyIcon,
} from '@mui/icons-material';
import { useTranslation } from 'react-i18next';
interface ToolbarProps {
    onClear: () => void;
    onUndo: () => void;
    onRedo: () => void;
    onDelete: () => void;
    onCopy: () => void;
    canDelete: boolean;
    canCopy: boolean;
    canUndo: boolean;
    canRedo: boolean;
}

const Toolbar: React.FC<ToolbarProps> = ({
    onClear,
    onUndo,
    onRedo,
    onDelete,
    onCopy,
    canDelete,
    canCopy,
    canUndo,
    canRedo,
}) => {
    const { t } = useTranslation();
    return (
        <MuiToolbar
            variant="dense"
            sx={{
                borderBottom: 1,
                borderColor: 'divider',
                backgroundColor: 'background.paper',
                minHeight: 48,
            }}
        >
            <Typography variant="h6" component="h1" sx={{ flexGrow: 0, mr: 3 }}>
                {t('workflow.toolbarLabel.workflowEditor')}
            </Typography>

            <Divider orientation="vertical" flexItem sx={{ mx: 1 }} />

            {/* 编辑操作 */}
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                <Tooltip title={t('workflow.toolbarLabel.undo')}>
                    <span>
                        <IconButton
                            onClick={onUndo}
                            size="small"
                            disabled={!canUndo}
                        >
                            <UndoIcon />
                        </IconButton>
                    </span>
                </Tooltip>

                <Tooltip title={t('workflow.toolbarLabel.redo')}>
                    <span>
                        <IconButton
                            onClick={onRedo}
                            size="small"
                            disabled={!canRedo}
                        >
                            <RedoIcon />
                        </IconButton>
                    </span>
                </Tooltip>
            </Box>

            <Divider orientation="vertical" flexItem sx={{ mx: 1 }} />

            {/* 选择操作 */}
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                <Tooltip title={t('workflow.toolbarLabel.copy')}>
                    <span>
                        <IconButton
                            onClick={onCopy}
                            size="small"
                            disabled={!canCopy}
                        >
                            <CopyIcon />
                        </IconButton>
                    </span>
                </Tooltip>

                <Tooltip title={t('workflow.toolbarLabel.delete')}>
                    <span>
                        <IconButton
                            onClick={onDelete}
                            size="small"
                            disabled={!canDelete}
                            color="error"
                        >
                            <DeleteIcon />
                        </IconButton>
                    </span>
                </Tooltip>
            </Box>

            <Divider orientation="vertical" flexItem sx={{ mx: 1 }} />

            {/* 画布操作 */}
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                <Tooltip title={t('workflow.toolbarLabel.clearCanvas')}>
                    <span>
                        <IconButton
                            onClick={onClear}
                            size="small"
                            color="warning"
                        >
                            <ClearIcon />
                        </IconButton>
                    </span>
                </Tooltip>
            </Box>

            <Box sx={{ flexGrow: 1 }} />
        </MuiToolbar>
    );
};

export default Toolbar; 