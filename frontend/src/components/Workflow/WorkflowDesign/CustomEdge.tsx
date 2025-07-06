import React from 'react';
import { EdgeProps, getSmoothStepPath, getBezierPath, getStraightPath } from '@xyflow/react';
import { Box } from '@mui/material';

const CustomEdge: React.FC<EdgeProps> = ({
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
}) => {
    const [edgePath, labelX, labelY] = getSmoothStepPath({
        sourceX,
        sourceY,
        sourcePosition,
        targetX,
        targetY,
        targetPosition,
    });

    const arrowMarkerId = `arrow-${id}`;

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
                    <path d="M 0 0 L 10 5 L 0 10 z" fill={selected ? '#1976d2' : '#555'} />
                </marker>
            </defs>

            <path
                id={id}
                style={{
                    ...style,
                    strokeWidth: selected ? 3 : 2,
                    stroke: selected ? '#1976d2' : '#555',
                    fill: 'none',
                }}
                className="react-flow__edge-path"
                d={edgePath}
                markerEnd={`url(#${arrowMarkerId})`}
            />

            {/* 其他代码保持不变 */}
        </>
    );
};

export { CustomEdge };