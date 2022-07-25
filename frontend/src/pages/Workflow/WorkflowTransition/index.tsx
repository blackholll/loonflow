import React, { Component } from "react";
import { Table, From, Popconfirm, Row, Col, Input, InputNumber, Button, Modal} from "antd";
import {QuestionCircleOutlined} from "@ant-design/icons/lib";
import {
  addWorkflowState, addWorkflowTransition,
  delWorkflowTransition,
  getWorkflowState, getWorkflowTransition,
  updateWorkflowState,
  updateWorkflowTransition
} from "@/services/workflows";
import {message} from "antd";
import {Form} from "antd";
import {Tooltip} from "antd";
import {Switch} from "antd";
import {Radio} from "antd";
import {Select} from "antd";

const { TextArea } = Input;


class WorkflowTransiton extends Component<any, any> {
  constructor(props) {
    super(props);
    this.state = {
      transitionList: [],
      transitionDetail: {},
      transitionListLoading: false,
      transitionModalVisible: false,
      stateList : [],
      pagination: {
        current: 1,
        total: 0,
        pageSize: 10,
        onChange: (current)=> {
          const pagination = { ...this.state.pagination };
          pagination.page = current;
          pagination.current = current;
          this.setState({ pagination }, () => {
            this.fetchTransitionListData({
              page: pagination.page,
              per_page: pagination.pageSize
            })
          });
        }
      }
    }
  }

  componentDidMount() {
    this.fetchTransitionListData({page:1, per_page:10})
    this.fetchStateListData({per_page:1000, page:1})
  }

  fetchStateListData = async(params: any) => {
    const result = await getWorkflowState(this.props.workflowId, params);
    if (result.code === 0 ){
      this.setState({stateList: result.data.value})
    }

  }

  fetchTransitionListData = async(params:any) => {
    this.setState({transitionListLoading: true});
    const result = await getWorkflowTransition(this.props.workflowId, params);
    const pagination = { ...this.state.pagination };
    pagination.page = result.data.page;
    pagination.pageSize = result.data.per_page;
    pagination.total = result.data.total;
    if (result.code ===0){
      this.setState({transitionList: result.data.value, pagination, transtionListLoading:false})
    }
    else {
      message.error(`Failed to get workflow flow：${result.msg}`)
    }
  }

  searchTransiton = (values:any) => {
    this.fetchTransitionListData({...values, page:10, page:1})
  }

  showWorkflowTransitionModal = (workflowTransitionDetail)=> {
    this.setState({transitionDetail:workflowTransitionDetail, transitionModalVisible:true})
  }

  handleTransitionCancel = () => {
    this.setState({transitionDetail:{}, transitionModalVisible:false})
  }
  handleTransitionOk = () => {
    this.setState({transitionDetail:{}, transitionModalVisible:false})
  }

  getFieldInitialValues = () => {
    const result = this.state.transitionDetail;

    if (!result.condition_expression) {
      result.condition_expression = '[]'
    }
    if (result.source_state_id){
      result.source_state_id = String(result.source_state_id)
    }
    if (result.destination_state_id){
      result.destination_state_id = String(result.destination_state_id)
    }
    if (result.destination_state_id){
      result.destination_state_id = String(result.destination_state_id)
    }
    if (!result.timer){
      result.timer = 0
    }
    return result
  }

