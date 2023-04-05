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
    pagination.current = result.data.page;
    pagination.pageSize = result.data.per_page;
    pagination.total = result.data.total;
    if (result.code ===0){
      this.setState({transitionList: result.data.value, pagination, transtionListLoading:false})
    }
    else {
      message.error(`获取工作流流转失败：${result.msg}`)
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
    return Promise.reject('格式不正确，需要是数组的json格式');
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
      message.success('保存成功');
      this.setState({transitionDetail:{}, transitionModalVisible:false})
      this.fetchTransitionListData({page:1, per_page:10});

    } else {
      message.error(`保存失败:${result.msg}`);
    }
  }

  delWorkflowTransition=async(transitionId:Number) => {
    const result = await delWorkflowTransition(this.props.workflowId, transitionId);
    if (result.code === 0){
      message.success('删除成功');
      this.fetchTransitionListData({page:1, per_page:10});
    } else {
      message.error(`删除失败:${result.msg}`);
    }
  }

  render() {
    const columns = [
      {
        title: "名称",
        dataIndex: "name",
        key: "name"
      },
      {
        title: "定时器(单位:秒)",
        dataIndex: "timer",
        key: "timer"
      },
      {
        title: "源状态",
        dataIndex: ["source_state_info", "name"],
        key: "source_state_info"
      },
      {
        title: "目标状态",
        dataIndex: ["destination_state_info", "name"],
        key: "destination_state_info"
      },
      {
        title: "条件表达式",
        dataIndex: "condition_expression",
        key: "condition_expression"
      },
      {
        title: "属性类型",
        key: "attribute_type_id",
        render:(text:string, record:any) => {
          if (record.attribute_type_id == 1) {
            return "同意"
          } else if (record.attribute_type_id == 2) {
            return "拒绝"
          }
          return "其他"
        }
      },
      {
        title: "是否校验必填项",
        key: "field_require_check",
        render:(text:string, record:any) => {
          if (record.field_require_check) {
            return "是"
          }
          return "否"
        }
      },
      {
        title: "点击弹窗提示",
        key: "alert_enable",
        render:(text:string, record:any) => {
          if (record.alert_enable) {
            return "是"
          }
          return "否"
        }
      },
      {
        title: "创建人",
        dataIndex: "creator",
        key: "creator",
      },
      {
        title: "创建时间",
        dataIndex: "gmt_created",
        key: "gmt_created",
      },
      {
        title: "操作",
        key: "action",
        render:(text:string, record:any) => (
          <span>
                <a style={{marginRight: 16}} onClick={() => this.showWorkflowTransitionModal(record)}>编辑</a>
                <a style={{marginRight: 16, color: "red"}}>
                  <Popconfirm
                    title="确认删除么？"
                    onConfirm={()=>{this.delWorkflowTransition(record.id)}}
                  >
                    删除
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
                label={"查询"}
              >
                <Input placeholder="支持根据流转名称模糊查询" />
              </Form.Item>
            </Col>
            <Col>
              <Button type="primary" htmlType="submit">
                搜索
              </Button>
            </Col>
          </Row>
          <Row>
            <Col span={24} style={{ textAlign: 'right' }}>
              <Button type="primary" onClick={()=>this.showWorkflowTransitionModal({})}>
                新增
              </Button>
            </Col>
          </Row>
        </Form>

        <Table loading={this.state.workflowStateListLoading} columns={columns} dataSource={this.state.transitionList}
               rowKey={record => record.id} pagination={this.state.pagination}/>
        <Modal
          title="流转"
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
                       label={<span>名称<Tooltip title="请输入流转的名称"><QuestionCircleOutlined /></Tooltip></span>}
                       rules={[{ required: true }]} >
              <Input />
            </Form.Item>
            <Form.Item name="source_state_id"
                       label={<span>源状态<Tooltip title="请选择流转的初始状态，即在哪个状态下出现这个按钮"><QuestionCircleOutlined /></Tooltip></span>}
                       rules={[{ required: true }]}
            >
              <Select
                allowClear
                style={{ width: '100%' }}
                placeholder="请选择流转的源状态"
                //defaultValue={['a10', 'c12']}
              >
                {this.state.stateList.map(d => (
                  <Option key={d.id}>{d.name}</Option>
                ))}
              </Select>

            </Form.Item>
            <Form.Item name="destination_state_id"
                       label={<span>目标状态<Tooltip title="请选择流转的目标，即点击此流转操作后工单状态的变化"><QuestionCircleOutlined /></Tooltip></span>}
            >
              <Select
                allowClear
                style={{ width: '100%' }}
                placeholder="请选择流转的目标状态"
              >
                {this.state.stateList.map(d => (
                  <Option key={d.id}>{d.name}</Option>
                ))}
              </Select>
            </Form.Item>

            <Form.Item name="condition_expression"
                       label={<span>条件表达式<Tooltip title='流转条件表达式，根据表达式中的条件来确定流转的下个状态，格式为[{"expression":"{days} > 3 and {days} ≤10", "target_state_id":11},{"expression":"{days} >10", "target_state_id":12}] 其中{}用于填充工单的字段key,运算时会换算成实际的值，当符合条件下个状态将变为target_state_id中的值,表达式只支持简单的运算或datetime/time运算.loonflow会以首次匹配成功的条件为准，所以多个条件不要有冲突'><QuestionCircleOutlined /></Tooltip></span>}
                       rules={[{ validator: this.isExpressionCheck}]}
            >
              <TextArea/>
            </Form.Item>
            <Form.Item name="timer"
                       label={<span>定时器(单位秒)<Tooltip title='设置定时器后，当超过定时器的时间无处理操作，则自动流转到下个状态。0表示不设置'><QuestionCircleOutlined /></Tooltip></span>}
            >
              <InputNumber />
            </Form.Item>
            <Form.Item name="attribute_type_id"
                       label={<span>属性类型<Tooltip title="可用于标识工单的状态:审批通过，被拒绝等"><QuestionCircleOutlined /></Tooltip></span>}
                       rules={[{ required: true }]} >
              <Radio.Group >
                <Radio value={1}>同意</Radio>
                <Radio value={2}>拒绝</Radio>
                <Radio value={3}>其他</Radio>
              </Radio.Group>
            </Form.Item>
            <Form.Item name="field_require_check"
                       valuePropName="checked"
                       label={<span>校验必填项<Tooltip title="默认在用户点击操作的时候需要校验工单表单的必填项,如果设置为否则不检查。用于如'退回'属性的操作，不需要填写表单内容"><QuestionCircleOutlined /></Tooltip></span>}
            >
              <Switch checkedChildren="是" unCheckedChildren="否" />
            </Form.Item>
            <Form.Item name="alert_enable"
                       valuePropName="checked"
                       label={<span>点击弹窗提示<Tooltip title="可以用于当用户在处理工单时做特定操作时，弹窗提示信息。 如用户点击'拒绝'时弹窗提示要求用户确认是否真的拒绝，避免点错"><QuestionCircleOutlined /></Tooltip></span>}>
              <Switch checkedChildren="是" unCheckedChildren="否" />
            </Form.Item>

            <Form.Item name="alert_text"
                       label={<span>弹窗内容<Tooltip title='当开启点击弹窗提示时生效，详情中用户点击操作后弹窗提示的内容'><QuestionCircleOutlined /></Tooltip></span>}
            >
              <Input />

            </Form.Item>

            <Form.Item {...tailLayout}>
              <Button type="primary" htmlType="submit">
                确定
              </Button>
            </Form.Item>

          </Form>
        </Modal>
      </div>
    )

  }
}

export default WorkflowTransiton;
