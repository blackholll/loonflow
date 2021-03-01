import React, { useEffect, useState } from "react";
import { Steps } from 'antd';
import {getTicketStepRequest} from "@/services/ticket";

const { Step } = Steps;

export interface TicketStepType {
  ticketId: number
}

const TicketStep = (props: TicketStepType) => {
  const [stepData, setStepData] = useState([]);
  const [currentState, setCurrentState] = useState(0);

  useEffect (() => {
    fetchTicketStepData();
  }, [props.ticketId])

  const fetchTicketStepData = async() => {
    const result = await getTicketStepRequest(props.ticketId);
    if (result.code === 0){
      setStepData(result.data.value);
      setCurrentState(result.data.current_state_id)
    }
  }

  return (
    <div style={{ margin: '0 40px', overflowX: 'scroll' }}>
      <Steps size="small">
        {stepData.map(item => {
          const title = item.state_name;
          let description = "";
          let status = 'wait'
          if (item.state_flow_log_list[0]) {
            const user = item.state_flow_log_list[0].participant_info.participant_alias
            description = `${user} ${item.state_flow_log_list[0].transition.transition_name} @ ${item.state_flow_log_list[0].gmt_created}`
            status = 'finish'
          } else {
            status = 'wait'
          }
          if (item.state_id === currentState) {
            status = 'process'
          }
          return (
            <Step key={item.state_id} status={status} title={title} description={description}/>
          )
        })}
      </Steps>
    </div>
  )

}

export default TicketStep;
