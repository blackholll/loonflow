import {
  Autocomplete,
  Box,
  Button,
  CircularProgress,
  Dialog,
  DialogActions,
  DialogContent,
  Paper,
  TextField,
  Tooltip,
  Typography
} from "@mui/material";
import Grid from '@mui/material/Grid2';
import { useCallback, useEffect, useState } from "react";

import { HelpOutline as HelpIcon } from '@mui/icons-material';
import useSnackbar from "../../../hooks/useSnackbar";
import { getTicketDetailActions, getTicketDetailAdminActions, getTicketDetailForm, handleTicket, newTicket } from "../../../services/ticket";
import { getSimpleUsers } from '../../../services/user';
import { getTicketCreationActions, getTicketCreationForm } from "../../../services/workflow";
import { ISimpleUser } from '../../../types/user';
import { IFormSchema, IWorkflowAction, IWorkflowComponent, IWorkflowComponentRow } from "../../../types/workflow";
import RenderFormComponent from "../../Workflow/WorkflowForm/RenderFormComponent";
import getButtonProps from './getButtonProps';
import TicketHistory from './TicketFlowHistory';
import WorkflowDiagram from "./WorkflowDiagram";

interface TicketDetailProps {
  workflowId?: string;
  ticketId?: string;
  onTicketHandledChange?: (ticketId: string) => void;
  refreshToken?: number;
}


