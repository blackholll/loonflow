import React, {Component} from "react";
import TicketList from "@/pages/ticket/TicketList";
import {Card} from "antd";

class OwnerTicket extends Component<any, any> {
  constructor(props) {
    super(props);
  }


   render() {


    return (
      <Card>
        <TicketList category={'owner'}/>
      </Card>
    )
  }
}

export default OwnerTicket;
