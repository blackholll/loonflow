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
      message.error('两次密码不一致，请重新输入')
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
      message.success('修改密码成功')
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
        label = "原密码"
        name = "sourcePwd"
        rules={[{ required: true, message: '请输入你的原密码!' }]}
      >
        <Input />

      </Form.Item>
      <Form.Item
        label = "新密码"
        name = "newPwd"
        rules={[{ required: true, message: '请输入新密码!' }]}
      >
        <Input.Password />

      </Form.Item>
      <Form.Item
        label = "再次输入新密码"
        name = "newPwdAgain"
        rules={[{ required: true, message: '请再次输入新密码' }]}
      >
        <Input.Password />

      </Form.Item>

      <Form.Item {...tailLayout}>
        <Button type="primary" htmlType="submit">
          确认
        </Button>
      </Form.Item>

    </Form>
    </Card>
  )


}

export default ChangePwd
