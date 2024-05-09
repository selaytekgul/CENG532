import time

from adhoccomputing.Generics import *
from adhoccomputing.Experimentation.Topology import Topology
from adhoccomputing.Networking.LogicalChannels.GenericChannel import GenericChannel

import networkx as nx

from ringelec.ChangRoberts import ChangRobertsNode

def main():
    # setAHCLogLevel(DEBUG)
    topo = Topology()
    graph = nx.Graph()
    graph.add_nodes_from(list(range(0, 10)))

    for first_val in range(0, 10):
        for second_val in range(first_val + 1, 10):
            graph.add_edge(first_val, second_val)

    topo.construct_from_graph(graph, ChangRobertsNode, GenericChannel)

    # for i in topo.nodes:
    #     topo.nodes[i].set_leader(0)
    #     topo.nodes[i].set_callback(callback)

    event = Event(ChangRobertsNode, EventTypes.MFRT, "A to lower layer")
    topo.nodes[0].on_init(event)

    topo.start()
    time.sleep(1)

if __name__ == "__main__":
    exit(main())