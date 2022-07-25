import React, { Component } from "react";
import {Table, Col, Form, Input, Card, Row, Button, Modal, Select, Radio, message, Popconfirm} from "antd";
import {addDeptRequest, delDeptRequest, getDeptList, queryUserSimple, updateDeptRequest} from "@/services/user";


const { Option } = Select;

class DeptList extends Component<any, any> {
  constructor(props) {
    super();
    this.state = {
      deptResult: [],
      deptDetail: {},
      deptResultLoading: false,
      deptModalVisible: false,
      searchLeaderResult: [],
      searchApproverResult: [],
      pagination: {
        current: 1,
        total: 0,
        pageSize: 10,
        onChange: (current) => {
          const pagination = { ...this.state.pagination };
          pagination.page = current;
          pagination.current = current;
          this.setState({ pagination }, () => {
            this.fetchDeptData({
              page: pagination.page,
              per_page: pagination.pageSize
            })
          });
        }
      }
    }
  }

  componentDidMount() {
    this.fetchDeptData({per_page:10, page:1});
  }

  fetchDeptData = async(params: object) => {
    this.setState({deptResultLoading: true})
    const result = await getDeptList(params);
    if (result.code === 0 ){
      const pagination = { ...this.state.pagination };
      pagination.page = result.data.page;
      pagination.pageSize = result.data.per_page;
      pagination.total = result.data.total;


      this.setState({deptResult: result.data.value, deptResultLoading:false, pagination})
    } else {
      message.error(`获取部门列表失败: ${result.msg}`)
    }

  }

  searchDept = (values) => {
    this.fetchDeptData({...values, per_page:10, page:10})
  }

  showDeptModal = (record: any) => {
    this.setState({
      deptDetail: record,
      deptModalVisible: true,

    })
  }

  getDeptDetailField = (fieldName:string) =>{
    if(this.state && this.state.deptDetail && this.state.deptDetail[fieldName]){
      if (fieldName === 'approver') {
        return this.state.deptDetail[fieldName].split(',');
      }
      return this.state.deptDetail[fieldName]
    }
    return ''
  }

  delDept = async(deptId) => {
    const result = await delDeptRequest(deptId);
    if (result.code ===0 ) {
      message.success('删除成功');
      this.fetchDeptData({});
    } else {
      message.error(`删除失败: ${result.msg}`)
    }
  }

  onDeptFinish = async(values: any) => {
    let result = {};
    values.parent_dept_id = Number(values.parent_dept_id);
    values.approver = values.approver? values.approver.join(','): "";
    if (this.state.deptDetail && this.state.deptDetail.id) {
      result = await updateDeptRequest(this.state.deptDetail.id, values);
    } else {
      result = await addDeptRequest(values);
    }
    if (result.code === 0) {
      message.success('保存成功');
      this.setState({deptModalVisible: false, deptDetail: {}});
      this.fetchDeptData({});
    } else {
      message.error(`保存失败: ${result.msg}`);
    }
  }

  handleDeptOk = () =>{
    this.setState({
      deptModalVisible: false
    })
  }

  handleDeptCancel = () =>{
    this.setState({
      deptModalVisible: false
    })
  }

  searchLeader = async(search_value: string) => {
    const result = await queryUserSimple({search_value:search_value});
    if (result.code ===0 ) {
      this.setState({searchLeaderResult: result.data.value});
    }
  }

  searchApprover = async(search_value: string) => {
    const result = await queryUserSimple({search_value:search_value});
    if (result.code ===0 ) {
      this.setState({searchApproverResult: result.data.value});
    }
  }


