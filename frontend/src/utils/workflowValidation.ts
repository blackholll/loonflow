import { IWorkflowFullDefinition } from '../types/workflow';

/**
 * Workflow validation result
 */
export interface WorkflowValidationResult {
    /** List of detected problems */
    problems: string[];
    /** Whether there are any problems */
    hasProblems: boolean;
}

/**
 * Check for problems in workflow definition
 * @param workflowData Complete workflow definition data
 * @returns Validation result
 */
export const checkWorkflowProblems = (workflowData: IWorkflowFullDefinition): WorkflowValidationResult => {
    const problems: string[] = [];

    // Check if form design is empty
    if (workflowData.formSchema.componentInfoList.length === 0) {
        problems.push('表单设计不能为空');
    }
    // check if every row componet has children
    for (const component of workflowData.formSchema.componentInfoList) {
        if (component.type === 'row') {
            if (component.children.length === 0) {
                problems.push('行组件不能没有子组件');
            }
        }
    }
    // check normal node must has assignee
    for (const node of workflowData.processSchema.nodeInfoList) {
        if (node.type === 'normal') {
            if (node.props.assignee === '' || node.props.assigneeType === '') {
                problems.push('普通节点不能没有处理人');
            }
        }
    }

    // Check if process design is empty
    if (workflowData.processSchema.nodeInfoList.length === 0) {
        problems.push('流程设计不能为空');
    }
    // check if dissociative node exist, means start node has no output edge, end node has no input edge, common node missing input edge or output edge
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
            if (outputEdgeList.length === 0 || outputEdgeList.length === 0) {
                problems.push(`${node.type}节点不能没有输入连线或输出连线`);
            }
        }
    }


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
