import React, { Component, Fragment, PureComponent } from "react";
import {Input, Form, Radio, Button, message} from "antd";
import { FormInstance } from 'antd/lib/form';

import {addNoticeListRequest, getNoticeDetailRequest, updateNoticeDetailRequest} from "@/services/manage";

class NoticeDetail extends PureComponent<any, any> {
  formRef = React.createRef<FormInstance>();
  constructor(props) {
    super(props);
    this.state = {
      typeId : 1,
      noticeInfo: {},
      noticeId: this.props.noticeId
    };
  }

  componentDidMount() {
    if (this.props.noticeId !== 0 ) {
      this.fetchNoticeDetailData(this.props.noticeId);
    }
  };

  static getDerivedStateFromProps(nextProps, prevState) {
    if (nextProps.noticeId !== prevState.noticeId) {
      return {
        noticeId: nextProps.noticeId
      }
    }
    return null;

  }

  componentDidUpdate(prevProps: Readonly<any>, prevState: Readonly<any>, snapshot?: any) {
    if (this.props.noticeId && this.props.noticeId !== prevProps.noticeId) {
      this.fetchNoticeDetailData(this.props.noticeId);
    }
  }

  fetchNoticeDetailData = async (noticeId) => {
    //
    const result = await getNoticeDetailRequest({noticeId:noticeId});
    if (result.code === 0) {
      console.log(result.data.value)
      this.setState({noticeInfo: result.data.value});
      // todo: set field
      let newValue = result.data.value;
      newValue.type_id = String(newValue.type_id);
      this.formRef.current.setFieldsValue(newValue);
    }
  }
  onTypeChange = (e) => {
    this.setState({
      typeId: Number(e.target.value),
    });
  }


  onFinish = async (value) => {
    value.type_id = Number(value.type_id)
    if (this.state.noticeId !== 0 ) {
      // todo: update
      const result = await updateNoticeDetailRequest(this.state.noticeId, value);
      if (result.code === 0) {
        message.success('更新成功');
        this.props.reloadList();

      } else {
        message.error(`更新失败: ${result.msg}`);
      }

    } else {
      const result = await addNoticeListRequest( value);
      if (result.code === 0) {
        message.success('新增成功');
        this.props.reloadList();

      } else {
        message.error(`新增失败:${result.msg}`);
      }
    }

  }


  render() {
    const layout = {
      labelCol: { span: 8 },
      wrapperCol: { span: 16 },
    };
    const tailLayout = {
      wrapperCol: { offset: 8, span: 16 },
    };

    return (
      <Form
        name="basic"
        onFinish={this.onFinish}
        ref={this.formRef}
        {...layout}
      >
        <Form.Item
          label="名称"
          name="name"
          rules={[{ required: true, message: 'Please input notice name!' }]}
        >
          <Input />
        </Form.Item>
        <Form.Item
          label="描述"
          name="description"
        >
          <Input />
        </Form.Item>
        <Form.Item name="type_id" label="类型"
                   rules={[{ required: true, message: 'Please select notice type!' }]}
        >
          <Radio.Group onChange={this.onTypeChange} defaultValue={String(this.state.noticeInfo.type_id)}>
            <Radio value="1">hook</Radio>
            {/*<Radio value="2">企微消息</Radio>*/}
            {/*<Radio value="3">钉钉消息</Radio>*/}
          </Radio.Group>
        </Form.Item>
        {
          this.state.typeId === 1 ?
            (
              <Fragment>
            <Form.Item
              label="hook url"
              name="hook_url"
              rules={[{ required: true, message: 'Please input hook_url!' }]}
            >
              <Input />
            </Form.Item>
            <Form.Item
              label="hook token"
              name="hook_token"
              rules={[{ required: true, message: 'Please input hook token!' }]}
            >
              <Input />
            </Form.Item></Fragment>) : null
        }
        {
          this.state.typeId === 2 ?
            (<Fragment>
              <Form.Item
                label="corpid"
                name="corpid"
                rules={[{ required: true, message: 'Please input wechat work"s corpid!' }]}
              >
                <Input />
              </Form.Item>
              <Form.Item
                label="corpsecret"
                name="corpsecret"
                rules={[{ required: true, message: 'Please input wechat work"s corpsecret!' }]}
              >
                <Input />
              </Form.Item>
            </Fragment>): null
        }
        {
          this.state.typeId === 3 ? (
            <Fragment>
              <Form.Item
                label="appkey"
                name="appkey"
                rules={[{ required: true, message: 'Please input dingtalk"s corpsecret!' }]}
              >
                <Input />
              </Form.Item>
              <Form.Item
                label="appsecret"
                name="appsecret"
                rules={[{ required: true, message: 'Please input dingtalk"s appsecret!' }]}
              >
                <Input />
              </Form.Item>
            </Fragment>
          ): null
        }
        <Form.Item {...tailLayout}>
          <Button type="primary" htmlType="submit">
            确定
          </Button>

        </Form.Item>



      </Form>
    )
    }


}

export default  NoticeDetail;
