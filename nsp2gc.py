from dimod import DiscreteQuadraticModel
from dwave.system import LeapHybridDQMSampler
from params import *


def nsp_to_graph_coloring(nurses, days, shifts, nurses_per_shift):
    adj = {}
    
    # add all nodes
    for layer in range(nurses_per_shift):
        for d in range(days):
            for s in range(shifts):
                adj[f"l{layer}_d{d}_s{s}"] = set()
                
    # add intra-layer edges
    for layer in range(nurses_per_shift):
        for d in range(days):
            for s in range(shifts):
                for s_ in range(s+1, shifts):
                    adj[f"l{layer}_d{d}_s{s}"].add(f"l{layer}_d{d}_s{s_}")
                if s == shifts - 1 and d < days - 1:
                    adj[f"l{layer}_d{d}_s{s}"].add(f"l{layer}_d{d+1}_s0")
                    
    #add inter-layer edges
    for l1 in range(nurses_per_shift):
        for l2 in range(l1 + 1, nurses_per_shift):
            for d in range(days):
                for s in range(shifts):
                    adj[f"l{l1}_d{d}_s{s}"].add(f"l{l2}_d{d}_s{s}")
                    
                    for s_ in range(shifts):
                        adj[f"l{l1}_d{d}_s{s}"].add(f"l{l2}_d{d}_s{s_}")
                    if s == shifts - 1 and d < days - 1:
                        adj[f"l{l1}_d{d}_s{s}"].add(f"l{l2}_d{d+1}_s0")
                        adj[f"l{l2}_d{d}_s{s}"].add(f"l{l1}_d{d+1}_s0")
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
    print("Nurses per shift: ", NURSES_PER_SHIFT)
    
    adj = nsp_to_graph_coloring(NURSES, DAYS, SHIFTS, NURSES_PER_SHIFT)
    print("Adjacency list: ", adj)

    adj_nodes, adj_edges = adj_to_nodes_and_edges(adj)
    print("Num nodes: ", len(adj_nodes))
    print("Nodes: ", adj_nodes)
    print("Num edges: ", len(adj_edges))
    print("Edges: ", adj_edges)
    
            

    
    