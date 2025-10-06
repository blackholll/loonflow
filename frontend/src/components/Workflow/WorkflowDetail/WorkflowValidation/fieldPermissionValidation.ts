import { IWorkflowFullDefinition } from '../../../../types/workflow';

/**
 * Validate field permissions for start and normal nodes
 * @param workflowData Complete workflow definition data
 * @returns List of field permission validation problems
 */
export const validateFieldPermissions = (workflowData: IWorkflowFullDefinition): string[] => {
    const problems: string[] = [];

    // Find title component and detect auto-generate mode
    const allComponents = workflowData.formSchema.componentInfoList.flatMap((component: any) => {
        if (component.type === 'row') {
            return component.children || [];
        }
        return [component];
    });
    const titleComponent = allComponents.find((c: any) => c.type === 'title');
    const isTitleAuto = Boolean(titleComponent?.props?.titleGenerateMode === 'automatic');
    const titleKey = titleComponent?.componentKey;

    for (const node of workflowData.processSchema.nodeInfoList) {
        const read_fields = ['creator', 'createdAt', 'ticketNodes', 'approvalStatus', 'ticketType', 'currentHandler'];
        const fieldPermissions = node.props.fieldPermissions || {};
        // 遍历fieldPermissions的key
        for (const key of Object.keys(fieldPermissions)) {
            if (read_fields.includes(key)) {
                if (fieldPermissions[key] === 'optional' || fieldPermissions[key] === 'required') {
                    problems.push(`信息组件"${key}"的只能设置为隐藏或者只读`);
                }
            }
        }

        // Check start and normal nodes
        if (node.type === 'start') {
            if (!Object.values(fieldPermissions).some(permission => permission === 'optional' || permission === 'required')) {
                problems.push(`开始节点"${node.name}"的字段权限中至少有一个可输入字段`);
            }

            // Rule: if title is auto-generated, start node must set it to hidden
            if (isTitleAuto && titleKey) {
                // keys are camelCased in property panel
                const camelKey = titleKey
                    .replace(/[-_ ]+([a-zA-Z0-9])/g, (_match: string, group1: string) => group1.toUpperCase())
                    .replace(/^[A-Z]/, (first: string) => first.toLowerCase());
                const titlePermission = fieldPermissions?.[camelKey];
                if (titlePermission !== 'hidden') {
                    problems.push(`存在自动生成标题时，开始节点"${node.name}"必须将标题字段设置为隐藏`);
                }
            }
        }

        if (node.type === 'normal') {

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
