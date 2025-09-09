import React, { useState, useEffect, useCallback } from "react";
import {
  Box,
  Paper,
  Typography,
  Tooltip,
  Button,
  Divider,
  Chip,
  Avatar
} from "@mui/material";
import Grid from '@mui/material/Grid2';
import {
  getFieldComponent,
  TextField,
  // NumberField,
  // SelectField,
  // DateTimeField,
  // UserField,
  // DepartmentField,
} from "../../formFields";
import { IFormField } from "../../../types/workflowDesign";
import RenderFormComponent from "../../Workflow/WorkflowForm/RenderFormComponent";
import { HelpOutline as HelpIcon } from '@mui/icons-material';
import { IWorkflowComponent, IWorkflowComponentRow, IFormSchema, IWorkflowNodeSchema, IWorkflowAction } from "../../../types/workflow";
import { getTicketCreationForm, getTicketCreationActions } from "../../../services/workflow";
import { newTicket, getTicketDetailForm, getTicketDetailActions } from "../../../services/ticket";
import useSnackbar from "../../../hooks/useSnackbar";


interface TicketDetailProps {
  workflowId?: string;
  ticketId?: string;
  onTicketHandledChange?: (ticketId: string) => void;
}

function TicketDetail({ workflowId, ticketId, onTicketHandledChange }: TicketDetailProps) {
  const [ticketFullDetail, setTicketFullDetail] = useState<IFormSchema>();
  const [creationFormData, setCreationFormData] = useState<any>();
  const [creationFormActions, setCreationFormActions] = useState<any>();
  const [fields, setFields] = useState<any>();
  const { showMessage } = useSnackbar();

  console.log("ticketdetail")

  const [formSchema, setFormSchema] = useState<IFormSchema>();

  const fetchTicketCreationForm = useCallback(async () => {
    const res = await getTicketCreationForm(workflowId!);
    if (res.code === 0) {
      setFormSchema(res.data.formSchema);
    } else {
      showMessage(res.msg, 'error');
    }
  }, [workflowId]);

  const fetchTicketCreationActions = useCallback(async () => {
    const res = await getTicketCreationActions(workflowId!);
    if (res.code === 0) {
      setCreationFormActions(res.data.actions);
    } else {
      showMessage(res.msg, 'error');
    }
  }, [workflowId]);

  const fetchTicketDetailFrom = useCallback(async (ticketId: string) => {
    const res = await getTicketDetailForm(ticketId);
    if (res.code === 0) {
      console.log("get ticketDetail form")
      setFormSchema(res.data.formSchema);
    } else {
      showMessage(res.msg, 'error');
    }
  }, []);
  const fetchTicketDetailActions = useCallback(async (ticketId: string) => {
    const res = await getTicketDetailActions(ticketId);
    if (res.code === 0) {
      setCreationFormActions(res.data.actions);
    } else {
      showMessage(res.msg, 'error');
    }
  }, []);

  useEffect(() => {
    if (workflowId) {
      fetchTicketCreationForm();
      fetchTicketCreationActions();
    }
    if (ticketId) {
      fetchTicketDetailFrom(ticketId);
      fetchTicketDetailActions(ticketId);
    }
  }, [workflowId, fetchTicketCreationForm, fetchTicketCreationActions]);

  const updateFormValue = (component: IWorkflowComponent) => {
    setFields({
      ...fields,
      [component.componentKey]: component.props.value
    })
  }


  const handleActionClick = async (action: IWorkflowAction) => {
    console.log('action', action)
    if (ticketId) {
      // handle ticket
      console.log('ticketId', ticketId)
      const res = await handleTicket(ticketId, action.type, action.id, fields)
      if (res.code === 0 && onTicketHandledChange) {
        showMessage(res.msg, 'success')
        onTicketHandledChange(res.data.ticketId)
      } else {
        showMessage(res.msg, 'error')
      }
    } else {
      // new ticket
      console.log('no ticketId')
      const res = await newTicket({ workflowId: workflowId!, action_id: action.id, fields: fields })
      if (res.code === 0 && onTicketHandledChange) {
        onTicketHandledChange(res.data.ticketId)
      }
    }
  }

  return (
    <Paper
      sx={{
        flex: 1,
        p: 3,
        overflow: 'auto',
        backgroundColor: 'background.paper',
        border: '1px solid',
        borderColor: 'divider'
      }}
    >
      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
        {formSchema?.componentInfoList.map((component) => {
          if (component.type === 'row') {
            return (
              <Grid container spacing={2} key={component.id}>
                {(component as IWorkflowComponentRow).children.map((fieldComponent: IWorkflowComponent) => (
                  <Grid
                    key={fieldComponent.id}
                    size={fieldComponent.layout.span || 12}
                  >
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <Typography
                          variant="body2"
                          fontWeight="medium"
                          sx={{
                            minWidth: 80,
                          }}
                        >
                          {fieldComponent.componentName}{fieldComponent.description && (
                            <Tooltip
                              title={fieldComponent.description}
                              placement="top"
                              arrow
                            >
                              <HelpIcon
                                sx={{
                                  fontSize: 16,
                                  color: 'text.secondary',
                                  cursor: 'help',
                                  ml: 0.25
                                }}
                              />
                            </Tooltip>
                          )}
                        </Typography>

                      </Box>
                      <Box sx={{ flex: 1 }}>
                        <RenderFormComponent
                          component={fieldComponent}
                          handleComponentUpdate={(updatedComponent) => {
                            updateFormValue(updatedComponent)
                          }}
                        />
                      </Box>
                    </Box>
                  </Grid>
                ))}
              </Grid>
            );
          }
          return null;
        })}
      </Box>
      <Box sx={{ display: 'flex', justifyContent: 'flex-start', gap: 2, mt: 2 }}>
        {creationFormActions?.map((action: IWorkflowAction) => (
          <Button key={action.id} variant="contained" color="primary" onClick={() => {
            handleActionClick(action)
          }}>
            {action.name}
          </Button>
        ))}
      </Box>
    </Paper>
  );
}

export default TicketDetail;