import React, { Component } from "react";
import {Table, Form, Card} from "antd";


class WorkflowDetail extends Component<any, any> {
  constructor(props) {
    super(props);
    this.state = {
      workflowDetailResult: {},

    }
  }

  componentDidMount() {
    console.log(this.props.location);
    let workflow_id = new URLSearchParams(this.props.location.search).get('workflow_id');
    console.log(workflow_id);
  }

  render() {
    return (
      <Card>
        哈哈
      </Card>
    )

  }

}

export default WorkflowDetail;
