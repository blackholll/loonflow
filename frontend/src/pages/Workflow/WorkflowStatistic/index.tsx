import React, {useState, Fragment, useEffect} from "react";
import { Line } from '@ant-design/charts';
import {Button, Col, Form, Input, Row, DatePicker, message} from "antd";
import moment from 'moment';
import {workflowStatisticsRequest} from "@/services/workflows";


const { RangePicker } = DatePicker;


const WorkflowStatistic: React.FC =(props) => {
  const [ticketCountData, setTicketCountData] = useState([])
  const [queryTime, setQueryTime] = useState([])

  useEffect( () => {
    const defaultStart= moment(new Date()).subtract(1,'months');
    const defaultEnd = moment(new Date());
    fetchNewData([defaultStart.format("YYYY-MM-DD HH:mm"), defaultEnd.format("YYYY-MM-DD HH:mm")])
  }, [props.workflowId])


  const onOk = async(values) => {
    setQueryTime([values[0].format("YYYY-MM-DD HH:mm"), values[1].format("YYYY-MM-DD HH:mm")])
    fetchNewData(queryTime);
  }

  const fetchNewData = async (values) => {
    const result = await workflowStatisticsRequest(props.workflowId, {start_time: values[0], end_time:values[1]})
    if (result.code === 0) {
      setTicketCountData(result.data.result_list)
    }
    else {
      message.error(`获取数据失败: %{result.msg}`)
    }

  }


  const data = [
    { day: '1991', count: 3 },
    { day: '1992', count: 4 },
    { day: '1993', count: 3.5 },
    { day: '1994', count: 5 },
    { day: '1995', count: 4.9 },
    { day: '1996', count: 6 },
    { day: '1997', count: 7 },
    { day: '1998', count: 9 },
    { day: '1999', count: 13 },
  ];
  const config = {
    // data,
    data: ticketCountData,
    height: 400,
    xField: 'day',
    yField: 'count',
    name: '工单数量',
    point: {
      size: 5,
      shape: 'diamond',
    },
  };

  const defaultStart= moment(new Date()).subtract(1,'months');
  const defaultEnd = moment(new Date());

  return (
    <div>
      <Row>
        <RangePicker
          showTime={{ format: 'HH:mm' }}
          format="YYYY-MM-DD HH:mm"
          onOk={onOk}
          defaultValue={[defaultStart, defaultEnd]}
        />
      </Row>
      {ticketCountData.length?
        <Line {...config} />: null
      }
    </div>
  )

}

export default WorkflowStatistic;
