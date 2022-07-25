import {Button, Form, Input, Card, message} from 'antd';
import React from "react";
import {changeUserPassword} from "@/services/user";

const layout = {
  labelCol: { span: 8},
  wrapperCol: {span: 8},
};

const tailLayout = {
  wrapperCol: { offset: 8, span:16},
};

const ChangePwd = () => {
  const onFinish = async (values: any) => {
    if (values.newPwd !== values.newPwdAgain) {
      message.error('The two passwords do not match, please re-enter')
    }
    console.log(values);
    values.source_password = values.sourcePwd
    values.new_password = values.newPwd
    values.new_password_again = values.newPwdAgain
    delete values.newPwdAgain
    delete values.sourcePwd
    delete values.newPwd
    const result = await changeUserPassword(values)
    if (result.code === 0) {
      message.success('password has been updated')
    } else {
      message.error(result.msg)
    }

  };

  return (
    <Card>
    <Form
      {...layout}
      name="changePwdForm"
      onFinish={onFinish}
    >
      <Form.Item
        label = "old password"
        name = "sourcePwd"
        rules={[{ required: true, message: 'Please enter your original password!' }]}
      >
        <Input />

      </Form.Item>
      <Form.Item
        label = "new password"
        name = "newPwd"
        rules={[{ required: true, message: 'Please enter a new password!' }]}
      >
        <Input.Password />

      </Form.Item>
      <Form.Item
        label = "Enter the new password again"
        name = "newPwdAgain"
        rules={[{ required: true, message: 'Please enter new password again' }]}
      >
        <Input.Password />

      </Form.Item>

      <Form.Item {...tailLayout}>
        <Button type="primary" htmlType="submit">
          confirm
        </Button>
      </Form.Item>

    </Form>
    </Card>
  )


}

export default ChangePwd
