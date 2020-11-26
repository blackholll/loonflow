import React, { useEffect } from 'react'
import G6 from '@antv/g6';
import insertCss from 'insert-css';

insertCss(`
  .g6-tooltip {
    border-radius: 6px;
    font-size: 12px;
    color: #fff;
    background-color: #000;
    padding: 2px 8px;
    text-align: center;
  }
`);
const data = {
  nodes: [
    {
      id: '1',
      dataType: 'alps',
      name: 'alps_file1',
      conf: [
        {
          label: 'conf',
          value: 'pai_graph.conf',
        },
        {
          label: 'dot',
          value: 'pai_graph.dot',
        },
        {
          label: 'init',
          value: 'init.rc',
        },
      ],
    },
    {
      id: '2',
      dataType: 'alps',
      name: 'alps_file2',
      conf: [
        {
          label: 'conf',
          value: 'pai_graph.conf',
        },
        {
          label: 'dot',
          value: 'pai_graph.dot',
        },
        {
          label: 'init',
          value: 'init.rc',
        },
      ],
    },
    {
      id: '3',
      dataType: 'alps',
      name: 'alps_file3',
      conf: [
        {
          label: 'conf',
          value: 'pai_graph.conf',
        },
        {
          label: 'dot',
          value: 'pai_graph.dot',
        },
        {
          label: 'init',
          value: 'init.rc',
        },
      ],
    },
    {
      id: '4',
      dataType: 'sql',
      name: 'sql_file1',
      conf: [
        {
          label: 'conf',
          value: 'pai_graph.conf',
        },
        {
          label: 'dot',
          value: 'pai_graph.dot',
        },
        {
          label: 'init',
          value: 'init.rc',
        },
      ],
    },
    {
      id: '5',
      dataType: 'sql',
      name: 'sql_file2',
      conf: [
        {
          label: 'conf',
          value: 'pai_graph.conf',
        },
        {
          label: 'dot',
          value: 'pai_graph.dot',
        },
        {
          label: 'init',
          value: 'init.rc',
        },
      ],
    },
    {
      id: '6',
      dataType: 'feature_etl',
      name: 'feature_etl_1',
      conf: [
        {
          label: 'conf',
          value: 'pai_graph.conf',
        },
        {
          label: 'dot',
          value: 'pai_graph.dot',
        },
        {
          label: 'init',
          value: 'init.rc',
        },
      ],
    },
    {
      id: '7',
      dataType: 'feature_etl',
      name: 'feature_etl_1',
      conf: [
        {
          label: 'conf',
          value: 'pai_graph.conf',
        },
        {
          label: 'dot',
          value: 'pai_graph.dot',
        },
        {
          label: 'init',
          value: 'init.rc',
        },
      ],
    },
    {
      id: '8',
      dataType: 'feature_extractor',
      name: 'feature_extractor',
      conf: [
        {
          label: 'conf',
          value: 'pai_graph.conf',
        },
        {
          label: 'dot',
          value: 'pai_graph.dot',
        },
        {
          label: 'init',
          value: 'init.rc',
        },
      ],
    },
  ],
  edges: [
    {
      source: '1',
      target: '2',
    },
    {
      source: '1',
      target: '3',
    },
    {
      source: '2',
      target: '4',
    },
    {
      source: '3',
      target: '4',
    },
    {
      source: '4',
      target: '5',
    },
    {
      source: '5',
      target: '6',
    },
    {
      source: '6',
      target: '7',
    },
    {
      source: '6',
      target: '8',
    },
  ],
};



const Tutorital = () => {
  const ref = React.useRef(null)
  let graph = null

  useEffect(() => {
    if(!graph) {
      const width = ref.current.scrollWidth;
      const height = ref.current.scrollHeight || 500;
      const graph = new G6.Graph({
        container: ref.current,
        width,
        height,
        layout: {
          type: 'dagre',
          nodesepFunc: (d) => {
            if (d.id === '3') {
              return 500;
            }
            return 50;
          },
          ranksep: 70,
          controlPoints: true,
        },
        defaultNode: {
          // shape: "circle",
          // size: [20],
          type: 'sql',
          style: {
            radius: 200,
            offset: 45,
            endArrow: true,
            lineWidth: 2,
            stroke: '#C2C8D5',
          },
        },
        defaultEdge: {
          type: 'polyline',
          style: {
            radius: 20,
            offset: 45,
            endArrow: true,
            lineWidth: 2,
            stroke: '#C2C8D5',
          },
        },
        nodeStateStyles: {
          selected: {
            stroke: '#d9d9d9',
            fill: '#5394ef',
          },
        },
        modes: {
          default: [
            'drag-canvas',
            'zoom-canvas',
            'click-select',
            {
              type: 'tooltip',
              formatText(model) {
                const cfg = model.conf;
                const text = [];
                cfg.forEach((row) => {
                  text.push(row.label + ':' + row.value + '<br>');
                });
                return text.join('\n');
              },
              offset: 30,
            },
          ],
        },
        fitView: true,
      });

      graph.data(data)

      graph.render()
    }


  }, [])

  return <div ref={ref}></div>
}

export default Tutorital
