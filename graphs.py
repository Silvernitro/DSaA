class Vertex:
    """Lightweight vertex structure for a graph."""
    __slots__ = "_element"

    def __init__(self, v):
        self._element = v

    def element(self):
        return self._element

    def __hash__(self):
        return hash(id(self))

class Edge:
    """Lightweight edge structure for a graph."""
    __slots__ = "_origin", "_destination", "_element"

    def __init__(self, origin, destination, element):
        self._origin = origin
        self._destination = destination
        self._element= element

    def endpoints(self):
        return self._origin, self._destination

    def opposite(self, v):
        return self._origin if v is self._destination else self._destination

    def element(self):
        return self._element

    def __hash__(self):
        return hash((self._origin, self._destination))

class Graph:
    """Implementation of a simple graph using an adjacency map."""
    def __init__(self, directed=False):
        self._outgoing = {}
        self._incoming = {} if directed else self._outgoing

    def is_directed(self):
        """Returns True if the graph is directed and False if otherwise."""
        return self._outgoing is not self._incoming

    def vertex_count(self):
        """Returns the number of vertices in the graph."""
        return len(self._outgoing)

    def vertices(self):
        """Returns a list of all vertices in the graph."""
        return self._outgoing.keys()

    def edge_count(self):
        """Returns the number of all edges in the graph."""
        total = sum(len(self._outgoing[vertex]) for vertex in self._outgoing)
        return total if self.is_directed else total//2

    def edges(self):
        """Returns a set of all edges in the graph."""
        result = set()
        for edge_map in self._outgoing.values():
            result.update(edge_map.values())
        return result

    def get_edge(self, u, v):
        """Returns the edge from u to v or None if not adjacent."""
        return self._outgoing[u].get(v)

    def degree(self, v, outgoing=True):
        """Returns the number of edges incoming/outgoing from/to v."""
        return len(self._outgoing[v]) if outgoing else len(self._incoming[v])

    def incident_edges(self, v, outgoing=True):
        """Generates an iteration of all edges incident to vertex v in the
        graph."""
        edge_map = self._outgoing if outgoing else self._incoming
        for edge in edge_map[v].values():
            yield edge

    def insert_vertex(self, element=None):
        """Insert a new Vertex with element into graph."""
        vertex = Vertex(element)
        self._outgoing[vertex] = {}
        if self.is_directed():
            self._incoming[vertex] = {}
        return vertex

    def insert_edge(self, u, v, x=None):
        """Insert an edge with origin y, destination v and element x into
        the graph."""
        e = Edge(u, v, x)
        self._outgoing[u][v] = e
        self._incoming[v][u] = e

    def remove_vertex(self, v):
        """Removes the vertex v from the graph and returns it."""
        for u in self._outgoing[v].keys():
            del self._incoming[u][v]
        if self.is_directed():
            for u in self._incoming[v].keys():
                del self._outgoing[u][v]
            del self._incoming[v]
        del self._outgoing[v]
        return v

    def remove_edge(self, u, v):
        """Removes the edge with origin u and destination v and returns the edge object."""
        edge = self.get_edge(u, v)
        del self._outgoing[u][v]
        del self._incoming[v][u]
        return edge

def dfs(g, u):
    """Perform a depth-first search of the undiscovered portion of Graph g at
    Vertex u."""
    discovered = {u: None}
    def inner_dfs(g, u, discovered):
        for edge in g.incident_edges(u):
            v = edge.opposite(u)
            if v not in discovered:
                discovered[v] = edge
                inner_dfs(g, v, discovered)
    inner_dfs(g, u, discovered)
    return discovered

def construct_path(u, v, discovered):
    """Returns a path from vertex u to vertex v. Returns empty list if they are
    not connected."""

    path=[]
    if v in discovered:
        path.append(v)
        walk = v
        while walk is not u:
            parent = discovered[walk].opposite(walk)
            path.append(parent)
            walk = parent
        path.reverse()
    return path

