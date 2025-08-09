import { IWorkflowFullDefinition } from "../../../types/workflow";

function checkWorkflowCompatibility(workflowDetailInfo: IWorkflowFullDefinition, workflowSourceDetailInfo: IWorkflowFullDefinition | null): Promise<{ isCompatible: boolean, messages: string[] }> {
    const messages: string[] = [];
    if (!workflowSourceDetailInfo) {
        return Promise.resolve({ isCompatible: true, messages });
    }
    // situaltions that not compatibility with old version: 1.node deleted
    const source_node = workflowSourceDetailInfo.processSchema.nodeInfoList;
    const detail_node = workflowDetailInfo.processSchema.nodeInfoList;
    for (const node of source_node) {
        if (!detail_node.find((detail_node) => detail_node.id === node.id)) {
            messages.push(`node(${node.name}) deleted`)
            return Promise.resolve({ isCompatible: false, messages });
        }
    }
    return Promise.resolve({ isCompatible: true, messages });
}

export default checkWorkflowCompatibility;