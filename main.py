from network import *


def optimization():
    vertex, values = network.best_place_for_source_vertex()
    print('Source node: : {}'.format(vertex))
    print('Cost of cables: {}'.format(values[vertex]))
    print('Cost of infrastructure: {}'.format(network.cost_of_mst))
    network.draw_solution(vertex)


if __name__ == '__main__':
    network = Network()
    network.draw_graph()
    network.draw_mst()
    source = 1
    destination = 10
    cost, previous = network.dijkstra(source, destination)
    path = network.find_path(previous, destination)
    print("{} -> {}: distance = {}, path = {}".format(source, destination, cost, path))
    network.draw_shortest_path(path, source, destination)
    optimization()


