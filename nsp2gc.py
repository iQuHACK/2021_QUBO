from dimod import DiscreteQuadraticModel
from dwave.system import LeapHybridDQMSampler
from params import *


def nsp_to_graph_coloring(nurses, days, shifts):
    adj = {}
    for d in range(days):
        for s in range(shifts):
            adj[f"d{d}_s{s}"] = set()
            
    for d in range(days):
        for s in range(shifts):
            for s_ in range(s+1, shifts):
                adj[f"d{d}_s{s}"].add(f"d{d}_s{s_}")
            if s == shifts - 1 and d < days - 1:
                adj[f"d{d}_s{s}"].add(f"d{d+1}_s0")
    
    return adj


def adj_to_nodes_and_edges(adj):
    nodes = list(adj.keys())
    edges = []
    for source, destinations in adj.items():
        for dest in destinations:
            edges.append((source, dest))
    return nodes, edges


if __name__ == "__main__":
    print("Number of nurses: ", NURSES)
    print("Number of days: ", DAYS)
    print("Shifts: ", list(range(SHIFTS)))
    
    adj = nsp_to_graph_coloring(NURSES, DAYS, SHIFTS)
    print("Adjacency list: ", adj)

    adj_nodes, adj_edges = adj_to_nodes_and_edges(adj)
    print("Nodes: ", adj_nodes)
    print("Edges: ", adj_edges)
    
            

    
    