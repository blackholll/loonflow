import {Form, Input, message, Col, Row, InputNumber, Radio, DatePicker, Checkbox, Select, Button} from 'antd';
import React, { Component, Fragment } from 'react';
import {getWorkflowInitState} from "@/services/workflows";
import {queryUserSimple} from "@/services/user";
import {getDetailDetailRequest, newTicketRequest, getTicketTransitionRequest} from "@/services/ticket";

const { Option } = Select;
const { TextArea } = Input;



export interface TicketDetailProps {
  ticketId?: number,
  workflowId?: number,

}

export interface TicketDetailState {
  // workflowInitResult: [],
  ticketDetailInfoData: [],
  ticketTransitionList: []
}

class TicketDetail extends Component<TicketDetailProps, TicketDetailState> {
  constructor(props: Readonly<TicketDetailProps>) {
    super(props);
    this.state = {
      // workflowInitResultFieldList: [],
      // workflowInitResultTransitionList: [],
      ticketTransitionList: [],
      ticketDetailInfoData: []
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
      })
    } else {
      message.error(result.msg)
    }
  }




  fetchWorkflowInitState = async () => {
    const result = await getWorkflowInitState({workflowId: this.props.workflowId})
    if (result.code === 0) {
      this.setState({
        ticketDetailInfoData: result.data.field_list,
        ticketTransitionList: result.data.transition
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
        child = <Input {...formItemChildOptions} defaultValue={item.field_value}/>

      } else if (item.field_type_id === 10){
        // 整形
        child = <InputNumber precision={0} {...formItemChildOptions} defaultValue={item.field_value} />
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
        child = <DatePicker {...formItemChildOptions} defaultValue={item.field_value}/>
      } else if (item.field_type_id == 30){
        // 日期时间类型
        child = <DatePicker {...formItemChildOptions} showTime defaultValue={item.field_value}/>
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
        child = <TextArea autoSize={{ minRows: 2, maxRows: 6 }} {...formItemChildOptions} defaultValue={item.field_value}/>
      }
      // 用户、多选用户、附件暂时不支持
      else {
        child = <Input {...formItemChildOptions} defaultValue={item.field_value}/>
      }
    }



    return (
      <Col span={12}>
        <Form.Item
          name={item.field_key}
          label={item.field_name}
          {...formItemOptions}
        >
          {child}
        </Form.Item>
      </Col>
    )
  }

  formRef = React.createRef<FormInstance>();

  handleNewTicket = async (transitionId: number) => {
    const values = this.formRef.current.getFieldsValue()
    this.state.ticketDetailInfoData.map(fieldObj => {
      // todo: 支持70（多选用户）后需要吧70也加上
      if ([40,50].indexOf(fieldObj.field_type_id)!== -1){
        if (values[fieldObj.field_key]){
          values[fieldObj.field_key] = values[fieldObj.field_key].join(',')
        }
      }
      if (fieldObj.field_type_id === 25) {
        values[fieldObj.field_key] = values[fieldObj.field_key].format('YYYY-MM-DD')
      }
        if (fieldObj.field_type_id === 30) {
          values[fieldObj.field_key] = values[fieldObj.field_key].format('YYYY-MM-DD HH:mm:ss')
        }
    }
    )


    values.transition_id = transitionId;
    values.workflow_id = Number(this.props.workflowId);
    const result = await newTicketRequest(values)
    if (result.code === 0) {
      message.success('创建工单成功');
    } else {
      message.error(result.msg);
    }


    console.log(`创建工单,transition_id:${transitionId}`);


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
          onClick={()=>this.handleNewTicket(result.transition_id)}
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
          onClick={()=>this.handleNewTicket(result.transition_id)}
        >
          {result.transition_name}
        </Button>
      } else if (result.attribute_type_id === 3) {
        // 其他类型
        buttonItem = <Button
          value = {result.transition_id}
          htmlType="submit"
          onClick={()=>this.handleNewTicket(result.transition_id)}
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
      <Fragment>
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

      </Fragment>
    )
  }
}

export default TicketDetail;
