import { IWorkflowFullDefinition } from '../../../../types/workflow';
import { getValidationMessage } from './i18n';

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
                problems.push(getValidationMessage('edge', 'conditionGroupRequired', {
                    edgeName: edge.name
                }));
            }
        }
    }

    return problems;
};
