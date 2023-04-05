import React, { Component } from "react";
import {Table, Form, Card, Popconfirm, Row, Col, Input, Button, Select, Modal, message, Tooltip} from "antd";
import {addCustomField, getWorkflowCustomField, updateCustomField, delCustomField} from "@/services/workflows";
import {addRole, updateRole} from "@/services/user";
import {QuestionCircleOutlined} from "@ant-design/icons/lib";

const { TextArea } = Input;


class WorkflowCustomFieldList extends Component<any, any> {
  constructor(props) {
    super(props);
    this.state = {
      customFieldDetail: {},
      customFieldList: [],
      customFieldListLoading: false,
      customFieldModalVisible: false,
      pagination: {
        current: 1,
        total: 0,
        pageSize: 10,
        onChange: (current) => {
          const pagination = { ...this.state.pagination };
          pagination.page = current;
          pagination.current = current;
          this.setState({ pagination }, () => {
            this.fetchCustomFieldListData({
              page: pagination.page,
              per_page: pagination.pageSize
            })
          });
        }
      }
    }
  }

  componentDidMount() {
    // get list data
    this.fetchCustomFieldListData({page:1, per_page:10});
  }

  fetchCustomFieldListData = async(params) => {
    this.setState({customFieldListLoading: true})
    const result = await getWorkflowCustomField(this.props.workflowId, params);
    const pagination = { ...this.state.pagination };
    pagination.current = result.data.page;
    pagination.pageSize = result.data.per_page;
    pagination.total = result.data.total;

    if (result.code ===0){
      this.setState({customFieldList: result.data.value, pagination, customFieldListLoading:false})
    }
  }

  searchCustomFiled = (values)=> {
    this.fetchCustomFieldListData({...values, per_page:10, page:1})
  }

  handleCustomFieldOk = () => {
    this.setState({customFieldModalVisible: false})
  }

  handleCustomFieldCancel = () => {
    this.setState({customFieldModalVisible: false})
  }

  onCustomFieldFinish = async(values) => {
    values.order_id = Number(values.order_id);
    let result = {};
    if (this.state.customFieldDetail && this.state.customFieldDetail.id) {
      result = await updateCustomField(this.props.workflowId, this.state.customFieldDetail.id, values);
    } else {
      result = await addCustomField(this.props.workflowId, values);
    }
    if (result.code === 0){
      message.success('保存成功');
      this.setState({customFieldDetail:{}, customFieldModalVisible:false})
      this.fetchCustomFieldListData({page:1, per_page:10});
    } else {
      message.error(`保存失败:${result.msg}`);
    }
  }

