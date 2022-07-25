import React, { Component } from "react";
import {
  Table,
  Form,
  Card,
  Popconfirm,
  Row,
  Col,
  Input,
  Button,
  Modal,
  Tooltip,
  Select,
  message,
  Switch,
  InputNumber,
  Radio
} from "antd";
import {QuestionCircleOutlined} from "@ant-design/icons/lib";
import {
  addWorkflowState,
  getWorkflowState,
  updateWorkflowState,
  delWorkflowState
} from "@/services/workflows";

const { TextArea } = Input;

class WorkflowState extends Component<any, any> {
  constructor(props) {
    super(props);
    this.state = {
      workflowStateList: [],
      workflowStateDetail: {},
      workflowStateListLoading: false,
      workflowStateModalVisible: false,
      pagination: {
        current: 1,
        total: 0,
        pageSize: 10,
        onChange: (current)=> {
          const pagination = { ...this.state.pagination };
          pagination.page = current;
          pagination.current = current;
          this.setState({ pagination }, () => {
            this.fetchStateListData({
              page: pagination.page,
              per_page: pagination.pageSize
            })
          });
        }
      }
    }
  }

  componentDidMount() {
    this.fetchStateListData({page:1, per_page:10});
  }

  fetchStateListData = async(params)=>{
    this.setState({workflowStateListLoading: true});
    const result = await getWorkflowState(this.props.workflowId, params);
    const pagination = { ...this.state.pagination };
    pagination.page = result.data.page;
    pagination.pageSize = result.data.per_page;
    pagination.total = result.data.total;
    if (result.code ===0){
      this.setState({workflowStateList: result.data.value, pagination, workflowStateListLoading:false})
    }
    else {
      message.error(`获取工作流状态失败：${result.msg}`)
    }
  }

  searchState = (values) => {
    this.fetchStateListData({...values, page_page:10, page:1})
  }

  showWorkflowStateModal = (workflowStateDetail) => {
    this.setState({workflowStateDetail: workflowStateDetail, workflowStateModalVisible:true})
  }

  handleStateCancel = () => {
    console.log('cancel')
    this.setState({workflowStateModalVisible: false, workflowStateDetail: {}},()=>console.log(this.state.workflowStateDetail))
  }

  handleStateOk = () => {
    console.log('handleok')
    this.setState({workflowStateModalVisible: false, workflowStateDetail: {}}, ()=>console.log(this.state.workflowStateDetail))
  }

  getFieldInitialValues = () => {
    const result = this.state.workflowStateDetail;

    if (result && result['label']) {
      if (!(typeof (result['label']) == "string")) {
        result['label'] = JSON.stringify(result['label'])
      }
    }else {
      result['label'] = "{}"
    }
    if (result && result['state_field_str']) {
      if (!(typeof (result['state_field_str']) == "string")) {
        result['state_field_str'] = JSON.stringify(result['state_field_str'])
      }
    }else {
      result['state_field_str'] = "{}"
    }

    if (! result.order_id) {
      result.order_id=0
    }
    if (! result.type_id) {
      result.type_id=0
    }
    if (! result.distribute_type_id) {
      result.distribute_type_id=2
    }

    return result
  }

  isJsonCheck = (str) => {
    if (typeof str === 'string') {
      try {
        const obj=JSON.parse(str);
        if(typeof obj == 'object' && obj ){
          return true;
        }else{
          return false;
        }

      } catch(e) {
        return false;
      }
    }
    return false;
  }

  isDictJsonCheck = (rule, value) => {
    if (typeof value === 'string') {
      if (value.startsWith('{') && this.isJsonCheck(value)){
        return Promise.resolve();
      }
    }
    return Promise.reject('The format is incorrect, it needs to be the json format of the dictionary');
  }


  onStateFinish = async(values) => {
    // values.order_id = Number(values.order_id);
    if (values.remember_last_man_enable){
      values.remember_last_man_enable = 1
    }
    else {
      values.remember_last_man_enable = 0
    }
    let result = {};
    if (this.state.workflowStateDetail && this.state.workflowStateDetail.id) {
      result = await updateWorkflowState(this.props.workflowId, this.state.workflowStateDetail.id, values);
    } else {
      result = await addWorkflowState(this.props.workflowId, values);
    }
    if (result.code === 0){
      message.success('Successfully saved');
      this.setState({customFieldDetail:{}, workflowStateModalVisible:false})
      this.fetchStateListData({page:1, per_page:10});
    } else {
      message.error(`Failed to save:${result.msg}`);
    }

  }

  delWorkflowState=async(stateId:Number) => {
    const result = await delWorkflowState(this.props.workflowId, stateId);
    if (result.code === 0){
      message.success('successfully deleted');
      this.fetchStateListData({page:1, per_page:10});
    } else {
      message.error(`failed to delete:${result.msg}`);
    }
  }


