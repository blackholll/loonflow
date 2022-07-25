import React, { Component } from "react";
import {Button, Card, Col, Form, Input, message, Row, Select, Switch, Tooltip} from "antd";
import {getWorkflowDetail} from "@/services/workflows";
import {getSimpleNoticeListRequest} from "@/services/manage";
import {getSimpleDeptList, getSimpleTokenListRequest, queryUserSimple} from "@/services/user";
import {QuestionCircleOutlined} from "@ant-design/icons/lib";

const { Option } = Select;
const { TextArea } = Input;


class WorkflowBasicInfo extends Component<any, any> {
  constructor(props) {
    super(props);
    this.state = {
      workflowBasicResult: {},
      noticeList: [],
      appTokenList: [],
      deptList: [],
      optionalFieldList: [],
      searchAdminerResult: [],
      searchIntervenerResult: [],
      searchViewerResult: [],
    }
  }

  formRef = React.createRef<FormInstance>();

  componentDidMount() {
    this.fetchNoticeList();
    this.fetchAppTokenList();
    this.fetchDeptList();
    this.fetchWorkflowDetail();
  }


  fetchWorkflowDetail = async() => {
    const result = await getWorkflowDetail(this.props.workflowId);
    if (result.code !==0) {
      message.error(`Failed to get workflow basic information: ${result.msg}`);
    } else {
      this.setState({workflowBasicResult: result.data});
    }
  }

  fetchNoticeList = async() => {
    const result = await getSimpleNoticeListRequest({per_page:1000, page:1});
    if (result.code === 0) {
      this.setState({noticeList: result.data.value});
    }
  }

  fetchAppTokenList = async() => {
    const result = await getSimpleTokenListRequest({per_page: 10000, page:1});
    if (result.code ===0 ) {
      this.setState({appTokenList: result.data.value})
    }
  }

  fetchDeptList = async()=>{
    const result = await getSimpleDeptList({per_page: 10000, page:1});
    if (result.code ===0 ) {
      this.setState({deptList: result.data.value})
    }
  }

  searchAdminer = async(search_value: string) => {
    const result = await queryUserSimple({search_value:search_value});
    if (result.code ===0 ) {
      this.setState({searchAdminerResult: result.data.value});
    }
  }


  searchIntervener = async(search_value: string) => {
    const result = await queryUserSimple({search_value:search_value});
    if (result.code ===0 ) {
      this.setState({searchIntervenerResult: result.data.value});
    }
  }


  searchViewer = async(search_value: string) => {
    const result = await queryUserSimple({search_value:search_value});
    if (result.code ===0 ) {
      this.setState({searchViewerResult: result.data.value});
    }
  }

  getWorkflowDetailField = (fieldName:string) =>{
    if(this.state && this.state.workflowBasicResult && this.state.workflowBasicResult[fieldName]){
      if (fieldName === 'notices') {
        return this.state.workflowBasicResult[fieldName].split(',');
      }
      return this.state.workflowBasicResult[fieldName]
    }
    return ''
  }

  getWorkflowInitialValues = () => {
    const result = this.state.workflowBasicResult;
    if (result && result['notices']) {
      console.log(result['notices']);
      const notices = result['notices']
      if (!Array.isArray(result['notices'])){
        result['notices'] = notices.split(',');

      }
    }
    return result
  }

  onWorkflowFinish = async(values) => {
    console.log(values);
  }


