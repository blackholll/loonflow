import React, {Component} from "react";
import styles from "./index.less";
import { Table, message } from "antd";
import { getTicketList } from '@/services/ticket';


class DutyTicket extends Component<any, any> {
  constructor(props) {
    super(props);
    this.state = {ticketResult: [], workflowResult: []};
  }


  componentDidMount() {
     this.fetchTicketData();
  };

  fetchTicketData = async () => {
    const result = await getTicketList({category: 'duty'});
    if (result.code === 0) {
      this.setState({ticketResult: result.data.value});
    } else {
      message.error(result.msg);
    }
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
        <a style={{ marginRight: 16 }}>详情</a>
        <a>新页面打开</a>
      </span>
        )
      }

    ];
    return (
      <div className={styles.container}>
        <div id="components-table-demo-basic">
          <Table columns={columns} dataSource={this.state.ticketResult} />
        </div>
      </div>
    )
  }
}

export default DutyTicket;