def dfs_complete(g):
    """Returns a dictionary mapping each vertex in Graph g to an integer that
    identifies its connected component."""
    forest = {}
    for u in g.vertices():
        if u not in forest:
            forest[u] = None
            dfs(g, u)

    component_map = {}
    component_id = 0
    for vert in forest:
        if forest[vert] is None:
            component_id += 1
        component_map[vert] = component_id
    return component_map

def dfs_search_path(g, u, v):
    """Efficient search for a path from vertex u to vertex v using DFS."""
    #Start DFS to search for v
    discovered = {u: None}
    while u is not v:
        for edge in g.incident_edges(u):
            next_vert = edge.opposite(u)
            if next_vert not in discovered:
                discovered[next_vert] = edge
                u = next_vert
    #Retrace the path discovered
    path = []
    if v in discovered:
        path.append[v]
        walk = v
        while walk is not u:
            parent = discovered[walk].opposite(walk)
            path.append(parent)
            walk = parent
        path.reverse()
    return path

def bfs(g, s, discovered):
    level = [s]
    while len(level) > 0:
        next_level = []
        for u in level:
            for e in g.incident_edges(u):
                v = e.opposite(u)
                if v not in discovered:
                    next_level.append(v)
                    discovered[v] = e
        level = next_level

def floyd_warshall(g):
    """Returns the transitive closure of graph g using the Floyd-Warshall
    Algorithm."""
    closure = deepcopy(g)
    verts = list(closure.vertices())
    n = len(verts)
    for k in range(n):
        for i in range(n):
            if i != k and closure.get_edge(verts[i], verts[k]) is not None:
                for j in range(n):
                    if i != k != j and closure.get_edge(verts[k], verts[j]) is
                    not None:
                        if closure.get_edge(verts[i], verts[j]) is not None:
                            closure.insert_edge(verts[i], verts[j])
    return closure

def floyd_warshall_v2(g):
    """Returns a list of all shortest paths between pairs of vertices in Graph
    g using Floyd-Warshall."""
    result = deepcopy(g)
    verts = list(result.vertices())
    n = len(verts)
    for k in range(n):
        for i in range(n):
            if i != k and result.get_edge(verts[i], verts[k]) is not None:
                d1 = result.get_edge(verts[i], verts[k]).element()
                for j in range(n):
                    if i != k != j and result.get_edge(verts[k], verts[j]) is
                    not None:
                        d2 = result.get_edge(verts[k], verts[j]).element()
                        if result.get_edge(verts[i], verts[j]) is None:
                            result.insert_edge(i, j, d1 + d2)
                        elif result.get_edge(verts[i], verts[j]).element() > d1 + d2:
                            result.get_edge(verts[i], verts[j])._element = d1 + d2
    result_lengths = [edge.element() for edge in result.edges()]
    return result_lengths

def topo_sort(g):
    topo = []
    ready = []
    incount = {}
    for v in g.vertices():
        incount[v] = g.incident_edges(v)
        if incount[v] == 0:
            ready.append(v)
    while len(ready) > 0:
        u = ready.pop()
        topo.append(u)
        for to_update in g.incident_edges(u):
            z = to_update.opposite(u)
            incount[z] -= 1
            if incount[z] == 0:
                ready.append(z)

    return topo

class MatrixGraph:
    """A simple implementation of an adjacency matrix-based graph."""

    def __init__(self, verts, edges, is_directed=False):
        self._vertices = verts
        self._edges = edges
        self._matrix = []
        self._is_directed = is_directed

        for i in range(len(self._vertices)):
            self._matrix.append([0]*len(verts))
        for edge in edges:
            origin, dest = edge.endpoints()
            self._matrix[self._vertices.index(origin)][self._vertices.index(dest)] = 1
            if not is_directed:
                self._matrix[self._vertices.index(dest)][self._vertices.index(origin)] = 1

    def is_directed(self):
        return self._is_directed

    def vertex_count(self):
        return len(self._matrix)

    def vertices(self):
        return self._vertices



