import { IWorkflowFullDefinition } from '../../../../types/workflow';

/**
 * Validate field permissions for start and normal nodes
 * @param workflowData Complete workflow definition data
 * @returns List of field permission validation problems
 */
export const validateFieldPermissions = (workflowData: IWorkflowFullDefinition): string[] => {
    const problems: string[] = [];

    for (const node of workflowData.processSchema.nodeInfoList) {
        // Check start and normal nodes
        if (node.type === 'start') {
            const fieldPermissions = node.props.fieldPermissions || {};
            if (!Object.values(fieldPermissions).some(permission => permission === 'optional' || permission === 'required')) {
                problems.push(`开始节点"${node.name}"的字段权限中至少有一个可输入字段`);
            }
        }

        if (node.type === 'normal') {
            const fieldPermissions = node.props.fieldPermissions || {};

            // Check if there's at least one non-hidden field
            const hasNonHiddenField = Object.values(fieldPermissions).some(
                permission => permission !== 'hidden'
            );

            if (!hasNonHiddenField) {
                problems.push(`节点"${node.name}"的字段权限中至少有一个非隐藏字段`);
            }
        }
    }

    return problems;
};
