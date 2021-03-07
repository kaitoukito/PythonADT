class DoublyLinkedBase:
    """A base class provide a doubly linked list presentation."""

    # -------------------- nested Node class --------------------
    class Node:
        """Lightweight, nonpublic class for storing a singly linked node."""
        __slots__ = ('element', 'prev', 'next')

        def __init__(self, element, prev, next):
            self.element = element
            self.prev = prev
            self.next = next

    def __init__(self):
        """Create an empty list."""
        self.header = self.Node(None, None, None)
        self.trailer = self.Node(None, None, None)
        self.header.next = self.trailer
        self.trailer.prev = self.header
        self.size = 0

    def __len__(self):
        """Return the number of elements in the stack."""
        return self.size

    def is_empty(self):
        """Return True if the stack is empty."""
        return self.size == 0

    def insert_between(self, e, predecessor, successor):
        """Add element e between two existing nodes and return new node."""
        newest = self.Node(e, predecessor, successor)
        predecessor.next = newest
        successor.prev = newest
        self.size += 1
        return newest

    def delete_node(self, node):
        """Delete non-sentinel node from the list and return its element."""
        predecessor = node.prev
        successor = node.next
        predecessor.next = successor
        successor.prev = predecessor
        self.size -= 1
        element = node.element
        node.prev = node.next = node.element = None
        return element