  render() {
    const columns = [
      {
        title: "ID",
        dataIndex: "id",
        key: "id"
      },
      {
        title: "name",
        dataIndex: "name",
        key: "name"
      },
      {
        title: "whether to hide",
        key: "is_hidden",
        render: (text:string, record:any) => {
          if(record.is_hidden) {
            return "Yes"
          }
          return "No"
        }
      },
      {
        title: "Order Id",
        dataIndex: "order_id",
        key: "order_id",
      },
      {
        title: "type",
        key: "type_id",
        render: (text: string, record: any) =>{
          if(record.type_id ===0) {
            return "normal state"
          } else if (record.type_id === 1) {
            return "initial state"
          } else if (record.type_id === 2) {
            return "end state"
          }
        }
      },
      {
        title: "participant type",
        key: "participant_type",
        render: (text:string, record: any) =>{
          if (record.participant_type_id === 1) {
            return "personal"
          } else if (record.participant_type_id === 2) {
            return "multiple people"
          }else if (record.participant_type_id === 3) {
            return "Department"
          }else if (record.participant_type_id === 4) {
            return "Role"
          }else if (record.participant_type_id === 5) {
            return "variable"
          }else if (record.participant_type_id === 6) {
            return "Screenplay"
          }else if (record.participant_type_id === 7) {
            return "Ticket fields"
          }else if (record.participant_type_id === 8) {
            return "Parent Ticket Fields"
          }else if (record.participant_type_id === 10) {
            return "hook"
          }
        }

      },
      {
        title: "participant",
        dataIndex: ["participant_info", "participant_alias"],
        key: "participant",
      },
      {
        title: "Allocation",
        key: "distribute_type_id",
        render: (text:string, record:any) => {
          if (record.distribute_type_id ===1 ){
            return "Active order"
          }else if (record.distribute_type_id ===2 ){
            return "direct processing"
          }else if (record.distribute_type_id ===3 ){
            return "Randomly assigned"
          }else if (record.distribute_type_id ===4 ){
            return "Process all"
          }
        }
      },
      {
        title: "creator",
        key: "creator",
        dataIndex: "creator"
      },
      {
        title: "gmt_created",
        key: "gmt_created",
        dataIndex: "gmt_created"
      },
      {
        title: "action",
        key: "action",
        render:(text:string, record:any) => (
          <span>
                <a style={{marginRight: 16}} onClick={() => this.showWorkflowStateModal(record)}>edit</a>
                <a style={{marginRight: 16, color: "red"}}>
                  <Popconfirm
                    title="Are you sure to delete? After deletion, if there is a work order in this state, it will not be processed. In addition, check whether this state is used in the workflow flow configuration."
                    onConfirm={()=>{this.delWorkflowState(record.id)}}
                  >
                    delete
                  </Popconfirm>
                </a>
              </span>

        )
      }
    ]

    const layout = {
      labelCol: { span: 8 },
      wrapperCol: { span: 16 },
    };
    const tailLayout = {
      wrapperCol: { offset: 8, span: 16 },
    };

    const formInitialValues = this.getFieldInitialValues();
    console.log(formInitialValues);

    return (
      <div>
        <Form
          name="advanced_search"
          className="ant-advanced-search-form"
          onFinish={this.searchState}
        >
          <Row gutter={24}>
            <Col span={6} key={"search_value"}>
              <Form.Item
                name={"search_value"}
                label={"search_value"}
              >
                <Input placeholder="Support fuzzy query based on state name" />
              </Form.Item>
            </Col>
            <Col>
              <Button type="primary" htmlType="submit">
                search
              </Button>
            </Col>
          </Row>
          <Row>
            <Col span={24} style={{ textAlign: 'right' }}>
              <Button type="primary" onClick={()=>this.showWorkflowStateModal({})}>
                new
              </Button>
            </Col>
          </Row>
        </Form>

        <Table loading={this.state.workflowStateListLoading} columns={columns} dataSource={this.state.workflowStateList}
               rowKey={record => record.id} pagination={this.state.pagination}/>
        <Modal
          title="state"
          visible={this.state.workflowStateModalVisible}
          onOk={this.handleStateOk}
          onCancel={this.handleStateCancel}
          width={800}
          footer={null}
          destroyOnClose
        >
          <Form
            {...layout}
            onFinish={this.onStateFinish}
            initialValues={ formInitialValues }
          >
            <Form.Item name="name"
                       label={<span>name<Tooltip title="Please enter the name of the status, such as sponsor editing, sponsor tl reviewing, ending, etc."><QuestionCircleOutlined /></Tooltip></span>}
                       rules={[{ required: true }]} >
              <Input />
            </Form.Item>
            <Form.Item name="is_hidden"
                       valuePropName="checked"
                       label={<span>whether to hide<Tooltip title="When enabled, the step diagram in the work order details does not display this state (except when it is currently in this state)"><QuestionCircleOutlined /></Tooltip></span>}
            >
              <Switch checkedChildren="Yes" unCheckedChildren="No" />
            </Form.Item>
            <Form.Item name="order_id"
                       label={<span>Order id <Tooltip title="This sequence id is used to obtain the sorting of the work order step records. Because the steps are sequential, and the workflow of loonflow is meshed, it is necessary to specify the sequence id for sorting. The smaller the number, the higher the priority."><QuestionCircleOutlined /></Tooltip></span>}
                       rules={[{ required: true }]}
            >
              <InputNumber min={0}/>
            </Form.Item>
            <Form.Item name="type_id"
                       label={<span>state type<Tooltip title="Every workflow needs to have an initial state, an end state, and the others are normal states. The initial state and end state do not need to set the participant type and participant"><QuestionCircleOutlined /></Tooltip></span>}
                       rules={[{ required: true }]} >
              <Radio.Group >
                <Radio value={0}>normal state</Radio>
                <Radio value={1}>initial state</Radio>
                <Radio value={2}>end state</Radio>
              </Radio.Group>
            </Form.Item>
            <Form.Item name="remember_last_man_enable"
                       valuePropName="checked"
                       label={<span>memory last processor<Tooltip title="After it is turned on, when reaching this state, it will first check whether someone has processed it in this state before, and if so, the processing person will be the last processing person."><QuestionCircleOutlined /></Tooltip></span>}
                       >
              <Switch checkedChildren="Yes" unCheckedChildren="No" />
            </Form.Item>
            <Form.Item name="enable_retreat"
                       valuePropName="checked"
                       label={<span>Allow withdrawal<Tooltip title="After opening, the creator of the ticket can withdraw the ticket to the initial state when the ticket is in this state"><QuestionCircleOutlined /></Tooltip></span>}>
              <Switch checkedChildren="Yes" unCheckedChildren="No" />
            </Form.Item>
            <Form.Item name="participant_type_id"
                       rules={[{ required: true }]}
                       label={<span>participant type<Tooltip title='Handler type and handler and selection of initial state are none and left blank (the handler of the state is only used to determine a new handler when the state changes, and will not be used as the destination state during the transfer, so no configuration is required), the end state handler type and handler, please select None and leave it blank, because the end state does not need to be processed by anyone.'><QuestionCircleOutlined /></Tooltip></span>}
            >
              <Select
                allowClear
                style={{ width: '100%' }}
                placeholder="Please select participant type"
              >
                  <Option value={1}>personal</Option>
                  <Option value={2}>multiple people</Option>
                  <Option value={3}>department</Option>
                  <Option value={4}>Role</Option>
                  <Option value={5}>variable</Option>
                  <Option value={6}>Screenplay</Option>
                  <Option value={7}>Ticket fields</Option>
                  <Option value={8}>Parent Ticket Fields</Option>
                  <Option value={10}>hook</Option>
                  <Option value={0}>none</Option>
              </Select>
            </Form.Item>
            <Form.Item name="participant"
                       label={<span>participant<Tooltip title='Individual (username)\multiple people (multiple usernames separated by ,\department (department id, multiple departments separated by comma)\role (role id)\variable (creator: creator of the work order, creator_tl: work order TL of the creator, multiple variables separated by commas)\id of script record\work order fields (multiple separated by commas)\parent ticket fields (multiple separated by commas), etc. You need to create sub-work orders in this state You need to set the handler here as loonrobot. When the handler type is hook, the handler needs to configure {"hook_url":"http://xxx.com/xxx", "hook_token":"xxxx", "wait":true, "extra_info":"xxxx"}. See documentation for details'><QuestionCircleOutlined /></Tooltip></span>}
            >
              <Input />

            </Form.Item>
            <Form.Item name="distribute_type_id"
                       label={<span>Allocation<Tooltip title='Direct processing: the current handler does not need to accept the order, and takes the initiative to accept the order: the current handler needs to take the order first and then process it, random allocation: the work order will randomly assign one of the configured current handlers, and all processing: all currently need to After processing and the processing action is the same, it will flow to the next state'><QuestionCircleOutlined /></Tooltip></span>}
            >
              <Select
                allowClear
                style={{ width: '100%' }}
                placeholder="Please select a distribution method"
              >
                <Option value={2}>direct processing</Option>
                <Option value={1}>Active order</Option>
                <Option value={3}>Randomly assigned</Option>
                <Option value={4}>Process all</Option>
              </Select>

            </Form.Item>
            <Form.Item name="state_field_str"
                       label={<span>form fields<Tooltip title='json format dictionary storage, including read-write attributes 1: read-only, 2: required, 3: optional. Example: {"gmt_created":1,"title":2, "sn":1}, built-in special field participant_info .participant_name: current processor information (department name, role name), state.state_name: state name of the current state, workflow.workflow_name: workflow name'><QuestionCircleOutlined /></Tooltip></span>}
                       rules={[{ validator: this.isDictJsonCheck}]}
            >
              <Input />

            </Form.Item>
            <Form.Item name="label"
                       label= {<span>label<Tooltip title="Custom label, json format, the caller can handle special scene logic according to the label, loonflow only saves the text content"><QuestionCircleOutlined /></Tooltip></span>}
                       rules={[{ validator: this.isDictJsonCheck}]}
            >
              <Input />
            </Form.Item>

            <Form.Item {...tailLayout}>
              <Button type="primary" htmlType="submit">
                Submit
              </Button>
            </Form.Item>

          </Form>
        </Modal>
      </div>
    )
  }

}

export default WorkflowState;