interface IOption {
  label: string;
  value: string;
}
function TicketDetail({ workflowId, ticketId, onTicketHandledChange, refreshToken }: TicketDetailProps) {

  const [formActions, setFormActions] = useState<any>();
  const [adminFormActions, setAdminFormActions] = useState<any>();
  const [actionBaseNodeId, setActionBaseNodeId] = useState<string>();
  const [adminActionBaseNodeId, setAdminActionBaseNodeId] = useState<string>();
  const [openWorkflowDiagram, setOpenWorkflowDiagram] = useState(false);
  const [openCommentDialog, setOpenCommentDialog] = useState(false);
  const [actionRunning, setActionRunning] = useState<('common' | 'admin')>('common');
  const [dialogComment, setDialogComment] = useState<string>('');
  const [dialogActionType, setDialogActionType] = useState<string>('');
  const [users, setUsers] = useState<IOption[]>([]);
  const [selectedAssignee, setSelectedAssignee] = useState<{ label: string, value: string } | null>(null);

  const [fields, setFields] = useState<any>();
  const [loadingUsers, setLoadingUsers] = useState(false);

  const { showMessage } = useSnackbar();

  console.log("ticketdetail")

  const [formSchema, setFormSchema] = useState<IFormSchema>();

  const handleDialogClose = () => {
    setOpenCommentDialog(false);
  }

  const handleWorkflowDiagramClose = () => {
    setOpenWorkflowDiagram(false);
  }
  const handleAssigneeSelectChange = (value: { label: string, value: string } | null) => {
    setSelectedAssignee(value);

  }

  const fetchTicketCreationForm = useCallback(async () => {
    const res = await getTicketCreationForm(workflowId!);
    if (res.code === 0) {
      setFormSchema(res.data.formSchema);
    } else {
      showMessage(res.msg, 'error');
    }
  }, [workflowId, showMessage]);

  const fetchTicketCreationActions = useCallback(async () => {
    const res = await getTicketCreationActions(workflowId!);
    if (res.code === 0) {
      setFormActions(res.data.actions);
    } else {
      showMessage(res.msg, 'error');
    }
  }, [workflowId, showMessage]);

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
  }, [showMessage]);

  const fetchTicketDetailActions = useCallback(async (ticketId: string) => {
    const res = await getTicketDetailActions(ticketId);
    if (res.code === 0) {
      setFormActions(res.data.actions);
      setActionBaseNodeId(res.data.actionBaseNodeId);
    } else {
      showMessage(res.msg, 'error');
    }
  }, [showMessage]);

  const fetchTicketDetailAdminActions = useCallback(async (ticketId: string) => {
    const res = await getTicketDetailAdminActions(ticketId);
    if (res.code === 0) {
      setAdminFormActions(res.data.actions);
      setAdminActionBaseNodeId(res.data.actionBaseNodeId);
    } else {
      showMessage(res.msg, 'error');
    }
  }, [showMessage]);

  useEffect(() => {
    if (workflowId) {
      fetchTicketCreationForm();
      fetchTicketCreationActions();
    }
    if (ticketId) {
      fetchTicketDetailFrom(ticketId);
      fetchTicketDetailActions(ticketId);
      fetchTicketDetailAdminActions(ticketId);
    }
  }, [workflowId, fetchTicketCreationForm, fetchTicketCreationActions, refreshToken, ticketId, fetchTicketDetailFrom, fetchTicketDetailActions, fetchTicketDetailAdminActions]);

  const updateFormValue = (component: IWorkflowComponent) => {
    setFields({
      ...fields,
      [component.componentKey]: component.props.value
    })
  }

  const loadUsers = async (searchValue: string = '') => {
    if (loadingUsers) return;
    setLoadingUsers(true);
    try {
      const response = await getSimpleUsers(searchValue);
      if (response.code === 0) {
        setUsers(response.data.userInfoList.map((user: ISimpleUser) => ({ label: `${user.name}(${user.alias})`, value: user.id })) || []);
      }
    } catch (error) {
      console.error('加载用户列表失败:', error);
    } finally {
      setLoadingUsers(false);
    }
  };
  const handleActionClick = async (action: IWorkflowAction) => {
    console.log('action', action)
    if (ticketId) {
      // handle ticket
      console.log('ticketId', ticketId)
      // if action typ
      if (["add_comment", "forward", "consult", "consult_submit"].indexOf(action.type) !== -1) {
        // show comment dialog
        setOpenCommentDialog(true)
        setDialogActionType(action.type)
        setActionRunning('common')
      } else if (["force_forward", "force_close", "force_alter_node"].indexOf(action.type) !== -1) {
        setActionRunning('admin')
        setOpenCommentDialog(true)
        setDialogActionType(action.type)
      }
      else {
        const res = await handleTicket({
          ticketId: ticketId, actionType: action.type, actionId: action.id, fields: fields, actionProps: {
            comment: '',
            nodeId: actionBaseNodeId,
          }
        })
        if (res.code === 0) {
          showMessage(res.msg, 'success')
          if (onTicketHandledChange) {
            onTicketHandledChange(res.data.ticketId)
          }
        } else {
          showMessage(res.msg, 'error')
        }
      }


    } else {
      // new ticket
      console.log('no ticketId')
      const res = await newTicket({ workflowId: workflowId!, actionId: action.id, fields: fields })
      if (res.code === 0) {
        showMessage(res.msg, 'success')
        if (onTicketHandledChange) {
          onTicketHandledChange(res.data.ticketId)
        }
      }
      else {
        showMessage(res.msg, 'error')
      }
    }
  }

  const handleDialogActionSubmit = async (actionType: string) => {
    console.log('comment submit')
    const actionProps: any = {
      comment: dialogComment, nodeId: actionBaseNodeId
    }
    if (["forward", "consult", "force_forward"].indexOf(actionType) !== -1) {
      actionProps.targetAssigneeId = selectedAssignee?.value
    }
    const res = await handleTicket({
      ticketId: ticketId!, actionType: actionType, actionId: '', actionProps
    })
    if (res.code === 0) {
      showMessage('操作成功', 'success')
      if (onTicketHandledChange) {
        onTicketHandledChange(res.data.ticketId)
      }
    } else {
      showMessage(res.msg, 'error')
    }
    handleDialogClose()
  }

  return (
    <>
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
        <Typography variant="h6" marginBottom={2}>

          {workflowId ? 'New Ticket' : 'Ticket Detail'}
          <Button variant="text" onClick={() => setOpenWorkflowDiagram(true)}>{formSchema?.workflowMetadata?.name}</Button>
        </Typography>
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
                            {fieldComponent.componentName}
                            {fieldComponent.componentPermission === 'required' && (
                              <Box component="span" sx={{ color: 'error.main', ml: 0.25 }}>*</Box>
                            )}
                            {fieldComponent.description && (
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
                        <Box sx={{ flex: 1, display: 'flex', alignItems: 'center', minHeight: 40 }}>
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
          {formActions?.map((action: IWorkflowAction) => {
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
      {ticketId && (
        <Paper sx={{ mt: 2, p: 2, border: '1px solid', borderColor: 'divider' }}>
          <Typography variant="h6" sx={{ mb: 1 }}>管理员操作</Typography>
          <Box sx={{ display: 'flex', justifyContent: 'flex-start', gap: 2, mt: 2 }}>
            {adminFormActions?.map((action: IWorkflowAction) => {
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
        </Paper >
      )
      }
      {
        ticketId && (
          <TicketHistory ticketId={ticketId} refreshToken={refreshToken} />
        )
      }
      <Dialog
        maxWidth="lg"
        fullWidth
        open={openWorkflowDiagram}
        onClose={handleWorkflowDiagramClose}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogContent>
          <WorkflowDiagram workflowId={formSchema?.workflowMetadata?.id ?? ''} workflowVersionId={formSchema?.workflowMetadata?.versionId ?? ''} ticketId={ticketId ?? ''} />
        </DialogContent>
      </Dialog>

      <Dialog
        maxWidth="sm"
        fullWidth
        open={openCommentDialog}
        onClose={handleDialogClose}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        {["forward", "consult", "force_forward"].indexOf(dialogActionType) !== -1 && (
          <DialogContent>
            <Autocomplete
              options={users}
              getOptionLabel={(option) => option.label}
              value={selectedAssignee}
              onChange={(e, value) => handleAssigneeSelectChange(value)}
              onInputChange={(e, value) => {
                if (value.length > 0) {
                  loadUsers(value);
                }
              }}
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="选择处理人"
                  placeholder="输入关键词后搜索用户..."
                  InputProps={{
                    ...params.InputProps,
                    endAdornment: (
                      <>
                        {loadingUsers ? <CircularProgress color="inherit" size={20} /> : null}
                        {params.InputProps.endAdornment}
                      </>
                    ),
                  }}
                />
              )}
              loading={loadingUsers}
              size="small"
              fullWidth
            />
          </DialogContent>
        )}
        <DialogContent>
          <TextField
            label="Comment"
            fullWidth
            multiline
            rows={4}
            value={dialogComment}
            onChange={(e) => setDialogComment(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleDialogClose}>Cancel</Button>
          <Button onClick={() => handleDialogActionSubmit(dialogActionType)}>Submit</Button>
        </DialogActions>
      </Dialog>
    </>
  );
}

export default TicketDetail;