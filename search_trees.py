class Tree():
    class Position():
        def element(self):
            raise NotImplementedError('must be implemented by subclass')
        def __eq__(self, other):
            raise NotImplementedError('must be implemented by subclass')
        def __ne__(self, other):
            return not(self==other)

    def root(self):
        raise NotImplementedError('must be implemeneted by subclass')

    def is_root(self, p):
        return (p==self.root())

    def parent(self, p):
        raise NotImplementedError('must be implemeneted by subclass')

    def num_children(self, p):
        raise NotImplementedError('must be implemeneted by subclass')

    def children(self, p):
        raise NotImplementedError('must be implemeneted by subclass')

    def is_leaf(self, p):
        return (self.num_children(p)==0)

    def __len__(self):
        raise NotImplementedError('must be implemeneted by subclass')

    def is_empty(self):
        return (self.len()==0)

    def iter(self):
        raise NotImplementedError('must be implemeneted by subclass')

    def depth(self, p):
        if self.is_root(p):
            return 0
        else:
            return 1+self.depth(self.parent(p))

    def _height_aux(self, p):
        if self.is_leaf(p):
            return 0
        else:
            return 1+max(self._height_aux(child) for child in self.children(p))

    def height(self, p=None):
        if p is None:
            p=self.root()
        return _height_aux(p)

    def _subtree_preorder(self, p):
        """A utility generator for preorder traversal of a subtree at p"""
        yield p
        for c in self.children(p):
            for other in self._subtree_preorder(c):
                yield other

    def preorder(self):
        """Preorder generator of all positions in the tree"""
        if not self._is_empty():
            for p in self._subtree_preorder(self.root()):
                yield p

    def positions(self):
        """Generates a preorder iteration of all positions in the tree"""
        return self.preorder()

    def _subtree_postorder(self, p):
        """A utility generator for postorder traversal of a subtree at p"""
        for c in self.children(p):
            for other in self._subtree_postorder(c):
                yield other
        yield p

    def postorder(self):
        """Postorder generator for all positions in the tree"""
        if not self._is_empty:
            for p in self._subtree_postorder(self.root()):
                yield p

class BinaryTree(Tree):
    def left(self, p):
        raise NotImplementedError('must be implemeneted by subclass')

    def right(self, p):
        raise NotImplementedError('must be implemeneted by subclass')

    def sibling(self, p):
        parent=self.parent(p)
        if parent is None:
            return None
        else:
            if p==self.left(parent):
                return self.right(parent)
            else:
                return self.left(parent)

    def children(self, p):
        if self.left(p) is not None:
            yield self.left(p)
        if self.right(p) is not None:
            yield self.right(p)

    def num_children(self, p):
        """Returns the number of children for position p"""
        count=0
        for child in self.children(p):
            count+=1
        return count

class LinkedBinaryTree(BinaryTree):
    class _Node:
        def __init__(self, element, parent=None, left=None, right=None):
            self._element=element
            self._parent=parent
            self._left=left
            self._right=right

    class Position(BinaryTree.Position):
        def __init__(self, node, container):
            self._container=container
            self._node=node

        def element(self):
            return self._node._element

        def __eq__(self, other):
            return type(self) is type(other) and self._node is other._node

    def _validate(self, p):
        if not isinstance(p, self.Position):
            raise TypeError("input is not a valid Position")
        if p._container is not self:
            raise ValueError("position given is not part of this tree")
        if p._node._parent is p._node:
            raise ValueError("this position has been deprecated")
        else:
            return p._node

    def _make_position(self, node):
        """Wraps a node in a Position and returns it if the node is not the
        root"""
        return Position(node, self) if node is not None else None

    def __init__(self):
        self._root=None
        self._size=0

    def __len__(self):
        return self._size

    def root(self):
        return self._make_position(self._root)

    def parent(self, p):
        node=self._validate(p)
        return self._make_position(node._parent)

    def left(self, p):
        node=self._validate(p)
        return self._make_position(node._left)

    def right(self, p):
        node=self._validate(p)
        return self._make_position(node._right)

    def num_children(self, p):
        node=self._validate(p)
        child_count=0
        if node._left is not None:
            child_count+=1
        if node._right is not None:
            child_count+=1
        return child_count

    def _add_root(self, e):
        if self._root is not None:
            raise ValueError("Tree is not empty, a root exists!")
        self._root=self._Node(e)
        self._size=1
        return self._make_position(self._root)

    def _add_left(self, p, e):
        node=self._validate(p)
        if node is None:
            raise ValueError("cannot add element to an invalid node")
        if node._left is not None:
            raise ValueError("node already has a left child")
        node._left=self._Node(e, parent=node)
        self._size+=1
        return self._make_position(node._left)

    def _add_right(self, p, e):
        node=self._validate(p)
        if node is None:
            raise ValueError("cannot add element to an invalid node")
        if node._right is not None:
            raise ValueError("node already has a right child")
        node._right=self._Node(e, parent=node)
        self._size+=1
        return self._make_position(node._right)

    def _delete(self, p):
        node=self._validate(p)
        if node is None:
            raise ValueError("cannot delete an invalid node")
        if self.num_children(p)==2:
            raise ValueError("node with 2 children cannot be deleted")
        child=node._left if node._left else node._right
        if node is self._root:
            self._root=child
        parent=node._parent
        child._parent=parent
        if node is parent._left:
            parent._left=child
        else:
            parent._right=child
        node._parent=node
        self._size-=1
        return node._element

    def _replace(self, p, e):
        node=self._validate(p)
        if node is None:
            raise ValueError("the node is invalid")
        old=node._element
        node._element=e
        return old

    def _subtree_inorder(self, p):
        """Utility generator for inorder traversal of a binary subtree at p"""
        if self.left(p):
            yield self._subtree_inorder(self.left(p))
        yield p
        if self.right(p):
            yield self._subtree_inorder(self.right(p))

    def inorder(self):
        """Generator for inorder traversal of the binary subtree"""
        if not self._is_empty():
            for other in _subtree_inorder(self.root()):
                yield other

    def positions(self):
        """Generates an iteration  of all positions. Overrides parent method to
        use inorder traversal instead"""
        return self.inorder()

