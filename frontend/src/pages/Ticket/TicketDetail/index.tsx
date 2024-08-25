import {
  Form,
  Input,
  message,
  Col,
  Row,
  InputNumber,
  Radio,
  DatePicker,
  Checkbox,
  Select,
  Button,
  Upload,
  Collapse,
  Card, Divider,
  Popconfirm, Modal
} from 'antd';

import BraftEditor from 'braft-editor';
import "braft-editor/dist/index.css";

import React, { Component, Fragment } from 'react';
import moment from 'moment';
import {canInterveneRequest, getWorkflowInitState, getWorkflowSimpleState} from "@/services/workflows";
import {queryUserSimple} from "@/services/user";
import {
  getDetailDetailRequest,
  newTicketRequest,
  getTicketTransitionRequest,
  handleTicketRequest,
  closeTicketRequest,
  changeTicketStateRequest,
  deliverTicketRequest,
  acceptTicketRequest,
  addNodeEndTicketRequest,
  addNodeTicketRequest, addCommentRequest, retreatRequest
} from "@/services/ticket";
import {UploadOutlined} from "@ant-design/icons/lib";
import TicketLog from "@/pages/Ticket/TicketLog";
import WorkflowGraph from "@/pages/Workflow/WorkflowGraph";
import TicketStep from "@/pages/Ticket/TicketStep";
import {decodeJwt, getCookie} from "@/utils/utils";
import TicketList from "@/pages/Ticket/TicketList";

const { Option } = Select;
const { TextArea } = Input;



export interface TicketDetailProps {
  ticketId?: number,
  workflowId?: number,

}

export interface TicketDetailState {
  ticketDetailInfoData: [],
  ticketTransitionList: [],
  ticketInfo: {},
  isRetreatModalVisible:false,
  fieldTypeDict: {},
  currentStateId: 0,
  fileList: {},
  enable_retreat: false,
  nowTicketWorkflowId: 0, // 当前工单详情的workflowid
  canIntervene: false, // 是否可以干预工单
  simpleStateList: [],
  isChangeStateModalVisible: false,
  isDeliverModalVisible: false,
  isCloseModalVisible: false,
  isAddNodeModalVisible: false,
  newStateId:0,
  deliverFromAdmin: false,
  isCommentModalVisible: false,
  userSelectDict: {}

}




const myUploadFn =(param) =>{
  const serverURL = 'api/v1.0/tickets/upload_file';
  const xhr = new XMLHttpRequest
  const fd = new FormData()

  const successFn = (response) => {
    // 假设服务端直接返回文件上传后的地址
    // 上传成功后调用param.success并传入上传后的文件地址
    param.success({
      url: JSON.parse(xhr.responseText).data.file_path,
      meta: {
        id: JSON.parse(xhr.responseText).data.file_name,
        title: JSON.parse(xhr.responseText).data.file_name,
        alt: JSON.parse(xhr.responseText).data.file_name,
        loop: true, // 指定音视频是否循环播放
        autoPlay: true, // 指定音视频是否自动播放
        controls: true, // 指定音视频是否显示控制栏
      }
    })
  }

  const progressFn = (event) => {
    // 上传进度发生变化时调用param.progress
    param.progress(event.loaded / event.total * 100)
  }

  const errorFn = (response) => {
    // 上传发生错误时调用param.error
    param.error({
      msg: 'unable to upload.'
    })
  }

  xhr.upload.addEventListener("progress", progressFn, false)
  xhr.addEventListener("load", successFn, false)
  xhr.addEventListener("error", errorFn, false)
  xhr.addEventListener("abort", errorFn, false)

  fd.append('file', param.file)
  xhr.open('POST', serverURL, true)
  xhr.send(fd)

}

class TicketDetail extends Component<TicketDetailProps, TicketDetailState> {
  constructor(props: Readonly<TicketDetailProps>) {
    super(props);
    this.state = {
      ticketDetailInfoData: [],
      ticketTransitionList: [],
      fieldTypeDict: {},
      fileList: {},
      isRetreatModalVisible: false,
      isCloseModalVisible: false,
      enable_retreat: false,
      currentStateId: 0,
      nowTicketWorkflowId: 0, // 当前工单详情的workflowid
      canIntervene: false, // 是否可以干预工单
      simpleStateList: [],
      isChangeStateModalVisible: false,
      isDeliverModalVisible: false,
      isAddNodeModalVisible: false,
      newStateId:0,
      deliverFromAdmin: false,
      isCommentModalVisible: false,
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
      // get ticket transition
      this.fetchTicketTransitionInfo();
    }

  }

