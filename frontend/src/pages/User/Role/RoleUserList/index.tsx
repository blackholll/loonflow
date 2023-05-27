import React, { Component } from "react";
import {Table, message, Popconfirm, Row, Col, Form, Input, Button, Modal, Select, Radio} from "antd";
import {getRoleUserList, delRoleUser, delRoleUserRequest, queryUserSimple, addRoleUser} from "@/services/user";

const { Option } = Select;


class RoleUserList extends Component<any, any> {
  constructor(props) {
    super();
    this.state = {
      roleUserResult: [],
      roleUserLoading: false,
      searchUserResult: [],
      roleUserModalVisible: false,
      data: [],
      pagination: {
        current: 1,
        total: 0,
        pageSize: 10,
        onChange: (current) => {
          const pagination = { ...this.state.pagination };
          pagination.current = current;
          this.setState({pagination}, ()=> {
            this.fetchRoleUser({page:pagination.current, per_page: pagination.pageSize})
          })
        }
      }
    }

  }
  componentDidMount() {
    this.fetchRoleUser({per_page:10, page:1})
  }



  searchRoleUser = (values: object) => {
    console.log(values);
    this.fetchRoleUser({...values, per_page:10, page:1})
  }

  handleRoleUserOk = () => {
    this.setState({roleUserModalVisible: false})
  }

  showRoleUserModal = (userId) => {
    this.setState({roleUserModalVisible: true, selectUserId: userId});
  }


  handleRoleUserCancel = () => {
    this.setState({roleUserModalVisible: false})
  }

  fetchRoleUser = async(params: any) => {
    this.setState({roleUserLoading: true})
    const result = await getRoleUserList(this.props.roleId, params)
    if (result.code === 0 ) {
      const pagination = { ...this.state.pagination };
      pagination.current = result.data.page;
      pagination.pageSize = result.data.per_page;
      pagination.total = result.data.total;
      this.setState({roleUserResult: result.data.value, roleUserLoading:false,pagination});
    } else {
      message.error(`获取角色用户列表失败: ${result.msg}`)
      this.setState({roleUserLoading:false});
    }
  }

  delRoleUser = async(userId: number) => {
    const result = await delRoleUserRequest(this.props.roleId, userId);
    if (result.code === 0 ) {
      message.success('删除角色用户成功');
      this.fetchRoleUser({page:1, per_page:10});
    } else {
      message.error(`删除角色用户失败: ${result.msg}`)
    }
  }

  searchUser = async(search_value: string) => {
    const result = await queryUserSimple({search_value:search_value});
    if (result.code ===0 ) {
      this.setState({searchUserResult: result.data.value});
    }
  }

  onRoleUserFinish = async(values: object) => {
    const result = await addRoleUser(this.props.roleId,{user_id: Number(values.user)});
    if (result.code ===0 ) {
      message.success('新增角色用户成功');
      this.setState({roleUserModalVisible: false})
      this.fetchRoleUser({});
    } else {
      message.error(`新增角色用户失败:${result.msg}`);
    }
  }

  render() {
    const columns = [
      {
        title: "ID",
        dataIndex: "id",
        key: "id"
      },
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
        title: "操作",
        key: "action",
        render: (text: string, record: any) => (
          <span>
            <a style={{marginRight: 16, color: "red"}}>
              <Popconfirm
                title="确认删除么"
                onConfirm={()=>{this.delRoleUser(record.id)}}
              >
                删除
              </Popconfirm>
            </a>
          </span>
        )
      }
    ]
    const layout = {
      labelCol: { span: 8 },
      wrapperCol: { span: 16 },
    };
    const tailLayout = {
      wrapperCol: { offset: 8, span: 16 },
    };


    return (
      <div>
        <Form
          name="advanced_search"
          className="ant-advanced-search-form"
          onFinish={this.searchRoleUser}
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
              <Button type="primary" onClick={()=>this.showRoleUserModal(0)}>
                新增
              </Button>
            </Col>
          </Row>
        </Form>
      <Table loading={this.state.roleUserLoading} columns={columns} dataSource={this.state.roleUserResult}
             rowKey={record => record.id} pagination={this.state.pagination}/>
      <Modal
        title={"角色用户"}
        visible={ this.state.roleUserModalVisible}
        width={800}
        footer={null}
        onOk={this.handleRoleUserOk}
        onCancel={this.handleRoleUserCancel}
        destroyOnClose
      >
        <Form
          {...layout}
          onFinish={this.onRoleUserFinish}
        >
          <Form.Item name="user" label="用户" rules={[{ required: true }]}>
            <Select
              showSearch
              allowClear
              style={{ width: '100%' }}
              placeholder="请搜索用户"
              onSearch = {this.searchUser}
              filterOption={(input, option) =>
                option.children.toLowerCase().indexOf(input.toLowerCase()) >= 0
              }
            >
              {this.state.searchUserResult && this.state.searchUserResult.map(d => (<Option key={d.id} value={d.id}>{`${d.alias}(${d.username})`}</Option>))}



            </Select>
          </Form.Item>
          <Form.Item {...tailLayout}>
            <Button type="primary" htmlType="submit">
              确定
            </Button>
          </Form.Item>

        </Form>

      </Modal>
      </div>
     )
  }

}

export default RoleUserList;
