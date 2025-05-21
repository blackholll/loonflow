import React, { useEffect, useState } from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid2';
import { ISimpleWorkflowEntity } from '@/types/workflow';
import { getSimpleWorkflowList } from '../services/workflow';
import TicketList from './Ticket/TicketList';
import useSnackbar from '../hooks/useSnackbar';


function Workbench() {
  const [workflowList, setWorkflowList] = useState<ISimpleWorkflowEntity[]>([]);
  const [workflowValue, setWorkflowValue] = useState<ISimpleWorkflowEntity | null>(null);
  const { showMessage } = useSnackbar();

  useEffect(() => {
    const fetchSimpleWorkflow = async () => {
      try {
        const res = await getSimpleWorkflowList('', 1, 10000);
        if (res.code === 0) {
          console.log('res.data.wokflow_info_listres.data.wokflow_info_list:', res)
          setWorkflowList(res.data.workflowInfoList);
        } else {
          showMessage(res.msg, 'error');
        }
      } catch (error: any) {
        showMessage(error.message, 'error');
        console.log(error);
      }

    };
    fetchSimpleWorkflow();

  }, [])
  // const workflowList = [{ label: 'The Shawshank Redemption', year: 1994 },
  // { label: 'The Godfather', year: 1972 },
  // { label: 'The Godfather: Part II', year: 1974 }]
  return (
    <React.Fragment>
      <Card>
        <CardContent>
          <Grid container spacing={1} justifyContent="left" alignItems="center">
            {/* 搜索部分 */}
            <Grid size={{ xs: 12, sm: 6, md: 3 }}>
              <Autocomplete
                value={workflowValue}
                onChange={(event, newValue) => setWorkflowValue(newValue)}
                getOptionLabel={(option) => option.name}
                disablePortal
                options={workflowList}
                sx={{ margeLeft: 0, margeRight: 0 }}
                renderInput={(params) => <TextField {...params} label="Select Ticke Type" />}
              />
            </Grid>
            <Grid size={{ xs: 12, sm: 6, md: 3 }} justifyContent="left" >
              <Button variant="outlined" sx={{ margeLeft: 0, margeRight: 0, height: '55px' }}>New Ticket</Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      <TicketList category="duty" />



    </React.Fragment>
  )
}

export default Workbench;