class MapBase(MutableMapping):
    """Serves as a the abstract base class for all maps."""
    class _Item:
        __slots__='_key', '_value'

        def __init__(self, k ,v):
            self._key=k
            self._value=k
        def __eq__(self, other):
            return self._key==other._key
        def __ne__(self, other):
            return not (self==other)
        def __It__(self, other):
            return self._key<other._key

class TreeMap(LinkedBinaryTree, MapBase):
    """Sorted map implementation using a Binary Search Tree."""

    class Position(LinkedBinaryTree.Position):
        def key(self):
            return self.element()._key

        def value(self):
            return self.element()._value

    #Non-public utilities
    def _subtree_search(self, p, k):
        """Returns Position of p's subtree that contains k, or last node search
        if k does not exist."""
        if p._key == k:
            return p
        elif p._key < k:
            if self.left(p) is not None:
                self._subtree_search(self.left(p), k)
        else:
            if self.right(p) is not None:
                self._subtree_search(self.right(p), k)
        return p

    def _subtree_search_v2(self, p, k):
        while p._key != k and p is not None:
            if p._key < k:
                p = self.left(p)
            else:
                p = self.right(p)
        return p

    def _subtree_first_position(self, p):
        walk = p
        while self.left(p) is not None:
            walk = self.left(p)
        return walk

    def _subtree_last_position(self, p):
        walk = p
        while self.right(p) is not None:
            walk = self.right(p)
        return walk

    #Balancing utilities
    def _rebalance_insert(self, p):
        pass

    def _rebalance_delete(self, p):
        pass

    def _rebalance_access(self, p):
        pass

    def _relink(self, parent, child, is_child_left):
        """Links child node to parent node. is_child_left is a boolean that determines if
        child is left child of the parent or not."""
        if is_child_left:
            parent._left = child
        else:
            parent._right = child
        if child is not None:
            child._parent = parent

    def _rotate(self, p):
        """Rotates node at position p above its parent."""
        x = p._node
        y = x._parent
        z = y._parent

        if z is None:
            self._root = x
        else:
            self._relink(z, x, y == self.left(z))
        if x == y._left:
            self._relink(y, self.right(x), True)
            self._relink(x, y, False)
        else:
            self._relink(y, self.left(x), False)
            self._relink(x, y, True)

    def _restructure(self, x):
        """Performs a trinode restructure of Position x with its
        parent/grandparent."""
        y = self.parent(x)
        z = self.parent(y)
        #checks if x,y,z are aligned
        if ((self.right(z) == y) and (self.right(y) == x))\
                or ((self.left(z) == y) and (self.left(y) == x)):
            self._rotate(x)
            return z
        else:
            self._rotate(x)
            self._rotate(x)
            return x

    #Public utilities
    def first(self):
        if len(self) > 0:
            return self._subtree_first_position(self.root())
        else:
            return None
    def last(self):
        if len(self) > 0:
            return self._subtree_last_position(self.root())
        else:
            return None

    def after(self, p):
        self._validate(p)
        if self.right(p):
            return self._subtree_first_position(self.right(p))
        else:
            walk = p
            ancestor = self.parent(walk)
            while walk is not None and walk == self.right(ancestor):
                walk = ancestor
                ancestor = self.parent(walk)
            return ancestor

    def before(self, p):
        self._validate(p)
        if self.left(p):
            return self._subtree_last_position(self.left(p))
        else:
            walk = p
            ancestor = self.parent(walk)
            while walk is not None and walk == self.left(ancestor):
                walk = ancestor
                ancestor = self.parent(walk)
            return ancestor

        def find_position(self, k):
            if self._is_empty():
                return None
            p = self._subtree_search(self.root(), k)
            self._rebalance_access(p)
            return p

    def find_position(self, k):
        """Returns the Position of k in tree, or neightbour if k does not
        exist."""
        if self.is_empty():
            return None
        else:
            p = self._subtree_search(self.root(), k)
            self._rebalance_access(p)
            return p

    def find_min(self):
        """Returns key-value pair of the smallest key in the tree."""
        if self.is_empty():
            return None
        else:
            p  = self.first()
            return (p.key(), p.value())

    def find_ge(self, k):
        """Returns the key-value pair of the smallest key greater than or equal
        to k."""
        if self.is_empty():
            return None
        else:
            p = self._subtree_search(self.root(), k)
            if self.key(p) < k:
                p = self.after(p)
            return (p.key(), p.value()) if p is not None else None

    def find_range(self, start, stop):
        """Generates an iteration of all Positions with start <= key < stop.

        If start is None, iteration starts from smallest key.
        If stop is None, iteration continues till largest key."""

        if self.is_empty():
            return None
        else:
            if start is None:
                p = self.first()
            else:
                p = self.find_position(start)
                if p.key() < start:
                    p = self.after(p)
            while p is not None and (stop is None or p.key() < stop):
                yield p
                p = self.after(p)

    #Private core map utilities
    def __getitem__(self, k):
        if self.is_empty():
            raise KeyError("Key Error: " +k)
        p = self._subtree_search(self.root(), repr(k))
        self._rebalance_access(p)
        if p.key() != k:
            raise KeyError("Key Error: " + repr(k))
        return p.value()
            p = self._subtree_search(self.root(), start)

    def __setitem__(self, k, v):
        if self.is_empty():
            leaf = self._add_root(self._Item(k, v))
        else:
            p = self._subtree_search(self.root(), k)
            if p.key() == k:
               p.element()._value = v
               p._rebalance_access(p)
               return
           else:
               item = self._Item(k, v)
               if p.key() < k:
                   leaf = self._add_right(p, item)
                else:
                    leaf = self._add_left(p, item)
        self._rebalance_insert(leaf)

    def __iter__(self):
        if not self.is_empty:
            p = self.first()
            while p is not None:
                yield p
                p = self.after(p)

    def delete(self, p):
        """Utility function to delete a position in a tree."""
        self._validate(p)
        if self.left(p) and self.right(p):
            replacement = self._subtree_last_position(self.left(p))
            self._replace(p, replacement.element())
            p = replacement
        parent = self.parent(p)
        self._delete(p)
        self._rebalance_delete(parent)

    def __del__(self, k):
        if self.is_empty():
            raise KeyError("Key Error: " + repr(k))
        p = self._subtree_search(self.root(), k)
        self._rebalance_access(p)
        if p.key() != k:
            raise KeyError("Key Error: " + repr(k))
        else:
            self.delete(p)
            return

