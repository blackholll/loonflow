import { IWorkflowFullDefinition } from '../../../../types/workflow';
import { getValidationMessage } from './i18n';

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
        console.log('validatfieldpermission')
        const read_fields = ['creatorInfo', 'createdAt', 'ticketNodeInfos', 'actState', 'approvalStatus', 'workflowInfo', 'currentAssigneeInfos'];
        const fieldPermissions = node.props.fieldPermissions || {};
        // 遍历fieldPermissions的key
        for (const key of Object.keys(fieldPermissions)) {
            console.log('key', key);
            if (read_fields.includes(key)) {
                if (fieldPermissions[key] === 'optional' || fieldPermissions[key] === 'required') {
                    problems.push(getValidationMessage('fieldPermission', 'infoComponentReadOnly', {
                        key: key
                    }));
                }
            }
        }

        // Check start and normal nodes
        if (node.type === 'start') {
            if (!Object.values(fieldPermissions).some(permission => permission === 'optional' || permission === 'required')) {
                problems.push(getValidationMessage('fieldPermission', 'startNodeNeedInputField', {
                    nodeName: node.name
                }));
            }

            // Rule: if title is auto-generated, start node must set it to hidden
            if (isTitleAuto && titleKey) {
                // keys are camelCased in property panel
                const camelKey = titleKey
                    .replace(/[-_ ]+([a-zA-Z0-9])/g, (_match: string, group1: string) => group1.toUpperCase())
                    .replace(/^[A-Z]/, (first: string) => first.toLowerCase());
                const titlePermission = fieldPermissions?.[camelKey];
                if (titlePermission !== 'hidden') {
                    problems.push(getValidationMessage('fieldPermission', 'autoTitleMustHidden', {
                        nodeName: node.name
                    }));
                }
            }
        }

        if (node.type === 'normal') {

            // Check if there's at least one non-hidden field
            const hasNonHiddenField = Object.values(fieldPermissions).some(
                permission => permission !== 'hidden'
            );

            if (!hasNonHiddenField) {
                problems.push(getValidationMessage('fieldPermission', 'nodeNeedNonHiddenField', {
                    nodeName: node.name
                }));
            }
        }
    }

    return problems;
};
