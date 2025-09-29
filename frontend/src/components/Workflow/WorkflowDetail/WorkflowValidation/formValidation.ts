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

    // Rule: title component MUST exist exactly once
    // Flatten components to count title components
    const allComponents = workflowData.formSchema.componentInfoList.flatMap((component: any) => {
        if (component.type === 'row') {
            return component.children || [];
        }
        return [component];
    });

    const titleComponents = allComponents.filter((c: any) => c.type === 'title');
    if (titleComponents.length !== 1) {
        problems.push(`表单中标题组件（type="title"）有且只能有一个，当前为${titleComponents.length}个`);
    }

    return problems;
};
