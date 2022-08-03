import React, {useEffect, useState} from 'react';
import { Steps } from 'antd';
import {getTicketFlowLogRequest} from "@/services/ticket";

const { Step } = Steps;

export interface TicketLogType {
  ticketId: number
}

const TicketLog = (props: TicketLogType) => {

  const [flowLogData, setFlogData] = useState([]);


  useEffect(()=>{
    fetchTicketLogData();
  },[props.ticketId])

  const fetchTicketLogData = async() => {
    const result = await getTicketFlowLogRequest(props.ticketId);
    if (result.code === 0) {
      setFlogData(result.data.value);
    }
  }

  return <Steps direction="vertical" size="small" current={0}>

    {flowLogData.map(item => (
      <Step key={item.id} title={item.participant_info.participant_alias} description={`At ${item.gmt_created} exist "${item.state.state_name}" state, executed "${item.transition.transition_name}", view: ${item.suggestion}`} />
    ))}

  </Steps>

}

export default TicketLog;
