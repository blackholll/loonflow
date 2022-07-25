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
    pagination.page = result.data.page;
    pagination.pageSize = result.data.per_page;
    pagination.total = result.data.total;

    if (result.code ===0){
      this.setState({customFieldList: result.data.value, pagination, customFieldListLoading:false})
    }
  }

  searchCustomFiled = (values)=> {
    this.fetchCustomFieldListData({...values, page_page:10, page:1})
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
      message.success('Successfully saved');
      this.setState({customFieldDetail:{}, customFieldModalVisible:false})
      this.fetchCustomFieldListData({page:1, per_page:10});
    } else {
      message.error(`Failed to save:${result.msg}`);
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
    return Promise.reject('The format is incorrect, it needs to be the json format of the dictionary');
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
      message.success('Delete field succeeded');
      this.fetchCustomFieldListData({per_page:10, page:1})
    }
    else {
      message.error(`Delete field failed: ${result.msg}`);
    }

  }



  render() {
    const columns = [
      {
        title: "Field Name",
        dataIndex: "field_name",
        key: "field_name"
      },
      {
        title: "Field Key",
        dataIndex: "field_key",
        key: "name"
      },

      {
        title: "Field Type",
        key: "field_type",
        render: (text: string, record: any) => {
          if (record.field_type_id === 5) {
            return "string"
          } else if (record.field_type_id === 10){
            return "Integer"
          } else if (record.field_type_id === 15) {
            return "floating"
          } else if (record.field_type_id === 20) {
            return "boolean"
          } else if (record.field_type_id === 25) {
            return "date"
          } else if (record.field_type_id === 30) {
            return "datetime"
          } else if (record.field_type_id === 35) {
            return "Single box"
          } else if (record.field_type_id === 40) {
            return "Checkbox"
          } else if (record.field_type_id === 45) {
            return "drop-down list"
          } else if (record.field_type_id === 50) {
            return "Multi-select drop-down list"
          } else if (record.field_type_id === 55) {
            return "text field"
          } else if (record.field_type_id === 58) {
            return "rich text"
          } else if (record.field_type_id === 60) {
            return "user"
          } else if (record.field_type_id === 70) {
            return "Multiple users"
          } else if (record.field_type_id === 80) {
            return "appendix"
          }
        }
      },
      {
        title: "Order Id",
        dataIndex: "order_id",
        key: "order_id"
      },
      {
        title: "Description",
        dataIndex: "description",
        key: "description"
      },
      {
        title: "Creator",
        dataIndex: "creator",
        key: "creator"
      },
      {
        title: "creation time",
        dataIndex: "gmt_created",
        key: "gmt_created"
      },
      {
        title: "action",
        key: "action",
        render:(text:string, record:any) => (
          <span>
            <a style={{marginRight: 16}} onClick={() => this.showCustomFieldModal(record)}>edit</a>
            <a style={{marginRight: 16, color: "red"}}>
              <Popconfirm
                title="Are you sure to delete? After deleting, you need to delete the configuration of this field in other places, such as the workflow presentation form, the form field configuration of the status"
                onConfirm={()=>{this.delCustomField(record.id)}}
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
                label={"search value"}
              >
                <Input placeholder="Support fuzzy query based on field name" />
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
              <Button type="primary" onClick={()=>this.showCustomFieldModal({})}>
                new
              </Button>
            </Col>
          </Row>
        </Form>
        <Table loading={this.state.deptListLoading} columns={columns} dataSource={this.state.customFieldList}
               rowKey={record => record.id} pagination={this.state.pagination}/>
        <Modal
          title="custom field"
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
                       label={<span>Field ID<Tooltip title="Please enter the identifier of the field, which must be composed of English letters and underscores, start with a letter, and must not use the basic fields of the work order such as (sn, title, state_id, etc.)"><QuestionCircleOutlined /></Tooltip></span>}
                       rules={[{ required: true }]} >
              <Input />
            </Form.Item>
            <Form.Item name="field_name"
                       label={<span>Field Name<Tooltip title="Please enter the name of the field, Chinese is recommended, such as the reason for leave, server specifications, etc."><QuestionCircleOutlined /></Tooltip></span>}
                       rules={[{ required: true }]} >
              <Input />
            </Form.Item>
            <Form.Item name="description"
                       label={<span>Description<Tooltip title="Field description information will be displayed below the field in the ticket details"><QuestionCircleOutlined /></Tooltip></span>}>
              <Input />
            </Form.Item>
            <Form.Item name="field_type_id" label="Field Type" rules={[{ required: true }]} >
              <Select
                allowClear
                showSearch
                style={{ width: '100%' }}
                placeholder="type of field"
              >
                <Select.Option value={5}>character type</Select.Option>
                <Select.Option value={10}>Integer</Select.Option>
                <Select.Option value={15}>floating field</Select.Option>
                <Select.Option value={20}>boolean</Select.Option>
                <Select.Option value={25}>date</Select.Option>
                <Select.Option value={30}>datetime</Select.Option>
                <Select.Option value={35}>Single box</Select.Option>
                <Select.Option value={40}>Checkbox</Select.Option>
                <Select.Option value={45}>drop-down list</Select.Option>
                <Select.Option value={50}>Multi-select drop-down list</Select.Option>
                <Select.Option value={55}>text field</Select.Option>
                <Select.Option value={58}>Rich text (to be supported)</Select.Option>
                <Select.Option value={60}>username</Select.Option>
                <Select.Option value={70}>Multiple Username</Select.Option>
                <Select.Option value={80}>appendix</Select.Option>
              </Select>
            </Form.Item>
            <Form.Item name="order_id"
                       label={<span>Order Id<Tooltip title="The order of fields in the ticket details. The smaller the value, the higher the priority. The built-in field sequence is: sn:10, title:20, state_id:40, state.state_name:41,participant_info.participant_name:50, participant_info.participant_alias:55,workflow.workflow_name:60,creator :80,gmt_created:100,gmt_modified:120"><QuestionCircleOutlined /></Tooltip></span>}
                       rules={[{ required: true }]} >
              <Input />
            </Form.Item>
            <Form.Item name="default_value"
                       label={<span>Defaults<Tooltip title="When a new work order is created, it is used as the default value of this field"><QuestionCircleOutlined /></Tooltip></span>}>
              <Input />
            </Form.Item>
            <Form.Item name="boolean_field_display"
                       label={<span>boolean display definition<Tooltip title='When it is a boolean type, it can support a custom display form. {"1":"yes","0":"no"} or {"1":"required","0":"not required"}, note that numbers also need quotes'><QuestionCircleOutlined /></Tooltip></span>}
                       rules={[{ validator: this.isDictJsonCheck}]}
            >
              <Input />
            </Form.Item>
            <Form.Item name="field_choice"
                       label={<span>Options<Tooltip title='Options for radio, checkbox, select, multiselect types, the format is json such as: {"1":"China", "2":"United States"}, note that numbers also need quotation marks'><QuestionCircleOutlined /></Tooltip></span>}
                       rules={[{ validator: this.isDictJsonCheck}]}
            >
              <Input />

            </Form.Item>
            <Form.Item name="label"
                       label= {<span>Label<Tooltip title="Custom label, json format, the caller can handle special scene logic according to the label, loonflow only saves the text content"><QuestionCircleOutlined /></Tooltip></span>}
                       rules={[{ validator: this.isDictJsonCheck}]}
            >
              <Input />
            </Form.Item>
            <Form.Item name="field_template"
                       label={<span>template<Tooltip title="This content can be used as the placeholder or default value of the field when the text field type field is displayed on the front end"><QuestionCircleOutlined /></Tooltip></span>}
            >
              <TextArea
                autoSize={{ minRows: 2, maxRows: 6 }}
              />
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

export default WorkflowCustomFieldList;
