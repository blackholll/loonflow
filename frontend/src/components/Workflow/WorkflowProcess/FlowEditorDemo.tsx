import React from 'react';
import { Box } from '@mui/material';
import SimpleFlowEditor from './SimpleFlowEditor';

function FlowEditorDemo() {
    return (
        <Box sx={{ height: '100vh', width: '100vw' }}>
            <SimpleFlowEditor />
        </Box>
    );
};

export default FlowEditorDemo; 