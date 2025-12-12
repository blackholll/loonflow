import { IWorkflowFullDefinition } from '../../../../types/workflow';
import { getValidationMessage } from './i18n';

/**
 * Validate node connectivity
 * @param workflowData Complete workflow definition data
 * @returns List of connectivity validation problems
 */
export const validateNodeConnectivity = (workflowData: IWorkflowFullDefinition): string[] => {
    const problems: string[] = [];

    // Check if process design is empty
    if (workflowData.processSchema.nodeInfoList.length === 0) {
        problems.push(getValidationMessage('connectivity', 'processDesignEmpty'));
    }

    // Check if dissociative node exist, means start node has no output edge, end node has no input edge, common node missing input edge or output edge
    for (const node of workflowData.processSchema.nodeInfoList) {
        const outputEdgeList = workflowData.processSchema.edgeInfoList.filter((edge) => edge.sourceNodeId === node.id);
        const inputEdgeList = workflowData.processSchema.edgeInfoList.filter((edge) => edge.targetNodeId === node.id);

        if (node.type === 'start') {
            if (outputEdgeList.length === 0) {
                problems.push(getValidationMessage('connectivity', 'startNodeNoOutput'));
            }
        }

        if (node.type === 'end') {
            if (inputEdgeList.length === 0) {
                problems.push(getValidationMessage('connectivity', 'endNodeNoInput'));
            }
        }

        if (['normal', 'parallel', 'exclusive', 'timer', 'hook'].includes(node.type)) {
            if (outputEdgeList.length === 0 || inputEdgeList.length === 0) {
                problems.push(getValidationMessage('connectivity', 'nodeNoConnection', {
                    nodeType: node.type
                }));
            }
        }
    }

    return problems;
};
