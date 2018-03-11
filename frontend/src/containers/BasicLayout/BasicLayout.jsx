import React from 'react'
import { Layout, Menu, Breadcrumb, Icon } from 'antd';
const { Header, Content, Footer } = Layout;
const SubMenu = Menu.SubMenu;
import './BasicLayout.less';

import Routers from '../../routers/index.jsx'
import BasicSider from "../BasicSider/BasicSider";

class SiderDemo extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      collapsed: false,
    };
    this.onCollapse = this.onCollapse.bind(this)
  }

  onCollapse(collapsed) {
    console.log(collapsed);
    this.setState({ collapsed });
  }
  render() {
    return (
      <Layout style={{ minHeight: '100vh' }}>
        <BasicSider collapsed={this.state.collapsed} onCollapse = {this.onCollapse}/>
        <Layout>
          <Header style={{ background: '#fff', padding: 0 }} />
          <Content style={{ margin: '0 16px' }}>
            <Breadcrumb style={{ margin: '16px 0' }}>
              <Breadcrumb.Item>User</Breadcrumb.Item>
              <Breadcrumb.Item>Bill</Breadcrumb.Item>
            </Breadcrumb>
            {/* <MainContent /> */}
            <Routers />
          </Content>
          <Footer style={{ textAlign: 'center' }}>
            Ant Design ©2016 Created by Ant UED
          </Footer>
        </Layout>
      </Layout>
    );
  }
}

export default SiderDemo
