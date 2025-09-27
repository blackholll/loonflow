import { IWorkflowFullDefinition } from '../../../../types/workflow';
import { WorkflowValidationResult } from './types';
import { validateFormSchema } from './formValidation';
import { validateNormalNodes } from './normalNodeValidation';
import { validateNodeConnectivity } from './connectivityValidation';
import { validateParallelNodes } from './parallelNodeValidation';

/**
 * Check for problems in workflow definition
 * @param workflowData Complete workflow definition data
 * @returns Validation result
 */
export const checkWorkflowProblems = (workflowData: IWorkflowFullDefinition): WorkflowValidationResult => {
    const problems: string[] = [];

    // Validate form schema
    problems.push(...validateFormSchema(workflowData));

    // Validate normal nodes
    problems.push(...validateNormalNodes(workflowData));

    // Validate node connectivity
    problems.push(...validateNodeConnectivity(workflowData));

    // Validate parallel nodes
    problems.push(...validateParallelNodes(workflowData));

    return {
        problems,
        hasProblems: problems.length > 0
    };
};

/**
 * Check if workflow can be published
 * @param workflowData Complete workflow definition data
 * @returns Whether the workflow can be published
 */
export const canPublishWorkflow = (workflowData: IWorkflowFullDefinition): boolean => {
    const result = checkWorkflowProblems(workflowData);
    return !result.hasProblems;
};

export type { WorkflowValidationResult } from './types';

export { validateFormSchema } from './formValidation';
export { validateNormalNodes } from './normalNodeValidation';
export { validateNodeConnectivity } from './connectivityValidation';
export { validateParallelNodes } from './parallelNodeValidation';
