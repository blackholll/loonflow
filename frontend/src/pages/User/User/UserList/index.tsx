import React, { Component } from "react";
import {Table, Col, Card, Row, Form, Input, Button, message, Modal, Select, Radio, Popconfirm} from "antd";
import {addUser, delUserRequest, getDeptList, getUserList, resetUserPasswd, updateUser} from "@/services/user";
import UserRoleList from "@/pages/User/User/UserRoleList";

const { Option } = Select;


class UserList extends Component<any, any> {
  constructor(props) {
    super();
    this.state = {
      userResult: [],
      deptResult: [],
      userListLoading: false,
      userModalVisible: false,
      userRoleModalVisible: false,
      userDetail: {},
      userIdForRole: 0,
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
            this.fetchUserData({
              page: pagination.page,
              per_page: pagination.pageSize
            })
          });
        }
      }
    }
  }


  componentDidMount() {
    this.fetchUserData({});
    this.fetchDeptData({"per_page":10000});
  }

  fetchDeptData = async (params) => {
    // todo get dept data
    const result = await getDeptList(params);
    if (result.code ===0 ) {
      this.setState({deptResult: result.data.value})
    }
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

  searchTicket = (values) => {
    this.fetchUserData({per_page:10, page:1, search_value: values.search_value});
  }

  showUserModal =(userId) =>{
    this.setState({
      userModalVisible: true,
    })
  }

  onUserFinish= async (values) =>{
    values.dept_ids = values.dept.join(',');
    delete values['dept'];
    console.log(this.state.userDetail);
    console.log(this.state.userDetail.id)
    let result = {}
    if (this.state.userDetail && this.state.userDetail.id){
      result = await updateUser(this.state.userDetail.id, values);
    } else {
      result = await addUser(values);
    }
    if (result.code === 0) {
      message.success('保存成功');
      this.setState({userModalVisible: false});
      this.fetchUserData({});
    } else {
      message.error(`保存失败: ${result.msg}`);
    }
  }

  handleUserOk = () => {
    this.setState({
      userModalVisible: false,
      userRoleModalVisible: false
    })
  }

  handleUserCancel = () => {
    this.setState({
      userModalVisible: false,
      userRoleModalVisible: false
    })
  }

  resetPasswd = async (userId: number) => {
    const result = await resetUserPasswd(userId);
    if (result.code === 0 ) {
      message.success('重置成功,密码被初始化为123456');
    }
    else {
      message.error(`重置密码失败: ${result.message}`);
    }

  }

  delUser = async(userId:number) => {
    const result = await delUserRequest(userId);
    if (result.code === 0 ) {
      // 刷新用户列表
      this.fetchUserData({});
      message.success('删除成功');
    }
    else {
      message.error(`删除失败: ${result.message}`);
    }
  }


  showEditModal = (record: any) =>{
    record.is_active = record.is_active? 1: 0;
    const deptInfo: Arrary = [];
    if (record.user_dept_info_list.length===0){
      record.dept = []
    } else {
      record.user_dept_info_list.forEach(result =>{
        deptInfo.push(result.id);
      })
      record.dept = deptInfo;
    }
    console.log(record);

    this.setState({userDetail:record, userModalVisible:true})
  }

  getUserDetailField = (fieldName:string) =>{
    if(this.state && this.state.userDetail){
      return this.state.userDetail[fieldName]
    }
    return ''
  }

  showUserRole = (userId: number) => {
    this.setState({userIdForRole: userId, userRoleModalVisible:true});
  }

  render() {

    const columns = [
      {
        title: "username",
        dataIndex: "username",
        key: "username"
      },
      {
        title: "alias",
        dataIndex: "alias",
        key: "alias"
      },
      {
        title: "email",
        dataIndex: "email",
        key: "email"
      },
      {
        title: "phone",
        dataIndex: "phone",
        key: "phone"
      },
      {
        title: "user dept",
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
        title: "is_active",
        dataIndex: "is_active",
        key: "is_active",
        render: (text: string, record:any) => {
          if (record.is_active) {
            return 'yes'
          } else {
            return 'no'
          }
        }
      },
      {
        title: "userType",
        key: "userType",
        render: (text: string, record: any) => {
          if (record.type_id === 0) {
            return "general user"
          } else if (record.type_id === 1) {
            return "Workflow administrator"
          } else if (record.type_id === 2) {
            return "super administrator"
          } else {
            return "unknown"
          }
        }
      },
      {
        title: "creator_info",
        dataIndex: ["creator_info", "creator_alias"],
        key: "creator_info"
      },
      {
        title: "created",
        dataIndex: "gmt_created",
        key: "gmt_created"
      },
      {
        title: "action",
        key: "action",
        render: (text: string, record: any) => (
          <span>
            <a style={{marginRight: 16}} onClick={() => this.showEditModal(record)}>edit</a>
            <a style={{marginRight: 16}}>
              <Popconfirm
                title="Are you sure to reset? After confirmation, the password will be reset to 123456"
                onConfirm={()=>this.resetPasswd(record.id)}>
                <a href="#">reset Password</a>
              </Popconfirm>
            </a>
            <a style={{marginRight: 16}} onClick={()=>this.showUserRole(record.id)}>View roles</a>
            <a style={{marginRight: 16, color: "red"}}>
              <Popconfirm
                title="Are you sure to delete?"
                onConfirm={()=>{this.delUser(record.id)}}
              >
                delete
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
        <Card>
        <Form
          name="advanced_search"
          className="ant-advanced-search-form"
          onFinish={this.searchTicket}
        >
          <Row gutter={24}>
            <Col span={6} key={"search_value"}>
              <Form.Item
                name={"search_value"}
                label={"search"}
              >
                <Input placeholder="Support user name and name fuzzy query" />
              </Form.Item>
            </Col>
            <Col>
            <Button type="primary" htmlType="submit">
              search
            </Button>
            </Col>
          </Row>
          <Row>
            <Col span={24} style={{ textAlign: 'right' }}>
              <Button type="primary" onClick={()=>this.showUserModal(0)}>
                new
              </Button>
              </Col>
          </Row>
        </Form>
          <Table loading={this.state.userListLoading} columns={columns} dataSource={this.state.userResult}
                 rowKey={record => record.id} pagination={this.state.pagination}/>
        </Card>
        <Modal
          title="user"
          visible={this.state.userModalVisible}
          onOk={this.handleUserOk}
          onCancel={this.handleUserCancel}
          width={800}
          footer={null}
          destroyOnClose
        >
          <Form
            {...layout}
            onFinish={this.onUserFinish}
          >
            <Form.Item name="username" label="username" rules={[{ required: true }]} initialValue={this.getUserDetailField('username')}>
              <Input />
            </Form.Item>
            <Form.Item name="alias" label="alias" rules={[{ required: true }]} initialValue={this.getUserDetailField('alias')}>
              <Input />
            </Form.Item>
            <Form.Item name="email" label="email" rules={[{ required: true }]} initialValue={this.getUserDetailField('email')}>
              <Input />
            </Form.Item>
            <Form.Item name="phone" label="phone" rules={[{ required: true }]} initialValue={this.getUserDetailField('phone')}>
              <Input />
            </Form.Item>
            <Form.Item name="dept" label="department" rules={[{ required: true }]}  initialValue={this.getUserDetailField('department')}>
              <Select
                mode="multiple"
                allowClear
                style={{ width: '100%' }}
                placeholder="Please select the user's department"
              >
                {this.state.deptResult.map(d => (

                  <Option key={d.id} value={d.id}>{d.name}</Option>
                ))}
              </Select>
            </Form.Item>
            <Form.Item name="is_active" label="on-the-job" initialValue={this.getUserDetailField('is_active')}>
              <Radio.Group value = {this.state.defaultUserState}>
                <Radio value={1}>on-the-job</Radio>
                <Radio value={0}>resign</Radio>
              </Radio.Group>
            </Form.Item>
            <Form.Item name="type_id" label="user type" initialValue={this.getUserDetailField('type_id')}>
              <Radio.Group >
                <Radio value={0}>general user</Radio>
                <Radio value={1}>Workflow administrator</Radio>
                <Radio value={2}>super administrator</Radio>
              </Radio.Group>
            </Form.Item>

            <Form.Item {...tailLayout}>
              <Button type="primary" htmlType="submit">
                Sure
              </Button>
            </Form.Item>

          </Form>
        </Modal>

        <Modal
          title={"user role"}
          visible={ this.state.userRoleModalVisible}
          width={800}
          footer={null}
          onOk={this.handleUserOk}
          onCancel={this.handleUserCancel}
          destroyOnClose
        >
          <UserRoleList userId={this.state.userIdForRole}/>

        </Modal>
      </div>

    )

  }

}

export default UserList;
