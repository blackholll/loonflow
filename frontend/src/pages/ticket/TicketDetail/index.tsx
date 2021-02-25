import {Form, Input, message, Col, Row, InputNumber, Radio, DatePicker, Checkbox, Select, Button, Upload, Collapse} from 'antd';
import React, { Component, Fragment } from 'react';
import {getWorkflowInitState} from "@/services/workflows";
import {queryUserSimple} from "@/services/user";
import {
  getDetailDetailRequest,
  newTicketRequest,
  getTicketTransitionRequest,
  handleTicketRequest
} from "@/services/ticket";
import {UploadOutlined} from "@ant-design/icons/lib";
import TicketLog from "@/pages/ticket/TicketLog";
import WorkflowGraph from "@/pages/workflow/workflowGraph";
import TicketStep from "@/pages/ticket/TicketStep";

const { Option } = Select;
const { TextArea } = Input;



export interface TicketDetailProps {
  ticketId?: number,
  workflowId?: number,

}

export interface TicketDetailState {
  // workflowInitResult: [],
  ticketDetailInfoData: [],
  ticketTransitionList: [],
  fieldTypeDict: {},
  fileList: {},
  nowTicketWorkflowId: 0, // 当前工单详情的workflowid
  userSelectDict: {}

}

class TicketDetail extends Component<TicketDetailProps, TicketDetailState> {
  constructor(props: Readonly<TicketDetailProps>) {
    super(props);
    this.state = {
      ticketTransitionList: [],
      ticketDetailInfoData: [],
      fileList: {},
      fieldTypeDict: {},
      userSelectDict: {}
    }
  }

  componentDidMount() {
    if (this.props.ticketId === 0) {
      // new ticket
      this.fetchWorkflowInitState();
    } else {
      // ticket detail
      this.fetchTicketDetailInfo();
      // get ticket transiton
      this.fetchTicketTransitionInfo();
    }

  }
  // shouldComponentUpdate(nextProps: Readonly<TicketDetailProps>, nextState: Readonly<TicketDetailState>, nextContext: any): boolean {
  //   this.fetchWorkflowInitState();
  // }

  userSimpleSearch = async(field_key, search_value) => {
    // 获取用户列表
    const result = await queryUserSimple({search_value:search_value});
    if (result.code ===0 ) {
      let userSelectDict = {}
      userSelectDict[field_key] = result.data.value
      this.setState({userSelectDict})
    }
  }

  fetchTicketTransitionInfo = async() => {
    //get
    const result = await getTicketTransitionRequest({ticket_id: this.props.ticketId});
    if (result.code === 0) {
      this.setState({
        ticketTransitionList: result.data.value
      })
    }
    else {
      message.error(`获取用户可以执行的操作失败:${result.msg}`)
    }
  }

  fetchTicketDetailInfo = async() => {
    const result = await getDetailDetailRequest({ticket_id: this.props.ticketId});
    if (result.code === 0 ){
      this.setState({
        ticketDetailInfoData: result.data.value.field_list,
        nowTicketWorkflowId: result.data.value.workflow_id
      })
    } else {
      message.error(result.msg)
    }
  }

  fileChange = (field_key:string, info: any) => {

    console.log(info)
    console.log(field_key)
    let fileList = [...info.fileList];
    if (info.file.status === 'done') {
      fileList = fileList.map(file=>{
        if (file.response.code === 0){
          file.url = file.response.data.file_path
          file.name = file.response.data.file_name
        }
        return file;
      })
    }
    // this.setState({ fileList });
    let newList = this.state.fileList;
    newList[field_key] = fileList
    this.setState({ fileList: newList });

  }


  fetchWorkflowInitState = async () => {
    const result = await getWorkflowInitState({workflowId: this.props.workflowId})
    if (result.code === 0) {
      let fieldTypeDict = {};
      result.data.field_list.map(field =>{
          fieldTypeDict[field.field_key] = field.field_type_id
      }
      )
      this.setState({
        ticketDetailInfoData: result.data.field_list,
        ticketTransitionList: result.data.transition,
        fieldTypeDict: fieldTypeDict
      });
    } else {
      message.error(result.msg);
    }
  }


