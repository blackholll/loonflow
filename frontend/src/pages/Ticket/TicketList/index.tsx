import React, {Component} from "react";
import moment from 'moment';
import styles from "./index.less";
import {Table, message, Modal, Col, Form, Input, Row, DatePicker, Button, Select, Popconfirm} from "antd";
import {addCommentRequest, delTicketRequest, getTicketList} from '@/services/ticket';
import TicketDetail from "@/pages/Ticket/TicketDetail";
import {getWorkflowList} from "@/services/workflows";

const { RangePicker } = DatePicker;
let timeout;
let currentValue;
const { TextArea } = Input;

class TicketList extends Component<any, any> {
  constructor(props) {
    super(props);
    this.state = {
      ticketResult: [],
      workflowResult: [],
      ticketListLoading: false,
      deleteVisible: false,
      deleteId: 0,
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
    if(this.props.parentTicketId){
      values.parent_ticket_id = this.props.parentTicketId
    }
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
      deleteVisible: false
    });
  };

  handleCancel = e => {
    console.log(e);
    this.setState({
      visible: false,
      deleteVisible: false
    });
  };

  handleTicketOk = () => {
    this.setState({visible:false});
    this.fetchTicketData({});
  }

  deleteOk = async(values:any) => {
    const result = await delTicketRequest(this.state.deleteId, values);
    if (result.code === 0){
      message.success('successfully deleted');
      this.setState({deleteVisible: false});
      this.fetchTicketData({});
    } else {
      message.error(`failed to delete：${result.msg}`);
    }
  }

  showDeleteModal = (ticketId:number) => {
    this.setState({deleteVisible: true, deleteId:ticketId});
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
        title: "serial number",
        dataIndex: "sn",
        key: "sn"
      },
      {
        title: "title",
        dataIndex: "title",
        key: "title"
      },
      {
        title: "type",
        dataIndex: "workflow_info",
        key: "workflow_info",
        render: (text: { workflow_name: any }) => (
          text.workflow_name
        )
      },
      {
        title: "state",
        dataIndex: "state",
        key: "state",
        render: (text: { state_name: string }) => (
          text.state_name
        )
      },
      {
        title: "creator",
        dataIndex: "creator",
        key: "creator"
      },
      {
        title: "gmt_created",
        dataIndex: "gmt_created",
        key: "gmt_created"
      },
      {
        title: "action",
        key: "action",
        render: (text: string, record: any) => {
          if (["all", "intervene"].indexOf(this.props.category) !== -1 && !this.props.parentTicketId) {
            return (
              <span>
                <a style={{marginRight: 5}} onClick={() => this.showTicketDetail(record.id)}>Details</a> |
                <a onClick={() => this.showDeleteModal(record.id)} style={{color:'red', marginLeft: 5}}>delete</a>

              </span>
            )
          } else {
            return (
              <span>
                <a style={{marginRight: 5}} onClick={() => this.showTicketDetail(record.id)}>Details</a>
              </span>
            )
          }
        }
  }
    ];

    const getFields = () => {
      const children = [
        <Col span={6} key={"titleCol"}>
          <Form.Item
            name={"title"}
            label={"Title"}
          >
        <Input placeholder="Support title fuzzy query" />
          </Form.Item>
        </Col>,
        <Col span={6} key={"workflowId"}>
          <Form.Item
            name={"workflow_ids"}
            label={"Ticket type"}
          >
            <Select
              showSearch
              // labelInValue
              style={{ width: 200 }}
              placeholder="Select ticket type"
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
        </Col>
        ,
        <Col span={6} key={"creator"}>
          <Form.Item
            name={"creator"}
            label={"Creator"}
          >
            <Input placeholder="Please fill in the ticket creator" />
          </Form.Item>
        </Col>,
        <Col span={6} key={"sn"}>
          <Form.Item
            name={"sn"}
            label={"serial number"}
          >
            <Input placeholder="Please enter the work order serial number" />
          </Form.Item>
        </Col>,
        <Col span={6} key={"create_time"}>
          <Form.Item
            name={"create_time"}
            label={"create_time"}
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
        {!this.props.parentTicketId? <Form
          name="advanced_search"
          className="ant-advanced-search-form"
          ref={this.formRef}
          onFinish={this.searchTicket}
        >
          <Row gutter={24}>{getFields()}</Row>
          <Row>
            <Col span={24} style={{ textAlign: 'right' }}>
              <Button type="primary" htmlType="submit">
                search
              </Button>
              <Button
                style={{ margin: '0 8px' }}
                onClick={() => {
                  this.formRef.current.resetFields();
                }}
              >
                reset
              </Button>
            </Col>
          </Row>

        </Form>: null}

        <div id="components-table-demo-basic">
          {this.props.parentTicketId && this.state.ticketResult.length ?
            <Table loading={this.state.ticketListLoading}
                   title={()=>{return 'Sub work order'}}
                   columns={columns}
                   dataSource={this.state.ticketResult}
                   rowKey={record=>record.id}
                   pagination={this.state.pagination}
            />
          : null
          }
          {!this.props.parentTicketId? <Table loading={this.state.ticketListLoading}
                                               columns={columns}
                                               dataSource={this.state.ticketResult}
                                               rowKey={record=>record.id}
                                               pagination={this.state.pagination}
          />: null}

        </div>
        <Modal
          title={`Ticket Details: #${this.state.openTicketId}`}
          width={1024}
          visible={this.state.visible}
          onOk={this.handleOk}
          onCancel={this.handleCancel}
          destroyOnClose
          footer={null}

        >
          <TicketDetail ticketId={this.state.openTicketId} handleTicketOk={()=>this.handleTicketOk()}/>
        </Modal>

        <Modal
          title={"delete ticket"}
          visible={this.state.deleteVisible}
          onCancel={this.handleCancel}
          footer={null}>
          <Form
            onFinish={this.deleteOk}
          >
            <Form.Item
              name="suggestion"
            >
              <TextArea
                placeholder="Please enter the reason for deletion"
              />
            </Form.Item>
            <Form.Item>
              <Button type="primary" htmlType="submit" className="login-form-button">
                提交
              </Button>
            </Form.Item>
          </Form>
        </Modal>

      </div>
    )
  }
}

export default TicketList;
