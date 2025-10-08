import { IWorkflowFullDefinition } from '../../../../types/workflow';
import { getValidationMessage } from './i18n';

/**
 * Validate form schema
 * @param workflowData Complete workflow definition data
 * @returns List of form validation problems
 */
export const validateFormSchema = (workflowData: IWorkflowFullDefinition): string[] => {
    const problems: string[] = [];

    // Check if form design is empty
    if (workflowData.formSchema.componentInfoList.length === 0) {
        problems.push(getValidationMessage('form', 'formDesignEmpty'));
    }

    // Check if every row component has children
    for (const component of workflowData.formSchema.componentInfoList) {
        if (component.type === 'row') {
            if (component.children.length === 0) {
                problems.push(getValidationMessage('form', 'rowComponentNoChildren'));
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
        problems.push(getValidationMessage('form', 'titleComponentCountError', {
            count: titleComponents.length
        }));
    }

    return problems;
};
