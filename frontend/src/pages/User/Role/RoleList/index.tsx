import React, { Component } from "react";
import {Table, Col, Card, Popconfirm, Form, Input, Select, Radio, Button, Modal, Row, message} from "antd";
import {addRole, delRoleRequest, getRoleList, updateRole} from "@/services/user";
import RoleUserList from "@/pages/User/Role/RoleUserList";


class RoleList extends Component<any, any> {
  constructor(props) {
    super();
    this.state = {
      roleListResult : [],
      roleListLoading: false,
      roleModalVisible: false,
      roleUserModalVisible: false,
      roleIdForRoleUser: 0,
      pagination: {
        current: 1,
        total: 0,
        pageSize: 10,
        onChange: (current) => {
          const pagination = { ...this.state.pagination };
          pagination.current = current;
          this.setState( { pagination }, ()=> {
            this.fetchRoleData({
              page: pagination.current,
              per_page: pagination.pageSize
            })
          });
        }
      }
    }
  }

  componentDidMount() {
    this.fetchRoleData({page:1, per_page:10})
  }

  fetchRoleData = async (params) => {
    this.setState({ roleListLoading: true})
    const result = await getRoleList(params);
    if (result.code === 0 ) {
      const pagination = { ...this.state.pagination };
      pagination.page = result.data.page;
      pagination.pageSize = result.data.per_page;
      pagination.total = result.data.total;

      this.setState({
        roleListLoading: false,
        roleListResult: result.data.value,
        pagination
      })
    }
  }

  searchRole =(values: object)=>{
    this.fetchRoleData({...values, per_page:10, page:1})
  }

  showEditModal = (record: any) => {
    this.setState({roleDetail: record, roleModalVisible:true});
  }

  showRoleUserModal = (roleId: number) => {
    this.setState({roleUserModalVisible: true, roleIdForRoleUser: roleId});
  }
  showRoleModal = (roleId: number) => {
    this.setState({roleModalVisible: true});
  }

  handleRoleOk = () => {
    this.setState({roleModalVisible: false, roleDetail:{}});
  }

  handleRoleCancel = () => {
    this.setState({roleModalVisible: false, roleDetail:{}});
  }

  onRoleFinish = async (values) =>{
    console.log(values);
    let result = {};
    if (this.state.roleDetail && this.state.roleDetail.id) {
      result = await updateRole(this.state.roleDetail.id, values);
    } else {
      result = await addRole(values);
    }
    if (result.code === 0){
      message.success('Successfully saved');
      this.setState({roleDetail:{}, roleModalVisible:false})
      this.fetchRoleData({});
    } else {
      message.error(`Failed to save:${result.msg}`)
    }
  }

  delRole = async(roldId) => {
    const result = await delRoleRequest(roldId);
    if (result.code === 0 ) {
      message.success('Delete role succeeded');
      this.fetchRoleData({});
    }
    else{
      message.error(result.msg);
    }

  }

  handleRoleUserOk = () => {
    this.setState({roleUserModalVisible: false})
  }

  handleRoleUserCancel = () => {
    this.setState({roleUserModalVisible: false})
  }


  getRoleDetailField = (fieldName:string) =>{
    if(this.state && this.state.roleDetail){
      return this.state.roleDetail[fieldName]
    }
    return ''
  }

  render() {
    const columns = [
      {
        title: "name",
        dataIndex: "name",
        key: "name"
      },
      {
        title: "description",
        dataIndex: "description",
        key: "description"
      },
      {
        title: "label",
        dataIndex: "label",
        key: "label"
      },
      {
        title: "creator_info",
        dataIndex: ["creator_info", "creator_alias"],
        key: "creator_info",
      },
      {
        title: "gmt_created",
        dataIndex: "gmt_created",
        key: "gmt_created"
      },
      {
        title: "操作",
        key: "action",
        render: (text: string, record: any) => (
          <span>
            <a style={{marginRight: 16}} onClick={() => this.showEditModal(record)}>edit</a>
            <a style={{marginRight: 16}} onClick={() => this.showRoleUserModal(record.id)}>Manage role users</a>
            <a style={{marginRight: 16, color: "red"}}>
              <Popconfirm
                title="Are you sure to delete?"
                onConfirm={()=>{this.delRole(record.id)}}
              >
                delete
              </Popconfirm>
            </a>
          </span>
        )
      },
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
            onFinish={this.searchRole}
          >
            <Row gutter={24}>
              <Col span={6} key={"search_value"}>
                <Form.Item
                  name={"search_value"}
                  label={"search_value"}
                >
                  <Input placeholder="Support role name fuzzy query" />
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
                <Button type="primary" onClick={()=>this.showRoleModal(0)}>
                  new
                </Button>
              </Col>
            </Row>
          </Form>
          <Table
            loading={this.state.roleListLoading}
            columns={columns}
            dataSource={this.state.roleListResult}
            rowKey={record=>record.id}
            pagination={this.state.pagination}
          />
        </Card>
        <Modal
          title="Role"
          visible={this.state.roleModalVisible}
          onOk={this.handleRoleOk}
          onCancel={this.handleRoleCancel}
          width={800}
          footer={null}
          destroyOnClose
        >
          <Form
            {...layout}
            onFinish={this.onRoleFinish}
          >
            <Form.Item name="name" label="character name" rules={[{ required: true }]} initialValue={this.getRoleDetailField('name')}>
              <Input />
            </Form.Item>
            <Form.Item name="description" label="description" initialValue={this.getRoleDetailField('description')}>
              <Input />
            </Form.Item>
            <Form.Item name="label" label="Label" initialValue={this.getRoleDetailField('label')}>
              <Input />
            </Form.Item>
            <Form.Item {...tailLayout}>
              <Button type="primary" htmlType="submit">
                Submit
              </Button>
            </Form.Item>

          </Form>
        </Modal>
        <Modal
          title="role user"
          visible={this.state.roleUserModalVisible}
          onOk={this.handleRoleUserOk}
          onCancel={this.handleRoleUserCancel}
          width={800}
          footer={null}
          destroyOnClose
        >
          <RoleUserList roleId={this.state.roleIdForRoleUser}/>
        </Modal>
      </div>



    )
  }


}

export default RoleList;
