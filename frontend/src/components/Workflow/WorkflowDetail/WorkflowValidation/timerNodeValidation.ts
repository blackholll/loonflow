import { IWorkflowFullDefinition } from '../../../../types/workflow';
import { getValidationMessage } from './i18n';

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
                problems.push(getValidationMessage('timer', 'needInputEdge', {
                    nodeName: node.name,
                    count: inputEdges.length
                }));
            }

            // 检查定时器节点只能有一个出边
            if (outputEdges.length !== 1) {
                problems.push(getValidationMessage('timer', 'onlyOneOutputEdge', {
                    nodeName: node.name,
                    count: outputEdges.length
                }));
            }

            // 检查定时器节点的出边目标节点不可以是自己
            for (const outputEdge of outputEdges) {
                if (outputEdge.targetNodeId === node.id) {
                    problems.push(getValidationMessage('timer', 'outputEdgeCannotBeSelf', {
                        nodeName: node.name
                    }));
                }
            }
        }
    }

    return problems;
};
