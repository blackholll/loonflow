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
      <Step key={item.id} title={item.participant_info.participant_alias} description={`于 ${item.gmt_created} 在 "${item.state.state_name}" 状态下，执行了 "${item.transition.transition_name}", 意见: ${item.suggestion}`} />
    ))}

  </Steps>

}

export default TicketLog;
