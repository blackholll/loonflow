import { IWorkflowFullDefinition } from '../../../../types/workflow';
import { getValidationMessage } from './i18n';

/**
 * Validate exclusive gateway nodes
 * @param workflowData Complete workflow definition data
 * @returns List of exclusive gateway validation problems
 */
export const validateExclusiveNodes = (workflowData: IWorkflowFullDefinition): string[] => {
    const problems: string[] = [];

    for (const node of workflowData.processSchema.nodeInfoList) {
        if (node.type === 'exclusive') {
            // 获取排他网关的入边和出边
            const inputEdges = workflowData.processSchema.edgeInfoList.filter(
                (edge) => edge.targetNodeId === node.id
            );
            const outputEdges = workflowData.processSchema.edgeInfoList.filter(
                (edge) => edge.sourceNodeId === node.id
            );

            // 检查排他网关必须有入边和出边
            if (inputEdges.length === 0) {
                problems.push(getValidationMessage('exclusive', 'noInputEdge', {
                    nodeName: node.name
                }));
            }
            if (outputEdges.length === 0) {
                problems.push(getValidationMessage('exclusive', 'noOutputEdge', {
                    nodeName: node.name
                }));
            }

            // 检查排他网关的起始节点不可以是结束类型的节点
            for (const inputEdge of inputEdges) {
                const sourceNode = workflowData.processSchema.nodeInfoList.find(
                    (n) => n.id === inputEdge.sourceNodeId
                );
                if (sourceNode && sourceNode.type === 'end') {
                    problems.push(getValidationMessage('exclusive', 'sourceNodeCannotBeEnd', {
                        nodeName: node.name,
                        sourceNodeName: sourceNode.name
                    }));
                }
            }
        }
    }

    return problems;
};