  userSimpleSearch = async(field_key, search_value) => {
    // 获取用户列表
    const result = await queryUserSimple({search_value:search_value});
    if (result.code ===0 ) {
      let userSelectDict = {}
      userSelectDict[field_key] = result.data.value
      this.setState({userSelectDict})
    }
  }

  fetchCanIntervene = async(workflowId: number) => {
    const result = await canInterveneRequest(workflowId);
    if (result.code === 0) {
      this.setState({
        canIntervene: result.data.can_intervene
      })
    }
  }

  fetchWorkflowSimpleState = async(workflowId: number) => {
    console.log('get simple state');
    const result = await getWorkflowSimpleState(workflowId, {per_page:1000});
    if (result.code === 0) {
      this.setState({
        simpleStateList: result.data.value
      })
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
      this.fetchCanIntervene(result.data.value.workflow_id);
      this.fetchWorkflowSimpleState(result.data.value.workflow_id);
      this.setState({
        ticketInfo: result.data,
        enable_retreat: result.data.value.state_info.enable_retreat,
        ticketDetailInfoData: result.data.value.field_list,
        currentStateId: result.data.value.state_id,
        nowTicketWorkflowId: result.data.value.workflow_id
      })

      let formInitValues = {};
      let fieldTypeDict = {}
      if (result.data.value.field_list !== []){
        result.data.value.field_list.map(result => {
          fieldTypeDict[result.field_key] = result.field_type_id
          if (result.field_type_id === 30 && result.field_value !== null){
            formInitValues[result.field_key] = moment(result.field_value);
          } else if (result.field_type_id === 25 && result.field_value !== null){
            formInitValues[result.field_key] = moment(result.field_value);
          }
          else if ([40, 50, 70].indexOf(result.field_type_id) >= 0) {
            formInitValues[result.field_key] = result.field_value? result.field_value.split(','): []
            console.log(formInitValues);
          }

          else if (result.field_type_id === 80){
            // 附件
            let newList = this.state.fileList;
            let fileList1 = [];
            if(result.field_value && result.field_value.startsWith('[')) {
              //为了兼容旧格式，所以这么写
              const urlInfo = JSON.parse(result.field_value)
              urlInfo.forEach((elem, index) => {
                fileList1.push(
                  {
                    url: elem.url,
                    name: elem.file_name,
                    uid: elem.url,
                    linkProps: `{"download": "${elem.file_name}"}`
                  }
                )
              })
            }
            else{
              let fileList0 = result.field_value? result.field_value.split(): [];
              fileList0.forEach((file0)=>{
                fileList1.push(
                  {
                    url: file0,
                    name: file0.split('/').slice(-1)[0],
                    uid: file0,
                  }
                )

              })
            }

            // newList[result.field_key] = result.field_value.split();
            newList[result.field_key] = fileList1
            console.log('newList')
            console.log(newList)
            // this.setState({ fileList: newList });
            formInitValues[result.field_key] = {fileList: fileList1};

          }
          else{
            formInitValues[result.field_key] = result.field_value;
          }
        })
      }
      this.setState({fieldTypeDict});

      this.formRef.current.setFieldsValue(formInitValues);
    } else {
      message.error(result.msg)
    }
  }

  onCloseTicketFinish = async (values) => {
    const result = await closeTicketRequest(this.props.ticketId, values);
    if (result.code === 0) {
      message.success('关闭工单成功');
      this.setState({isCloseModalVisible: false});
      this.props.handleTicketOk();
      // this.fetchTicketDetailInfo();
      // this.fetchTicketTransitionInfo();
    } else {
      message.error(`关闭工单失败:${result.msg}`)
    }

  }

  showChangeStateModal = () => {
    this.setState({isChangeStateModalVisible: true})
  }

