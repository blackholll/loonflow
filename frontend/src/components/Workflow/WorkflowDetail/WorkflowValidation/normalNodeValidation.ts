import { IWorkflowFullDefinition } from '../../../../types/workflow';
import { getValidationMessage } from './i18n';

/**
 * Validate normal nodes
 * @param workflowData Complete workflow definition data
 * @returns List of normal node validation problems
 */
export const validateNormalNodes = (workflowData: IWorkflowFullDefinition): string[] => {
    const problems: string[] = [];

    // Check normal node must has assignee
    for (const node of workflowData.processSchema.nodeInfoList) {
        if (node.type === 'normal') {
            // 检查处理人类型
            if (!node.props.assigneeType) {
                problems.push(getValidationMessage('normal', 'assigneeTypeRequired', {
                    nodeName: node.name
                }));
            }

            // 检查用户/部门设置
            if (!node.props.assignee || node.props.assignee === '') {
                problems.push(getValidationMessage('normal', 'assigneeRequired', {
                    nodeName: node.name
                }));
            }

            // 检查分配策略
            if (!node.props.assignmentStrategy) {
                problems.push(getValidationMessage('normal', 'assignmentStrategyRequired', {
                    nodeName: node.name
                }));
            }
        }
    }

    return problems;
};
