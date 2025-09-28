import { IWorkflowFullDefinition, IWorkflowNode, IWorkflowEdge } from '../../../../types/workflow';

/**
 * Find the convergence node where all parallel paths first meet
 * @param parallelNodeId The parallel node ID
 * @param nodeList List of all nodes
 * @param edgeList List of all edges
 * @returns The convergence node ID, or null if not found
 */
const findParallelConvergenceNode = (
    parallelNodeId: string,
    nodeList: IWorkflowNode[],
    edgeList: IWorkflowEdge[]
): string | null => {
    // 获取并行节点的所有出边
    const parallelOutputEdges = edgeList.filter(edge => edge.sourceNodeId === parallelNodeId);

    if (parallelOutputEdges.length === 0) {
        return null;
    }

    // 记录每个节点被哪些路径访问过
    const nodePathMap = new Map<string, Set<number>>();

    // 为每个路径独立进行BFS遍历
    for (let pathIndex = 0; pathIndex < parallelOutputEdges.length; pathIndex++) {
        const startNodeId = parallelOutputEdges[pathIndex].targetNodeId;
        const visited = new Set<string>();
        const queue: string[] = [startNodeId];

        while (queue.length > 0) {
            const currentNodeId = queue.shift()!;

            if (visited.has(currentNodeId)) {
                continue;
            }
            visited.add(currentNodeId);

            // 记录这个节点被当前路径访问
            if (!nodePathMap.has(currentNodeId)) {
                nodePathMap.set(currentNodeId, new Set());
            }
            nodePathMap.get(currentNodeId)!.add(pathIndex);

            // 如果这个节点被所有路径访问，说明找到了汇聚点
            if (nodePathMap.get(currentNodeId)!.size === parallelOutputEdges.length) {
                return currentNodeId;
            }

            // 继续追踪这个节点的出边
            const currentNode = nodeList.find(n => n.id === currentNodeId);
            if (currentNode) {
                const outputEdges = edgeList.filter(edge => edge.sourceNodeId === currentNodeId);
                for (const edge of outputEdges) {
                    if (!visited.has(edge.targetNodeId)) {
                        queue.push(edge.targetNodeId);
                    }
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
            // 找到并行节点所有出边路径第一次同时指向的汇聚节点
            const convergenceNodeId = findParallelConvergenceNode(
                node.id,
                workflowData.processSchema.nodeInfoList,
                workflowData.processSchema.edgeInfoList
            );

            if (convergenceNodeId) {
                const convergenceNode = workflowData.processSchema.nodeInfoList.find(
                    (n) => n.id === convergenceNodeId
                );
                if (convergenceNode && convergenceNode.type !== 'normal') {
                    problems.push(`并行节点"${node.name}"的出边最终汇聚到的节点"${convergenceNode.name}"不是普通节点类型`);
                }
            } else {
                problems.push(`并行节点"${node.name}"的出边没有找到汇聚节点`);
            }
        }
    }

    return problems;
};
