import random

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

class UnsortedTableMap(MapBase):
    def __init__(self):
        self._table=[]

    def __getitem__(self, k):
        """Returns value associated with key k. Raises KeyError if k is not found."""
        for item in self._table:
            if item._key==k:
                return item._value
        raise KeyError("Key error: "+k)

    def __setitem__(self,k,v):
        """Assigns v to item with key k. Overwrites existing value if any.."""
        for item in self._table:
            if item._key==k:
                item._value=v
                return
        self._table.append(self._Item(k,v))

    def __delitem__(self,k):
        """Deletes item associated with key k. Raises KeyError if k is not
        found."""
        for j in range(len(self._table)):
            if self._table[j]._key==k:
                self._table.pop(j)
                return
        raise KeyError("Key error: "+k)

    def __len__(self):
        """Returns the no. of items in the map."""
        return len(self._data)

    def set_default(self, k, d):
        """Returns the value associated with k if k exists in map. Else sets
        value of k to d."""
        for item in self._table:
            if item._key == k:
                return item._value
            else:
                self._table.append(self._Item(k,d))

    def __iter__(self):
        """Generates an iteration of the map's keys.."""
        for item in self._table:
            return item._key

   def items(self):
       """Generates an interation of key-value pairs in the map in linear time."""
       for item in self._table:
           return (item._key, item._value)

class HashMapBase(MapBase):
    class _Item_hash:
        __slots__ = '_value', '_hash'

        def __init__(self, v, h):
            self._value = v
            self._hash = h

    def __init__(self, cap=10, p=109345121, load_threshold=0.5):
        self._table=[None]*cap
        self._n=0
        self._prime=p
        self._scale=1+random.randrange(p+1)
        self._shift=random.randrange(p)
        self._threshold=load_threshold

    def _hash_function(self,k):
        """Returns the hash code of k."""
        return (hash(k)*self._scale+self._shift)%self._prime%len(self._table)

    def __len__(self):
        """Returns the no. of key-value pairs stored in the map."""
        return len(self._table)

    def __getitem__(self, k):
        """Returns the item associated with k."""
        j=self._hash_function(k)
        return self._bucket_getitem(j,k)

    def __setitem__(self,k,v):
        """Sets k to be associated with v. Resizes the table to maintain load
        factor."""
        if v.isinstance(self._Item_hash):
            j = v._hash_code
            v = v._value
        else:
            j = self._hash_function(k)
        self._bucket_setitem(j, k, v)
        if self._n>len(self._table) * self._threshold:
            self._resize(2*len(self._table)-1)

    def __delitem__(self,k):
        """Deletes the item associated with k. Decrements n."""
        j=self._hash_function(k)
        self._bucket_delitem(j,k)
        self._n-=1

    def _resize(self,n):
        old_items=list(self.items())
        self._table=[None]*n
        self._n=0
        for (k,v) in old_items:
            self[k]=v

class ChainHashMap(HashMapBase):
    """Hash map implementation using separate chaining for collision
    resolution."""

    def _bucket_getitem(self,j,k):
        bucket = self._table[j]
        if bucket is None:
            raise KeyError("Key Error: "+repr(k))
        return bucket[k]._value

    def _bucket_setitem(self,j,k,v):
        #If bucket does not have an existing item, store new item directly to
        #bucket.
        if self._table[j] is None:
            self._table[j] = self._Item(k, self._Item_hash(v, j))
        #If updating an existing bucket with only one item:
        elif self._table[j]._key == k:
            self._table[j]._value._value = v
        #If collision occurs and a new item must be assigned to same bucket.
        else:
            old_item = self._table[j]
            self._table[j] = UnsortedTableMap()
            self._table[j][old_item._key] = old_item._value
            self._table[j][k] = self._Item_hash(v, j)
            self._n += 1

    def _bucket_delitem(self,j,k):
        """Deletes a key-val pair. Raises KeyError is key does not exist."""
        bucket = self._table[j]
        if bucket is None:
            raise KeyError("Key Error: "+repr(k))
        #If bucket stores a single item directly that matches search.
        elif bucket._key == k:
            self._table[j] = None
        else:
            del bucket[k]

    def __iter__(self):
        """Generates an iteration of all keys in the map."""
        for bucket in self._table:
            if bucket is not None:
                for key in bucket:
                    yield key

    def setdefault(self, k, d):
        """Returns the value of k if k is in the map. Else assigns the value d
        to key k."""
        j = self._hash_function(k)
        bucket = self._table[j]
        if bucket is None:
            self._table[j] = UnsortedTableMap()
        return self._table[j].setdefault(k, d)

