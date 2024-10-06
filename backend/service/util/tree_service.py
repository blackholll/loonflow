from service.base_service import BaseService


class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []


class TreeService(BaseService):
    def __init__(self):
        pass

    @classmethod
    def build_tree_from_lists(cls, lists: list) -> tuple:
        """
        build tree from lists,
        [1,2,3], [1,2,4], [1,5,6]-->
            1
          /   \
         2     5
        / \   /
        3  4  6
        :param lists:
        :return:
        """
        root = TreeNode(0)
        for lst in lists:
            current_node = root
            for val in lst:
                # search same value child node
                child_node = None
                for child in current_node.children:
                    if child.value == val:
                        child_node = child
                        break
                # can not get child node, then create a new child
                if child_node is None:
                    child_node = TreeNode(val)
                    current_node.children.append(child_node)
                # move to child node
                current_node = child_node

        return root

    @classmethod
    def get_value_list_from_tree(cls, tree_node: TreeNode) -> tuple:
        """
        get value list from a tree's node
        :param tree_node:
        :return:
        """
        result_list = []
        if tree_node:
            result_list.append(tree_node.value)
            for child in tree_node.children:
                result_list += cls.get_value_list_from_tree(child)
        return result_list

    @classmethod
    def get_node_list_from_tree(cls, tree_node:TreeNode) -> tuple:
        """
        get all node list from tree
        :param tree_node:
        :return:
        """
        result_list = []
        if tree_node:
            result_list.append(tree_node)
            for child in tree_node.children:
                result_list += cls.get_node_list_from_tree(child)[1]
        return True, result_list

    @classmethod
    def get_leaf_value_list_from_tree(cls, tree_node: TreeNode) -> tuple:
        """
        get leaf node value list
        :param tree_node:
        :return:
        """
        result_list = []
        flag, node_list = cls.get_node_list_from_tree(tree_node)
        for node0 in node_list:
            if not node0.children:
                result_list.append(node0.value)
        return True, result_list


tree_service_ins = TreeService()
