import React from "react";
import { Link } from 'react-router-dom'
import { Menu, Icon, Layout } from 'antd';
const { Sider } = Layout
const SubMenu = Menu.SubMenu;
import "./BasicSider.less";

class BasicSider extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    return (
      <React.Fragment>
        <Sider
          collapsible
          collapsed={this.props.collapsed}
          onCollapse={this.props.onCollapse}
        >
          <div className="logo" />
          <Menu theme="dark" defaultSelectedKeys={['1']} mode="inline">
            <Menu.Item key="1">
              <Link to="/">
                <Icon type="pie-chart" />
                <span>Home</span>
              </Link>
            </Menu.Item>
            <Menu.Item key="2">
              <Link to="/Users">
                <Icon type="desktop" />
                <span>User</span>
              </Link>
            </Menu.Item>
            {/* <SubMenu
              key="sub1"
              title={<span><Icon type="user" /><span>User</span></span>}
            >
              <Menu.Item key="3">Tom</Menu.Item>
              <Menu.Item key="4">Bill</Menu.Item>
              <Menu.Item key="5">Alex</Menu.Item>
            </SubMenu>
            <SubMenu
              key="sub2"
              title={<span><Icon type="team" /><span>Team</span></span>}
            >
              <Menu.Item key="6">Team 1</Menu.Item>
              <Menu.Item key="8">Team 2</Menu.Item>
            </SubMenu> */}
            {/* <Menu.Item key="9">
              <Icon type="file" />
              <span>File</span>
            </Menu.Item> */}
          </Menu>
        </Sider>
      </React.Fragment>
    )
  }
}

export default BasicSider;
