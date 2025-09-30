import { IWorkflowFullDefinition } from '../../../../types/workflow';

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
                problems.push(`普通节点"${node.name}"必须设置处理人类型`);
            }

            // 检查用户/部门设置
            if (!node.props.assignee || node.props.assignee === '') {
                problems.push(`普通节点"${node.name}"必须设置处理人`);
            }

            // 检查分配策略
            if (!node.props.assignmentStrategy) {
                problems.push(`普通节点"${node.name}"必须设置分配策略`);
            }
        }
    }

    return problems;
};
