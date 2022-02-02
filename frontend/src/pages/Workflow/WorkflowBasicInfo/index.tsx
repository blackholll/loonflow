import {Form, Input, Button, Checkbox, Row, Col, Tooltip, Select, Switch, message} from 'antd';
import React, {useState, userEffect, useEffect} from 'react';
import {QuestionCircleOutlined} from "@ant-design/icons/lib";
import {addWorkflow, getWorkflowDetail, updateWorkflowDetail, updateWorkflowState} from "@/services/workflows";
import {getSimpleNoticeListRequest} from "@/services/manage";
import {getSimpleDeptList, getSimpleTokenListRequest, queryUserSimple} from "@/services/user";


const { Option } = Select;
const { TextArea } = Input;

const layout = {
  labelCol: { span: 8 },
  wrapperCol: { span: 16 },
};
const tailLayout = {
  wrapperCol: { offset: 8, span: 16 },
};

const WorkflowBasicInfo = (props) => {

  const [form] = Form.useForm();

  const onFinish = (values: any) => {
    console.log('Success:', values);
  };

  const onFinishFailed = (errorInfo: any) => {
    console.log('Failed:', errorInfo);
  };

  const [workflowBasicInfo, setWorkflowInfo] = useState({})
  const [noticeList, setNoticeList] = useState([])
  const [appTokenList, setAppTokenList] = useState([])
  const [deptList, setDeptList] = useState([])
  const [searchAdminerResult, setSearchAdminerResult] = useState([])
  const [searchIntervenerResult, setSearchIntervenerResult] = useState([])
  const [searchViewerResult, setSearchViewerResult] = useState([])

  useEffect( () => {
    console.log('newnewew');
    // 获取通知列表
    // 获取 授权应用
    fetchNoticeList();
    fetchAppTokenList();
    fetchDeptList();
    if (props.workflowId){
      fetchWorkflowDetail();
    }
    else{
      console.log('new workflowid')
    }


  }, [])

  const fetchWorkflowDetail = async() => {
    const result = await getWorkflowDetail(props.workflowId);
    if (result.code !==0) {
      message.error(`获取工作流基础信息失败: ${result.msg}`);
    } else {
      setWorkflowInfo(result.data);

      const infoResult = result.data;
      if (infoResult.notices){
        infoResult['notices'] = infoResult.notices.split(',');
      } else {
        infoResult['notices'] = []
      }
      form.setFieldsValue(infoResult)
    }
  }

  const fetchNoticeList = async() => {
    const result = await getSimpleNoticeListRequest({per_page:1000, page:1});
    if (result.code === 0) {
      setNoticeList(result.data.value);
    }
  }

  const fetchAppTokenList = async() => {
    const result = await getSimpleTokenListRequest({per_page: 10000, page:1});
    if (result.code ===0 ) {
      setAppTokenList( result.data.value)
    }
  }

  const fetchDeptList = async()=>{
    const result = await getSimpleDeptList({per_page: 10000, page:1});
    if (result.code ===0 ) {
      setDeptList(result.data.value)
    }
  }

  const searchAdminer = async(search_value: string) => {
    const result = await queryUserSimple({search_value:search_value});
    if (result.code ===0 ) {
      setSearchAdminerResult(result.data.value);
    }
  }


  const searchIntervener = async(search_value: string) => {
    const result = await queryUserSimple({search_value:search_value});
    if (result.code ===0 ) {
      setSearchIntervenerResult(result.data.value);
    }
  }


  const searchViewer = async(search_value: string) => {
    const result = await queryUserSimple({search_value:search_value});
    if (result.code ===0 ) {
      setSearchViewerResult( result.data.value);
    }
  }

  const onWorkflowFinish = async(values: any) => {
    console.log(values);
    for (let key in values) {
      if (Array.isArray(values[key])) {
        values[key] = values[key].join(',')
      }
      if (values[key] === undefined) {
        values[key] = ''
      }
    }
    if (values.view_permission_check) {
      values.view_permission_check = 1
    } else {
      values.view_permission_check = 0
    }


    if (props.workflowId){
      const result = await updateWorkflowDetail(props.workflowId, values);
      if (result.code ===0){
        message.success('更新成功')
      } else {
        message.error(result.msg)
      }
    }
    else {
      // 新增
      const result = await addWorkflow(values);
      if (result.code ===0){
        message.success('新增成功')
        window.location.href = `/workflows/detail?workflow_id=${result.data.workflow_id}`

      } else {
        message.error(result.msg)
      }
    }

  }



  return (
    <Form
      name="workflowDetailForm"
      form={form}
      className="ant-advanced-search-form"
      {...layout}
      onFinish={onWorkflowFinish}
    >
      <Row gutter={24}>
        <Col span={12} key="firstCol">
          <Form.Item
            name="name"
            label= "名称"
            rules={[
              {
                required: true,
                message: '请输入工作流名称',
              },
            ]}
          >
            <Input placeholder="请输入工作流名称"/>
          </Form.Item>
        </Col>
        <Col span={12} key="secondCol">
          <Form.Item
            name="description"
            label= {<span>描述<Tooltip title={"描述信息将出现在新建工单页面"}><QuestionCircleOutlined/></Tooltip></span>}
          >
            <Input placeholder="描述信息将显示在新建工单页面" />
          </Form.Item>
        </Col>
      </Row>
      <Row gutter={24}>
        <Col span={12} key="firstCol">
          <Form.Item
            name="notices"
            label= "选择通知"
          >
            <Select
              allowClear
              showSearch
              mode= "multiple"
              style={{ width: '100%' }}
              placeholder="请选择通知方式"
            >
              {noticeList.map(d => (
                <Option key={d.id}>{d.name}</Option>
              ))}
            </Select>
          </Form.Item>
        </Col>
        <Col span={12} key="secondCol">
          <Form.Item
            name="limit_expression"
            label= {<span>限制表达式<Tooltip title='默认"{}"，限制周期({"period":24} 24小时), 限制次数({"count":1}在限制周期内只允许提交1次), 限制级别({"level":1} 针对(1单个用户 2全局)限制周期限制次数,默认特定用户);允许特定人员提交({"allow_persons":"zhangsan,lisi"}只允许张三提交工单,{"allow_depts":"1,2"}只允许部门id为1和2的用户提交工单，{"allow_roles":"1,2"}只允许角色id为1和2的用户提交工单)'>
             <QuestionCircleOutlined />
        </Tooltip></span>}
          >
            <Input placeholder="请设置展现表单字段" />
          </Form.Item>
        </Col>
      </Row>
      <Row gutter={24}>
        <Col span={12} key="firstCol">
          <Form.Item
            name="display_form_str"
            label= {<span>展现表单<Tooltip title={"当用户只有查看权限，非当前处理人时，工单详情展示的字段信息，格式[\"gmt_created\",\"title\", \"creator\"],"}><QuestionCircleOutlined/></Tooltip></span>}
          >
            <Input placeholder="请填写需要展示的字段"/>
          </Form.Item>
        </Col>
        <Col span={12} key="secondCol">
          <Form.Item
            name="title_template"
            label= {<span>标题模板<Tooltip title="用户新建工单时未传标题字段(及title字段)时，自动生生成标题。支持将工单字段作为参数写到模板中，如{creator}的请假申请，({date_start}-{date_end})"><QuestionCircleOutlined /></Tooltip></span>}
          >
            <Input placeholder="请设置标题模板" />
          </Form.Item>
        </Col>
      </Row>
      <Row gutter={24}>
        <Col span={12} key="firstCol">
          <Form.Item
            name="content_template"
            label= {<span>通知内容模板<Tooltip title="用于工单消息通知时，消息内容。支持将工单字段作为参数写到模板中，如: 标题:{title}, 创建时间:{gmt_created}"><QuestionCircleOutlined /></Tooltip></span>}
          >
            <TextArea
              placeholder="用于工单消息通知时，消息内容。支持将工单字段作为参数写到模板中，如: 标题:{title}, 创建时间:{gmt_created}"
              autoSize={{ minRows: 2, maxRows: 6 }}
            />
          </Form.Item>
        </Col>
        <Col span={12} key="secondCol">
          <Form.Item
            name="view_permission_check"
            valuePropName= {workflowBasicInfo && workflowBasicInfo.view_permission_check? "checked": "unchecked"}

            label= {<span>查看权限校验<Tooltip title="开启后，非对应工单关系人(创建人、当前处理人、曾经需要其处理的处理人)无查看工单详情的权限"><QuestionCircleOutlined /></Tooltip></span>}
          >
            <Switch checkedChildren="开启" unCheckedChildren="关闭" />
          </Form.Item>
        </Col>
      </Row>
      <Row gutter={24}>
        <Col span={12} key="firstCol">
          <Form.Item
            name="workflow_admin"

            label= {<span>管理员<Tooltip title="被设置管理员，则可以修改工作流，干预对应的工单状态(强制修改状态)"><QuestionCircleOutlined /></Tooltip></span>}
          >
            <Select
              allowClear
              showSearch
              mode="multiple"
              style={{ width: '100%' }}
              placeholder="请输入关键词搜索并选择工作流管理员"
              onSearch = {searchAdminer}
              filterOption={(input, option) =>
                option.children.toLowerCase().indexOf(input.toLowerCase()) >= 0
                || option.value.toLowerCase().indexOf(input.toLowerCase()) >= 0
              }
            >
              {searchAdminerResult && searchAdminerResult.map(d => (
                <Option key={d.username} value={d.username}>{`${d.alias}(${d.username})`}</Option>
              ))}
            </Select>
          </Form.Item>
        </Col>
        <Col span={12} key="secondCol">
          <Form.Item
            name="intervener"
            label= {<span>干预人<Tooltip title="被设置为干预人，可以在'工单管理'-'工单干预'中看到该类型所有工单，并可以对这些工单干预操作(强制修改工单状态)"><QuestionCircleOutlined /></Tooltip></span>}
          >
            <Select
              allowClear
              showSearch
              mode="multiple"
              style={{ width: '100%' }}
              placeholder="请输入关键词搜索并请选择工作流管理员"
              onSearch = {searchIntervener}
              filterOption={(input, option) =>
                option.children.toLowerCase().indexOf(input.toLowerCase()) >= 0
                || option.value.toLowerCase().indexOf(input.toLowerCase()) >= 0
              }
            >
              {searchIntervenerResult && searchIntervenerResult.map(d => (
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
            label= {<span>查看权限人<Tooltip title="被设置为查看权限人，可以在'工单管理'-'工单查看'中看到该类型的所有工单列表"><QuestionCircleOutlined /></Tooltip></span>}
          >
            <Select
              allowClear
              showSearch
              mode="multiple"
              style={{ width: '100%' }}
              placeholder="请输入关键词搜索并请选择查看权限人"
              onSearch = {searchViewer}
              filterOption={(input, option) =>
                option.children.toLowerCase().indexOf(input.toLowerCase()) >= 0
                || option.value.toLowerCase().indexOf(input.toLowerCase()) >= 0
              }
            >
              {searchViewerResult && searchViewerResult.map(d => (
                <Option value={d.username}>{`${d.alias}(${d.username})`}</Option>
              ))}
            </Select>
          </Form.Item>
        </Col>
        <Col span={12} key="secondCol">
          <Form.Item
            name="view_depts"
            label= {<span>查看权限部门<Tooltip title="被设置为查看权限部门的下属所有人，可以在'工单管理'-'工单查看'中看到该类型的所有工单列表"><QuestionCircleOutlined /></Tooltip></span>}
          >
            <Select
              mode="multiple"
              allowClear
              showSearch
              style={{ width: '100%' }}
              placeholder="请选择授予查看权限的部门"
            >
              {deptList.map(d => (
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
            label= "API授权应用"
          >
            <Select
              mode="multiple"
              allowClear
              showSearch
              style={{ width: '100%' }}
              placeholder="请选择允许调用接口的应用"
              filterOption={(input, option) =>
                option.children.toLowerCase().indexOf(input.toLowerCase()) >= 0
              }
            >
              {appTokenList.map(d => (
                <Option key={d.app_name}>{d.app_name}</Option>
              ))}
            </Select>
          </Form.Item>
        </Col>
      </Row>
      <Form.Item {...tailLayout}>
        <Button type="primary" htmlType="submit">
          确定
        </Button>
      </Form.Item>
    </Form>
  );
};


export default WorkflowBasicInfo;
