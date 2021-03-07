class LinkedStack:
    """LIFO Stack implementation using a singly linked list for storage."""

    # -------------------- nested Node class --------------------
    class Node:
        """Lightweight, nonpublic class for storing a singly linked node."""
        __slots__ = ('element', 'next')

        def __init__(self, element, next):
            self.element = element
            self.next = next

    # -------------------- stack methods --------------------
    def __init__(self):
        """Create an empty stack."""
        self.head = None
        self.size = 0

    def __len__(self):
        """Return the number of elements in the stack."""
        return self.size

    def is_empty(self):
        """Return True if the stack is empty."""
        return self.size == 0

    def push(self, e):
        """Add element e to the top of the stack."""
        self.head = self.Node(e, self.head)    # create and link a new node
        self.size += 1

    def top(self):
        """Return (but do not remove) the element at the top of the stack.

        Raise Empty exception if the stack is empty.
        """
        if self.is_empty():
            raise Exception('Stack is empty')
        return self.head.element

    def pop(self):
        """Remove and return the element from the top of the stack (i.e. LIFO).

        Raise Empty exception if the stack is empty.
        """
        if self.is_empty():
            raise Exception('Stack is empty')
        answer = self.head.element
        self.head = self.head.next
        self.size -= 1
        return answer
