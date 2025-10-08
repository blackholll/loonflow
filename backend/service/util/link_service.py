class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __int__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head  
            while current.next:
                current = current.next
            current.next = new_node
