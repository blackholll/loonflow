import { TextField } from '@mui/material';
import { useCallback, useEffect, useState } from 'react';

import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Grid from '@mui/material/Grid2';
import Tab from '@mui/material/Tab';
import Tabs from '@mui/material/Tabs';
import Markdown from 'react-markdown';

interface WorkflowBasicProps {
    onBasicChange: (name: string, description: string) => void;
    basicInfo?: {
        name: string;
        description: string;
    };
}

function WorkflowBasic({ onBasicChange, basicInfo }: WorkflowBasicProps) {
    const [activeTab, setActiveTab] = useState('description');
    const [name, setName] = useState(basicInfo?.name || '');
    const [description, setDescription] = useState(basicInfo?.description || '');

    useEffect(() => {
        console.log('load basicInfo', basicInfo);
        setName(basicInfo?.name || '');
        setDescription(basicInfo?.description || '');
    }, [basicInfo]);

    const handleTabChange = useCallback((event: React.SyntheticEvent, newValue: string) => {
        setActiveTab(newValue);
    }, []);

    const handleNameChange = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
        const newName = event.target.value;
        setName(newName);
        onBasicChange(newName, description);
    }, [description, onBasicChange]);

    const handleDescriptionChange = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
        const newDescription = event.target.value;
        setDescription(newDescription);
        onBasicChange(name, newDescription);
    }, [name, onBasicChange]);

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
                            onChange={handleNameChange}
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
                            onChange={handleDescriptionChange}
                        />}
                        {activeTab === 'descriptionPreview' && <Markdown>{description}</Markdown>}

                    </CardContent>
                </Card>
            </Grid>
        </Grid>
    );
}

export default WorkflowBasic;