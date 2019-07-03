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

class MutableLinkedBinaryTree(LinkedBinaryTree):
    def add_left(self, p, e):
        return self._add_left(p, e)

    def add_right(self, p ,e):
        return self._add_right(p,e)

    def delete(self, p):
        return self._delete(p)

    def replace(self, p, e):
        return self._replace(p, e)
