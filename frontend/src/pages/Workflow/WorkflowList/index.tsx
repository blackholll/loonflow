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
      message.error(`Failed to get workflow list: ${result.msg}`)
    }
  }

  fetchWorkflowData = async(params: object) => {
    params.from_admin=1
    this.setState({
      workflowListLoading: true
    });
    const result = await getWorkflowList( params);
    const pagination = { ...this.state.pagination };
    pagination.page = result.data.page;
    pagination.pageSize = result.data.per_page;
    pagination.total = result.data.total;


    if (result.code ===0 ){
      this.setState({
        workflowListLoading: false,
        workflowListResult: result.data.value,
        pagination: pagination
      })
    } else {
      message.error(`Failed to get workflow list: ${result.msg}`)
    }
  }


  delWorkflowRequest = async(workflowId: number) => {
    const result = await delWorkflow(workflowId);
    if (result.code === 0 ){
      message.success('Delete workflow succeeded');
      this.fetchWorkflowData({});
    }

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
        title: "view_permission_check",
        dataIndex: "view_permission_check",
        key: "view_permission_check",
        render: (text:boolean, record: any) => {
          if (text) {
            return "Yes"
          } else {
            return "no"
          }

        }

      },
      {
        title: "founder",
        dataIndex: "creator",
        key: "creator"
      },
      {
        title: "creation time",
        dataIndex: "gmt_created",
        key: "gmt_created"
      },
      {
        title: "action",
        key: "action",
        render: (text: string, record: any) => (
          <span>
            <Link to={ `/workflows/detail?workflow_id=${record.id}`}>Details</Link>
            |
            <a style={{marginRight: 16, color: "red"}}>
              <Popconfirm
                title="Are you sure to delete?"
                onConfirm={()=>{this.delWorkflowRequest(record.id)}}
              >
                delete
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
                label={"search_value"}
              >
                <Input placeholder="Support workflow name fuzzy query" />
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
              {/*<Button type="primary" onClick={()=> window.location.href = '/workflows/detail'*/}
              {/*}>*/}
              {/*  new*/}
              {/*</Button>*/}

              <Link to={ '/workflows/detail'}>
                <Button type="primary" >
                new
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
