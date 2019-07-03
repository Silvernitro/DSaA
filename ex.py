class Empty(Exception):
    pass

class _DoublyLinkedList():
    class _Node():
        __slots__='_element', '_prev', '_next'
        def __init__(self, element, prev, next):
            self._element=element
            self._prev=prev
            self._next=next

    def __init__(self):
        """Create an empty list"""
        self._header=_Node(None, None, None)
        self._trailer=_Node(None, None, None)
        self._header._prev=self._trailer
        self._trailer._next=self._header
        self._size=0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size==0

    def _insert_between(self, element, before, after):
        new_node=Node(element, before, after)
        before._next=element
        after._prev=element
        self._size+=1
        return new_node

    def _delete_node(self, node):
        before=node._prev
        after=node._next
        before._next=after
        after._prev=before
        element=node._element
        node._element, node._prev, node._next=None, None, None
        self._size-=1
        return element

    def reverse(self):
        current=self._header
        while current is not self._header:
            prev=current._prev
            next=current._next
            current._next=prev
            current._prev=next
            current=next

class LinkedDeque(_DoublyLinkedList):
    def first(self):
        return self._header._next

    def last(self):
        return self._trailer._prev

    def insert_first(self, element):
        self._insert_between(element, self._header, self._header._next)

    def insert_last(self, element):
        self._insert_between(element, self._trailer._prev, self._trailer)

    def delete_first(self):
        if self.is_empty():
            raise Empty("The deque is empty.")
        self._delete_node(self, self._trailer._prev)

    def delete_last(self):
        if self.is_empty():
            raise Empty("The deque is empty.")
        self._delete_node(self, self._header._next)

class PositionList(_DoublyLinkedList):
    class Position():
        def __init__(self, container, node):
            self._container=container
            self._node=node

        def element(self):
            return self._node._element

        def __eq__(self, other):
            return type(self) is type(other) and self._node is other_node

        def __ne__(self, other):
            return not (self==other)

    def _validate(self, p):
        """Returns the node associated with the given position only if 
        the position is valid."""
        if not isinstance(p, self.Position):
            raise TypeError("p is not a valid Position type.")
        if p._container is not self:
            raise ValueError("p is not a position in this list.")
        if p._node.element is None:
            raise ValueError("p is no longer a valid position (deprecated).")
        return p._node

    def _make_position(self, node):
        """Returns a position instance for the node given."""
        if node is self._header or node is self._trailer:
            raise None
        return Position(self, node)

    def first(self):
        """returns the first Position in the list"""
        return self._make_position(self._header._next)

    def last(self):
        """returns the last Position in the list"""
        return self._make_position(self._trailer._prev)

    def before(self, p):
        """returns the position before p in the list"""
        node=self._validate(p)
        return self._make_position(node._prev)

    def after(self, p):
        """returns the position after p in the list"""
        node=self._validate(p)
        return self._make_position(node._after)

    def __iter__(self):
        """generates the forward iteration of the list"""
        cursor=self.first()
        while cursor is not None:
            yield cursor.element()
            cursor = self.after(cursor)

    def _insert_between(self, e, predecessor, successor):
        """Utility function similar to the DoublyLinkList._insert_between, but
        returns a Position instance instead of a Node instance."""
        node = super()._insert_between(e, predecessor, successor)
        return self._make_position(node)

    def add_first(self, e):
        return self._insert_between(e, self._header, self._header._next)

    def add_last(self, e):
        return self._insert_between(e, self._trailer._prev, self._trailer)

    def add_before(self, p, e):
        original=self._validate(p)
        return self._insert_between(e, original._prev, original)

    def add_after(self, p, e):
        original=self._validate(p)
        return self._insert_between(e, original, original._next)

    def delete(self, p):
        node=self._validate(p)
        return self._delete_node(node)

    def replace(self, p, e):
        original=self._validate(p)
        original_element=original._element
        original._element=e
        return original._element

    def max_element(self):
        """returns the maximum element in the list"""
        marker=self.first()
        max_val=marker.element()
        while marker is not self.last():
            if marker.element()>max_val:
                max_val=marker.element()
            marker=self.after(marker)
        return max_val

    def find(self,e):
        """returns the first position that matches the given element"""
        current=self.first()
        while current is not self.last():
            if current.element()==e:
                return current
            current=self.after(current)
        return None

    def find_recursive(self,e):
        """a recursive implementation of self.find()"""
        p=self.first()
        def find(self,p,e):
            if p.element()==e:
                return p
            elif p is self.last():
                return None
            else:
                find(self.after(p),e)
        return find(p,e)

    def __reversed__(self):
        """iterates through the list backwards"""
        current=self.last()
        while current is not None:
            yield current.element()
            current=self.before(current)

    def swap(self,p,q):
        p_node=self._validate(p)
        q_node=self._validate(q)
        if self.before(p) is q or self.before(q) is p:
            p_node._prev._next = q_node
            q_node._next._prev = p_node
            p_node._prev, q_node._prev = q_node, p_node._prev
            p_node._next, q_node._next = q_node._next, p_node
        p_node._prev._next, p_node._next._prev = q_node, q_node
        q_node._prev._next, q_node._next._prev = p_node, p_node
        p_node._next, p_node._pre, q_node_._next, q_node._prev= q_node._next,\
        q_node._prev, p_node._next, p_node._prev

class LinkedStack():
    class _Node():
        __slots__='_element', '_next'
        def __init__(self, element, next):
            self._element=element
            self._next=next

    def __init__(self):
        self._header=self._Node(None, None)
        self._size=0

    def _is_empty(self):
        return self._size==0

    def __len__(self):
        return self._size

    def push(self, e):
        self._header._next=self._Node(e, self._header._next)
        self._size+=1

    def pop(self):
        if self._is_empty():
            raise Empty("The stack is empty.")
        answer=self._header._next
        self._header._next=answer._next
        self._size-=1
        return answer._element

    def top(self):
        if self._is_empty():
            raise Empty("The stack is empty.")
        return self._header._next._element 

class RecursiveList():
    def __init__(self, element, rest=None):
        self._element=element
        self._rest=rest

    def add(self, e):
        return RecursiveList(e, self)

    def __str__(self):
        data=[]
        def recursive_print(self):
            if self._rest is None:
                data.append(self._element)
            else:
                data.append(self._element)
                data.append(recursive_print(self._rest))
        recursive_print(self)
        return(", ".join(str(x) for x in data))
