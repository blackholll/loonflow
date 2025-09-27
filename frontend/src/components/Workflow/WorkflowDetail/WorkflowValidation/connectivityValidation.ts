import { IWorkflowFullDefinition } from '../../../../types/workflow';

/**
 * Validate node connectivity
 * @param workflowData Complete workflow definition data
 * @returns List of connectivity validation problems
 */
export const validateNodeConnectivity = (workflowData: IWorkflowFullDefinition): string[] => {
    const problems: string[] = [];

    // Check if process design is empty
    if (workflowData.processSchema.nodeInfoList.length === 0) {
        problems.push('流程设计不能为空');
    }

    // Check if dissociative node exist, means start node has no output edge, end node has no input edge, common node missing input edge or output edge
    for (const node of workflowData.processSchema.nodeInfoList) {
        const outputEdgeList = workflowData.processSchema.edgeInfoList.filter((edge) => edge.sourceNodeId === node.id);
        const inputEdgeList = workflowData.processSchema.edgeInfoList.filter((edge) => edge.targetNodeId === node.id);

        if (node.type === 'start') {
            if (outputEdgeList.length === 0) {
                problems.push('开始节点不能没有输出连线');
            }
        }

        if (node.type === 'end') {
            if (inputEdgeList.length === 0) {
                problems.push('结束节点不能没有输入连线');
            }
        }

        if (['normal', 'parallel', 'exclusive', 'timer', 'hook'].includes(node.type)) {
            console.log(outputEdgeList, inputEdgeList);
            if (outputEdgeList.length === 0 || inputEdgeList.length === 0) {
                problems.push(`${node.type}节点不能没有输入连线或输出连线`);
            }
        }
    }

    return problems;
};
