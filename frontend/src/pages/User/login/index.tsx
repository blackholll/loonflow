import { Alert, message } from 'antd';
import React, { useState } from 'react';
import Cookies from 'js-cookie';
import { Link, useModel } from 'umi';
import { getPageQuery } from '@/utils/utils';
import logo from '@/assets/logo.svg';
import { LoginParamsType, fakeAccountLogin } from '@/services/login';
import Footer from '@/components/Footer';
import LoginFrom from './components/Login';
import styles from './style.less';

const { Tab, Username, Password, Submit } = LoginFrom;

const LoginMessage: React.FC<{
  content: string;
}> = ({ content }) => (
  <Alert
    style={{
      marginBottom: 24,
    }}
    message={content}
    type="error"
    showIcon
  />
);

/**
 * This method will jump to the location of the redirect parameter
 */
const replaceGoto = () => {
  const urlParams = new URL(window.location.href);
  const params = getPageQuery();
  let { redirect } = params as { redirect: string };
  if (redirect) {
    const redirectUrlParams = new URL(redirect);
    if (redirectUrlParams.origin === urlParams.origin) {
      redirect = redirect.substr(urlParams.origin.length);
      if (redirect.match(/^\/.*#/)) {
        redirect = redirect.substr(redirect.indexOf('#'));
      }
    } else {
      window.location.href = '/';
      return;
    }
  }
  window.location.href = urlParams.href.split(urlParams.pathname)[0] + (redirect || '/');
};

const Login: React.FC<{}> = () => {
  const [userLoginState, setUserLoginState] = useState<API.LoginStateType>({});
  const [submitting, setSubmitting] = useState(false);

  const { refresh } = useModel('@@initialState');
  const [type, setType] = useState<string>('account');

  const handleSubmit = async (values: LoginParamsType) => {
    setSubmitting(true);
    try {
      // Log in
      const msg = await fakeAccountLogin({ ...values, type });
      if (msg.code === 0) {
        Cookies.set('jwt',msg.data.jwt);
        message.success('login successful！');
        replaceGoto();
        setTimeout(() => {
          refresh();
        }, 0);
        return;
      }
      // 如果失败去设置用户错误信息
      setUserLoginState(msg);
    } catch (error) {
      message.error('Login failed, please try again！');
    }
    setSubmitting(false);
  };

  const { code, type: loginType } = userLoginState;

  return (
    <div className={styles.container}>
      <div className={styles.content}>
        <div className={styles.top}>
          <div className={styles.header}>
            <Link to="/">
              <img alt="logo" className={styles.logo} src={logo} />
              <span className={styles.title}>Loonflow</span>
            </Link>
          </div>
          <div className={styles.desc}>Loonflow Committed to providing enterprises with a unified workflow solution</div>
        </div>

        <div className={styles.main}>
          <LoginFrom activeKey={type} onTabChange={setType} onSubmit={handleSubmit}>
            <Tab key="account" tab="Account password login">
              {code === -1 && loginType === 'account' && !submitting && (
                <LoginMessage content="wrong account or password（admin/ant.design）" />
              )}

              <Username
                name="username"
                placeholder="please enter user name"
                rules={[
                  {
                    required: true,
                    message: 'please enter user name!',
                  },
                ]}
              />
              <Password
                name="password"
                placeholder="Please enter password"
                rules={[
                  {
                    required: true,
                    message: 'Please enter password！',
                  },
                ]}
              />
            </Tab>
            <Submit loading={submitting}>Log in</Submit>
          </LoginFrom>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default Login;
