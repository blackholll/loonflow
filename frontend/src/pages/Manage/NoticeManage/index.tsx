import React, { Component } from "react";
import {Table, Button, Modal, message, Popconfirm} from "antd";
import {delNoticeDetailRequest, getNoticeListRequest} from "@/services/manage";
import NoticeDetail from "@/pages/Manage/NoticeManage/NoticeDetail";


class NoticeRecord extends Component<any, any> {
  constructor(props) {
    super(props);
    this.state = {
      noticeListLoading: false,
      NoticeList: [],
      showNoticeModal: false,
      openNoticeId: 0,
    };
  }

  componentDidMount() {
    this.fetchNoticeData();
  };

  fetchNoticeData = async () => {
    //
    this.setState({noticeListLoading: true})
    const result = await getNoticeListRequest({per_page: 10})
    if (result.code === 0) {
      this.setState ({NoticeList: result.data.value, noticeListLoading: false})
    }

  }

  showNoticeDetail = (noticeId: number) => {
    console.log(`noticeid: ${noticeId}`)
    this.setState({
      openNoticeId: noticeId,
      showNoticeModal: true,
    })
  }

  handleOk = e => {
    this.setState({
      showNoticeModal: false,
    })
  }


  reloadList =() => {
    this.setState({
      showNoticeModal: false,
    });
    this.fetchNoticeData();

  }



  handleCancel = e => {
    this.setState({
      showNoticeModal: false,
    })
  }

  deleteConfirm = async(noticeId) =>{
    const result = await delNoticeDetailRequest({noticeId: noticeId});
    if (result.code === 0) {
      message.success('删除成功');
      this.fetchNoticeData();
    } else {
      message.error(`删除失败: ${result.msg}`);

    }

  }

  render() {
    const columns = [
      {
        title: "Id",
        dataIndex: "id",
        key: "id",
      },
      {
        title: "名称",
        dataIndex: "name",
        key: "name",
      },
      {
        title: "类型",
        key: "type_id",
        render: (text: any, record: any) => {
          if (record.type_id === 1) {
            return "hook";
          } else if (record.type_id === 2) {
            return "企业微信消息";
          } else if (record.type_id === 3) {
            return "钉钉消息";
          }
        }
      },
      {
        title: "描述",
        dataIndex: "description",
        key: "description",
      },
      {
        title: "创建人",
        dataIndex: "creator",
        key: "creator",
      },
      {
        title: "创建时间",
        dataIndex: "gmt_created",
        key: "gmt_created",
      },
      {
        title: "操作",
        key: "action",
        render: (text: string, record: any) => (
          <span>
            <a style={{marginRight: 16}} onClick={ ()=>this.showNoticeDetail(record.id)}>编辑</a>
            <Popconfirm
              title="确认删除此通知记录? 请在删除前确认没有工作流使用该通知"
              onConfirm={()=>this.deleteConfirm(record.id)}
              okText="Yes"
              cancelText="No"
            >
              <a href="#" style={{color: "red"}}>删除</a>
            </Popconfirm>
          </span>
        )
      }

    ]
    const openNoticeId = this.state.openNoticeId;
    return (
      <div>
        <Button onClick={()=>this.showNoticeDetail(0)} type="primary" style={{ marginBottom: 16 }}>
          新建
        </Button>
        <Table loading={this.state.noticeListLoading} columns={columns} dataSource={this.state.NoticeList}
               rowKey={record => record.id}/>

        <Modal
          title="自定义通知"
          visible={this.state.showNoticeModal}
          onOk={this.handleOk}
          onCancel={this.handleCancel}
          footer= {null}
          destroyOnClose
        >
          <NoticeDetail noticeId={openNoticeId} reloadList={ this.reloadList}/>
        </Modal>
      </div>
    )

  }
}

export default NoticeRecord;
