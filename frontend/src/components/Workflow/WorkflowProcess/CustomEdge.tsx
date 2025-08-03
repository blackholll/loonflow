import React from 'react';
import { EdgeProps, getSmoothStepPath, getBezierPath, getStraightPath, EdgeLabelRenderer, useReactFlow } from '@xyflow/react';
import { Box, Typography } from '@mui/material';

interface EdgeData {
    properties?: {
        name?: string;
        description?: string;
        condition?: string;
        [key: string]: any;
    };
}

function CustomEdge(props: EdgeProps) {
    const {
        id,
        sourceX,
        sourceY,
        targetX,
        targetY,
        sourcePosition,
        targetPosition,
        style = {},
        markerEnd,
        selected,
        data,
    } = props;
    const { setEdges } = useReactFlow();

    const [edgePath, labelX, labelY] = getSmoothStepPath({
        sourceX,
        sourceY,
        sourcePosition,
        targetX,
        targetY,
        targetPosition,
    });

    const arrowMarkerId = `arrow-${id}`;

    const handleLabelClick = (event: React.MouseEvent) => {
        console.log('handleLabelClick', event);
        event.stopPropagation();

        // 选中当前连线
        setEdges((edges) =>
            edges.map((edge) => ({
                ...edge,
                selected: edge.id === id,
            }))
        );

        // 触发自定义事件来通知父组件
        const customEvent = new CustomEvent('edgeLabelClick', {
            detail: { edgeId: id },
            bubbles: true,
        });
        event.currentTarget.dispatchEvent(customEvent);
    };

    return (
        <>
            <defs>
                <marker
                    id={arrowMarkerId}
                    viewBox="0 0 10 10"
                    refX="8"
                    refY="5"
                    markerWidth="6"
                    markerHeight="6"
                    orient="auto"
                >
                    <path d="M 0 0 L 10 5 L 0 10 z" fill={selected ? '#1976d2' : 'gray'} />
                </marker>
            </defs>

            <path
                id={id}
                style={{
                    ...style,
                    strokeWidth: selected ? 2 : 1.5,
                    stroke: selected ? '#1976d2' : 'gray',
                    fill: 'none',
                }}
                className="react-flow__edge-path"
                d={edgePath}
                markerEnd={`url(#${arrowMarkerId})`}
            />

            {/* 连线标签 */}
            {(data as EdgeData)?.properties?.name && (
                <>
                    {/* 可点击的背景区域 */}
                    <rect
                        x={labelX - 50}
                        y={labelY - 15}
                        width={100}
                        height={30}
                        fill="transparent"
                        style={{ cursor: 'pointer' }}
                        onClick={handleLabelClick}
                    />
                    {/* 文字标签 */}
                    <text
                        x={labelX}
                        y={labelY}
                        textAnchor="middle"
                        dominantBaseline="middle"
                        style={{
                            fontSize: '12px',
                            fontWeight: 'bold',
                            fill: selected ? '#1976d2' : 'gray',
                            cursor: 'pointer',
                            userSelect: 'none',
                            textShadow: '0 0 2px rgba(255, 255, 255, 0.8)',
                        }}
                        onClick={handleLabelClick}
                    >
                        {(data as EdgeData).properties!.name}
                    </text>
                </>
            )}
        </>
    );
};

export { CustomEdge };