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
    pagination.current = result.data.page;
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
    this.fetchStateListData({...values, per_page:10, page:1})
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
    return Promise.reject('格式不正确，需要是字典的的json格式');
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
      message.success('保存成功');
      this.setState({customFieldDetail:{}, workflowStateModalVisible:false})
      this.fetchStateListData({page:1, per_page:10});
    } else {
      message.error(`保存失败:${result.msg}`);
    }

  }

  delWorkflowState=async(stateId:Number) => {
    const result = await delWorkflowState(this.props.workflowId, stateId);
    if (result.code === 0){
      message.success('删除成功');
      this.fetchStateListData({page:1, per_page:10});
    } else {
      message.error(`删除失败:${result.msg}`);
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
        title: "名称",
        dataIndex: "name",
        key: "name"
      },
      {
        title: "是否隐藏",
        key: "is_hidden",
        render: (text:string, record:any) => {
          if(record.is_hidden) {
            return "是"
          }
          return "否"
        }
      },
      {
        title: "顺序ID",
        dataIndex: "order_id",
        key: "order_id",
      },
      {
        title: "类型",
        key: "type_id",
        render: (text: string, record: any) =>{
          if(record.type_id ===0) {
            return "普通状态"
          } else if (record.type_id === 1) {
            return "初始状态"
          } else if (record.type_id === 2) {
            return "结束状态"
          }
        }
      },
      {
        title: "参与人类型",
        key: "participant_type",
        render: (text:string, record: any) =>{
          if (record.participant_type_id === 1) {
            return "个人"
          } else if (record.participant_type_id === 2) {
            return "多人"
          }else if (record.participant_type_id === 3) {
            return "部门"
          }else if (record.participant_type_id === 4) {
            return "角色"
          }else if (record.participant_type_id === 5) {
            return "变量"
          }else if (record.participant_type_id === 6) {
            return "脚本"
          }else if (record.participant_type_id === 7) {
            return "工单字段"
          }else if (record.participant_type_id === 8) {
            return "父工单字段"
          }else if (record.participant_type_id === 10) {
            return "hook"
          }
        }

      },
      {
        title: "参与人",
        dataIndex: ["participant_info", "participant_alias"],
        key: "participant",
      },
      {
        title: "分配方式",
        key: "distribute_type_id",
        render: (text:string, record:any) => {
          if (record.distribute_type_id ===1 ){
            return "主动接单"
          }else if (record.distribute_type_id ===2 ){
            return "直接处理"
          }else if (record.distribute_type_id ===3 ){
            return "随机分配"
          }else if (record.distribute_type_id ===4 ){
            return "全部处理"
          }
        }
      },
      {
        title: "创建人",
        key: "creator",
        dataIndex: "creator"
      },
      {
        title: "创建时间",
        key: "gmt_created",
        dataIndex: "gmt_created"
      },
      {
        title: "操作",
        key: "action",
        render:(text:string, record:any) => (
          <span>
                <a style={{marginRight: 16}} onClick={() => this.showWorkflowStateModal(record)}>编辑</a>
                <a style={{marginRight: 16, color: "red"}}>
                  <Popconfirm
                    title="确认删除么？ 删除后如果有工单处于此状态将无法被处理，另外检查下是否工作流流转配置中是否用了此状态"
                    onConfirm={()=>{this.delWorkflowState(record.id)}}
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
          onFinish={this.searchState}
        >
          <Row gutter={24}>
            <Col span={6} key={"search_value"}>
              <Form.Item
                name={"search_value"}
                label={"查询"}
              >
                <Input placeholder="支持根据状态名称模糊查询" />
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
              <Button type="primary" onClick={()=>this.showWorkflowStateModal({})}>
                新增
              </Button>
            </Col>
          </Row>
        </Form>

        <Table loading={this.state.workflowStateListLoading} columns={columns} dataSource={this.state.workflowStateList}
               rowKey={record => record.id} pagination={this.state.pagination}/>
        <Modal
          title="状态"
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
                       label={<span>名称<Tooltip title="请输入状态的名称,如发起人编辑中，发起人tl审批中，结束等"><QuestionCircleOutlined /></Tooltip></span>}
                       rules={[{ required: true }]} >
              <Input />
            </Form.Item>
            <Form.Item name="is_hidden"
                       valuePropName="checked"
                       label={<span>是否隐藏<Tooltip title="开启时,工单详情中step图不显示此状态(当前处于此状态时除外)"><QuestionCircleOutlined /></Tooltip></span>}
            >
              <Switch checkedChildren="是" unCheckedChildren="否" />
            </Form.Item>
            <Form.Item name="order_id"
                       label={<span>顺序id<Tooltip title="此顺序id,用于获取工单step记录的排序用,因为step是顺序的，而loonflow的工作流是网状的，所以需要指定顺序id以便排序,数字越小越靠前"><QuestionCircleOutlined /></Tooltip></span>}
                       rules={[{ required: true }]}
            >
              <InputNumber min={0}/>
            </Form.Item>
            <Form.Item name="type_id"
                       label={<span>状态类型<Tooltip title="每个工作流都需要有一个初始状态，一个结束状态，其他为普通状态。初始状态及结束状态无需设置参与人类型及参与人"><QuestionCircleOutlined /></Tooltip></span>}
                       rules={[{ required: true }]} >
              <Radio.Group >
                <Radio value={0}>普通状态</Radio>
                <Radio value={1}>初始状态</Radio>
                <Radio value={2}>结束状态</Radio>
              </Radio.Group>
            </Form.Item>
            <Form.Item name="remember_last_man_enable"
                       valuePropName="checked"
                       label={<span>记忆最后处理人<Tooltip title="开启后，到达此状态时会先检查之前是否有人在此状态处理过，如果有则处理人为最后一次处理的人"><QuestionCircleOutlined /></Tooltip></span>}
                       >
              <Switch checkedChildren="是" unCheckedChildren="否" />
            </Form.Item>
            <Form.Item name="enable_retreat"
                       valuePropName="checked"
                       label={<span>允许撤回<Tooltip title="开启后，工单的创建人可以在工单处于此状态时将工单撤回到初始状态"><QuestionCircleOutlined /></Tooltip></span>}>
              <Switch checkedChildren="是" unCheckedChildren="否" />
            </Form.Item>
            <Form.Item name="participant_type_id"
                       rules={[{ required: true }]}
                       label={<span>参与人类型<Tooltip title='初始状态的处理人类型和处理人和选择无和留空(状态的处理人仅供状态变化时确定新的处理人用，不会作为流转时目的状态，所以无需配置)， 结束状态处理人类型和处理人也请选择无和留空，因为结束状态无需人再处理'><QuestionCircleOutlined /></Tooltip></span>}
            >
              <Select
                allowClear
                style={{ width: '100%' }}
                placeholder="请选择参与人类型"
              >
                  <Option value={1}>个人</Option>
                  <Option value={2}>多人</Option>
                  <Option value={3}>部门</Option>
                  <Option value={4}>角色</Option>
                  <Option value={5}>变量</Option>
                  {/*/!*<Option value={6}>脚本</Option>*!/ 已废弃*/}
                  <Option value={7}>工单字段</Option>
                  <Option value={8}>父工单字段</Option>
                  <Option value={10}>hook</Option>
                  <Option value={11}>外部获取</Option>
                  <Option value={0}>无</Option>
              </Select>
            </Form.Item>
            <Form.Item name="participant"
                       label={<span>参与人<Tooltip title='个人(username)\多人(多个username以,隔开\部门(部门id，多个部门以逗号隔开)\角色(角色id)\变量(creator:工单的创建人,creator_tl:工单创建人的TL,多个变量逗号隔开)\脚本记录的id\工单字段(逗号隔开多个)\父工单字段(逗号隔开多个)等，需要在此状态创建子工单时需要设置此处处理人为loonrobot。 当处理人类型为hook方式时,处理人需要按照如下规则配置 {"hook_url":"http://xxx.com/xxx", "hook_token":"xxxx", "wait":true, "extra_info":"xxxx"},外部获取配置规则:{"external_url":"http://xxx.com/xxx", "external_token":"xxxx", "extra_info":"xxxx"}。详见文档'><QuestionCircleOutlined /></Tooltip></span>}
            >
              <Input />

            </Form.Item>
            <Form.Item name="distribute_type_id"
                       label={<span>分配方式<Tooltip title='直接处理:当前处理人无需接单，主动接单:当前处理人需要先接单再处理，随机分配:工单将随机指定所配置的当前处理人中一个人， 全部处理:当前所有人都需要处理完且处理动作相同才会流转到下个状态'><QuestionCircleOutlined /></Tooltip></span>}
            >
              <Select
                allowClear
                style={{ width: '100%' }}
                placeholder="请选择分配方式"
              >
                <Option value={2}>直接处理</Option>
                <Option value={1}>主动接单</Option>
                <Option value={3}>随机分配</Option>
                <Option value={4}>全部处理</Option>
              </Select>

            </Form.Item>
            <Form.Item name="state_field_str"
                       label={<span>表单字段<Tooltip title='json格式字典存储,包括读写属性1：只读，2：必填，3：可选. 示例：{"gmt_created":1,"title":2, "sn":1}, 内置特殊字段participant_info.participant_name:当前处理人信息(部门名称、角色名称)，state.state_name:当前状态的状态名,workflow.workflow_name:工作流名称'><QuestionCircleOutlined /></Tooltip></span>}
                       rules={[{ validator: this.isDictJsonCheck}]}
            >
              <Input />

            </Form.Item>
            <Form.Item name="label"
                       label= {<span>标签<Tooltip title="自定义标签，json格式，调用方可根据标签自行处理特殊场景逻辑，loonflow只保存文本内容"><QuestionCircleOutlined /></Tooltip></span>}
                       rules={[{ validator: this.isDictJsonCheck}]}
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

export default WorkflowState;
