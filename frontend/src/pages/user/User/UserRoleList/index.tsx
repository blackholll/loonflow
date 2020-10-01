import React, { Component } from "react";
import { Table, message } from "antd";
import {getUserRole} from "@/services/user";


class UserRoleList extends Component<any, any> {
  constructor(props) {
    super();
    this.state = {
      userRoleResult: [],
      pagination: {
        current: 1,
        total: 0,
        pageSize: 10,
        onChange: (current) => {
          const pagination = { ...this.state.pagination };
          pagination.current = current;
          this.setState({pagination}, ()=>{
            // get data
          })
        }
      }
    }
  }

  componentDidMount() {
    // get data
    this.fetchUserRole({});
  }

  fetchUserRole = async (params: any) => {
    const result = await getUserRole(this.props.userId, params)
    if (result.code ===0) {
      this.setState({userRoleResult: result.data.value})
    }
    else {
      message.error(`获取用户角色信息失败: ${result.message}`)
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
        title: "角色名",
        dataIndex: "name",
        key: "name"
      },
    ]

    return (
      <Table
        loading={this.state.userRoleLoadin}
        columns={columns}
        dataSource={this.state.userRoleResult}
        rowKey={record=>record.id}
        pagination={this.state.pagination}
      />
    )
  }


}

export default UserRoleList
