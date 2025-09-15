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
import { newTicket, getTicketDetailForm, getTicketDetailActions, handleTicket } from "../../../services/ticket";
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
  const [actionBaseNodeId, setActionBaseNodeId] = useState<string>();
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
      // get component value and update fields
      const fields: { [key: string]: any } = {};
      res.data.formSchema.componentInfoList.forEach((component: IWorkflowComponentRow | IWorkflowComponent) => {
        if (component.type === 'row') {
          (component as IWorkflowComponentRow).children.forEach((fieldComponent: IWorkflowComponent) => {
            fields[fieldComponent.componentKey] = fieldComponent.props.value;
          });
        }
      });
      setFields(fields);

    } else {
      showMessage(res.msg, 'error');
    }
  }, []);
  const fetchTicketDetailActions = useCallback(async (ticketId: string) => {
    const res = await getTicketDetailActions(ticketId);
    if (res.code === 0) {
      setCreationFormActions(res.data.actions);
      setActionBaseNodeId(res.data.actionBaseNodeId);
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
      const res = await handleTicket({
        ticketId: ticketId, actionType: action.type, actionId: action.id, fields: fields, actionProps: {
          comment: '',
          nodeId: actionBaseNodeId,
        }
      })
      if (res.code === 0 && onTicketHandledChange) {
        showMessage(res.msg, 'success')
        onTicketHandledChange(res.data.ticketId)
      } else {
        showMessage(res.msg, 'error')
      }
    } else {
      // new ticket
      console.log('no ticketId')
      const res = await newTicket({ workflowId: workflowId!, actionId: action.id, fields: fields })
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
        {creationFormActions?.map((action: IWorkflowAction) => {
          // 根据 actionType 设置不同的按钮样式
          const getButtonProps = (actionType: string) => {
            switch (actionType) {
              case 'agree':
                return {
                  variant: 'contained' as const,
                  color: 'success' as const,
                  sx: {
                    backgroundColor: '#4caf50',
                    '&:hover': {
                      backgroundColor: '#45a049',
                    }
                  }
                };
              case 'reject':
                return {
                  variant: 'contained' as const,
                  color: 'error' as const,
                  sx: {
                    backgroundColor: '#f44336',
                    '&:hover': {
                      backgroundColor: '#da190b',
                    }
                  }
                };
              case 'forward':
              case 'consult':
              case 'consult_submit':
                return {
                  variant: 'outlined' as const,
                  color: 'primary' as const,
                  sx: {
                    borderColor: '#1976d2',
                    color: '#1976d2',
                    '&:hover': {
                      backgroundColor: '#1976d2',
                      color: 'white',
                    }
                  }
                };
              case 'add_comment':
                return {
                  variant: 'outlined' as const,
                  color: 'primary' as const,
                  sx: {
                    borderColor: '#1976d2',
                    color: '#1976d2',
                    '&:hover': {
                      backgroundColor: '#1976d2',
                      color: 'white',
                    }
                  }
                };
              case 'other':
                return {
                  variant: 'outlined' as const,
                  color: 'primary' as const,
                  sx: {
                    borderColor: '#1976d2',
                    color: '#1976d2',
                    '&:hover': {
                      backgroundColor: '#1976d2',
                      color: 'white',
                    }
                  }
                };

              default:
                return {
                  variant: 'contained' as const,
                  color: 'primary' as const
                };
            }
          };

          const buttonProps = getButtonProps(action.type);

          return (
            <Button
              key={action.id}
              {...buttonProps}
              onClick={() => {
                handleActionClick(action)
              }}
            >
              {action.name}
            </Button>
          );
        })}
      </Box>
    </Paper>
  );
}

export default TicketDetail;