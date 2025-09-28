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
            if (node.props.assignee === '' || node.props.assigneeType === '') {
                problems.push(`节点:"${node.name}"不能没有处理人`);
            }
        }
    }

    return problems;
};
