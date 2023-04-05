import React, { Component } from "react";
import { Link } from 'umi';
import {Table, Form, Modal, Popconfirm, Card, Row, Col, Input, Button, message} from "antd";
import {delWorkflow, getWorkflowList} from "@/services/workflows";


class WorkflowList extends Component<any, any> {
  constructor(props) {
    super(props);
    this.state = {
      workflowListResult : [],
      workflowListLoading: false,
      workflowModalVisible: false,
      pagination: {
        current: 1,
        total: 0,
        pageSize: 10,
        onChange: (current) => {
          const pagination = { ...this.state.pagination };
          pagination.current = current;
          this.setState( { pagination }, ()=> {
            this.fetchWorkflowData({
              page: pagination.current,
              per_page: pagination.pageSize
            })
          });
        }
      }
    }
  }

  componentDidMount() {
    this.fetchWorkflowData({per_page:10, page:1});
  }

  searchWorkflow = async(values) => {
    const result = await getWorkflowList({...values, per_page:10, page:1, from_admin:1});
    if (result.code ===0 ){
      this.setState({workflowListResult: result.data.value});
    } else
    {
      message.error(`获取工作流列表失败: ${result.msg}`)
    }
  }

  fetchWorkflowData = async(params: object) => {
    params.from_admin=1
    this.setState({
      workflowListLoading: true
    });
    const result = await getWorkflowList( params);
    const pagination = { ...this.state.pagination };
    pagination.current = result.data.page;
    pagination.pageSize = result.data.per_page;
    pagination.total = result.data.total;


    if (result.code ===0 ){
      this.setState({
        workflowListLoading: false,
        workflowListResult: result.data.value,
        pagination: pagination
      })
    } else {
      message.error(`获取工作流列表失败: ${result.msg}`)
    }
  }


  delWorkflowRequest = async(workflowId: number) => {
    const result = await delWorkflow(workflowId);
    if (result.code === 0 ){
      message.success('删除工作流成功');
      this.fetchWorkflowData({});
    }

  }

  render() {
    const columns = [
      {
        title: "名称",
        dataIndex: "name",
        key: "name"
      },
      {
        title: "描述",
        dataIndex: "description",
        key: "description"
      },
      {
        title: "工单查看权限校验",
        dataIndex: "view_permission_check",
        key: "view_permission_check",
        render: (text:boolean, record: any) => {
          if (text) {
            return "是"
          } else {
            return "否"
          }

        }

      },
      {
        title: "创建人",
        dataIndex: "creator",
        key: "creator"
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
            <Link to={ `/workflows/detail?workflow_id=${record.id}`}>详情</Link>
            |
            <a style={{marginRight: 16, color: "red"}}>
              <Popconfirm
                title="确认删除么"
                onConfirm={()=>{this.delWorkflowRequest(record.id)}}
              >
                删除
              </Popconfirm>
            </a>
          </span>
        )
      }

    ]
    return (
      <Card>
        <Form
          name="advanced_search"
          className="ant-advanced-search-form"
          onFinish={this.searchWorkflow}
        >
          <Row gutter={24}>
            <Col span={6} key={"search_value"}>
              <Form.Item
                name={"search_value"}
                label={"查询"}
              >
                <Input placeholder="支持工作流名模糊查询" />
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
              {/*<Button type="primary" onClick={()=> window.location.href = '/workflows/detail'*/}
              {/*}>*/}
              {/*  新增*/}
              {/*</Button>*/}

              <Link to={ '/workflows/detail'}>
                <Button type="primary" >
                新增
                </Button>
              </Link>
            </Col>
          </Row>
        </Form>
        <Table
          loading={this.state.workflowListLoading}
          columns={columns}
          dataSource={this.state.workflowListResult}
          rowKey={record=>record.id}
          pagination={this.state.pagination}
        />
      </Card>

    )
  }

}

export default WorkflowList;
