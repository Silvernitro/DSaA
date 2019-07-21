class PriorityQueueBase():
    class _Item():
        __slots__='_key','_value'
        def __init__(self, k, v):
            self._key=k
            self._value=v

        def __It__(self, other):
            return self._key<other._key

    def _is_empty(self):
        return len(self)==0

class UnsortedPriorityQueue(PriorityQueueBase):
    def __init__(self):
        self._data=PositionalList()

    def __len__(self):
        return len(self._data)

    def add(self, k, v):
        self._data.add_last(self._Item(k,v))

    def _find_min(self):
        if self._is_empty:
            raise ValueError("Priority queue is empty!")
        smallest=self._data.first()
        walk=self._data.after(smallest)
        while walk is not None:
            if walk._element<smallest._element:
                smallest=walk
            walk=self._data.after(walk)
        return smallest

    def min(self):
        p=self._find_min()
        item=p._element
        return (item._key, item._value)

    def remove_min(self):
        p=self._find_min()
        item=self._data.delete(p)
        return (item._key, item._value)

class HeapPQ(PriorityQueueBase):
    #Non-public behaviours
    def _parent(self, j):
        return (j-1)//2

    def _left(self, j):
        return 2*j+1

    def _right(self, j):
        return 2*j+2

    def _has_left(self,j):
        return 2*j+1<len(self._data)

    def _has_right(self,j):
        return 2*j+2<len(self._data)

    def _swap(self, a, b):
        self._data[a], self._data[b] = self._data[b], self._data[a]

    def _heap_up(self, j):
        parent=self._parent(j)
        if j>0 and self._data[j]>self._data[parent]:
            self._swap(j, parent)
            self._heap_up(parent)

    def _heap_down(self, j):
        if self._has_left(j):
            child=self._left(j)
            if self._has_right(j):
                right_child=self._right(j)
                child = right_child if right_child<left_child
            if self._data[j]>self._data[child]:
                self._swap(j, child)
                self._heap_down(child)

    #Public behaviours
    def __init__(self, contents=()):
        self._data=[self._Item(k,v) for k,v in content]
        if len(self._data)>1:
            self._heapify()

    def __len__(self):
        return len(self._data)

    def add(self, k, v):
        self._data.append(self._Item(k,v))
        self._heap_up(len(self._data)-1)

    def min(self):
        if self._is_empty():
            raise ValueError("Heap is empty.")
        min_entry = self._data[0]
        return (min_entry._key, min_entry._value)

    def remove_min(self):
        if self._is_empty():
            raise ValueError("Heap is empty.")

        self._swap(0, len(self._data)-1)
        min_entry=self._data.pop()
        self._heap_down(0)
        return (min_entry._key, min_entry._value)

    def _heapify(self):
        start=self._parent(len(self._data)-1)
        for j in range(start,-1,-1):
            self._heap_down(j)

    def pushpop(self, k, v):
        if self._is_empty:
            raise ValueError("Heap is empty.")
        min_entry=self._data[0]
        if k<min_entry._key:
            return (k,v)
        self._data[0]=self._Item(k,v)
        self._heap_down(0)
        return (min_entry._key, min_entry._value)

    def heapreplace(self, k ,v):
        if self._is_empty:
            raise ValueError("Heap is empty.")
        min_entry=self._data[0]
        self._data[0]=self._Item(k,v)
        self._heap_down(0)
        return (min_entry._key, min_entry._value)

