import React, { useState } from 'react';
import { Form, Input, Button, message } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import { history } from 'umi';
import Cookies from 'js-cookie';
import axios from 'axios';
import { AccountLogin } from '@/services/login';

const Login: React.FC = () => {
  const [loading, setLoading] = useState<boolean>(false);

  const onFinish = async (values: any) => {
    setLoading(true);
    try {
      const response = await AccountLogin(values);
      const { code, data } = response;
      if (code === 0 && data.jwt) {
        Cookies.set('jwt', data.jwt);
        history.push('/tickets');
      } else {
        message.error('Login failed');
      }
    } catch (error) {
      message.error('Login failed');
    }
    setLoading(false);
  };

  return (
    <div style={{ width: 300, margin: 'auto', marginTop: 100 }}>
      <h1>Loonflow</h1>
      <Form name="login" onFinish={onFinish}>
        <Form.Item
          name="email"
          rules={[{ required: true, message: 'Please input your email!' }]}
        >
          <Input prefix={<UserOutlined />} placeholder="Email" />
        </Form.Item>
        <Form.Item
          name="password"
          rules={[{ required: true, message: 'Please input your password!' }]}
        >
          <Input.Password prefix={<LockOutlined />} placeholder="Password" />
        </Form.Item>
        <Form.Item>
          <Button type="primary" htmlType="submit" loading={loading} style={{ width: '100%' }}>
            Log in
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
};

export default Login;