class AVLTreeMap(TreeMap):
    """Sorted Map implementation using an AVL Tree."""

    class _Node(TreeMap._Node):
        """Node class for AVL tree to maintain height value for balancing."""
        __slots__ = "_height"
        def __init__(self, element, parent=None, left=None, right=None):
            super().__init__(element, parent, left, right)
            self._height = 0

        def left_height(self):
            return self._left._height if self._left else 0

        def right_height(self):
            return self.right._height if self._right else 0

#Positional-based utilities for balancing
    def _recompute_height(self, p):
        p._node._height = 1 + max(p._node.left_height(), p._node.right_height())

    def _is_balanced(self, p):
        return abs(p._node.left_height() - p._node.right_height()) <= 1

    def _tall_child(self, p, favorleft = False):
        """Returns the tallest child of Position p. In case of a tie, favorleft
        acts as a tie-breaker."""
        if p._node.left_height + (1 if favorleft else 0) >
        p._node.right_height:
            return self.left(p)
        else:
            return self.right(p)

    def _tall_grandchild(self, p):
        """Returns tallest grandchild of Position p."""
        child = self._tall_child(p)
        alignment = (child == self.left(p))
        return self._tall_child(p, alignement)

    def _rebalance(self, p):
        """Rebalances the AVL Tree."""
        ancestor = p
        while ancestor is not None:
            old_height = self._node._height
            if not self._is_balanced(ancestor):
                ancestor = self._restructure(self._tall_grandchild(ancestor))
                self._recompute_height(self.left(ancestor))
                self._recompute_height(self.right(ancestor))
            new_height = self._recompute_height(ancestor)
            if old_height == new_height:
                    p = None
            ancestor = self.parent(ancestor)

#Override balancing hooks
    def _rebalance_insert(self, p):
        self._rebalance(p)

    def _rebalance_delete(self, p):
        self._rebalance(p)

class SplayTreeMap(TreeMap):
    """Sorted Map implementation using a Splay Tree."""

    def _splay(self, p):
        while p != self.root():
            parent = self.parent(p)
            grandparent = self.parent(parent)
            if grandparent is None:
                #zig operation
                self._rotate(p)
            elif (p == self.left(parent)) == (parent ==
                    self.left(grandparent)):
                #zig-zig operation
                self._rotate(parent)
                self._rotate(p)
            else:
                #zig-zag operation
                self._rotate(p)
                self._rotate(p)

    def _rebalance_access(self, p):
        self._splay(p)

    def _rebalance_insert(self, p):
        self._splay(p)

    def _rebalance_delete(self, p):
        if p is not None:
            self._splay(p)
