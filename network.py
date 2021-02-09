import networkx as nx
import matplotlib.pyplot as plt
from vertex import Vertex
from edge import Edge
from math import inf
from collections import defaultdict
import warnings
from unionfind import *

warnings.filterwarnings("ignore", category=UserWarning)


class Network:
    vertices = {}
    edges = {}
    number_of_vertices = 0
    number_of_edges = 0
    dict_of_edges = defaultdict(list)

    def __init__(self):
        self.vertices = {}
        self.edges = {}
        with open('./Resources/plik.txt', 'r') as f:
            number_of_vertices = int(next(f))
            for i in range(0, number_of_vertices):
                id, x, y = f.readline().rstrip().split(' ')
                node = Vertex(int(id), float(x), float(y))
                self.vertices[node.id] = node
            number_of_edges = int(f.readline().rstrip())
            for i in range(0, number_of_edges):
                idd, start, end = f.readline().rstrip().split(' ')
                start_vertex = self.vertices[int(start)]
                end_vertex = self.vertices[int(end)]
                edge = Edge(int(idd), start_vertex, end_vertex)
                self.edges[edge.id] = edge
        self.number_of_edges = number_of_edges
        self.number_of_vertices = number_of_vertices
        self.cost_of_mst = 0

    def draw_graph(self):
        plt.switch_backend('TkAgg')
        g = nx.Graph()
        for id, vertex in self.vertices.items():
            g.add_node(int(id), pos=(vertex.x, vertex.y))
        for id, edge in self.edges.items():
            g.add_edge(edge.source.id, edge.destination.id, weight=edge.weight)
        position = nx.get_node_attributes(g, 'pos')
        nx.draw_networkx(g, position)
        plt.title('Network')
        plt.show()

    def get_vertices(self):
        return self.vertices

    def get_edges(self):
        return self.edges

    def find_mst(self):
        result = []
        weight_sum = 0.0
        union_find = UnionFind(self.number_of_vertices + 1)
        edges_copy = sorted(self.get_edges().items(), key=lambda e_dge: e_dge[1].weight)
        for id, edge in edges_copy:
            # edge = [x, y, weight]
            vertex_x = edge.source
            vertex_y = edge.destination
            weight_of_edge = edge.weight
            if not union_find.are_connected(vertex_x.id, vertex_y.id):
                union_find.union(vertex_x.id, vertex_y.id)
                result.append([vertex_x.id, vertex_y.id, weight_of_edge])
                weight_sum += weight_of_edge
        # print("Result: ")
        # for f, s, w in result:
            # print(f'{f} --> {s} = {round(w, 3)}')
        # print(f'Total cost: {round(weight_sum, 3)}')
        self.cost_of_mst = weight_sum
        return result

    def create_adjacency_list(self):  # function used in dijkstra, it is to simplify iteration through the edges
        edges = defaultdict(list)
        for id, edge in self.get_edges().items():
            edges[int(edge.source.id)].append((int(edge.destination.id), edge.weight))
            edges[int(edge.destination.id)].append((int(edge.source.id), edge.weight))
        return edges

    def dijkstra(self, src, destination=None, for_mst=True):
        nodes = []
        if for_mst:
            adj = self.create_adjacency_for_mst()
        else:
            adj = self.create_adjacency_list()
        for n in adj:
            nodes.append(n)
        nodes_left = set(nodes)
        distance = dict()
        previous = dict()
        for n in nodes:
            distance[n] = inf
            previous[n] = None
        distance[src] = 0
        while nodes_left:
            closest_node = min(nodes_left, key=distance.get)
            nodes_left.remove(closest_node)
            if destination is not None and closest_node == destination:
                return distance[destination], previous
            for edge in adj.get(closest_node, ()):
                # returns attributes with key 'closest_node'
                node = edge[0]
                weight = edge[1]
                new_distance = distance[closest_node] + weight
                if new_distance < distance[node]:
                    distance[node] = new_distance
                    previous[node] = closest_node
        return distance, previous

    @staticmethod
    def find_path(pr, node):  # generate path list based on parent points 'prev'
        p = list()
        while node is not None:
            p.append(node)
            node = pr[node]
        return p[::-1]

    def draw_shortest_path(self, path, f, l):  # drawing
        g = nx.Graph()
        edgelist = []
        for key, vertex in self.vertices.items():
            g.add_node(int(key), pos=(vertex.x, vertex.y))
        for i in range(len(path) - 1):
            edgelist.append((path[i], path[i + 1]))
            g.add_edge(path[i], path[i + 1])
        position = nx.get_node_attributes(g, 'pos')
        nx.draw_networkx(g, position)
        plt.title('Shortest path from: {} to {} '.format(f, l))
        plt.show()

    def graph_from_mst(self):
        result = self.find_mst()
        return result

    def create_adjacency_for_mst(self):
        edges = defaultdict(list)
        result = self.graph_from_mst()
        for x, y, weight in result:
            edges[x].append((y, weight))
            edges[y].append((x, weight))
        return edges

    def draw_mst(self):
        g = nx.Graph()
        mst = self.find_mst()
        edgelist = []
        for key, vertex in self.vertices.items():
            g.add_node(int(key), pos=(vertex.x, vertex.y))
        for f, s, w in mst:
            edgelist.append((f, s))
            g.add_edge(f, s, weight=w)
        position = nx.get_node_attributes(g, 'pos')
        nx.draw_networkx(g, position)
        plt.title('MST tree')
        plt.show()

    def draw_solution(self, minimum):  # drawing, you do not have to understand this (i do )
        g = nx.Graph()
        mst = self.find_mst()
        pose = {}
        edgelist = []
        for key, value in self.vertices.items():
            pose[int(key)] = (value.x, value.y)
        for key in pose.keys():
            nx.draw_networkx_nodes(g, pose, nodelist=[key])
            if key == minimum:
                nx.draw_networkx_nodes(g, pose, node_color='red', nodelist=[key])
        for f, s, w in mst:
            edgelist.append((f, s))
        nx.draw_networkx_edges(g, pos=pose, edgelist=edgelist, edge_color='black')
        plt.title('Red node is the proper place for the source')
        labels = dict()
        for j in range(0, 10):
            labels[j] = j+1
        nx.draw_networkx_labels(g, pose, {n +1: lab for n, lab in labels.items() if n + 1 in pose})
        plt.show()

    def best_place_for_source_vertex(self):
        sources = []
        total_cost = 0.0
        dictionary = {}
        for key in self.get_vertices().keys():
            sources.append(key)
        for vertex in sources:
            distance, prev = self.dijkstra(vertex, None, True)
            for cost in distance:
                path = self.find_path(prev, cost)
                total_cost += distance[cost]
            dictionary[vertex] = round(total_cost, 3)
            total_cost = 0
        #        print(dictionary)
        minimum_vertex = min(dictionary, key=dictionary.get)
        return minimum_vertex, dictionary


