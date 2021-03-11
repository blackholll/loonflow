import React, {Component} from "react";
import TicketList from "@/pages/Ticket/TicketList";
import {Card} from "antd";

class AllTicket extends Component<any, any> {
  constructor(props) {
    super(props);
  }


   render() {


    return (
      <Card>
        <TicketList category={'all'}/>
      </Card>
    )
  }
}

export default AllTicket;
