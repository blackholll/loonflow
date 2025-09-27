import { IWorkflowFullDefinition, IWorkflowNode, IWorkflowEdge } from '../../../../types/workflow';

/**
 * Find the convergence node for a given starting node
 * A convergence node is typically a parallel gateway or end node that collects multiple paths
 * @param startNodeId Starting node ID
 * @param nodeList List of all nodes
 * @param edgeList List of all edges
 * @returns The convergence node ID, or null if not found
 */
const findConvergenceNode = (
    startNodeId: string,
    nodeList: IWorkflowNode[],
    edgeList: IWorkflowEdge[]
): string | null => {
    const visited = new Set<string>();
    const queue: string[] = [startNodeId];

    while (queue.length > 0) {
        const currentNodeId = queue.shift()!;

        if (visited.has(currentNodeId)) {
            continue;
        }
        visited.add(currentNodeId);

        const currentNode = nodeList.find(n => n.id === currentNodeId);
        if (!currentNode) {
            continue;
        }

        // 如果当前节点是并行网关或结束节点，说明找到了汇聚点
        if (currentNode.type === 'parallel' || currentNode.type === 'end') {
            return currentNodeId;
        }

        // 如果当前节点是普通节点，继续追踪其出边
        if (currentNode.type === 'normal') {
            const outputEdges = edgeList.filter(edge => edge.sourceNodeId === currentNodeId);
            for (const edge of outputEdges) {
                if (!visited.has(edge.targetNodeId)) {
                    queue.push(edge.targetNodeId);
                }
            }
        }

        // 对于其他类型的节点（exclusive, timer, hook等），也继续追踪
        if (['exclusive', 'timer', 'hook'].includes(currentNode.type)) {
            const outputEdges = edgeList.filter(edge => edge.sourceNodeId === currentNodeId);
            for (const edge of outputEdges) {
                if (!visited.has(edge.targetNodeId)) {
                    queue.push(edge.targetNodeId);
                }
            }
        }
    }

    return null;
};

/**
 * Validate parallel nodes
 * @param workflowData Complete workflow definition data
 * @returns List of parallel node validation problems
 */
export const validateParallelNodes = (workflowData: IWorkflowFullDefinition): string[] => {
    const problems: string[] = [];

    for (const node of workflowData.processSchema.nodeInfoList) {
        // 并行网关后的并行节点需要汇聚到一个normal类型的节点
        if (node.type === 'parallel') {
            // 获取并行节点的所有出边
            const parallelOutputEdges = workflowData.processSchema.edgeInfoList.filter(
                (edge) => edge.sourceNodeId === node.id
            );

            if (parallelOutputEdges.length > 0) {
                // 使用深度优先搜索找到所有出边路径最终汇聚的节点
                const convergenceNodes = new Set<string>();

                for (const edge of parallelOutputEdges) {
                    const convergenceNode = findConvergenceNode(
                        edge.targetNodeId,
                        workflowData.processSchema.nodeInfoList,
                        workflowData.processSchema.edgeInfoList
                    );
                    if (convergenceNode) {
                        convergenceNodes.add(convergenceNode);
                    }
                }

                // 检查汇聚节点是否都是normal类型
                for (const convergenceNodeId of Array.from(convergenceNodes)) {
                    const convergenceNode = workflowData.processSchema.nodeInfoList.find(
                        (n) => n.id === convergenceNodeId
                    );
                    if (convergenceNode && convergenceNode.type !== 'normal') {
                        problems.push(`并行节点"${node.name}"的出边最终汇聚到的节点"${convergenceNode.name}"必须是普通节点类型`);
                    }
                }
            }
        }
    }

    return problems;
};
