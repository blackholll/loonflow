import React, {Component} from "react";
import moment from 'moment';
import styles from "./index.less";
import {Table, message, Modal, Col, Form, Input, Row, DatePicker, Button, Select} from "antd";
import { getTicketList } from '@/services/ticket';
import TicketDetail from "@/pages/Ticket/TicketDetail";
import {getWorkflowList} from "@/services/workflows";

const { RangePicker } = DatePicker;
let timeout;
let currentValue;

class TicketList extends Component<any, any> {
  constructor(props) {
    super(props);
    this.state = {
      ticketResult: [],
      workflowResult: [],
      ticketListLoading: false,
      searchArgs: {},
      userResult: [],
      pagination: {
        current: 1,
        total: 0,
        pageSize: 10,
        onChange: (current) => {
          const pagination = { ...this.state.pagination };
          pagination.page = current;
          pagination.current = current;
          this.setState({ pagination }, () => {
            this.fetchTicketData({
              page: pagination.page,
              per_page: pagination.pageSize
            })
          });
        }
      }
    };
  }
  formRef = React.createRef<FormInstance>();


  componentDidMount() {
    this.fetchTicketData({});
    this.fetchWorkflowData();
  };

  componentDidUpdate(prevProps: Readonly<any>, prevState: Readonly<any>, snapshot?: any) {
    if (this.props.reloadFlag !== prevProps.reloadFlag) {
      this.fetchTicketData({});
    }
  }

  fetchTicketData = async (values) => {
    this.setState({ticketListLoading: true})
    values.category = this.props.category;
    values = Object.assign(values, this.state.searchArgs);
    const result = await getTicketList(values);
    if (result.code === 0) {
      const pagination = { ...this.state.pagination };
      pagination.page = result.data.page;
      pagination.pageSize = result.data.per_page;
      pagination.total = result.data.total;

      this.setState({ticketResult: result.data.value, ticketListLoading: false, pagination});
    } else {
      message.error(result.msg);
      this.setState({ticketListLoading: false});
    }
  };

  fetchWorkflowData = async () => {
    const result = await getWorkflowList({per_page: 1000})
    if (result.code === 0) {
      this.setState({workflowResult: result.data.value});
    } else {
      message.error(result.msg);
    }

  }

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

  handleTicketOk = () => {
    this.setState({visible:false});
    this.fetchTicketData({});
  }

  searchTicket = (values) => {
    console.log(values);
    if (values.create_time){
      if (values.create_time[0]){
        values.create_start = values.create_time[0].format('YYYY-MM-DD HH:mm:ss')
      }
      if (values.create_time[1]){
        values.create_end = values.create_time[1].format('YYYY-MM-DD HH:mm:ss')
      }
      delete(values.create_time)

    }
    this.setState({searchArgs: values})
    this.fetchTicketData(values);
  }


  render() {

    const userOptions = this.state.userResult.map(d => <Select.Option key={d.value}>{d.text}</Select.Option>);

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
        title: "标题",
        dataIndex: "title",
        key: "title"
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
      </span>
        )
      }

    ];

    const getFields = () => {
      const children = [
        <Col span={6} key={"titleCol"}>
          <Form.Item
            name={"title"}
            label={"标题"}
          >
            <Input placeholder="支持标题模糊查询" />
          </Form.Item>
        </Col>,
        <Col span={6} key={"workflowId"}>
          <Form.Item
            name={"workflow_ids"}
            label={"工单类型"}
          >
            <Select
              showSearch
              // labelInValue
              style={{ width: 200 }}
              placeholder="选择工单类型"
              optionFilterProp="children"
              filterOption={(input, option) =>
                Select.Option.children.toLowerCase().indexOf(input.toLowerCase()) >= 0
              }
            >
              {this.state.workflowResult.map(d => (
                <Select.Option key={d.id} value={d.id}>{d.name}</Select.Option>
              ))}
            </Select>
          </Form.Item>

        </Col>,
        <Col span={6} key={"creator"}>
          <Form.Item
            name={"creator"}
            label={"创建人"}
          >
            <Input placeholder="请填写工单创建人" />
          </Form.Item>
        </Col>,
        <Col span={6} key={"sn"}>
          <Form.Item
            name={"sn"}
            label={"流水号"}
          >
            <Input placeholder="请输入工单流水号" />
          </Form.Item>
        </Col>,
        <Col span={6} key={"create_time"}>
          <Form.Item
            name={"create_time"}
            label={"创建时间"}
          >
            <RangePicker
              showTime={{
                hideDisabledOptions: true,
                defaultValue: [moment('00:00:00', 'HH:mm:ss'), moment('11:59:59', 'HH:mm:ss')],
              }}
              format="YYYY-MM-DD HH:mm:ss "
            />
          </Form.Item>
        </Col>
      ]
      return children;
    };

    return (
      <div className={styles.container}>
        <Form
          name="advanced_search"
          className="ant-advanced-search-form"
          ref={this.formRef}
          onFinish={this.searchTicket}
        >
          <Row gutter={24}>{getFields()}</Row>
          <Row>
            <Col span={24} style={{ textAlign: 'right' }}>
              <Button type="primary" htmlType="submit">
                搜索
              </Button>
              <Button
                style={{ margin: '0 8px' }}
                onClick={() => {
                  this.formRef.current.resetFields();
                }}
              >
                重置
              </Button>
            </Col>
          </Row>

        </Form>
        <div id="components-table-demo-basic">
          <Table loading={this.state.ticketListLoading}
                 columns={columns}
                 dataSource={this.state.ticketResult}
                 rowKey={record=>record.id}
                 pagination={this.state.pagination}
          />
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
          <TicketDetail ticketId={this.state.openTicketId} handleTicketOk={()=>this.handleTicketOk()}/>
        </Modal>
      </div>
    )
  }
}

export default TicketList;
