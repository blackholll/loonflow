import { IWorkflowFullDefinition } from '../../../../types/workflow';

/**
 * Validate condition edges must have conditionGroups
 * @param workflowData Complete workflow definition data
 * @returns List of edge condition validation problems
 */
export const validateEdgeConditions = (workflowData: IWorkflowFullDefinition): string[] => {
    const problems: string[] = [];

    // Check condition edges must have conditionGroups
    for (const edge of workflowData.processSchema.edgeInfoList) {
        if (edge.type === 'condition') {
            if (!edge.props.conditionGroups ||
                !Array.isArray(edge.props.conditionGroups) ||
                edge.props.conditionGroups.length === 0) {
                problems.push(`条件连线"${edge.name}"必须设置条件组`);
            }
        }
    }

    return problems;
};