  isJsonCheck = (str: any)=> {
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

  isExpressionCheck = (rule, value) => {
    if (typeof value === 'string') {
      if (value.startsWith('[') && this.isJsonCheck(value)){
        return Promise.resolve();
      }
    }
    return Promise.reject('The format is incorrect, it needs to be the json format of the array');
  }

  onTransitionFinish = async(values) => {
    let result = {};
    values.source_state_id = Number(values.source_state_id)
    if(values.destination_state_id){
      values.destination_state_id = Number(values.destination_state_id)
    }
    else{
      values.destination_state_id = 0
    }
    if (values.field_require_check == true){
      values.field_require_check = 1
    } else {
      values.field_require_check = 0
    }
    if (values.alert_enable){
      values.alert_enable =1
    } else {
      values.alert_enable = 0
    }


    if (this.state.transitionDetail && this.state.transitionDetail.id) {
      result = await updateWorkflowTransition(this.props.workflowId, this.state.transitionDetail.id, values);
    } else {
      result = await addWorkflowTransition(this.props.workflowId, values);
    }
    if (result.code === 0){
      message.success('Successfully saved');
      this.setState({transitionDetail:{}, transitionModalVisible:false})
      this.fetchTransitionListData({page:1, per_page:10});

    } else {
      message.error(`Failed to save:${result.msg}`);
    }
  }

  delWorkflowTransition=async(transitionId:Number) => {
    const result = await delWorkflowTransition(this.props.workflowId, transitionId);
    if (result.code === 0){
      message.success('successfully deleted');
      this.fetchTransitionListData({page:1, per_page:10});
    } else {
      message.error(`failed to delete:${result.msg}`);
    }
  }

  render() {
    const columns = [
      {
        title: "name",
        dataIndex: "name",
        key: "name"
      },
      {
        title: "Timer (unit: second)",
        dataIndex: "timer",
        key: "timer"
      },
      {
        title: "source status",
        dataIndex: ["source_state_info", "name"],
        key: "source_state_info"
      },
      {
        title: "target state",
        dataIndex: ["destination_state_info", "name"],
        key: "destination_state_info"
      },
      {
        title: "conditional expression",
        dataIndex: "condition_expression",
        key: "condition_expression"
      },
      {
        title: "property type",
        key: "attribute_type_id",
        render:(text:string, record:any) => {
          if (record.attribute_type_id == 1) {
            return "agree"
          } else if (record.attribute_type_id == 2) {
            return "reject"
          }
          return "other"
        }
      },
      {
        title: "Whether to verify required items",
        key: "field_require_check",
        render:(text:string, record:any) => {
          if (record.field_require_check) {
            return "on"
          }
          return "off"
        }
      },
      {
        title: "Click on the pop-up prompt",
        key: "alert_enable",
        render:(text:string, record:any) => {
          if (record.alert_enable) {
            return "on"
          }
          return "off"
        }
      },
      {
        title: "creator",
        dataIndex: "creator",
        key: "creator",
      },
      {
        title: "gmt_created",
        dataIndex: "gmt_created",
        key: "gmt_created",
      },
      {
        title: "action",
        key: "action",
        render:(text:string, record:any) => (
          <span>
                <a style={{marginRight: 16}} onClick={() => this.showWorkflowTransitionModal(record)}>edit</a>
                <a style={{marginRight: 16, color: "red"}}>
                  <Popconfirm
                    title="Are you sure to delete?"
                    onConfirm={()=>{this.delWorkflowTransition(record.id)}}
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
          onFinish={this.searchTransiton}
        >
          <Row gutter={24}>
            <Col span={6} key={"search_value"}>
              <Form.Item
                name={"search_value"}
                label={"search_value"}
              >
                <Input placeholder="Support fuzzy query based on flow name" />
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
              <Button type="primary" onClick={()=>this.showWorkflowTransitionModal({})}>
                new
              </Button>
            </Col>
          </Row>
        </Form>

        <Table loading={this.state.workflowStateListLoading} columns={columns} dataSource={this.state.transitionList}
               rowKey={record => record.id} pagination={this.state.pagination}/>
        <Modal
          title="circulation"
          visible={this.state.transitionModalVisible}
          onOk={this.handleTransitionOk}
          onCancel={this.handleTransitionOk}
          width={800}
          footer={null}
          destroyOnClose
        >
          <Form
            {...layout}
            onFinish={this.onTransitionFinish}
            initialValues={ formInitialValues }
          >
            <Form.Item name="name"
                       label={<span>name<Tooltip title="Please enter the name of the transfer"><QuestionCircleOutlined /></Tooltip></span>}
                       rules={[{ required: true }]} >
              <Input />
            </Form.Item>
            <Form.Item name="source_state_id"
                       label={<span>source status<Tooltip title="Please select the initial state of the flow, that is, in which state this button appears"><QuestionCircleOutlined /></Tooltip></span>}
                       rules={[{ required: true }]}
            >
              <Select
                allowClear
                style={{ width: '100%' }}
                placeholder="Please select the source state of the flow"
                //defaultValue={['a10', 'c12']}
              >
                {this.state.stateList.map(d => (
                  <Option key={d.id}>{d.name}</Option>
                ))}
              </Select>

            </Form.Item>
            <Form.Item name="destination_state_id"
                       label={<span>target state<Tooltip title="Please select the transfer target, that is, the change of the work order status after clicking this transfer operation"><QuestionCircleOutlined /></Tooltip></span>}
            >
              <Select
                allowClear
                style={{ width: '100%' }}
                placeholder="Please select the destination state of the transfer"
              >
                {this.state.stateList.map(d => (
                  <Option key={d.id}>{d.name}</Option>
                ))}
              </Select>
            </Form.Item>

            <Form.Item name="condition_expression"
                       label={<span>conditional expression<Tooltip title='Flow condition expression, the next state of flow is determined according to the conditions in the expression, the format is [{"expression":"{days} > 3 and {days} ≤10", "target_state_id":11},{" expression":"{days} >10", "target_state_id":12}] where {} is used to fill in the field key of the work order, which will be converted to the actual value during operation, and the next state will become target_state_id when the conditions are met The value of , the expression only supports simple operations or datetime/time operations. Loonflow will take the first successful matching condition as the criterion, so multiple conditions should not conflict'><QuestionCircleOutlined /></Tooltip></span>}
                       rules={[{ validator: this.isExpressionCheck}]}
            >
              <TextArea/>
            </Form.Item>
            <Form.Item name="timer"
                       label={<span>Timer (in seconds)<Tooltip title='After setting the timer, if there is no processing operation after the timer expires, the flow will automatically go to the next state. 0 means not set'><QuestionCircleOutlined /></Tooltip></span>}
            >
              <InputNumber />
            </Form.Item>
            <Form.Item name="attribute_type_id"
                       label={<span>property type<Tooltip title="Can be used to identify the status of the work order: approved, rejected, etc."><QuestionCircleOutlined /></Tooltip></span>}
                       rules={[{ required: true }]} >
              <Radio.Group >
                <Radio value={1}>agree</Radio>
                <Radio value={2}>reject</Radio>
                <Radio value={3}>other</Radio>
              </Radio.Group>
            </Form.Item>
            <Form.Item name="field_require_check"
                       valuePropName="checked"
                       label={<span>Check required fields<Tooltip title="By default, when the user clicks the operation, the required items of the work order form need to be verified. If it is set to otherwise, it will not be checked. Used for operations such as 'return' attributes without filling in form content"><QuestionCircleOutlined /></Tooltip></span>}
            >
              <Switch checkedChildren="on" unCheckedChildren="off" />
            </Form.Item>
            <Form.Item name="alert_enable"
                       valuePropName="checked"
                       label={<span>Click on the pop-up prompt<Tooltip title="It can be used for pop-up prompts when the user performs a specific operation while processing a work order. For example, when the user clicks 'Reject', a pop-up window prompts the user to confirm whether it is really rejected, so as to avoid wrong clicks"><QuestionCircleOutlined /></Tooltip></span>}>
              <Switch checkedChildren="on" unCheckedChildren="off" />
            </Form.Item>

            <Form.Item name="alert_text"
                       label={<span>popup content<Tooltip title='It takes effect when the click pop-up prompt is turned on. In the details, the content of the pop-up prompt after the user clicks the operation'><QuestionCircleOutlined /></Tooltip></span>}
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

export default WorkflowTransiton;
