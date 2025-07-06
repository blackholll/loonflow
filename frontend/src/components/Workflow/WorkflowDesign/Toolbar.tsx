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

interface ToolbarProps {
    onClear: () => void;
    onUndo: () => void;
    onRedo: () => void;
    onDelete: () => void;
    onCopy: () => void;
    canDelete: boolean;
    canCopy: boolean;
}

const Toolbar: React.FC<ToolbarProps> = ({
    onClear,
    onUndo,
    onRedo,
    onDelete,
    onCopy,
    canDelete,
    canCopy,
}) => {
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
                流程图编辑器
            </Typography>

            <Divider orientation="vertical" flexItem sx={{ mx: 1 }} />

            {/* 编辑操作 */}
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                <Tooltip title="撤销">
                    <span>
                        <IconButton
                            onClick={onUndo}
                            size="small"
                            disabled={false} // 可以根据历史记录状态来控制
                        >
                            <UndoIcon />
                        </IconButton>
                    </span>
                </Tooltip>

                <Tooltip title="重做">
                    <span>
                        <IconButton
                            onClick={onRedo}
                            size="small"
                            disabled={false} // 可以根据历史记录状态来控制
                        >
                            <RedoIcon />
                        </IconButton>
                    </span>
                </Tooltip>
            </Box>

            <Divider orientation="vertical" flexItem sx={{ mx: 1 }} />

            {/* 选择操作 */}
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                <Tooltip title="复制">
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

                <Tooltip title="删除">
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
                <Tooltip title="清空画布">
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