from dimod import DiscreteQuadraticModel
from dwave.system import LeapHybridDQMSampler

# lagrange = 2
# nurses = 3
# days = 3
# shifts = 3


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
    
#     adj = nsp_to_graph_coloring(nurses, days, shifts)
#     print("Adjacency list: ", adj)
    
#     adj_nodes, adj_edges = adj_to_nodes_and_edges(adj)
#     print("Nodes: ", adj_nodes)
#     print("Edges: ", adj_edges)
    
#     dqm = DiscreteQuadraticModel()

#     for i in adj_nodes:
#       dqm.add_variable(nurses, label=i)
#     for i, p in enumerate(adj_nodes):
#       dqm.set_linear(p, range(nurses))
#     for i0,i1 in adj_edges:
#         dqm.set_quadratic(i0,i1, {(c,c): lagrange for c in range(nurses)})

#     sampler= LeapHybridDQMSampler(token="DEV-b2e2ec75f96b1660c40a2758aa1fe6f94e971898")
#     sampleset= sampler.sample_dqm(dqm, time_limit=10)
#     sample=sampleset.first.sample
#     energy = sampleset.first.energy
#     valid = True
    
#     for edge in adj_edges:
#             i, j=edge
#             if sample[i]== sample[j]:
#                 valid = False
#                 break
                
#     print("Solution: ", sample)
#     print("Solution energy:", energy)
#     print("Solution validity: ", valid)
            

    
    