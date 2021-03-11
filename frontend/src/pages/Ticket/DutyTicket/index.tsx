import React, {Component} from "react";
import TicketList from "@/pages/Ticket/TicketList";
import {Card} from "antd";

class DutyTicket extends Component<any, any> {
  constructor(props) {
    super(props);
  }


   render() {


    return (
      <Card>
        <TicketList category={'duty'}/>
      </Card>
    )
  }
}

export default DutyTicket;
