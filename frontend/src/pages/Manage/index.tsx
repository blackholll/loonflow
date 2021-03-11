import React, {Component} from 'react';
import { PageContainer } from '@ant-design/pro-layout';
import {Card, Select, Button, message, Modal, Tabs} from 'antd';
import {getWorkflowList} from "@/services/workflows";
import NoticeRecord from "@/pages/Manage/NoticeManage";

const { Option } = Select;

const { TabPane } = Tabs;


class Manage extends Component<any, any> {
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
          <Tabs defaultActiveKey="1" >
            <TabPane tab="通知配置" key="1">
              <NoticeRecord />
            </TabPane>
            {/*<TabPane tab="LDAP配置" key="2">*/}
            {/*  Content of Tab Pane 2*/}
            {/*</TabPane>*/}
          </Tabs>

        </Card>


      </PageContainer>
    )
  }
}

export default Manage;
