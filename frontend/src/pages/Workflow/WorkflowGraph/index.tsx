import React, { useState, useEffect, useRef } from 'react';
import { DagreGraph } from '@ant-design/charts';
import { message } from "antd";
import {getWorkflowSimpleDescription} from "@/services/workflows";

const WorkflowGraph = (props) => {

  const [data, setData] = useState({});
  const [nodeStyle, setNodeStyle] = useState();
  const [edgeStyle, setEdgeStyle] = useState();
  const [layoutCfg, setLayoutCfg] = useState();
  const [anchorPoints, setAnchorPoints] = useState();
  const [nodeType, setNodeType] = useState();
  const [minimapCfg, setMinimapCfg] = useState({
    show: true,
  });
  const [behaviors, setBehaviors] = useState(['drag-canvas', 'zoom-canvas']);
  const [nodeLabelCfg, setNodeLabelCfg] = useState();

  const ref = useRef();

  const destroyGraph = () => {
    ref.current.destroy();
  };

  const fetchGraphData = async() => {
    const result = await getWorkflowSimpleDescription(props.workflowId);
    if (result.code ===0) {
      let nodes = [];
      let edges = [];
      result.data.workflow_state_info.map(stateItem => (
          nodes.push({id: String(stateItem.id), name:stateItem.name, conf: stateItem.name, dataType: "sql", type:"rect", label:stateItem.name})
        )
      )
      result.data.workflow_transition_info.map(transitionItem => {
          if (transitionItem.condition_expression !== '[]'){
            let condition_expression_obj = JSON.parse(transitionItem.condition_expression);
            nodes.push({id: `condition_${transitionItem.id}`, name:'条件表达式', dataType:"sql", type: 'diamond', label:'条件表达式'});
            edges.push({
              source: String(transitionItem.source_state_id),
              target: `condition_${transitionItem.id}`,
              label: transitionItem.name
            });
            condition_expression_obj.map(conditionItem => {
                edges.push({source: `condition_${transitionItem.id}`,
                  target:String(conditionItem.target_state_id),
                  label: conditionItem.expression
                })
              }
            )
          } else{
            edges.push({source: String(transitionItem.source_state_id), target: String(transitionItem.destination_state_id), label:transitionItem.name})
          }
        }
      )
      setData({nodes:nodes, edges:edges});


    } else {
      message.error(result.msg);
    };
  };

  useEffect( () => {
    fetchGraphData();

  }, [])


  const updateBehaviors = () => {
    if (behaviors.indexOf('drag-node') !== -1) {
      setBehaviors(['drag-canvas', 'zoom-canvas']);
    } else {
      setBehaviors(['drag-canvas', 'zoom-canvas', 'drag-node']);
    }
  };

  const handleEdgeClick = (item, graph) => {
    graph.setItemState(item, 'selected', true);
  };
  const handleNodeClick = (item, graph) => {
    graph.setItemState(item, 'selected', true);
  };

  const handleCanvasClick = (graph) => {
    const selectedEdges = graph.findAllByState('edge', 'selected');
    selectedEdges.forEach((edge) => {
      graph.setItemState(edge, 'selected', false);
    });
    const selectedNodes = graph.findAllByState('node', 'selected');
    selectedNodes.forEach((node) => {
      graph.setItemState(node, 'selected', false);
    });
  };
  const edgeStateStyles = {
    hover: {
      stroke: '#1890ff',
      lineWidth: 2,
    },
    selected: {
      stroke: '#f00',
      lineWidth: 3,
    },
  };
  const nodeStateStyles = {
    hover: {
      stroke: '#1890ff',
      lineWidth: 2,
    },
    selected: {
      stroke: '#f00',
      lineWidth: 3,
    },
  };

  return (
    <DagreGraph
      nodeStyle={nodeStyle}
      layout={layoutCfg}
      nodeAnchorPoints={anchorPoints}
      nodeType={nodeType}
      nodeLabelCfg={nodeLabelCfg}
      minimapCfg={minimapCfg}
      behaviors={behaviors}
      data={data}
      graphRef={ref}
      handleEdgeClick={handleEdgeClick}
      handleCanvasClick={handleCanvasClick}
      edgeStateStyles={edgeStateStyles}
      nodeStateStyles={nodeStateStyles}
      handleNodeClick={handleNodeClick}
    />
  );
};

export default WorkflowGraph;

