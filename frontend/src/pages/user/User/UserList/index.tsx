import React, { Component } from "react";
import {Table, Col, Card, Row, Form, Input, Button, message, Pagination} from "antd";
import {getUserList} from "@/services/user";


class UserList extends Component<any, any> {
  constructor(props) {
    super();
    this.state = {
      userResult: [],
      userListLoading: false,
      pagination: {
        current: 1,
        total: 0,
        pageSize: 10,
        onChange: (current) => {
          const pagination = { ...this.state.pagination };
          pagination.page = current;
          pagination.current = current;
          this.setState({ pagination }, () => {
            console.log('newpage');
          });
        }
      }
    }
  }


  componentDidMount() {
    this.fetchUserData({});
  }

  fetchUserData = async (params) => {
    this.setState({userListLoading: true});
    const result = await getUserList(params);
    if (result.code === 0) {
      const pagination = { ...this.state.pagination };
      pagination.page = result.data.page;
      pagination.pageSize = result.data.per_page;
      pagination.total = result.data.total;

      this.setState({
        userResult: result.data.value,
        userListLoading: false,
        pagination

      });

    } else {
      message.error(result.msg);
    }
  }

  render() {

    const columns = [
      {
        title: "用户名",
        dataIndex: "username",
        key: "username"
      },
      {
        title: "姓名",
        dataIndex: "alias",
        key: "alias"
      },
      {
        title: "邮箱",
        dataIndex: "email",
        key: "email"
      },
      {
        title: "电话",
        dataIndex: "phone",
        key: "phone"
      },
      {
        title: "部门",
        key: "user_dept",
        render: (text: string, record: any) => {
          const deptInfoList = [];
          record.user_dept_info_list.forEach(function(item) {
            deptInfoList.push(item.name);
          });
          return deptInfoList.join(',');

        }
      },
      {
        title: "状态",
        dataIndex: "is_active",
        key: "is_active",
        render: (text: string, record:any) => {
          if (record.is_active) {
            return '在职'
          } else {
            return '已离职'
          }
        }
      },
      {
        title: "用户类型",
        key: "userType",
        render: (text: string, record: any) => {
          if (record.type_id === 0) {
            return "普通用户"
          } else if (record.type_id === 1) {
            return "工作流管理员"
          } else if (record.type_id === 2) {
            return "超级管理员"
          } else {
            return "未知"
          }
        }
      },
      {
        title: "创建人",
        dataIndex: ["creator_info", "creator_alias"],
        key: "creator_info"
      },
      {
        title: "创建时间",
        dataIndex: "gmt_created",
        key: "gmt_created"
      },
      {
        title: "操作",
        key: "action",
        render: (text: string, record: any) => (
          <span>
            <a style={{marginRight: 16}} onClick={() => console.log('ss')}>编辑</a>
            <a style={{marginRight: 16}}>重置密码</a>
            <a style={{marginRight: 16}}>查看角色</a>
            <a style={{marginRight: 16, color: "red"}}>删除</a>
          </span>
        )
      }

    ]


    return (
      <div>
        <Card>
        <Form
          name="advanced_search"
          className="ant-advanced-search-form"
          ref={this.formRef}
          onFinish={this.searchTicket}
        >
          <Row gutter={24}>
            <Col span={6} key={"search_value"}>
              <Form.Item
                name={"search_value"}
                label={"查询"}
              >
                <Input placeholder="支持姓名模糊查询" />
              </Form.Item>
            </Col>
            <Col>
            <Button type="primary" htmlType="submit">
              搜索
            </Button>
            </Col>
          </Row>
          <Row>
            <Col span={24} style={{ textAlign: 'right' }}>
              <Button type="primary" htmlType="submit">
                新增
              </Button>
              </Col>
          </Row>
        </Form>
          <Table loading={this.state.userListLoading} columns={columns} dataSource={this.state.userResult}
                 rowKey={record => record.id} pagination={this.state.pagination}/>
        </Card>
      </div>

    )

  }

}

export default UserList;
