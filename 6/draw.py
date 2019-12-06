import sys
import networkx as nx
import matplotlib 
import matplotlib.pyplot as plt
import pygraphviz
from networkx.drawing.nx_agraph import graphviz_layout

graph = nx.Graph()

def dtoCOM(a):
    global graph
    return nx.dijkstra_path_length(graph, a, "COM") 

for orbit in sys.stdin:
    A, B = [i.strip() for i in orbit.split(")")]
    graph.add_edge(A,B)

redges = zip(nx.dijkstra_path(graph, "YOU", "SAN")+[0], [0]+nx.dijkstra_path(graph, "YOU", "SAN"))
redges = list(redges)[1:-1]
labls = {
    "YOU": "YO",
    "SAN": "Santa",
    "COM": "COM"
}

pos = nx.spectral_layout(graph)
plt.subplot(1, 1, 1)
nx.draw_networkx_nodes(graph, pos, alpha=0.5, with_labels = True, node_size=10)
nx.draw_networkx_nodes(graph,pos, nodelist=nx.dijkstra_path(graph, "YOU", "SAN") , node_size=10, node_color='r' , alpha=0.8, with_labels = True)
nx.draw_networkx_labels(graph, pos, labels=labls)
nx.draw_networkx_edges(graph, pos, edge_color='b')
nx.draw_networkx_edges(graph, pos, edgelist=redges, edge_color='r')

plt.show()
