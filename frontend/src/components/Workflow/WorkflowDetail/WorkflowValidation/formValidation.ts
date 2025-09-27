import { IWorkflowFullDefinition } from '../../../../types/workflow';

/**
 * Validate form schema
 * @param workflowData Complete workflow definition data
 * @returns List of form validation problems
 */
export const validateFormSchema = (workflowData: IWorkflowFullDefinition): string[] => {
    const problems: string[] = [];

    // Check if form design is empty
    if (workflowData.formSchema.componentInfoList.length === 0) {
        problems.push('表单设计不能为空');
    }

    // Check if every row component has children
    for (const component of workflowData.formSchema.componentInfoList) {
        if (component.type === 'row') {
            if (component.children.length === 0) {
                problems.push('行组件不能没有子组件');
            }
        }
    }

    return problems;
};
