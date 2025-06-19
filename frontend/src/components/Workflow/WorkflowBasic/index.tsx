import react, { useState, useEffect } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField, FormControl, FormLabel, RadioGroup, FormControlLabel, Radio, Icon, Box, Tooltip, InputAdornment } from '@mui/material';

import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid2';
import Markdown from 'react-markdown';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';

interface WorkflowBasicProps {
    onBasicChange: (name: string, description: string) => void;
    basicInfo?: {
        name: string;
        description: string;
    };
}

function WorkflowBasic({ onBasicChange, basicInfo }: WorkflowBasicProps) {
    const [name, setName] = useState(basicInfo?.name || '');
    const [description, setDescription] = useState(basicInfo?.description || '');
    const [activeTab, setActiveTab] = useState('description');

    // 监听 basicInfo 变化，更新表单值
    useEffect(() => {
        if (basicInfo) {
            setName(basicInfo.name || '');
            setDescription(basicInfo.description || '');
        }
    }, [basicInfo]);

    const handleTabChange = (event: React.SyntheticEvent, newValue: string) => {
        console.log(newValue);
        setActiveTab(newValue);
    };

    return (
        <Grid
            container
            justifyContent="center"
            sx={{
                minHeight: "100vh",
                backgroundColor: "#EFF0F1",
                p: 2,
            }}
        >
            <Grid size={{ xs: 6, sm: 6, md: 6 }} >
                <Card elevation={3}>
                    <CardContent sx={{ p: 4 }}>
                        <TextField
                            label="Name"
                            value={name}
                            required
                            fullWidth
                            margin="normal"
                            onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
                                setName(event.target.value);
                                onBasicChange(event.target.value, description);
                            }}
                        />
                        <Tabs
                            value={activeTab}
                            onChange={handleTabChange}
                        >
                            <Tab label="description" value="description" />
                            <Tab label="description preview" value="descriptionPreview" />
                        </Tabs>
                        {activeTab === 'description' && <TextField
                            label="description"
                            value={description}
                            rows={4}
                            multiline
                            fullWidth
                            margin="normal"
                            onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
                                setDescription(event.target.value);
                                onBasicChange(name, event.target.value);
                            }}
                        />}
                        {activeTab === 'descriptionPreview' && <Markdown>{description}</Markdown>}

                    </CardContent>
                </Card>
            </Grid>
        </Grid>
    );
}

export default WorkflowBasic;