  switchFormItem =  (item: any) => {
    let child = null;
    const formItemOptions = {rules: [], extra: item.description};
    const formItemChildOptions = {disabled: false, placeholder:item.placeholder};



    if (item.field_attribute === 1) {
      // todo: 下拉列表、布尔radio等显示的处理
      child = <div>{item.field_value}</div>
    }  else {
      if (item.field_attribute === 2) {
        formItemOptions.rules = [{ required: true, message: `Please input ${item.field_key}` }]
      }

      if (item.field_type_id === 5) {
        // 字符串
        child = <Input {...formItemChildOptions}/>

      } else if (item.field_type_id === 10){
        // 整形
        child = <InputNumber precision={0} {...formItemChildOptions}/>
      } else if (item.field_type_id === 15){
        // 浮点型
        child = <InputNumber {...formItemChildOptions} />
      } else if (item.field_type_id === 20){
        // 布尔
        const radioOption = []
        for (var key in item.boolean_field_display) {
          radioOption.push(<Radio key={key} value={key}>{item.boolean_field_display[key]}</Radio>)
        }
        child = <Radio.Group
          {...formItemChildOptions}>
          {radioOption}
        </Radio.Group>
      } else if (item.field_type_id == 25){
        // 日期类型
        child = <DatePicker {...formItemChildOptions} />
      } else if (item.field_type_id == 30){
        // 日期时间类型
        child = <DatePicker {...formItemChildOptions} showTime />
      } else if (item.field_type_id == 35){
        // 单选
        const radioOption = []
        for (var key in item.field_choice) {
          radioOption.push(<Radio key={key} value={key}>{item.field_choice[key]}</Radio>)
        }
        child = <Radio.Group
          {...formItemChildOptions}>
          {radioOption}
        </Radio.Group>
      } else if (item.field_type_id == 40){
        // 多选checkbox
        const checkboxOption = []
        for (var key in item.field_choice) {
          checkboxOption.push(
            <Checkbox key={key} value={key}>{item.field_choice[key]}</Checkbox>
          )
        }
        child = <Checkbox.Group style={{ width: '100%' }}>{checkboxOption}</Checkbox.Group>
      } else if (item.field_type_id == 45){
        // 下拉列表
        const selectOption = []
        for (var key in item.field_choice) {
          selectOption.push(
            <Option key={key} value={key}>{item.field_choice[key]}</Option>
          )
        }
        child = <Select showSearch filterOption={(input, option) =>
          option.children.toLowerCase().indexOf(input.toLowerCase()) >= 0
        } {...formItemChildOptions}>
          {selectOption}
        </Select>

      } else if (item.field_type_id == 50){
        // 下拉列表
        const selectOption = []
        for (var key in item.field_choice) {
          selectOption.push(
            <Option key={key} value={key}>{item.field_choice[key]}</Option>
          )
        }
        child = <Select showSearch mode="multiple" filterOption={(input, option) =>
          option.children.toLowerCase().indexOf(input.toLowerCase()) >= 0
        } {...formItemChildOptions}>
          {selectOption}
        </Select>

      } else if (item.field_type_id === 55){
        // 文本
        child = <TextArea autoSize={{ minRows: 2, maxRows: 6 }} {...formItemChildOptions}/>
      } else if (item.field_type_id === 58){
        // 富文本，先以文本域代替，后续再支持
        child = <TextArea autoSize={{ minRows: 2, maxRows: 6 }} {...formItemChildOptions}/>
      }
      else if (item.field_type_id === 80){
        // 附件
        child = <Upload action="api/v1.0/tickets/upload_file" listType="text" onChange={(info)=>this.fileChange(item.field_key, info)} fileList={this.state.fileList[item.field_key]}>
          <Button icon={<UploadOutlined />}>Click to upload</Button>
        </Upload>
      }

      else if (item.field_type_id === 60){
        // 用户
        child = <Select
          showSearch onSearch = {(search_value)=>this.userSimpleSearch(item.field_key, search_value)} filterOption={(input, option) =>
          option.children.toLowerCase().indexOf(input.toLowerCase()) >= 0
        } {...formItemChildOptions}>
          {this.state.userSelectDict[item.field_key] && this.state.userSelectDict[item.field_key].map(d => (
            <Option key={d.username} value={d.username}>{`${d.alias}(${d.username})`}</Option>
          ))}

        </Select>
      }


      else if (item.field_type_id === 70){
        // 多选用户
        child = <Select
          showSearch onSearch = {(search_value)=>this.userSimpleSearch(item.field_key, search_value)} filterOption={(input, option) =>
          option.children.toLowerCase().indexOf(input.toLowerCase()) >= 0
        } {...formItemChildOptions}
         >
          {this.state.userSelectDict[item.field_key] && this.state.userSelectDict[item.field_key].map(d => (
            <Option key={d.username} value={d.username}>{`${d.alias}(${d.username})`}</Option>
          ))}

        </Select>
      }


      else {
        child = <Input {...formItemChildOptions} />
      }
    }



    return (
      <Col span={12}>
        <Form.Item
          name={item.field_key}
          label={item.field_name}
          // initialValue:
          {...formItemOptions}
        >
          {child}
        </Form.Item>
      </Col>
    )
  }

