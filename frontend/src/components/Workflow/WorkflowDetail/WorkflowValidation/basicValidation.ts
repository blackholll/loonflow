import { IWorkflowFullDefinition } from '../../../../types/workflow';

/**
 * Validate basic workflow information
 * @param workflowData Complete workflow definition data
 * @returns List of basic validation problems
 */
export const validateBasicInfo = (workflowData: IWorkflowFullDefinition): string[] => {
    const problems: string[] = [];

    // Check if workflow name is empty
    if (!workflowData.basicInfo.name || workflowData.basicInfo.name.trim() === '') {
        problems.push('工作流名称不能为空');
    }

    return problems;
};

/**
 * Validate node names
 * @param workflowData Complete workflow definition data
 * @returns List of node name validation problems
 */
export const validateNodeNames = (workflowData: IWorkflowFullDefinition): string[] => {
    const problems: string[] = [];

    // Check if all nodes have names
    for (const node of workflowData.processSchema.nodeInfoList) {
        if (!node.name || node.name.trim() === '') {
            problems.push(`${node.type}节点"${node.id}"必须要有名称`);
        }
    }

    return problems;
};

/**
 * Validate start node count
 * @param workflowData Complete workflow definition data
 * @returns List of start node validation problems
 */
export const validateStartNodeCount = (workflowData: IWorkflowFullDefinition): string[] => {
    const problems: string[] = [];

    // Check if there's exactly one start node
    const startNodes = workflowData.processSchema.nodeInfoList.filter(node => node.type === 'start');

    if (startNodes.length === 0) {
        problems.push('工作流必须有一个开始节点');
    } else if (startNodes.length > 1) {
        problems.push(`工作流只能有一个开始节点，当前有${startNodes.length}个开始节点`);
    }

    return problems;
};

/**
 * Validate end node count
 * @param workflowData Complete workflow definition data
 * @returns List of end node validation problems
 */
export const validateEndNodeCount = (workflowData: IWorkflowFullDefinition): string[] => {
    const problems: string[] = [];

    // Check if there's exactly one end node
    const endNodes = workflowData.processSchema.nodeInfoList.filter(node => node.type === 'end');

    if (endNodes.length === 0) {
        problems.push('工作流必须有一个结束节点');
    } else if (endNodes.length > 1) {
        problems.push(`工作流只能有一个结束节点，当前有${endNodes.length}个结束节点`);
    }

    return problems;
};
