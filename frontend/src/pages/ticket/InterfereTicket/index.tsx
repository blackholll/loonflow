import React, {Component} from "react";
import TicketList from "@/pages/ticket/TicketList";
import {Card} from "antd";

class InterfereTicket extends Component<any, any> {
  constructor(props) {
    super(props);
  }


   render() {


    return (
      <Card>
        <TicketList category={'interfere'}/>
      </Card>
    )
  }
}

export default InterfereTicket;