  showCustomFieldModal = (customFieldDetail) => {
    this.setState({customFieldDetail: customFieldDetail, customFieldModalVisible:true})
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

  getFieldInitialValues = () => {
    const result = this.state.customFieldDetail;

    if (result && result['field_choice']) {
      if (!(typeof(result['field_choice']) == "string")){
      result['field_choice'] = JSON.stringify(result['field_choice'])
      }
    }
      else {
      result['field_choice'] = "{}"
    }

    if (result && result['boolean_field_display']) {
      if (!(typeof(result['boolean_field_display']) == "string")){
        result['boolean_field_display'] = JSON.stringify(result['boolean_field_display'])
      }
      } else {
      result['boolean_field_display'] = "{}"
    }

    if (result && result['label']) {
      if (!(typeof(result['label']) == "string")){
        result['label'] = JSON.stringify(result['label'])
      }
    } else {
      result['label'] = "{}"
    }
    return result
  }

  delCustomField = async(fieldId) => {
    const result = await  delCustomField(this.props.workflowId, fieldId);
    if (result.code === 0) {
      message.success('删除字段成功');
      this.fetchCustomFieldListData({per_page:10, page:1})
    }
    else {
      message.error(`删除字段失败: ${result.msg}`);
    }

  }



  render() {
    const columns = [
      {
        title: "字段名称",
        dataIndex: "field_name",
        key: "field_name"
      },
      {
        title: "字段标识",
        dataIndex: "field_key",
        key: "name"
      },

      {
        title: "字段类型",
        key: "field_type",
        render: (text: string, record: any) => {
          if (record.field_type_id === 5) {
            return "字符串"
          } else if (record.field_type_id === 10){
            return "整型"
          } else if (record.field_type_id === 15) {
            return "浮点型"
          } else if (record.field_type_id === 20) {
            return "布尔"
          } else if (record.field_type_id === 25) {
            return "日期"
          } else if (record.field_type_id === 30) {
            return "日期时间"
          } else if (record.field_type_id === 35) {
            return "单选框"
          } else if (record.field_type_id === 40) {
            return "多选框"
          } else if (record.field_type_id === 45) {
            return "下拉列表"
          } else if (record.field_type_id === 50) {
            return "多选下拉列表"
          } else if (record.field_type_id === 55) {
            return "文本域"
          } else if (record.field_type_id === 58) {
            return "富文本"
          } else if (record.field_type_id === 60) {
            return "用户"
          } else if (record.field_type_id === 70) {
            return "多选用户"
          } else if (record.field_type_id === 80) {
            return "附件"
          }
        }
      },
      {
        title: "顺序Id",
        dataIndex: "order_id",
        key: "order_id"
      },
      {
        title: "字段描述",
        dataIndex: "description",
        key: "description"
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
        render:(text:string, record:any) => (
          <span>
            <a style={{marginRight: 16}} onClick={() => this.showCustomFieldModal(record)}>编辑</a>
            <a style={{marginRight: 16, color: "red"}}>
              <Popconfirm
                title="确认删除么？ 删除后需要删除其他地方此字段的配置，如工作流展现表单，状态的表单字段配置"
                onConfirm={()=>{this.delCustomField(record.id)}}
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

    return (
      <div>
        <Form
          name="advanced_search"
          className="ant-advanced-search-form"
          onFinish={this.searchCustomFiled}
        >
          <Row gutter={24}>
            <Col span={6} key={"search_value"}>
              <Form.Item
                name={"search_value"}
                label={"查询"}
              >
                <Input placeholder="支持根据字段名称模糊查询" />
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
              <Button type="primary" onClick={()=>this.showCustomFieldModal({})}>
                新增
              </Button>
            </Col>
          </Row>
        </Form>
        <Table loading={this.state.deptListLoading} columns={columns} dataSource={this.state.customFieldList}
               rowKey={record => record.id} pagination={this.state.pagination}/>
        <Modal
          title="自定义字段"
          visible={this.state.customFieldModalVisible}
          onOk={this.handleCustomFieldOk}
          onCancel={this.handleCustomFieldCancel}
          width={800}
          footer={null}
          destroyOnClose
        >
          <Form
            {...layout}
            onFinish={this.onCustomFieldFinish}
            initialValues={ formInitialValues }
          >
            <Form.Item name="field_key"
                       label={<span>字段标识<Tooltip title="请输入字段的标识,要求英文字母及下划线组成，以字母开头，且不得使用工单基础字段如(sn、title、state_id等字符)"><QuestionCircleOutlined /></Tooltip></span>}
                       rules={[{ required: true }]} >
              <Input />
            </Form.Item>
            <Form.Item name="field_name"
                       label={<span>字段名称<Tooltip title="请输入字段的名称，建议中文，如请假原因、服务器规格等"><QuestionCircleOutlined /></Tooltip></span>}
                       rules={[{ required: true }]} >
              <Input />
            </Form.Item>
            <Form.Item name="description"
                       label={<span>字段描述<Tooltip title="字段描述信息将显示在工单详情的该字段下方"><QuestionCircleOutlined /></Tooltip></span>}>
              <Input />
            </Form.Item>
            <Form.Item name="field_type_id" label="字段类型" rules={[{ required: true }]} >
              <Select
                allowClear
                showSearch
                style={{ width: '100%' }}
                placeholder="字段的类型"
              >
                <Select.Option value={5}>字符型</Select.Option>
                <Select.Option value={10}>整型</Select.Option>
                <Select.Option value={15}>浮点型</Select.Option>
                <Select.Option value={20}>布尔</Select.Option>
                <Select.Option value={25}>日期</Select.Option>
                <Select.Option value={30}>日期时间</Select.Option>
                <Select.Option value={35}>单选框</Select.Option>
                <Select.Option value={40}>多选框</Select.Option>
                <Select.Option value={45}>下拉列表</Select.Option>
                <Select.Option value={50}>多选下拉列表</Select.Option>
                <Select.Option value={55}>文本域</Select.Option>
                <Select.Option value={58}>富文本(待支持)</Select.Option>
                <Select.Option value={60}>用户名</Select.Option>
                <Select.Option value={70}>多选用户名</Select.Option>
                <Select.Option value={80}>附件</Select.Option>
              </Select>
            </Form.Item>
            <Form.Item name="order_id"
                       label={<span>顺序id<Tooltip title="工单详情中字段排列顺序。值越小，越靠前,内置字段顺序为: sn:10, title:20, state_id:40, state.state_name:41,participant_info.participant_name:50, participant_info.participant_alias:55,workflow.workflow_name:60,creator:80,gmt_created:100, gmt_modified:120"><QuestionCircleOutlined /></Tooltip></span>}
                       rules={[{ required: true }]} >
              <Input />
            </Form.Item>
            <Form.Item name="default_value"
                       label={<span>默认值<Tooltip title="新建工单时，作为该字段的默认值"><QuestionCircleOutlined /></Tooltip></span>}>
              <Input />
            </Form.Item>
            <Form.Item name="boolean_field_display"
                       label={<span>布尔显示定义<Tooltip title='当为布尔类型时候，可以支持自定义显示形式。{"1":"是","0":"否"}或{"1":"需要","0":"不需要"}，注意数字也需要引号'><QuestionCircleOutlined /></Tooltip></span>}
                       rules={[{ validator: this.isDictJsonCheck}]}
            >
              <Input />
            </Form.Item>
            <Form.Item name="field_choice"
                       label={<span>选项<Tooltip title='radio,checkbox,select,multiselect类型可供选择的选项，格式为json如:{"1":"中国", "2":"美国"},注意数字也需要引号'><QuestionCircleOutlined /></Tooltip></span>}
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
            <Form.Item name="field_template"
                       label={<span>模板<Tooltip title="文本域类型字段前端显示时可以将此内容作为字段的placeholder或默认值"><QuestionCircleOutlined /></Tooltip></span>}
            >
              <TextArea
                autoSize={{ minRows: 2, maxRows: 6 }}
              />
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

export default WorkflowCustomFieldList;
