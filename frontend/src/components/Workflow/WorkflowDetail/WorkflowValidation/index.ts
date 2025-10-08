import { IWorkflowFullDefinition } from '../../../../types/workflow';
import { WorkflowValidationResult } from './types';
import { validateBasicInfo, validateNodeNames, validateStartNodeCount, validateEndNodeCount } from './basicValidation';
import { validateFormSchema } from './formValidation';
import { validateFieldPermissions } from './fieldPermissionValidation';
import { validateNormalNodes } from './normalNodeValidation';
import { validateNodeConnectivity } from './connectivityValidation';
import { validateParallelNodes } from './parallelNodeValidation';
import { validateExclusiveNodes } from './exclusiveNodeValidation';
import { validateTimerNodes } from './timerNodeValidation';
import { validateHookNodes } from './hookNodeValidation';
import { validateEdgeConditions } from './edgeConditionValidation';

/**
 * Check for problems in workflow definition
 * @param workflowData Complete workflow definition data
 * @returns Validation result
 */
export const checkWorkflowProblems = (workflowData: IWorkflowFullDefinition): WorkflowValidationResult => {
    const problems: string[] = [];

    // Basic validation
    problems.push(...validateBasicInfo(workflowData));
    problems.push(...validateNodeNames(workflowData));
    problems.push(...validateStartNodeCount(workflowData));
    problems.push(...validateEndNodeCount(workflowData));

    // Form validation
    problems.push(...validateFormSchema(workflowData));

    // Field permission validation
    problems.push(...validateFieldPermissions(workflowData));

    // Node configuration validation
    problems.push(...validateNormalNodes(workflowData));

    // Connectivity validation
    problems.push(...validateNodeConnectivity(workflowData));

    // Gateway validation
    problems.push(...validateParallelNodes(workflowData));
    problems.push(...validateExclusiveNodes(workflowData));
    problems.push(...validateTimerNodes(workflowData));
    problems.push(...validateHookNodes(workflowData));

    // Edge validation
    problems.push(...validateEdgeConditions(workflowData));

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

// Basic validation
export { validateBasicInfo, validateNodeNames, validateStartNodeCount, validateEndNodeCount } from './basicValidation';

// Form validation
export { validateFormSchema } from './formValidation';

// Field permission validation
export { validateFieldPermissions } from './fieldPermissionValidation';

// Node configuration validation
export { validateNormalNodes } from './normalNodeValidation';

// Connectivity validation
export { validateNodeConnectivity } from './connectivityValidation';

// Gateway validation
export { validateParallelNodes } from './parallelNodeValidation';
export { validateExclusiveNodes } from './exclusiveNodeValidation';
export { validateTimerNodes } from './timerNodeValidation';
export { validateHookNodes } from './hookNodeValidation';

// Edge validation
export { validateEdgeConditions } from './edgeConditionValidation';
