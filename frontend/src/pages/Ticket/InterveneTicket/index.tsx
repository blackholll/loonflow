import React, {Component} from "react";
import TicketList from "@/pages/Ticket/TicketList";
import {Card} from "antd";

class InterveneTicket extends Component<any, any> {
  constructor(props) {
    super(props);
  }


   render() {


    return (
      <Card>
        <TicketList category={'intervene'}/>
      </Card>
    )
  }
}

export default InterveneTicket;