class ProbeHashMap(HashMapBase):
    """A hash map that implements linear probing for open-addressing collision resolution."""
    _AVAIL = object()

    def _is_available(self, j):
        """Returns True if index j is empty or is available."""
        return self._table[j] is None or self._table[j] is ProbeHashMap._AVAIL

    def _find_slot(self, j, k):
        """Utility function to find the bucket for key k using linear probing.
        Returns False and the first available bucket if k is not found."""
        first_avail=None
        while True:
            if self._is_available(j):
                if first_avail is None:
                    first_avail = j
                if self._table[j] is None:
                    return (False, first_avail)
            elif k == self._table[j]._key:
                return (True, j)
            j = (j+1) % len(self._table)

    def _bucket_getitem(self, j, k):
        """Returns the value associated with k in the map."""
        found, slot = self._find_slot(j, k)
        if not found:
            raise KeyError("Key Error: " + repr(k))
        return self._table[slot]._value

    def _bucket_setitem(self, j, k, v):
        """Adds key k and value v to the map. Updates existing value of k if k
        already exists."""
        found, slot = self._find_slot(j, k)
        if not found:
            self._table[slot]=self._Item(k, v)
            self._n += 1
        else:
            self._table[slot]._value=v

    def _bucket_delitem(self, j, k):
        """Deletes the item associated with k."""
        found, slot = self._find_slot(j, k)
        if not found:
            raise KeyError("Key Error: " + repr(k))
        self._table[slot] = ProbeHashMap._AVAIL

    def __iter__(self):
        """Generates an iteration of keys in the map."""
        for j in range(len(self._table)):
            if not self._is_available(j):
                yield self._table[j]._key

    def setdefault(self, k, d):
        j = self._hash_function(k)
        found, slot = self._find_slot(j, k)
        if found:
            return self._table[slot]._value
        else:
            self._table[slot]._value = d

class SortedTableMap(MapBase):
    """A sorted search table implementation of a map."""

    #Non-public behaviours
    def _find_index(self, k, low, high):
        """Searches the map for k and returns its index using Binary Search.
        If k is not found, index of smallest element with key>k is returned."""
        if high<low:
            return high + 1
        mid = (low + high) // 2
        if self._table[mid] == k:
            return mid
        elif self._table[mid] < k:
            return self._find_index(k, mid + 1, high)
        else:
            return self._find_index(k, low, mid - 1)

    #Public Behaviours
    def __init__(self):
        self._table=[]

    def __len__(self):
        return len(self._table)

    def __getitem__(self, k):
        """Returns the value associated with k. Raises KeyError is not found."""
        index = self._find_index(k, 0, len(self._table)-1)
        if index == len(self._table) or self._table[index]._key != k:
            raise KeyError("Key error: " + repr(k))
        return self._table[index]._value

    def __setitem__(self, k, v):
        index = self._find_index(k, 0, len(self._table) - 1)
        if self._table[index]._key == k and index < len(self._table):
            self._table[index]._value = v
        else:
            self._table.insert(index, self._Item(k,v))
            self._n += 1

    def __delitem__(self, k):
        index = self._find_index(k, 0 ,len(self._table - 1))
        if index == len(self._table) or self._table[index]._key != k:
            raise KeyError("Key error: " + repr(k))
        self._table.pop(index)

    def __iter__(self):
        for item in self._table:
            yield item._key

    def find_min(self):
        if len(self._table) > 0:
            return (self._table[0]._key, self._table[0]._value)
        return None

    def find_max(self):
        if len(self._table) > 0:
            return (self._table[-1]._key, self._table[-1]._value)
        return None

    def find_ge(self, k):
        """Return the smallest item with key greater than or equal to k."""

        index = self._find_index(k, 0, len(self._table)-1)
        if index == len(self._table):
            return None
        return (self._table[index]._key, self._table[index]._value)

    def find_lt(self, k):
        """Return the largest item with key stricly less than k."""

        index = self._find_index(k, 0, len(self._table)-1)
        if index > 0:
            return (self._table[index-1]._key, self._table[index-1]._value)
        return None

    def find_gt(self, k):
        """Return the smallest item with key strictly larger than k."""

        index = self._find_index(k, 0, len(self._table)-1)
        if index == len(self._table):
            return None
        if self._table[index] == k:
            return (self._table[index+1]._key, self._table[index+1]._value)
        else:
            return (self._table[index]._key, self._table[index]._value)

    def find_range(self, start, stop):
        """Generates an iteration of (key, value) pairs for start <= key <
        stop.
        If start is None, iteration starts with minimum key in the map.
        If stop is None, iteration continues until the maximum key in the map."""

        if start is None:
            j=0
        else:
            j = self._find_index(start, 0, len(self._table)-1)
        while j < len(self._table) and (stop is None or self._table[j]._key <
                stop):
            yield (self._table[j]._key, self._table[j]._value)
            j += 1

    def find_all(self, k):
        """Generates an iteration of all items with key == k."""
        j = self._find_index(k, 0 , len(self._table)-1)
        while j < len(self._table) and self._table[j]._key == k:
            yield (self._table[j]._key, self._table[j]._value)
            j += 1
