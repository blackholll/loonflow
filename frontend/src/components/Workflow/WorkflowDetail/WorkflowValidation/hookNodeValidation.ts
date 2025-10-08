import { IWorkflowFullDefinition } from '../../../../types/workflow';
import { getValidationMessage } from './i18n';

/**
 * Validate hook nodes
 * @param workflowData Complete workflow definition data
 * @returns List of hook node validation problems
 */
export const validateHookNodes = (workflowData: IWorkflowFullDefinition): string[] => {
    const problems: string[] = [];

    for (const node of workflowData.processSchema.nodeInfoList) {
        if (node.type === 'hook') {
            // 检查hook地址是否填写
            if (!node.props.hookUrl || node.props.hookUrl.trim() === '') {
                problems.push(getValidationMessage('hook', 'hookUrlRequired', {
                    nodeName: node.name
                }));
            }

            // 检查hook token是否填写
            if (!node.props.hookToken || node.props.hookToken.trim() === '') {
                problems.push(getValidationMessage('hook', 'hookTokenRequired', {
                    nodeName: node.name
                }));
            }

            // 获取钩子节点的入边和出边
            const inputEdges = workflowData.processSchema.edgeInfoList.filter(
                (edge) => edge.targetNodeId === node.id
            );
            const outputEdges = workflowData.processSchema.edgeInfoList.filter(
                (edge) => edge.sourceNodeId === node.id
            );

            // 检查钩子节点必须至少有一个入边
            if (inputEdges.length < 1) {
                problems.push(getValidationMessage('hook', 'needInputEdge', {
                    nodeName: node.name,
                    count: inputEdges.length
                }));
            }

            // 检查钩子节点只能有一个出边
            if (outputEdges.length !== 1) {
                problems.push(getValidationMessage('hook', 'onlyOneOutputEdge', {
                    nodeName: node.name,
                    count: outputEdges.length
                }));
            }

            // 检查钩子节点的出边目标节点不可以是自己
            for (const outputEdge of outputEdges) {
                if (outputEdge.targetNodeId === node.id) {
                    problems.push(getValidationMessage('hook', 'outputEdgeCannotBeSelf', {
                        nodeName: node.name
                    }));
                }
            }
        }
    }

    return problems;
};
