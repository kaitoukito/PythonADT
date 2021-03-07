import BinaryTree


class LinkedBinaryTree(BinaryTree.BinaryTree):
    """Linked representation of a binary tree structure."""

    class _Node:    # Lightweight, nonpublic class for storing a singly linked node.
        __slots__ = ('element', 'parent', 'left', 'right')

        def __init__(self, element, parent=None, left=None, right=None):
            self.element = element
            self.parent = parent
            self.left = left
            self.right = right

    class Position(BinaryTree.BinaryTree.Position):
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

    def _validate(self, p):
        """Return associated node, if Position is valid."""
        if not isinstance(p, self.Position):
            raise TypeError('p must be proper Position type')
        if p.container is not self:
            raise ValueError('p does not belong to this container')
        if p.node.parent is p.node:     # convention for deprecated nodes
            raise ValueError('p is no longer valid')
        return p.node

    def _make_position(self, node):
        """Return Position instance for given node (or None if no node)."""
        return self.Position(self, node) if node is not None else None

    # -------------------- binary tree constructor --------------------
    def __init__(self):
        """Create an initially empty binary tree."""
        self._root = None
        self._size = 0

    # -------------------- public accessors --------------------
    def __len__(self):
        """Return the total number of elements in the tree"""
        return self._size

    def root(self):
        """Return Position representing the tree's root (or None if empty)."""
        return self._make_position(self._root)

    def parent(self, p):
        """Return Position representing the tree's parent (or None if empty)."""
        node = self._validate(p)
        return self._make_position(node.parent)

    def left(self, p):
        """Return the Position of p's left child (or None if no left child)."""
        node = self._validate(p)
        return self._make_position(node.left)

    def right(self, p):
        """Return the Position of p's right child (or None if no right child)."""
        node = self._validate(p)
        return self._make_position(node.right)

    def num_children(self, p):
        """Return the number of children that p has."""
        node = self._validate(p)
        count = 0
        if node.left is not None:
            count += 1
        if node.right is not None:
            count += 1
        return count

    # -------------------- non-public methods --------------------
    def _add_root(self, e):
        """Place element e at the root of an empty tree and return new Position.

        Raise ValueError if tree nonempty.
        """
        if self._root is not None:
            raise ValueError('Root exists')
        self._size = 1
        self._root = self._Node(e)
        return self._make_position(self._root)

    def _add_left(self, p, e):
        """Create a new left child for Position p, storing element e.

        Return the Position of new node.
        Raise ValueError if Position p is invalid or already has a left child.
        """
        node = self._validate(p)
        if node.left is not None:
            raise ValueError('Left child exists')
        self._size += 1
        node.left = self._Node(e, node)
        return self._make_position(node.left)

    def _add_right(self, p, e):
        """Create a new right child for Position p, storing element e.

        Return the Position of new node.
        Raise ValueError if Position p is invalid or already has a right child.
        """
        node = self._validate(p)
        if node.right is not None:
            raise ValueError('Right child exists')
        self._size += 1
        node.right = self._Node(e, node)
        return self._make_position(node.right)

    def _replace(self, p, e):
        """Replace the element at position p with e, and return old element."""
        node = self._validate(p)
        old = node.element
        node.element = e
        return old

    def _delete(self, p):
        """Delete the node at Position p, and replace it with its child, if any.

        Return the element that had been stored at Position p.
        Raise ValueError if Position p is invalid or p has two children.
        """
        node = self._validate(p)
        if self.num_children(p) == 2:
            raise ValueError('p has two children')
        child = node.left if node.left else node.right
        if child is not None:
            child.parent = node.parent
        if node is self._root:
            self._root = child
        else:
            parent = node.parent
            if node is parent.left:
                parent.left = child
            else:
                parent.right = child
        self._size -= 1
        node.parent = node
        return node.element

    def _attach(self, p, t1, t2):
        """Attach trees t1 and t2 as left and right subtrees of external p."""
        node = self._validate(p)
        if not self.is_leaf(p):
            raise ValueError('position must be leaf')
        if not type(self) is type(t1) is type(t2):
            raise ValueError('Tree types must match')
        self._size += len(t1) + len(t2)
        if not t1.is_empty():
            t1._root.parent = node
            node.left = t1._root
            t1._root = None
            t1._size = 0
        if not t2.isempty():
            t2._root.parent = node
            node.right = t2._root
            t2._root = None
            t2._size = 0
