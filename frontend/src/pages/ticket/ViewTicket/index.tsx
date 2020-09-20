import React, {Component} from "react";
import TicketList from "@/pages/ticket/TicketList";
import {Card} from "antd";

class ViewTicket extends Component<any, any> {
  constructor(props) {
    super(props);
  }


   render() {


    return (
      <Card>
        <TicketList category={'view'}/>
      </Card>
    )
  }
}

export default ViewTicket;