  showAdminDeliverModal = () => {
    this.setState({isDeliverModalVisible: true, deliverFromAdmin: true})
  }

  showDeliverModal = () => {
    this.setState({isDeliverModalVisible: true, deliverFromAdmin: false})
  }

  showAddNodeModal = () => {
    this.setState({isAddNodeModalVisible: true})

  }
  showCloseModal = () => {
    this.setState({isCloseModalVisible: true})
  }
  showRetreatModal = () => {
    this.setState({isRetreatModalVisible: true})
  }


  showCommentModal = () => {
    this.setState({isCommentModalVisible: true})
  }

  closeModal = () => {
    this.setState({
        isChangeStateModalVisible: false,
        isDeliverModalVisible: false,
        isAddNodeModalVisible: false,
        isCommentModalVisible: false,
        isCloseModalVisible: false,
        isRetreatModalVisible: false,
      }
    )
  }

  onStateChange = (value: String) => {
    this.setState({newStateId : Number(value)})
  }

  onChangeStateFinish = async(values) => {
    const result = await changeTicketStateRequest(this.props.ticketId, values)
    if (result.code === 0 ) {
      message.success('修改状态成功');
      this.setState({isChangeStateModalVisible: false});
      this.fetchTicketDetailInfo();
      this.fetchTicketTransitionInfo();
    }
    else {
      message.error(`修改状态失败:${result.msg}`)
    }

  }

  onDeliverFinish = async(values) => {
    if (this.state.deliverFromAdmin){
      values.from_admin=1;
    }
    const result = await deliverTicketRequest(this.props.ticketId, values);
    if(result.code === 0) {
      message.success('转交成功');
      this.setState({isDeliverModalVisible: false});
      this.fetchTicketDetailInfo();
      this.fetchTicketTransitionInfo();
    }
    else {
      message.error(`转交失败:${result.msg}`)
    }
  }

  onAddNodeFinish = async(values:any) => {
    if (this.state.deliverFromAdmin){
      values.from_admin=1;
    }
    const result = await addNodeTicketRequest(this.props.ticketId, values);
    if(result.code === 0) {
      message.success('加签成功');
      this.setState({isAddNodeModalVisible: false});
      this.fetchTicketDetailInfo();
      this.fetchTicketTransitionInfo();
    }
    else {
      message.error(`加签失败:${result.msg}`)
    }
  }

  onCommentFinish = async(values:any) => {
    const result =  await addCommentRequest(this.props.ticketId, values);
    if(result.code === 0) {
      message.success('留言成功');
      this.setState({isCommentModalVisible: false});
    }
    else {
      message.error(`留言失败:${result.msg}`)
    }
  }

  onRetreatFinish = async(values:any) => {
    const result =  await retreatRequest(this.props.ticketId, values);
    if(result.code === 0) {
      message.success('撤回成功');
      this.setState({isRetreatModalVisible: false});
      this.props.handleTicketOk();
    }
    else {
      message.error(`撤回失败:${result.msg}`)
    }
  }


