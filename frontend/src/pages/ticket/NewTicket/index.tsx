import { Form, Input, Button, Checkbox, Col, Row } from 'antd';
import Workbench from "@/pages/Workbench";

const layout = {
  labelCol: { span: 8},
  wrapperCol: { span: 16},
};

const tailLayout = {
  wrapperCol: { offset:8, span: 16},
};

const Demo = () => {
  const onFinish = values => {
    console.log('success:', values);

  };

  const onFinishFailed = errorInfo => {
    console.log('Failed:', errorInfo);
  };

  return (
    <Form
      {...layout}
      name="basic"
      initialValues = {{ remember: true}}
      onFinish={onFinish}
      onFinishFailed={{onFinishFailed}}
      >
      <Row gutter={24}>
      <Col span={12}>
        <Form.Item
          label="Username"
          name="username"
          rules={[{ required: true, message:'please input you username'}]}
          >
          <Input />

        </Form.Item>
      </Col>
      <Col span={12}>
        <Form.Item
          label="Username1"
          name="username1"
          rules={[{ required: true, message:'please input you username'}]}
        >
          <Input />

        </Form.Item>
      </Col>
      </Row>
    </Form>
  )
}
export default Demo;



// import React, { Component } from "react";
// import { Input, Form, Input, Radio, Checkbox, Select,  } from "antd";
// import { getWorkflowInitState } from "@/services/workflows";
//
// const FormItem = Form.Item;
// const { TextArea } = Input;
// const RadioGroup = Radio.Group;
// const Option = Select.Option;
//
//
// class NewTicketForm extends Component<any, any> {
//   constructor(props) {
//     super(props);
//     this.state = {};
//   }
//
//   componentDidMount() {
//     this.fetchWorkflowInitState();
//   }
//
//   fetchWorkflowInitState = async () => {
//     console.log(`worklfoid: ${this.props.workflowId}`)
//     const result = await getWorkflowInitState({ workflowId: this.props.workflowId});
//     if (result.code === 0){
//       this.setState({initState: result.data.value});
//
//
//     }
//
//   }
//   render() {
//     return (
//       'ticket detail'
//     )
//   }
//
// }
//
// const NewTicket = Form.create()(NewTicketForm)
// export default NewTicket
