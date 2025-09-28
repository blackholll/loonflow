import { IWorkflowFullDefinition } from '../../../../types/workflow';

/**
 * Validate timer nodes
 * @param workflowData Complete workflow definition data
 * @returns List of timer node validation problems
 */
export const validateTimerNodes = (workflowData: IWorkflowFullDefinition): string[] => {
    const problems: string[] = [];

    for (const node of workflowData.processSchema.nodeInfoList) {
        if (node.type === 'timer') {
            // 获取定时器节点的入边和出边
            const inputEdges = workflowData.processSchema.edgeInfoList.filter(
                (edge) => edge.targetNodeId === node.id
            );
            const outputEdges = workflowData.processSchema.edgeInfoList.filter(
                (edge) => edge.sourceNodeId === node.id
            );

            // 检查定时器节点必须有超过一个入边
            if (inputEdges.length < 1) {
                problems.push(`定时器节点"${node.name}"必须至少一个入边，当前有${inputEdges.length}个入边`);
            }

            // 检查定时器节点只能有一个出边
            if (outputEdges.length !== 1) {
                problems.push(`定时器节点"${node.name}"只能有一个出边，当前有${outputEdges.length}个出边`);
            }

            // 检查定时器节点的出边目标节点不可以是自己
            for (const outputEdge of outputEdges) {
                if (outputEdge.targetNodeId === node.id) {
                    problems.push(`定时器节点"${node.name}"的出边目标节点不能是自己`);
                }
            }
        }
    }

    return problems;
};
