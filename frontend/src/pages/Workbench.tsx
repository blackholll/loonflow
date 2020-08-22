import React, {Component} from 'react';
import { PageContainer } from '@ant-design/pro-layout';
import {Card, Select, Button, message, Modal} from 'antd';
import DutyTicket from './ticket/DutyTicket';
import {getWorkflowList} from "@/services/workflows";
import TicketDetail from "@/pages/ticket/TicketDetail";

const { Option } = Select;



class Workbench extends Component<any, any> {
  constructor(props) {
    super(props);
    this.state = {
      workflowResult: [],
      selectWorkflowId: 0,
      selectWorkflowName: '',
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
          <Button type="primary" onClick={this.showNewTicketModal}>新建</Button>

        </Card>
        <Card title="我的待办">
          <DutyTicket />
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
        <TicketDetail workflowId={this.state.selectWorkflowId} ticketId={0}/>

        </Modal>

      </PageContainer>
    )
  }
}

export default Workbench;
