import React from 'react';
import { EdgeProps, getSmoothStepPath, getBezierPath, getStraightPath, EdgeLabelRenderer } from '@xyflow/react';
import { Box, Typography } from '@mui/material';

interface EdgeData {
    properties?: {
        name?: string;
        description?: string;
        condition?: string;
        [key: string]: any;
    };
}

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

            {/* 连线标签 */}
            {(data as EdgeData)?.properties?.name && (
                <EdgeLabelRenderer>
                    <Typography
                        variant="caption"
                        sx={{
                            position: 'absolute',
                            left: labelX,
                            top: labelY,
                            transform: 'translate(-50%, -50%)',
                            fontSize: '0.75rem',
                            fontWeight: 'bold',
                            color: selected ? '#1976d2' : '#333',
                            lineHeight: 1.2,
                            whiteSpace: 'nowrap',
                            overflow: 'hidden',
                            textOverflow: 'ellipsis',
                            maxWidth: '100px',
                            pointerEvents: 'none',
                            zIndex: 10,
                            textAlign: 'center',
                            textShadow: '0 0 2px rgba(255, 255, 255, 0.8)',
                        }}
                    >
                        {(data as EdgeData).properties!.name}
                    </Typography>
                </EdgeLabelRenderer>
            )}
        </>
    );
};

export { CustomEdge };