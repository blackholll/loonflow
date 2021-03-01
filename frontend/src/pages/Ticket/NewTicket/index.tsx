import {Form, Input, Button, Checkbox, Col, Row, message} from 'antd';
import React, {Component} from 'react';
import {getWorkflowInitState} from "@/services/workflows";


class NewTicket extends Component<any, any> {
  constructor(props) {
    super();
    this.state = {
      workflowResult: [],

    };
  }

  componentDidMount() {
    this.fetchWorkflowInitData();
  }


  onFinish = values => {
    console.log('success:', values);

  };

  onFinishFailed = errorInfo => {
    console.log('Failed:', errorInfo);
  };



  fetchWorkflowInitData = async () => {
    const result = await getWorkflowInitState({workflowId: this.props.workflowId})
    if (result.code === 0) {
      this.setState({workflowResult: result.data.value});
    } else {
      message.error(result.msg);
    }

  }


  render(){
    const layout = {
      labelCol: { span: 8},
      wrapperCol: { span: 16},
    };

    const tailLayout = {
      wrapperCol: { offset:8, span: 16},
    };



    return (
      <Form
        {...layout}
        name="basic"
        initialValues = {{ remember: true}}
        onFinish={this.onFinish}
        onFinishFailed={this.onFinishFailed}
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

}

export default NewTicket;
