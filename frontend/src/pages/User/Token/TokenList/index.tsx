import React, { Component } from "react";
import {Table, Col, Popconfirm, Card, Form, Row, Input, Button, Select, Modal, message} from "antd";
import {addTokenRequest, delTokenRequest, getTokenListRequest, updateTokenRequest} from "@/services/user";
import {getWorkflowList} from "@/services/workflows";

const { Option } = Select;

class TokenList extends Component<any, any> {
  constructor(props) {
    super();
    this.state = {
      tokenResult: [],
      tokenDetail: {},
      workflowResult: [],
      tokenResultLoading: false,
      tokenModalVisible: false,
      pagination: {
        current: 1,
        total: 0,
        pageSize: 10,
        onChange: (current) => {
          const pagination = {...this.state.pagination};
          pagination.page = current;
          pagination.current = current;
          this.setState({pagination}, () => {
            this.fetchTokenList({
              page: pagination.page,
              per_page: pagination.pageSize
            })
          });
        }
      }

    }
  }

  componentDidMount() {
    this.fetchTokenList({per_page:10, page:1});
    this.fetchWorkflowList({per_page:1000, page:1});
  }

  fetchTokenList = async(params: any) => {
    this.setState({tokenResultLoading: true});
    const result = await getTokenListRequest(params);
    if (result.code === 0) {
      const pagination = { ...this.state.pagination };
      pagination.page = result.data.page;
      pagination.pageSize = result.data.per_page;
      pagination.total = result.data.total;
      pagination.current = result.data.page;

      this.setState({tokenResultLoading: false, tokenResult: result.data.value, pagination})
    }
  }

  fetchWorkflowList = async(params: any) => {
    const result = await getWorkflowList(params);
    console.log(result);
    if (result.code === 0 ) {
      this.setState({workflowResult: result.data.value}, ()=> console.log(this.state.workflowResult))
    }
  }

  searchToken = (values: any) => {
    this.fetchTokenList({...values, per_page:10, page:1});
  }

  showTokenModal = (record: any)=> {
    if (record !== 0 ) {
      this.setState({tokenModalVisible: true, tokenDetail: record})
    } else {
      this.setState({tokenModalVisible: true})
    }
  }

  handleTokenOk = () => {
    this.setState({tokenModalVisible: false, tokenDetail: {}})
  }

  handleTokenCancel = () => {
    this.setState({tokenModalVisible: false, tokenDetail: {}})
  }

  onTokenFinish = async(values) => {
    let result = {};

    values.workflow_ids = values.workflow_ids? values.workflow_ids.join(','): '';
    if (this.state.tokenDetail && this.state.tokenDetail.id ) {
      result = await updateTokenRequest(this.state.tokenDetail.id, values);
    } else {
      result = await addTokenRequest(values);
    }
    if (result.code === 0) {
      message.success('保存成功');
      this.setState({tokenModalVisible: false, tokenDetail: {}});
      this.fetchTokenList({per_page:10, page:1});
    } else {
      message.error(`保存失败:${result.msg}`)
    }
  }


  getTokenDetailField = (fieldName:string) =>{
    if(this.state && this.state.tokenDetail && this.state.tokenDetail[fieldName]){
      if (fieldName === 'workflow_ids') {
        return this.state.tokenDetail[fieldName].split(',');
      } else {
        return this.state.tokenDetail[fieldName]
      }
    }
    return ''
  }

  delToken = async(tokenId: number) => {
    const result = await delTokenRequest(tokenId);
    if (result.code ===0 ) {
      message.success('删除成功');
      this.fetchTokenList({per_page:10, page:1});
    } else {
      message.error(`删除失败:${result.msg}`)
    }

  }

  render() {
    const columns = [
      {
        title: "调用应用名",
        dataIndex: "app_name",
        key: "app_name"
      },
      {
        title: "token",
        dataIndex: "token",
        key: "token"
      },
      {
        title: "工单前缀",
        dataIndex: "ticket_sn_prefix",
        key: "ticket_sn_prefix"
      },
      {
        title: "工作流权限",
        dataIndex: "workflow_ids",
        key: "workflow_ids"
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
            <a style={{marginRight: 16}} onClick={() => this.showTokenModal(record)}>编辑</a>
            <a style={{marginRight: 16, color: "red"}}>
              <Popconfirm
                title="确认删除么"
                onConfirm={()=>{this.delToken(record.id)}}
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
      <Card>
        <Form
          name="advanced_search"
          className="ant-advanced-search-form"
          onFinish={this.searchToken}
        >
          <Row gutter={24}>
            <Col span={6} key={"search_value"}>
              <Form.Item
                name={"search_value"}
                label={"查询"}
              >
                <Input placeholder="支持部门名称模糊查询" />
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
              <Button type="primary" onClick={()=>this.showTokenModal(0)}>
                新增
              </Button>
            </Col>
          </Row>
        </Form>
        <Table loading={this.state.tokenResultLoading} columns={columns} dataSource={this.state.tokenResult}
               rowKey={record => record.id} pagination={this.state.pagination}/>

        <Modal
          title={this.state.tokenDetail.app_name? `调用权限:${this.state.tokenDetail.app_name}`: '调用权限'}
          visible={this.state.tokenModalVisible}
          onOk={this.handleTokenOk}
          onCancel={this.handleTokenCancel}
          width={800}
          footer={null}
          destroyOnClose
        >
          <Form
            {...layout}
            onFinish={this.onTokenFinish}
          >
            {this.state.tokenDetail && this.state.tokenDetail.id ? null :
              <Form.Item name="app_name" label="调用应用" rules={[{required: true}]}
                         initialValue={this.getTokenDetailField('app_name')}>
                <Input/>
              </Form.Item>
            }
            <Form.Item name="ticket_sn_prefix" label="工单前缀" initialValue={String(this.getTokenDetailField('ticket_sn_prefix'))}>
              <Input />
            </Form.Item>
            {/*<Form.Item name="workflow_ids" label="工作流权限" initialValue={this.getTokenDetailField('workflow_ids') ? this.getTokenDetailField('workflow_ids') : null}>*/}

            {this.getTokenDetailField('workflow_ids') ?
              <Form.Item name="workflow_ids" label="工作流权限" initialValue={this.getTokenDetailField('workflow_ids') ? this.getTokenDetailField('workflow_ids') : null}>
              <Select
                allowClear
                showSearch
                mode="multiple"
                style={{ width: '100%' }}
                placeholder="请选择授予的工作流权限"
              >
                {this.state.workflowResult.map(d => (
                  <Option key={d.id}>{`${d.name}`}</Option>
                ))}
              </Select>
            </Form.Item>:
              <Form.Item name="workflow_ids" label="工作流权限" >
                <Select
                  allowClear
                  showSearch
                  mode="multiple"
                  style={{ width: '100%' }}
                  placeholder="请选择授予的工作流权限"
                >
                  {this.state.workflowResult.map(d => (
                    <Option key={d.id}>{`${d.name}`}</Option>
                  ))}
                </Select>
              </Form.Item>
            }
            <Form.Item {...tailLayout}>
              <Button type="primary" htmlType="submit">
                确定
              </Button>
            </Form.Item>

          </Form>
        </Modal>
      </Card>

    )
  }
}

export default TokenList;
