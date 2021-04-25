import React, {Component} from 'react';
import { PageContainer } from '@ant-design/pro-layout';
import {Card, Select, Button, message, Modal, Tooltip} from 'antd';
import DutyTicket from './ticket/DutyTicket';
import {getWorkflowList} from "@/services/workflows";
import TicketDetail from "@/pages/Ticket/TicketDetail";
import TicketList from "@/pages/Ticket/TicketList";

const { Option } = Select;



class Workbench extends Component<any, any> {
  constructor(props) {
    super(props);
    this.state = {
      workflowResult: [],
      selectWorkflowId: 0,
      selectWorkflowName: '',
      newTicketId: 0,
      reloadFlag: 0,
      newTicketVisible:false};

  }

  componentDidMount() {
    this.fetchWorkflowData();
  };

  fetchWorkflowData = async () => {
    const result = await getWorkflowList({per_page: 1000})
    if (result.code === 0) {
      this.setState({workflowResult: result.data.value});
    } else {
      message.error(result.msg);
    }

  }

  workflowSelectOnchange = (value: any) => {
    this.setState({selectWorkflowId: value.value, selectWorkflowName:value.label})
  }

  showNewTicketModal = () => {
    this.setState({newTicketVisible: true});

  }

  handleNewTicketOk = () => {
    this.setState({newTicketVisible: false})
  }

  handleNewTicketCancle = () => {
    this.setState({newTicketVisible: false})
  }

  newTicketOk = (ticketId) =>{
    this.setState({newTicketVisible: false, reloadFlag: ticketId})
  }

  render() {
    return (
      <PageContainer>
        <Card>
          <Select
            showSearch
            labelInValue
            style={{ width: 200 }}
            placeholder="选择工单类型"
            optionFilterProp="children"
            onChange={this.workflowSelectOnchange}
            filterOption={(input, option) =>
              option.children.toLowerCase().indexOf(input.toLowerCase()) >= 0
            }
          >
            {this.state.workflowResult.map(d => (
              <Option key={d.id}>{d.name}</Option>
            ))}
          </Select>
          <Tooltip title={this.state.selectWorkflowId? "": "请先选择工单类型"}>
          <Button type="primary" onClick={this.showNewTicketModal} disabled={this.state.selectWorkflowId? false: true }>新建</Button>
          </Tooltip>

        </Card>
        <Card title="我的待办">
          <TicketList category={'duty'} reloadFlag={this.state.reloadFlag}/>
        </Card>

        <Modal
          title={`新建工单:${this.state.selectWorkflowName}`}
          visible={this.state.newTicketVisible}
          onOk={this.handleNewTicketOk}
          onCancel={this.handleNewTicketCancle}
          width={1024}
          footer={null}
          destroyOnClose
        >
        <TicketDetail workflowId={this.state.selectWorkflowId} ticketId={0} newTicketOk={(ticketId)=>this.newTicketOk(ticketId)}/>

        </Modal>

      </PageContainer>
    )
  }
}

export default Workbench;
