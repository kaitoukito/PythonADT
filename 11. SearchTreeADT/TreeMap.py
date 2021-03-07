import LinkedBinaryTree
import MapBase


class TreeMap(LinkedBinaryTree.LinkedBinaryTree, MapBase.MapBase):
    """Sorted map implementation using a binary search tree."""

    # -------------------- override Position class --------------------
    class Position(LinkedBinaryTree.LinkedBinaryTree.Position):
        def key(self):
            """Return key of map's key-value pair."""
            return self.element()._key

        def value(self):
            """Return value of map's key-value pair."""
            return self.element()._value

    # -------------------- nonpublic utilities --------------------
    def _subtree_search(self, p, k):
        """Return Position of p's subtree having key k, or last node searched."""
        if k == p.key():
            return p
        elif k < p.key():
            if self.left(p) is not None:
                return self._subtree_search(self.left(p), k)
        else:
            if self.right(p) is not None:
                return self._subtree_search(self.right(p), k)
        return p

    def _subtree_first_position(self, p):
        """Return Position of first item in subtree rooted at p."""
        walk = p
        while self.left(walk) is not None:
            walk = self.left(walk)
        return walk

    def _subtree_last_position(self, p):
        """Return Position of last item in subtree rooted at p."""
        walk = p
        while self.right(walk) is not None:
            walk = self.right(walk)
        return walk

    def first(self):
        """Return the first Position in the tree (or None if empty)."""
        return self._subtree_first_position(self.root()) if len(self) > 0 else None

    def last(self):
        """Return the last Position in the tree (or None if empty)."""
        return self._subtree_last_position(self.root()) if len(self) > 0 else None

    def before(self, p):
        """Return the Position just before p in the natural order.

        Return None if p is the first position.
        """
        self._validate(p)
        if self.left(p):
            return self._subtree_last_position(self.left(p))
        else:
            # walk upward
            walk = p
            above = self.parent(walk)
            while above is not None and walk == self.left(above):
                walk = above
                above = self.parent(walk)
            return above

    def after(self, p):
        """Return the position just after p in the natural order.

        Return None if p is the last position.
        """
        self._validate(p)
        if self.right(p):
            return self._subtree_first_position(self.right(p))
        else:
            # walk upward
            walk = p
            above = self.parent(walk)
            while above is not None and walk == self.right(above):
                walk = above
                above = self.parent(walk)
            return above

    def find_position(self, k):
        """Return position with key k, or else neighbour (or None if empty)."""
        if self.is_empty():
            return None
        else:
            p = self._subtree_search(self.root(), k)
            self._rebalance_access(p)   # hook for balanced tree subclasses
            return p

    def find_min(self):
        """Return (key, value) pair with minimum key (or None if empty)."""
        if self.is_empty():
            return None
        else:
            p = self.first()
            return p.key(), p.value()   # tuple

    def find_ge(self, k):
        """Return (key, value) pair with least key greater than or equal to k.

        Return None if there does not exists such a key.
        """
        if self.is_empty():
            return None
        else:
            p = self.find_position(k)
            if p.key() < k:
                p = self.after(p)
            return p.key(), p.value() if p is not None else None

    def find_range(self, start, stop):
        """Iterate all (key, value) pairs such that start <= key < stop.

        If start is None, iteration begins with minimum key of map.
        If stop is None, iteration continues through the maximum key of map.
        """
        if not self.is_empty():
            if start is None:
                p = self.first()
            else:
                # we initialize p with logic similar to find_ge
                p = self.find_position(start)
                if p.key() < start:
                    p = self.after(p)
            while p is not None and (stop is None or p.key() < stop):
                yield p.key(), p.value()    # tuple
                p = self.after(p)

    def __getitem__(self, k):
        """Return value associated with key k (raise KeyError if not found)."""
        if self.is_empty():
            raise KeyError('Key Error: ' + repr(k))
        else:
            p = self._subtree_search(self.root(), k)
            self._rebalance_access(p)   # hook for balanced tree subclasses
            if k != p.key():
                raise KeyError('Key Error: ' + repr(k))
            return p.value()

    def __setitem__(self, k, v):
        """Assign value v to key k, overwriting existing value if present."""
        if self.is_empty():
            leaf = self._add_root(self._Item(k, v))     # from LinkedBinaryTree
        else:
            p = self._subtree_search(self.root(), k)
            if p.key() == k:
                p.element()._value = v      # replace exiting item value
                self._rebalance_access(p)   # hook for balanced tree subclasses
                return
            else:
                item = self._Item(k, v)
                if p.key() < k:
                    leaf = self._add_right(p, item)     # inherited from LinkedBinaryTree
                else:
                    leaf = self._add_left(p, item)      # inherited from LinkedBinaryTree
            self._rebalance_insert(leaf)                # hook for balanced tree subclasses

    def __iter__(self):
        """Generate an iteration of all keys in the map in order."""
        p = self.first()
        while p is not None:
            yield p.key()
            p = self.after(p)

    def delete(self, p):
        """Remove the item at given Position."""
        self._validate(p)
        if self.left(p) and self.right(p):  # p has two children
            replacement = self._subtree_last_position(self.left(p))
            self._replace(p, replacement.element())
            p = replacement
        # now p has at most one child
        parent = self.parent(p)
        self._delete(p)                 # inherited from LinkedBinaryTree
        self._rebalance_delete(parent)  # hook for balanced tree subclasses

    def __delitem__(self, k):
        """Remove item associated with key k (raise KeyError if not found)."""
        if not self.is_empty():
            p = self._subtree_search(self.root(), k)
            if k == p.key():
                self.delete(p)
                return
            self._rebalance_access(p)   # hook for balanced tree subclasses
        raise KeyError('Key Error: ' + repr(k))

    def _rebalance_insert(self, p): pass
    def _rebalance_delete(self, p): pass
    def _rebalance_access(self, p): pass

    def _relink(self, parent, child, make_left_child):
        """Relink parent node with child node (we allow child to be None)."""
        if make_left_child:
            parent._left = child
        else:
            parent._right = child

    def _rotate(self, p):
        """Rotate Position p above its parent."""
        x = p._node
        y = x._parent
        z = y._parent
        if z is None:
            x._parent = None                    # x becomes root
        else:
            self._relink(z, x, y == z._left)    # x becomes a direct child of z
        # now rotate x and y, including transfer of middle subtree
        if x == y._left:
            self._relink(y, x._right, True)
            self._relink(x, y, False)
        else:
            self._relink(y, x._left, False)
            self._relink(x, y, True)

    def _restructure(self, x):
        """Perform tri-node restructure of Position x with parent/grandparent."""
        y = self.parent(x)
        z = self.parent(y)
        if(x == self.right(y)) == (y == self.right(z)):
            self._rotate(y)
            return y
        else:
            self._rotate(x)
            self._rotate(x)
            return x
