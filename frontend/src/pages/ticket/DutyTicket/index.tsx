import React, {Component} from "react";
import styles from "./index.less";
import { Table, message, Modal } from "antd";
import { getTicketList } from '@/services/ticket';
import TicketDetail from "@/pages/ticket/TicketDetail";


class DutyTicket extends Component<any, any> {
  constructor(props) {
    super(props);
    this.state = {ticketResult: [], workflowResult: [], dutyListLoading: false};
  }


  componentDidMount() {
     this.fetchTicketData();
  };

  fetchTicketData = async () => {
    this.setState({dutyListLoading: true})
    const result = await getTicketList({category: 'duty'});
    if (result.code === 0) {
      this.setState({ticketResult: result.data.value, dutyListLoading: false});
    } else {
      message.error(result.msg);
      this.setState({dutyListLoading: false});
    }
  };


  showTicketDetail = (ticketId) => {
    this.setState({
      openTicketId: ticketId,
      visible: true,
    });
  };

  handleOk = e => {
    console.log(e);
    this.setState({
      visible: false,
    });
  };

  handleCancel = e => {
    console.log(e);
    this.setState({
      visible: false,
    });
  };

   render() {

    const columns = [
      {
        title: "Id",
        dataIndex: "id",
        key: "id",
      },
      {
        title: "流水号",
        dataIndex: "sn",
        key: "sn"
      },
      {
        title: "类型",
        dataIndex: "workflow_info",
        key: "workflow_info",
        render: (text: { workflow_name: any }) => (
          text.workflow_name
        )
      },
      {
        title: "当前状态",
        dataIndex: "state",
        key: "state",
        render: (text: { state_name: string }) => (
          text.state_name
        )
      },
      {
        title: "创建人",
        dataIndex: "creator",
        key: "creator"
      },
      {
        title: "创建时间",
        dataIndex: "gmt_created",
        key: "gmt_created"
      },
      {
        title: "操作",
        key: "action",
        render: (text: string, record: any) => (
          <span>
        <a style={{ marginRight: 16 }} onClick={()=> this.showTicketDetail(record.id)}>详情</a>
        <a>新页面打开</a>
      </span>
        )
      }

    ];
    return (
      <div className={styles.container}>
        <div id="components-table-demo-basic">
          <Table loading={this.state.dutyListLoading} columns={columns} dataSource={this.state.ticketResult} rowKey={record=>record.id}/>
        </div>
        <Modal
          title={`工单详情: #${this.state.openTicketId}`}
          width={1024}
          visible={this.state.visible}
          onOk={this.handleOk}
          onCancel={this.handleCancel}
          destroyOnClose
          footer={null}

        >
          <TicketDetail ticketId={this.state.openTicketId} />
        </Modal>
      </div>
    )
  }
}

export default DutyTicket;