  render() {
    const layout = {
      labelCol: { span: 4 },
      wrapperCol: { span: 20 },
    };
    const tailLayout = {
      wrapperCol: { offset: 8, span: 16 },
    };
    const formInitialValues = this.getWorkflowInitialValues();
    // const formInitialValues = {"name":"tttt"};
    console.log('the first time')
    console.log(formInitialValues);
    console.log('the first time')
    this.props.form.resetFields(formInitialValues);


    return (
      <Card>
        <Form
          name="workflowDetailForm"
          className="ant-advanced-search-form"
          {...layout}
          onFinish={this.onWorkflowFinish}
          ref={this.formRef}
          initialValues={formInitialValues}
        >
          <Row gutter={24}>
            <Col span={12} key="firstCol">
              <Form.Item
                name="name"
                label= "name"
                rules={[
                  {
                    required: true,
                    message: 'Please enter a workflow name',
                  },
                ]}
              >
                <Input placeholder="Please enter a workflow name"/>
              </Form.Item>
            </Col>
            <Col span={12} key="secondCol">
              <Form.Item
                name="description"
                label= {<span>describe<Tooltip title={"The description will appear on the New Ticket page"}><QuestionCircleOutlined/></Tooltip></span>}
              >
                <Input placeholder="The description information will be displayed on the New Ticket page" value={'sss'}/>
              </Form.Item>
            </Col>
          </Row>
          <Row gutter={24}>
            <Col span={12} key="firstCol">
              <Form.Item
                name="notices"
                label= "notices"
              >
                <Select
                  allowClear
                  showSearch
                  mode= "multiple"
                  style={{ width: '100%' }}
                  placeholder="Please select a notification method"
                >
                  {this.state.noticeList.map(d => (
                    <Option key={d.id}>{d.name}</Option>
                  ))}
                </Select>
              </Form.Item>
            </Col>
            <Col span={12} key="secondCol">
              <Form.Item
                name="limit_expression"
                label= {<span>limit expression<Tooltip title='Default "{}", limit period ({"period":24} 24 hours), limit times ({"count":1} only allow one submission in the limit period), limit level ({"level":1 } For (1 single user 2 global) limit the number of cycles, the default is a specific user); allow specific people to submit ({"allow_persons":"zhangsan,lisi"}Only allow Zhang San to submit work orders,{"allow_depts":"1 ,2"} only allows users with department ids 1 and 2 to submit work orders, {"allow_roles":"1,2"} only allows users with role ids 1 and 2 to submit work orders)'>
             <QuestionCircleOutlined />
        </Tooltip></span>}
              >
                <Input placeholder="Please set the display form field" />
              </Form.Item>
            </Col>
          </Row>
          <Row gutter={24}>
            <Col span={12} key="firstCol">
              <Form.Item
                name="display_form_str"
                label= {<span>show form<Tooltip title={"When the user only has viewing permission and is not the current handler, the field information displayed in the ticket details, in the format [\"gmt_created\",\"title\", \"creator\"],"}><QuestionCircleOutlined/></Tooltip></span>}
              >
                <Input placeholder="Please select the fields to display"/>
              </Form.Item>
            </Col>
            <Col span={12} key="secondCol">
              <Form.Item
                name="title_template"
                label= {<span>title template<Tooltip title="When the user does not pass the title field (and the title field) when creating a new work order, the title is automatically generated. Supports writing work order fields as parameters into templates, such as {creator}'s leave application, ({date_start}-{date_end})"><QuestionCircleOutlined /></Tooltip></span>}
              >
                <Input placeholder="Please set a title template" />
              </Form.Item>
            </Col>
          </Row>
          <Row gutter={24}>
            <Col span={12} key="firstCol">
              <Form.Item
                name="content_template"
                label= {<span>Notification Content Template<Tooltip title="Message content when used for ticket notification. Supports writing ticket fields as parameters into templates, such as: title:{title}, creation time:{gmt_created}"><QuestionCircleOutlined /></Tooltip></span>}
              >
                <TextArea
                  placeholder="Message content when used for ticket notification. Supports writing ticket fields as parameters into templates, such as: title:{title}, creation time:{gmt_created}"
                  autoSize={{ minRows: 2, maxRows: 6 }}
                />
              </Form.Item>
            </Col>
            <Col span={12} key="secondCol">
              <Form.Item
                name="view_permission_check"
                valuePropName= {this.state.workflowDetailResult&& this.state.workflowDetailResult.view_permission_check? "checked": "unchecked"}

                label= {<span>View permission check<Tooltip title="After it is turned on, people who are not related to the work order (creator, current handler, and handlers who used to handle it) do not have permission to view the details of the work order"><QuestionCircleOutlined /></Tooltip></span>}
              >
                <Switch checkedChildren="on" unCheckedChildren="off" />
              </Form.Item>
            </Col>
          </Row>
          <Row gutter={24}>
            <Col span={12} key="firstCol">
              <Form.Item
                name="workflow_admin"

                label= {<span>administrator<Tooltip title="If an administrator is set, you can modify the workflow and interfere with the corresponding work order status (mandatory modification status)"><QuestionCircleOutlined /></Tooltip></span>}
              >
                <Select
                  allowClear
                  showSearch
                  mode="multiple"
                  style={{ width: '100%' }}
                  placeholder="Please enter a keyword search and select Workflow Manager"
                  onSearch = {this.searchAdminer}
                >
                  {this.state.searchAdminerResult && this.state.searchAdminerResult.map(d => (
                    <Option key={d.username}>{`${d.alias}(${d.username})`}</Option>
                  ))}
                </Select>
              </Form.Item>
            </Col>
            <Col span={12} key="secondCol">
              <Form.Item
                name="intervener"
                label= {<span>intervening person<Tooltip title="Set as the intervention person, you can see all the work orders of this type in 'work order management' - 'work order intervention', and can intervene on these work orders (mandatory modification of the work order status)"><QuestionCircleOutlined /></Tooltip></span>}
              >
                <Select
                  allowClear
                  showSearch
                  mode="multiple"
                  style={{ width: '100%' }}
                  placeholder="Please enter keyword search and please select Workflow Manager"
                  onSearch = {this.searchIntervener}
                >
                  {this.state.searchIntervenerResult && this.state.searchIntervenerResult.map(d => (
                    <Option key={d.username}>{`${d.alias}(${d.username})`}</Option>
                  ))}
                </Select>
              </Form.Item>
            </Col>
          </Row>
          <Row gutter={24}>
            <Col span={12} key="firstCol">
              <Form.Item
                name="view_persons"
                label= {<span>查看权限人<Tooltip title="The person who is set as the viewing authority can see the list of all work orders of this type in 'Work Order Management' - 'Work Order View'"><QuestionCircleOutlined /></Tooltip></span>}
              >
                <Select
                  allowClear
                  showSearch
                  mode="multiple"
                  style={{ width: '100%' }}
                  placeholder="Please enter a keyword to search and please select a viewing authority"
                  onSearch = {this.searchViewer}
                >
                  {this.state.searchViewerResult && this.state.searchViewerResult.map(d => (
                    <Option key={d.username}>{`${d.alias}(${d.username})`}</Option>
                  ))}
                </Select>
              </Form.Item>
            </Col>
            <Col span={12} key="secondCol">
              <Form.Item
                name="view_depts"
                label= {<span>View permission department<Tooltip title="The subordinate owner of the department that is set to view the authority can see a list of all work orders of this type in 'Work Order Management' - 'Work Order View'"><QuestionCircleOutlined /></Tooltip></span>}
              >
                <Select
                  mode="multiple"
                  allowClear
                  showSearch
                  style={{ width: '100%' }}
                  placeholder="Please select a department to grant viewing access"
                >
                  {this.state.deptList.map(d => (
                    <Option key={d.id}>{`${d.name}(id:${d.id})`}</Option>
                  ))}
                </Select>

              </Form.Item>
            </Col>
          </Row>
          <Row gutter={24}>
            <Col span={12} key="firstCol">
              <Form.Item
                name="api_permission_apps"
                label= "API authorization application"
              >
                <Select
                  mode="multiple"
                  allowClear
                  showSearch
                  style={{ width: '100%' }}
                  placeholder="Please select an application that is allowed to call the interface"
                >
                  {this.state.appTokenList.map(d => (
                    <Option key={d.id}>{d.app_name}</Option>
                  ))}
                </Select>
              </Form.Item>
            </Col>
          </Row>
          <Form.Item {...tailLayout}>
            <Button type="primary" htmlType="submit">
              submit
            </Button>
          </Form.Item>
        </Form>
      </Card>
    )
  }

}

export default WorkflowBasicInfo;
