import React, {useEffect, useState} from 'react'
import G6 from '@antv/g6';
import {getWorkflowSimpleDescription} from "@/services/workflows";
import {message} from "antd";

const WorkflowGraph = (props) => {
  const ref = React.useRef(null);
  let graph = null;


  const [workflowData, setData] = useState({});

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

  useEffect( () => {
    if (!graph) {
      // 实例化 Graph
      G6.registerNode(
        "sql",
        {
          drawShape(cfg, group) {
            const rect = group.addShape("rect", {
              attrs: {
                x: -75,
                y: -25,
                width: 150,
                height: 50,
                radius: 10,
                stroke: "#5B8FF9",
                fill: "#C6E5FF",
                lineWidth: 3
              },
              name: "rect-shape"
            });
            if (cfg.name) {
              group.addShape("text", {
                attrs: {
                  text: cfg.name,
                  x: 0,
                  y: 0,
                  fill: "#00287E",
                  fontSize: 14,
                  textAlign: "center",
                  textBaseline: "middle",
                  fontWeight: "bold"
                },
                name: "text-shape"
              });
            }
            return rect;
          }
        },
        "single-node"
      );

      graph = new G6.Graph({
        container: ref.current,
        width: 600,
        height: 400,
        layout: {
          type: "dagre",
          nodesepFunc: (d) => {
            if (d.id === "3") {
              return 500;
            }
            return 50;
          },
          ranksep: 70,
          controlPoints: true
        },
        defaultNode: {
          type: "sql"
        },
        defaultEdge: {
          type: "polyline",
          style: {
            radius: 20,
            offset: 45,
            endArrow: true,
            lineWidth: 2,
            stroke: "#C2C8D5"
          }
        },
        nodeStateStyles: {
          selected: {
            stroke: "#d9d9d9",
            fill: "#5394ef"
          }
        },
        modes: {
          default: [
            "drag-canvas",
            "zoom-canvas",
            "click-select",
            {
              type: "tooltip",
              formatText(model) {
                const cfg = model.conf;
                return cfg;

              },
              // offset: 30
            }
          ]
        },
        fitView: true
      });
      graph.data(workflowData);
      graph.render();
    }
  }, [workflowData]);

  return <div ref={ref}></div>;
};

export default WorkflowGraph;