  render(){
    const columns = [
      {
        title: "名称",
        dataIndex: "name",
        key: "name"
      },
      {
        title: "上级部门",
        dataIndex: ["parent_dept_info", "parent_dept_name"],
        key: "parent_dept"
      },
      {
        title: "部门负责人",
        key: "leader",
        render:(text: string, record: any)=>{
          return record.leader_info?record.leader_info.leader_alias: record.leader;
        }
      },
      {
        title: "部门审批人",
        // dataIndex: "approver",
        key: "approver",
        render:(text: string, record:any)=>{
          let approver_info_list = [];
          record.approver_info.forEach(approver0=>{
            approver_info_list.push(approver0.approver_alias);
          })
          return approver_info_list.join();
        }
      },
      {
        title: "label",
        dataIndex: "label",
        key: "label"
      },
      {
        title: "creator",
        dataIndex: ["creator_info", "creator_alias"],
        key: "creator"
      },
      {
        title: "gmt_created",
        dataIndex: "gmt_created",
        key: "gmt_created"
      },
      {
        title: "action",
        key: "action",
        render: (text: string, record: any) => (
          <span>
            <a style={{marginRight: 16}} onClick={() => this.showDeptModal(record)}>edit</a>
            <a style={{marginRight: 16, color: "red"}}>
              <Popconfirm
                title="Are you sure to delete?"
                onConfirm={()=>{this.delDept(record.id)}}
              >
                Delete
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
            onFinish={this.searchDept}
          >
            <Row gutter={24}>
              <Col span={6} key={"search_value"}>
                <Form.Item
                  name={"search_value"}
                  label={"Inquire"}
                >
                  <Input placeholder="Support department name fuzzy query" />
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
                <Button type="primary" onClick={()=>this.showDeptModal(0)}>
                  New
                </Button>
              </Col>
            </Row>
          </Form>
          <Table loading={this.state.deptListLoading} columns={columns} dataSource={this.state.deptResult}
                 rowKey={record => record.id} pagination={this.state.pagination}/>
        </Card>
        <Modal
          title="department"
          visible={this.state.deptModalVisible}
          onOk={this.handleDeptOk}
          onCancel={this.handleDeptCancel}
          width={800}
          footer={null}
          destroyOnClose
        >
          <Form
            {...layout}
            onFinish={this.onDeptFinish}
          >
            <Form.Item name="name" label="name" rules={[{ required: true }]} initialValue={this.getDeptDetailField('name')}>
              <Input />
            </Form.Item>
            <Form.Item name="parent_dept_id" label="Higher office" initialValue={String(this.getDeptDetailField('parent_dept_id'))}>
              <Select
                allowClear
                showSearch
                style={{ width: '100%' }}
                placeholder="Please select a superior department"
              >
              {this.state.deptResult.map(d => (
                <Option key={d.id}>{d.name}</Option>
              ))}
              </Select>
            </Form.Item>
            <Form.Item name="leader" label="leader" initialValue={this.getDeptDetailField('leader')}>
              <Select
                allowClear
                showSearch
                style={{ width: '100%' }}
                placeholder="Please select a department head"
                onSearch = {this.searchLeader}
              >
                {this.state.searchLeaderResult.map(d => (
                  <Option key={d.username}>{`${d.alias}(${d.username})`}</Option>
                ))}
              </Select>
            </Form.Item>
            { this.getDeptDetailField('approver')?
              <Form.Item name="approver" label="approver" initialValue={this.getDeptDetailField('approver')}>
                <Select
                  mode="multiple"
                  allowClear
                  style={{ width: '100%' }}
                  placeholder="Please select an approver"
                  onSearch = {this.searchApprover}

                >
                  {this.state.searchApproverResult.map(d => (
                    <Option key={d.username}>{`${d.alias}(${d.username})`}</Option>
                  ))}
                </Select>
              </Form.Item>:
              <Form.Item name="approver" label="approver" >
                <Select
                  mode="multiple"
                  allowClear
                  style={{ width: '100%' }}
                  placeholder="Please select an approver"
                  onSearch = {this.searchApprover}

                >
                  {this.state.searchApproverResult.map(d => (
                    <Option key={d.username}>{`${d.alias}(${d.username})`}</Option>
                  ))}
                </Select>
              </Form.Item>

            }

            <Form.Item name="label" label="label" initialValue={this.getDeptDetailField('label')}>
              <Input />
            </Form.Item>
            <Form.Item {...tailLayout}>
              <Button type="primary" htmlType="submit">
                Sure
              </Button>
            </Form.Item>

          </Form>
        </Modal>

      </div>

    )
  }


}

export default DeptList;
