import React, { Component } from "react";
import {Table, Col, Form, Input, Card, Row, Button, Modal, Select, Radio, message, Popconfirm} from "antd";
import {addDeptRequest, delDeptRequest, getDeptList, queryUserSimple, updateDeptRequest} from "@/services/user";


const { Option } = Select;

class DeptList extends Component<any, any> {
  constructor(props) {
    super();
    this.state = {
      deptResult: [],
      allDeptResult: [],
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
    this.fetchAlldeptData();
  }
  
  fetchAlldeptData = async() => {
    const allResult = await getDeptList({per_page: 10000, page:1});
    if (allResult.code === 0) {
      this.setState({allDeptResult: allResult.data.value});
    } else {
      message.error(`获取全部部门列表失败: ${allResult.msg}`);
    }
  }

  fetchDeptData = async(params: object) => {
    this.setState({deptResultLoading: true})
    const result = await getDeptList(params);
    if (result.code === 0 ){
      const pagination = { ...this.state.pagination };
      pagination.current = result.data.page;
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
      this.fetchAlldeptData();
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
      this.fetchAlldeptData();
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
        title: "标签",
        dataIndex: "label",
        key: "label"
      },
      {
        title: "创建人",
        dataIndex: ["creator_info", "creator_alias"],
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
            <a style={{marginRight: 16}} onClick={() => this.showDeptModal(record)}>编辑</a>
            <a style={{marginRight: 16, color: "red"}}>
              <Popconfirm
                title="确认删除么"
                onConfirm={()=>{this.delDept(record.id)}}
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
            onFinish={this.searchDept}
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
                <Button type="primary" onClick={()=>this.showDeptModal(0)}>
                  新增
                </Button>
              </Col>
            </Row>
          </Form>
          <Table loading={this.state.deptListLoading} columns={columns} dataSource={this.state.deptResult}
                 rowKey={record => record.id} pagination={this.state.pagination}/>
        </Card>
        <Modal
          title="部门"
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
            <Form.Item name="name" label="名称" rules={[{ required: true }]} initialValue={this.getDeptDetailField('name')}>
              <Input />
            </Form.Item>
            <Form.Item name="parent_dept_id" label="上级部门" initialValue={String(this.getDeptDetailField('parent_dept_id'))}>
              <Select
                allowClear
                showSearch
                style={{ width: '100%' }}
                placeholder="请选择上级部门"
              >
              {this.state.allDeptResult.map(d => (
                <Option key={d.id}>{d.name}</Option>
              ))}
              </Select>
            </Form.Item>
            <Form.Item name="leader" label="负责人" initialValue={this.getDeptDetailField('leader')}>
              <Select
                allowClear
                showSearch
                style={{ width: '100%' }}
                placeholder="请选择部门负责人"
                onSearch = {this.searchLeader}
              >
                {this.state.searchLeaderResult.map(d => (
                  <Option key={d.username}>{`${d.alias}(${d.username})`}</Option>
                ))}
              </Select>
            </Form.Item>
            { this.getDeptDetailField('approver')?
              <Form.Item name="approver" label="审批人" initialValue={this.getDeptDetailField('approver')}>
                <Select
                  mode="multiple"
                  allowClear
                  style={{ width: '100%' }}
                  placeholder="请选择审批人"
                  onSearch = {this.searchApprover}

                >
                  {this.state.searchApproverResult.map(d => (
                    <Option key={d.username}>{`${d.alias}(${d.username})`}</Option>
                  ))}
                </Select>
              </Form.Item>:
              <Form.Item name="approver" label="审批人" >
                <Select
                  mode="multiple"
                  allowClear
                  style={{ width: '100%' }}
                  placeholder="请选择审批人"
                  onSearch = {this.searchApprover}

                >
                  {this.state.searchApproverResult.map(d => (
                    <Option key={d.username}>{`${d.alias}(${d.username})`}</Option>
                  ))}
                </Select>
              </Form.Item>

            }

            <Form.Item name="label" label="标签" initialValue={this.getDeptDetailField('label')}>
              <Input />
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

export default DeptList;
