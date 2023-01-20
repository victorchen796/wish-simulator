# Copyright (c) 2023 Google LLC

# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""Implements a weighted directed Graph, using adjacency list vertices.

To build a Graph, acquire a Builder:

weighted_graph_builder = WeightedGraph.WeightedGraphBuilder()

and then proceed to add vertices and edges (requiring the vertices of an edge to
be added first) using the builder methods as a fluent interface:

weighted_graph_builder.add_vertex("Alice")
    .add_vertex("Bob")
    .add_vertex()
    .add_vertex()
    .add_edge_name("Alice", "Bob", 2.7)
    .add_edge(2, 3, 3.1)
    .add_edge_name("Alice", "vertex 2", 4.8)

then

weighted_graph = weighted_graph_builder.build()

WeightedGraph objects consist of a list of vertices, and a mapping of names to
vertices.

A Vertex object consists of a list of adjacencies. Call a given vertex object v
and let u be an arbitrary vertex. For all (v, u) edges with some weight w, v has
an entry containing u and an entry containing w with the same index, the first
in a list of adjacent vertices, and the second in a list of weights associated
with each edge.
"""

class Vertex:
    """An adjacency list representation of a vertex in a graph.

    Suppose we have some fixed vertex u that has three edges, one to v and two
    to w, with weights 1, 2 and 3. Then including multiplicity, u has three
    vertices it is incident to.

    Including multiplicity (so we may differentiate different edges to a vertex
    if there are), for each edge of vertex u, we record the vertex incident to u
    and the weight of its edge in parallel.

    Attributes:
        adjacent_vertices (list[Vertex]): List of all vertices incident to this
            vertex.
        weights (list[Float]): List of all edge weights on the edge to the
            vertex with the same index as the given weight
    """
    def __init__(self):
        self.adjacent_vertices = []
        self.weights = []

class WeightedGraph:
    """Adjacency list + vertex list representation of a weighted graph.

    Attributes:
        Vertices (list[Vertex]): List of all vertices in the Graph.
        name_to_vertex (dict[str, Vertex]): Mapping of names of vertices to the
            Vertext object.
    """
    def __init__(self, vertices: int, edges: dict[tuple[int, int], float], names_to_vertices):
        self.vertices = [Vertex() for _ in vertices]
        self.name_to_vertex = {name: self.vertices[i] for name, i in names_to_vertices.items()}

        for (src_v, dst_v), weight in edges.items():
            vertices[src_v].adjacent_vertices.append(vertices[dst_v])
            vertices[src_v].weights.append(weight)

    class WeightedGraphBuilder:
        """Fluent interface for constructing a WeightedGraph.

        Attributes:
            vertices (int): Number of vertices currently in the graph.
                Used as an ID to name unnamed vertices in the form "vertex i"
            edges (dict[tuple[Vertex], float]): Mapping of 2-tuple of vertices
                to weight of edge.
            name_to_vertex (dict[str, Vertex]): Mapping of name to vertex.
        """
        def __init__(self):
            self.vertices = 0
            self.edges = {}
            self.name_to_vertex = {}

        def add_vertex(self, name: str=None):
            """Adds a vertex.

            Args:
                name (str, optional): Name of vertex. Defaults to None,
                    but named "vertex i" where i is the 0-th indexed index for
                    the newest vertex.

            Returns:
                WeightedGraphBuilder: The modified WeightedGraphBuilder.
            """
            if name is None:
                name = f"vertex {self.vertices}"

            self.name_to_vertex[name] = self.vertices

            self.vertices += 1

            return self

        def add_edge(self, src_v: int, dst_v: int, weight: float):
            """Adds a weighted edge by indices of the vertices.

            Args:
                src_v (int): index of first Vertex.
                dst_v (int): index of second Vertex.
                weight (float): Weight of edge.

            Raises:
                ValueError: If index is < 0 or index >= number of vertices.

            Returns:
                WeightedGraphBuilder: The modified WeightedGraphBuilder.
            """
            if src_v < 0 or src_v >= self.vertices:
                raise ValueError
            if dst_v < 0 or dst_v >= self.vertices:
                raise ValueError

            self.edges[(src_v, dst_v)] = weight

            return self

        def add_edge_name(self, name1: str, name2: str, weight: float):
            """Adds a weighted edge by the name of the vertices.

            Args:
                name1 (str): Name of first vertex.
                name2 (str): Name of second vertex.
                weight (float): Weight of edge.

            Raises:
                KeyError: If name1 or name2 are not valid names of vertices.

            Returns:
                WeightedGraphBuilder: The modified WeightedGraphBuilder.
            """
            if name1 not in self.name_to_vertex:
                raise KeyError
            if name2 not in self.name_to_vertex:
                raise KeyError

            src_v = self.name_to_vertex[name1]
            dst_v = self.name_to_vertex[name2]

            self.add_edge(src_v, dst_v, weight)

            return self

        def build(self):
            """Constructs the WeightedGraph from current state of the Builder

            Returns:
                WeightedGraph: The WeightedGraph that represents the
                    WeightedGraphBuilders current state.
            """
            return WeightedGraph(self.vertices, self.edges, self.name_to_vertex)