  formRef = React.createRef<FormInstance>();

  handleTicket = async (transitionId: number) => {
    const values = this.formRef.current.getFieldsValue()
    for (let key in values){
      if ( [40,50].indexOf(this.state.fieldTypeDict[key]) !== -1){
        // 多选框，多选下拉
        values[key] = values[key].join(',')
      }

      if (this.state.fieldTypeDict[key] === 80 ) {
        // 文件   fieldList.url
        let urlList = [];
        values[key].fileList.map(attachment => {
          urlList.push(attachment.url)

        })
        values[key] = urlList.join(',')
      }
      if (this.state.fieldTypeDict[key] === 20 ) {
        // 日期
        values[key] = Number(values[key])
      }

      if (this.state.fieldTypeDict[key] === 25 ) {
        // 日期
        values[key] = values[key].format('YYYY-MM-DD')
      }
      if (this.state.fieldTypeDict[key] === 30 ) {
        // 时间
        values[key] = values[key].format('YYYY-MM-DD HH:mm:ss')
      }
    }

    values.transition_id = transitionId;
    if (this.props.ticketId) {
      // 处理工单
      const result = await handleTicketRequest(this.props.ticketId, values)
      if (result.code === 0) {
        message.success('处理工单成功');
        // #tode 刷新页面，关闭弹窗
        this.props.handleTicketOk();

      } else {
        message.error(result.msg);
      }

    } else {
      // 新建工单
      values.workflow_id = Number(this.props.workflowId);
      const result = await newTicketRequest(values)
      if (result.code === 0) {
        message.success('创建工单成功');
        this.props.newTicketOk(result.data.ticket_id)
        // #tode 刷新页面,关闭弹窗
      } else {
        message.error(result.msg);
      }
    }

  }



  genHandleButtonItem = (item: any) => {
    const buttonItems = []
    let buttonType = 'primary'
    let buttonAttribute = null
    let buttonItem = null

    item.map(result => {

      if (result.attribute_type_id === 1) {
        buttonItem = <Button
          type='primary'
          htmlType="submit"
          value = {result.transition_id}
          onClick={()=>this.handleTicket(result.transition_id)}
        >
          {result.transition_name}
        </Button>
      }
      else if (result.attribute_type_id === 2) {
        buttonItem = <Button
          htmlType="submit"
          type='primary'
          danger
          value = {result.transition_id}
          onClick={()=>this.handleTicket(result.transition_id)}
        >
          {result.transition_name}
        </Button>
      } else if (result.attribute_type_id === 3) {
        // 其他类型
        buttonItem = <Button
          value = {result.transition_id}
          htmlType="submit"
          onClick={()=>this.handleTicket(result.transition_id)}
        >
          {result.transition_name}
        </Button>
      }
      buttonItems.push(buttonItem);

    })
    return buttonItems;
  }



  render() {
    const form_items = [];
    if (this.state.ticketDetailInfoData !== []){
      this.state.ticketDetailInfoData.map(result => {
        form_items.push(this.switchFormItem(result))
      })
    }
    const handleButtonItems = this.genHandleButtonItem(this.state.ticketTransitionList);

    const formItemLayout = {
      labelCol: {
        xs: { span: 24 },
        sm: { span: 8 },
      },
      wrapperCol: {
        xs: { span: 24 },
        sm: { span: 16 },
      },
    };



    return (
      // <Fragment>
        <Collapse defaultActiveKey={['flowStep', 'ticketDetail']} bordered={false}>
          {this.props.ticketId?
            <Collapse.Panel header="流程图" key="flowchart">
              <WorkflowGraph workflowId={this.state.nowTicketWorkflowId}/>
            </Collapse.Panel>: null
          }

          {this.props.ticketId?
          <Collapse.Panel header="操作记录" key="flowLog">
            <TicketLog ticketId={this.props.ticketId}/>
          </Collapse.Panel> : null}

          {this.props.ticketId?
          <Collapse.Panel header="工单进度" key="flowStep">
            <TicketStep ticketId={this.props.ticketId}/>
          </Collapse.Panel> : null }

          <Collapse.Panel header="工单信息" key="ticketDetail">
            <Form
              {...formItemLayout}
              name="ticketDetailForm"
              ref={this.formRef}
              className="ant-advanced-search-form"
            >
              <Row gutter={24}>
                {form_items}
              </Row>
              {handleButtonItems}
            </Form>
          </Collapse.Panel>
        </Collapse>

      // </Fragment>
    )
  }
}

export default TicketDetail;
