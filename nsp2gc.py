from dimod import DiscreteQuadraticModel
from dwave.system import LeapHybridDQMSampler


def nsp_to_graph_coloring(nurses, days, shifts):
    adj = {}
    for d in range(days):
        for s in range(shifts):
            adj[f"d{d}_s{s}"] = set()
            
    for d in range(days):
        for s in range(shifts):
            adj[f"d{d}_s{s}"] = {f"d{d}_s{(s + 1) % shifts}", f"d{d}_s{(s + 2) % shifts}"}
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
    print("Number of nurses: ", nurses)
    print("Number of days: ", days)
    print("Shifts: ", list(range(shifts)))
    
            

    
    