  fileChange = (field_key:string, info: any) => {

    console.log(info)
    console.log(field_key)
    let fileList = [...info.fileList];
    if (info.file.status === 'done') {
      fileList = fileList.map(file=>{
        if (file.response && file.response.code === 0){
          file.url = file.response.data.file_path
          file.name = file.response.data.source_file_name
          file.linkProps= `{"download": "${file.response.data.source_file_name}"}`
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
      if (item.field_type_id === 20) {
        // 布尔
        let display_result = item.boolean_field_display[item.field_value]
        child = <div>{display_result}</div>
      }

      else if (item.field_type_id === 35) {
        // 单选框
        let display_result = item.field_choice[item.field_value]
        child = <div>{display_result}</div>
      }else if (item.field_type_id === 40) {
        //多选框
        let result_list = item.field_value?item.field_value.split(','):[]
        let result_display_list = []
        result_list.forEach((result0)=>{
          console.log(result0)
          if(item.field_choice[result0]){
            result_display_list.push(item.field_choice[result0])
          }
        })

        let display_result = result_display_list.join()
        child = <div>{display_result}</div>
      } else if (item.field_type_id === 45) {
        //下拉列表
        let display_result = item.field_choice[item.field_value]
        child = <div>{display_result}</div>
      } else if (item.field_type_id === 50) {
        //多选下拉列表
        let result_list = item.field_value?item.field_value.split(','):[]
        let result_display_list = []
        result_list.forEach((result0)=>{
          console.log(result0)
          if(item.field_choice[result0]){
            result_display_list.push(item.field_choice[result0])
          }
        })

        let display_result = result_display_list.join()
        child = <div>{display_result}</div>
      }else if (item.field_type_id === 60) {
        //用户名
        child = <div>{item.field_value}</div>
      }else if (item.field_type_id === 70) {
        //多选用户
        child = <div>{item.field_value}</div>
      }
      else if (item.field_type_id === 58) {
        //富文本
        child = <div dangerouslySetInnerHTML={{__html: item.field_value }}/>
      }


      else if (item.field_type_id === 80){

        if (!item.field_value){
          child = <div></div>
        } else {
          child = []
        if(item.field_value.startsWith('[')){
          //为了兼容旧格式，所以这么写
          const urlInfo = JSON.parse(item.field_value)
          urlInfo.forEach((elem, index)=>{
            child.push(<a href={elem.url}>{elem.file_name}<br/></a>)
          })
        } else {
          const url_list = item.field_value.split()
          url_list.forEach((url0)=>{

            child.push(<a href={url0}>{url0.split('/').slice(-1)[0]}</a>)
          })
        }
        }
        
      }
      else{
        child = <div>{item.field_value}</div>

      }
    }  else {
      if (item.field_attribute === 2 ) {
        if (item.field_type_id === 80){
          formItemOptions.rules = [{ required: true, message: `Please upload ${item.field_key}` },
        () => ({
          validator(rule, value) {
            if (value.fileList.length === 0){
              return Promise.reject('please upload file');
            }
          return Promise.resolve();
         },
      })
        ]}
        
        else {
          formItemOptions.rules = [{ required: true, message: `Please input ${item.field_key}` }]
        }
      }

      if (item.field_type_id === 5) {
        // 字符串
        child = <Input {...formItemChildOptions}/>

      } else if (item.field_type_id === 10){
        // 整形
        child = <InputNumber precision={0} {...formItemChildOptions}/>
      } else if (item.field_type_id === 15){
        // 浮点型
        child = <InputNumber {...formItemChildOptions}/>
      } else if (item.field_type_id === 20){
        // 布尔
        const radioOption = []
        for (var key in item.boolean_field_display) {
          radioOption.push(<Radio key={key} value={key}>{item.boolean_field_display[key]}</Radio>)
        }
        child = <Radio.Group
          {...formItemChildOptions}
        >
          {radioOption}
        </Radio.Group>
      } else if (item.field_type_id == 25){
        // 日期类型
        child = <DatePicker {...formItemChildOptions}/>
      } else if (item.field_type_id == 30){
        // 日期时间类型
        child = <DatePicker {...formItemChildOptions} showTime/>
      } else if (item.field_type_id == 35){
        // 单选
        const radioOption = []
        for (var key in item.field_choice) {
          radioOption.push(<Radio key={key} value={key}>{item.field_choice[key]}</Radio>)
        }
        child = <Radio.Group
          {...formItemChildOptions}
        >
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
        child = <Checkbox.Group style={{ width: '100%' }}
        >{checkboxOption}</Checkbox.Group>
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
        } {...formItemChildOptions}
        >
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
        } {...formItemChildOptions}
        >
          {selectOption}
        </Select>

      } else if (item.field_type_id === 55){
        // 文本
        child = <TextArea autoSize={{ minRows: 2, maxRows: 6 }} {...formItemChildOptions}/>
        // child = <TextArea autoSize={{ minRows: 2, maxRows: 6 }} {...formItemChildOptions} defaultValue={item.field_value}/>
      } else if (item.field_type_id === 58){
        // 富文本，先以文本域代替，后续再支持
        // child = <TextArea autoSize={{ minRows: 2, maxRows: 6 }} {...formItemChildOptions}/>
        child = <BraftEditor
          media={{uploadFn: myUploadFn}}
        />

      }
      else if (item.field_type_id === 80){
        // 附件import BraftEditor from 'braft-editor'
        child = <Upload action="api/v1.0/tickets/upload_file" listType="text" onChange={(info)=>this.fileChange(item.field_key, info)} fileList={this.state.fileList[item.field_key]}>
        {/*child = <Upload action="api/v1.0/tickets/upload_file" listType="text" onChange={(info)=>this.fileChange(item.field_key, info)}>*/}
          <Button icon={<UploadOutlined />}>Click to upload</Button>
        </Upload>
      }

      else if (item.field_type_id === 60){
        // 用户
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


      else if (item.field_type_id === 70){
        // 多选用户
        child = <Select
          mode="multiple"
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
        child = <Input {...formItemChildOptions}/>
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

  handleTicket = async (transitionId: number) => {
    const values = await this.formRef.current.validateFields();
    console.log(values);
    for (let key in values){
      if (this.state.fieldTypeDict[key] === 80 ) {
        // 文件   fieldList.url
        let urlList = [];
        values[key] && values[key].fileList.map(attachment => {
          //urlList.push(attachment.url)
          urlList.push({"url":attachment.url, "file_name":attachment.name})

        })
          values[key] = JSON.stringify(urlList);
        console.log(values[key])
      }
      if (this.state.fieldTypeDict[key] === 20 ) {
        // 日期
        values[key] = Number(values[key])
      }

      if (this.state.fieldTypeDict[key] === 25 && values[key] && typeof(values[key])!='string') {
        // 日期
        values[key] = values[key].format('YYYY-MM-DD')
      }
      if (this.state.fieldTypeDict[key] === 30 && values[key] && typeof(values[key])!='string') {
        // 时间
        values[key] = values[key].format('YYYY-MM-DD HH:mm:ss')
      }
      if (this.state.fieldTypeDict[key] === 40 && values[key]) {
        // 多选框
        console.log(values);
        console.log(values[key]);
        values[key] = values[key].join()
      }
      if (this.state.fieldTypeDict[key] === 50 && values[key]) {
        // 多选下拉
        values[key] = values[key].join()
      }
      if (this.state.fieldTypeDict[key] === 58) {
        // 富文本

        console.log(values[key])
        values[key] = typeof(values[key])=='string'?values[key]:values[key].toHTML()

        // values[key] = values[key].content.toHTML()
      }
      if (this.state.fieldTypeDict[key] === 70 && values[key]) {
        // 多选用户
        values[key] = values[key].join()
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


  acceptTicket = async(ticketId: number) => {
    //接单
    const result = await acceptTicketRequest(ticketId)
    if (result.code === 0) {
      message.success('接单成功');
      this.fetchTicketDetailInfo();
      this.fetchTicketTransitionInfo();
    } else {
      message.error(`接单失败: ${result.msg}`)
    }
  }

  addNodeEndTicket =  async(ticketId: number) =>{
    //加签完成
    // const values = await this.formRef.current.validateFields();
    const suggestion = await this.formRef.current.getFieldValue('suggestion');

    const result = await addNodeEndTicketRequest(ticketId, {suggestion: suggestion});
    if (result.code === 0) {
      this.fetchTicketDetailInfo();
      this.fetchTicketTransitionInfo();
    } else {
      message.error(`处理失败: ${result.msg}`)
    }
  }

  genHandleButtonItem = (item: any) => {
    const buttonItems = []
    let buttonType = 'primary'
    let buttonAttribute = null
    let buttonItem = null

    item.map(result => {
      if (result.is_accept === true) {
        buttonItem = <Button
          htmlType="submit"
          value = {result.transition_id}
          onClick={()=>this.acceptTicket(this.props.ticketId)}
        >
          {result.transition_name}
        </Button>
      } else if(result.in_add_node === true){
        buttonItem = <Button
          htmlType="submit"
          value = {result.transition_id}
          onClick={()=>this.addNodeEndTicket(this.props.ticketId)}
        >
          {result.transition_name}
        </Button>
      }
      else {
        let buttonType = 'primary';
        let dangerAttr = false;
        if (result.attribute_type_id === 2) {
          dangerAttr = true
        } else if (result.attribute_type_id === 3) {
          // 其他类型
          buttonType = "default"
        }
          if (result.alert_enable) {
            buttonItem = <Popconfirm
              title={result.alert_text}
              onConfirm={()=>this.handleTicket(result.transition_id)}
              okText="Yes"
              cancelText="No"
            >
              <Button
                value = {result.transition_id}
                danger = {dangerAttr}
                type = {buttonType}
              >
                {result.transition_name}
              </Button>
            </Popconfirm>
          } else {
            buttonItem = <Button
              value = {result.transition_id}
              danger = {dangerAttr}
              type = {buttonType}
              htmlType="submit"
              onClick={()=>this.handleTicket(result.transition_id)}
            >
              {result.transition_name}
            </Button>
          }

      }

      buttonItems.push(buttonItem);

    })

    if (item&& item[0] &&item[0].in_add_node===false && item[0].is_accept===false){
      buttonItems.push(
        <Button type="dashed" onClick={this.showDeliverModal} style={{marginLeft:50}}>
          转交
        </Button>
      )
      buttonItems.push(
        <Button type="dashed"  onClick={this.showAddNodeModal}>
          加签
        </Button>
      )

    }

    if (this.props.ticketId) {
      buttonItems.push(
        <Button type="dashed"  onClick={this.showCommentModal}>
          留言
        </Button>
      )
    }

    if (this.state.enable_retreat) {
      buttonItems.push(
        <Button type="dashed" danger onClick={this.showRetreatModal}>
          撤回
        </Button>
      )
    }

    const jwtInfo = decodeJwt(getCookie('jwt'))
    const currentUserName = jwtInfo? JSON.parse(jwtInfo).data.username: ''
    const ticketCreator = this.state.ticketInfo? this.state.ticketInfo.value.creator: ''
    const ticketType = this.state.ticketInfo? this.state.ticketInfo.value.state_info.type_id: 0
    if (currentUserName === ticketCreator && ticketType===1) {
      buttonItems.push(
        <Button type="dashed" danger onClick={this.showCloseModal}>
          关闭
        </Button>
      )
    }

    return buttonItems;
  }



  render() {
    const form_items = [];
    if (this.state.ticketDetailInfoData !== []){
      this.state.ticketDetailInfoData.map(result => {
        form_items.push(this.switchFormItem(result));
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
      <div>
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

              {this.state.ticketTransitionList.length !== 0 && this.props.ticketId!==0?
                <Form.Item
                  name="suggestion"
                >
                  <TextArea
                    placeholder="请输入处理意见"
                  />
                </Form.Item>: null
              }

              {handleButtonItems}
            </Form>
            {this.props.ticketId?
              <TicketList category="all" parentTicketId={this.props.ticketId}/>: null
            }
          </Collapse.Panel>
        </Collapse>
        {this.state.canIntervene?
          <Card title="管理员操作">
            <Button type="primary" danger onClick={this.showCloseModal}>
              强制关闭工单
            </Button>
            <Divider type="vertical" />
            <Button type="primary" danger onClick={this.showChangeStateModal}>

              强制修改状态
            </Button>
            <Divider type="vertical" />
            <Button type="primary" danger onClick={this.showAdminDeliverModal}>
              强制转交
            </Button>

          </Card>: null
        }

        <Modal title="强制关闭工单"
               visible={this.state.isCloseModalVisible}
               onCancel={this.closeModal}
               footer={null}
        >
          <Form
            onFinish={this.onCloseTicketFinish}
          >
            <Form.Item
              name="suggestion"
            >
              <TextArea
                placeholder="请输入备注/意见"
              />
            </Form.Item>
            <Form.Item>
              <Button type="primary" htmlType="submit" className="login-form-button">
                确定
              </Button>
            </Form.Item>
          </Form>
        </Modal>

        <Modal title= {this.state.deliverFromAdmin? "强制转交": "转交"}
               visible={this.state.isDeliverModalVisible}
               onCancel={this.closeModal}
               footer={null}
        >
          <Form
            onFinish={this.onDeliverFinish}
          >
            <Form.Item
              name="target_username"
              rules={[{ required: true, message: '请选择转交对象' }]}
            >
              <Select
                placeholder="请输入关键词搜索转交人"
                showSearch onSearch = {(search_value)=>this.userSimpleSearch('target_username', search_value)} filterOption={(input, option) =>
                option.children.toLowerCase().indexOf(input.toLowerCase()) >= 0
              }>
                {this.state.userSelectDict['target_username'] && this.state.userSelectDict['target_username'].map(d => (
                  <Option key={d.username} value={d.username}>{`${d.alias}(${d.username})`}</Option>
                ))}

              </Select>
            </Form.Item>
            <Form.Item
              name="suggestion"
            >
              <TextArea
                placeholder="请输入备注/处理意见"
              />
            </Form.Item>
            <Form.Item>
              <Button type="primary" htmlType="submit" className="login-form-button">
                提交
              </Button>
            </Form.Item>
          </Form>
        </Modal>

        <Modal title="强制修改状态"
               visible={this.state.isChangeStateModalVisible}
               onCancel={this.closeModal}
               footer={null}
        >
          <Form
            onFinish={this.onChangeStateFinish}
          >
            <Form.Item
              name="state_id"
              rules={[{ required: true, message: '请选择目标状态' }]}
            >
              <Select
                showSearch
                style={{ width: 200 }}
                placeholder="请选择状态"
                optionFilterProp="children"
                onChange={this.onStateChange}
                filterOption={(input, option) =>
                  option.children.toLowerCase().indexOf(input.toLowerCase()) >= 0
                }
              >
                {this.state.simpleStateList && this.state.simpleStateList.map(simpleState =>{
                  return <Option key={simpleState.id} value={simpleState.id}>{simpleState.name}</Option>
                })}
              </Select>
            </Form.Item>
            <Form.Item
              name="suggestion"
            >
              <TextArea
                placeholder="请输入备注/处理意见"
              />
            </Form.Item>
            <Form.Item>
              <Button type="primary" htmlType="submit" className="login-form-button">
                提交
              </Button>
            </Form.Item>
          </Form>
        </Modal>

        <Modal title="加签"
               visible={this.state.isAddNodeModalVisible}
               onCancel={this.closeModal}
               footer={null}
        >
          <Form
            onFinish={this.onAddNodeFinish}
          >
            <Form.Item
              name="target_username"
              rules={[{ required: true, message: '请选择加签对象' }]}
            >
              <Select
                placeholder="请输入关键词搜索转交人"
                showSearch onSearch = {(search_value)=>this.userSimpleSearch('target_username', search_value)} filterOption={(input, option) =>
                option.children.toLowerCase().indexOf(input.toLowerCase()) >= 0
              }>
                {this.state.userSelectDict['target_username'] && this.state.userSelectDict['target_username'].map(d => (
                  <Option key={d.username} value={d.username}>{`${d.alias}(${d.username})`}</Option>
                ))}

              </Select>
            </Form.Item>
            <Form.Item
              name="suggestion"
            >
              <TextArea
                placeholder="请输入备注/处理意见"
              />
            </Form.Item>
            <Form.Item>
              <Button type="primary" htmlType="submit" className="login-form-button">
                提交
              </Button>
            </Form.Item>
          </Form>
        </Modal>

        <Modal title="留言"
               visible={this.state.isCommentModalVisible}
               onCancel={this.closeModal}
               footer={null}
        >
          <Form
            onFinish={this.onCommentFinish}
          >
            <Form.Item
              name="suggestion"
            >
              <TextArea
                placeholder="请输入意见"
              />
            </Form.Item>
            <Form.Item>
              <Button type="primary" htmlType="submit" className="login-form-button">
                提交
              </Button>
            </Form.Item>
          </Form>
        </Modal>

        <Modal title="撤回"
               visible={this.state.isRetreatModalVisible}
               onCancel={this.closeModal}
               footer={null}
        >
          <Form
            onFinish={this.onRetreatFinish}
          >
            <Form.Item
              name="suggestion"
            >
              <TextArea
                placeholder="请输入意见"
              />
            </Form.Item>
            <Form.Item>
              <Button type="primary" htmlType="submit" className="login-form-button">
                提交
              </Button>
            </Form.Item>
          </Form>
        </Modal>

      </div>
    )
  }
}

export default TicketDetail;
