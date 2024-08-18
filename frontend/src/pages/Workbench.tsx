import { Card, Select, Button, message, Modal, Tooltip, Option } from 'antd';
import { PageContainer } from '@ant-design/pro-layout';
// import DutyTicket from './ticket/DutyTicket';
// import TicketDetail from "@/pages/Ticket/TicketDetail";
// import TicketList from "@/pages/Ticket/TicketList";
import { useEffect, useState } from 'react';
import { getSimpleWorkflowList } from '@/services/workflow';


export default function Workbench() {
    const [workflowResult, setWorkflowResult] = useState([]);
    const [selectWorkflowId, setSelectWorkflowId] = useState(0);
    const [selectWorkflowName, setSelectWorkflowName] = useState('');
    const [newTicketId, setNewTicketId] = useState(0);
    const [reloadFlag, setReloadFlag] = useState(0);
    const [newTicketVisible, setNewTicketVisible] = useState(false);
    
    useEffect(() => {
        fetchWorkflowData();
    }, [reloadFlag]);

    const fetchWorkflowData = async () => {
        const result = await getSimpleWorkflowList({ perPage: 1000});
        if (result.code === 0) {
            setWorkflowResult(result.data.workflow_info_list);
        } else {
            message.error(result.msg);
        }
    }

    const workflowSelectOnchange = (value: any) => {
        setSelectWorkflowId(value.value);
        setSelectWorkflowName(value.label);
    }
    const showNewTicketModal = () => {
        setNewTicketVisible(true);
      };
    
      const handleNewTicketOk = () => {
        setNewTicketVisible(false);
      };
    
      const handleNewTicketCancel = () => {
        setNewTicketVisible(false);
      };
    
      const newTicketOk = (ticketId: number) => {
        setNewTicketVisible(false);
        setReloadFlag(ticketId);
      };
      
      const workflowOption = (workflows:any) =>  {
        return workflows.map((workflow:any) => ({value:workflow.id, label:workflow.name})
      )}

      return (
        <PageContainer>
          <Card>
            <Select
              showSearch
              labelInValue
              style={{ width: 200 }}
              placeholder="选择工单类型"
              optionFilterProp="children"
              onChange={workflowSelectOnchange}
              filterOption={(input:string, option?: { label: string; value:string}) =>
                (option?.label ?? '').toLowerCase().includes(input.toLowerCase())
              }
              options={workflowOption(workflowResult)}
            
            />              
            <Tooltip title={selectWorkflowId ? "" : "请先选择工单类型"}>
              <Button type="primary" onClick={showNewTicketModal} disabled={!selectWorkflowId}>
                新建
              </Button>
            </Tooltip>
          </Card>
          {/* <Card title="我的待办">
            <TicketList category="duty" reloadFlag={reloadFlag} />
          </Card> */}
    
          {/* <Modal
            title={`新建工单: ${selectWorkflowName}`}
            visible={newTicketVisible}
            onOk={handleNewTicketOk}
            onCancel={handleNewTicketCancel}
            width={1024}
            footer={null}
            destroyOnClose
          >
            <TicketDetail workflowId={selectWorkflowId} ticketId={0} newTicketOk={newTicketOk} />
          </Modal> */}
        </PageContainer>
      );
    };
    
