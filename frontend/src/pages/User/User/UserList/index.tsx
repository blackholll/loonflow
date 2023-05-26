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
      pagination.current = result.data.page;
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
            <a style={{marginRight: 16}} onClick={() => this.showEditModal(record)}>编辑</a>
            <a style={{marginRight: 16}}>
              <Popconfirm
                title="确认重置么？确定后密码将被重置为123456"
                onConfirm={()=>this.resetPasswd(record.id)}>
                <a href="#">重置密码</a>
              </Popconfirm>
            </a>
            <a style={{marginRight: 16}} onClick={()=>this.showUserRole(record.id)}>查看角色</a>
            <a style={{marginRight: 16, color: "red"}}>
              <Popconfirm
                title="确认删除么"
                onConfirm={()=>{this.delUser(record.id)}}
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
                label={"查询"}
              >
                <Input placeholder="支持用户名及姓名模糊查询" />
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
              <Button type="primary" onClick={()=>this.showUserModal(0)}>
                新增
              </Button>
              </Col>
          </Row>
        </Form>
          <Table loading={this.state.userListLoading} columns={columns} dataSource={this.state.userResult}
                 rowKey={record => record.id} pagination={this.state.pagination}/>
        </Card>
        <Modal
          title="用户"
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
            <Form.Item name="username" label="用户名" rules={[{ required: true }]} initialValue={this.getUserDetailField('username')}>
              <Input />
            </Form.Item>
            <Form.Item name="alias" label="姓名" rules={[{ required: true }]} initialValue={this.getUserDetailField('alias')}>
              <Input />
            </Form.Item>
            <Form.Item name="email" label="邮箱" rules={[{ required: true }]} initialValue={this.getUserDetailField('email')}>
              <Input />
            </Form.Item>
            <Form.Item name="phone" label="电话" rules={[{ required: true }]} initialValue={this.getUserDetailField('phone')}>
              <Input />
            </Form.Item>
            <Form.Item name="dept" label="部门" rules={[{ required: true }]}  initialValue={this.getUserDetailField('dept')}>
              <Select
                mode="multiple"
                allowClear
                style={{ width: '100%' }}
                placeholder="请选择用户所在部门"
              >
                {this.state.deptResult.map(d => (

                  <Option key={d.id} value={d.id}>{d.name}</Option>
                ))}
              </Select>
            </Form.Item>
            <Form.Item name="is_active" label="在职" rules={[{ required: true }]} initialValue={this.getUserDetailField('is_active')}>
              <Radio.Group value = {this.state.defaultUserState}>
                <Radio value={1}>在职</Radio>
                <Radio value={0}>离职</Radio>
              </Radio.Group>
            </Form.Item>
            <Form.Item name="type_id" label="用户类型" rules={[{ required: true }]} initialValue={this.getUserDetailField('type_id')}>
              <Radio.Group >
                <Radio value={0}>普通用户</Radio>
                <Radio value={1}>工作流管理员</Radio>
                <Radio value={2}>超级管理员</Radio>
              </Radio.Group>
            </Form.Item>

            <Form.Item {...tailLayout}>
              <Button type="primary" htmlType="submit">
                确定
              </Button>
            </Form.Item>

          </Form>
        </Modal>

        <Modal
          title={"用户角色"}
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
