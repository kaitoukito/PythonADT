import DoublyLinkedBase


class PositionList(DoublyLinkedBase.DoublyLinkedBase):
    # -------------------- nested Position class --------------------
    class Position:
        """An abstract representing the location of a single element."""

        def __init__(self, container, node):
            """Constructor should not be invoked by user."""
            self.container = container
            self.node = node

        def element(self):
            """Return the element stored at this Position."""
            return self.node.element

        def __eq__(self, other):
            """Return True if other Position represents the same location."""
            return type(other) is type(self) and other.node is self.node

        def __ne__(self, other):
            """Return True if other does not represents the same location."""
            return not (self == other)
