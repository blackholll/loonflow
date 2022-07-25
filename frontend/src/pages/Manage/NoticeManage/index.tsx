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
      message.success('successfully deleted');
      this.fetchNoticeData();
    } else {
      message.error(`failed to delete: ${result.msg}`);

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
        title: "name",
        dataIndex: "name",
        key: "name",
      },
      {
        title: "type",
        key: "type_id",
        render: (text: any, record: any) => {
          if (record.type_id === 1) {
            return "hook";
          } else if (record.type_id === 2) {
            return "Enterprise WeChat message";
          } else if (record.type_id === 3) {
            return "Dingding news";
          }
        }
      },
      {
        title: "description",
        dataIndex: "description",
        key: "description",
      },
      {
        title: "creator",
        dataIndex: "creator",
        key: "creator",
      },
      {
        title: "gmt_created",
        dataIndex: "gmt_created",
        key: "gmt_created",
      },
      {
        title: "action",
        key: "action",
        render: (text: string, record: any) => (
          <span>
            <a style={{marginRight: 16}} onClick={ ()=>this.showNoticeDetail(record.id)}>edit</a>
            <Popconfirm
              title="Are you sure you want to delete this notification record? Please confirm that no workflow is using this notification before deleting"
              onConfirm={()=>this.deleteConfirm(record.id)}
              okText="Yes"
              cancelText="No"
            >
              <a href="#" style={{color: "red"}}>delete</a>
            </Popconfirm>
          </span>
        )
      }

    ]
    const openNoticeId = this.state.openNoticeId;
    return (
      <div>
        <Button onClick={()=>this.showNoticeDetail(0)} type="primary" style={{ marginBottom: 16 }}>
          new
        </Button>
        <Table loading={this.state.noticeListLoading} columns={columns} dataSource={this.state.NoticeList}
               rowKey={record => record.id}/>

        <Modal
          title="Customize notifications"
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
