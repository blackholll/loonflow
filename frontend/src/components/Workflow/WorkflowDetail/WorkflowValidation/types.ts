/**
 * Workflow validation result
 */
export interface WorkflowValidationResult {
    /** List of detected problems */
    problems: string[];
    /** Whether there are any problems */
    hasProblems: boolean;
}
