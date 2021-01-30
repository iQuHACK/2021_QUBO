from dimod import DiscreteQuadraticModel
from dwave.system import LeapHybridDQMSampler
from nsp2gc import nsp_to_graph_coloring, adj_to_nodes_and_edges
from params import *
from config import API_TOKEN

lagrange = LAGRANGE
nurses = NURSES
days = DAYS
shifts = SHIFTS

def solve(adj_nodes, adj_edges):

    dqm = DiscreteQuadraticModel()

    for i in adj_nodes:
      dqm.add_variable(nurses, label=i)
    
    for i0,i1 in adj_edges:
        dqm.set_quadratic(i0,i1, {(c,c): lagrange for c in range(nurses)})
    
    shifts_per_nurse = days * shifts // nurses
    
    for i in range(nurses):
        for index, j in enumerate(adj_nodes):
            
            dqm.set_linear_case(j, i, dqm.get_linear_case(j, i) - lagrange*(2*shifts_per_nurse+1))
            
            for k_index in range(index+1, len(adj_nodes)):
                k = adj_nodes[k_index]
                dqm.set_quadratic_case(j, i, k, i, lagrange*(dqm.get_quadratic_case(j, i, k, i) + 2))


    sampler= LeapHybridDQMSampler(token=API_TOKEN)
    sampleset= sampler.sample_dqm(dqm, time_limit=10)
    print(sampleset)
    sample=sampleset.first.sample
    energy = sampleset.first.energy
    
    return sample, energy

    
def verify_solution(sample, adj_edges):
    valid = True
    
    for edge in adj_edges:
            i, j=edge
            if sample[i]== sample[j]:
                valid = False
                break
    return valid
    
if __name__ == "__main__":
    adj = nsp_to_graph_coloring(nurses, days, shifts)
    print("Adjacency list: ", adj)

    adj_nodes, adj_edges = adj_to_nodes_and_edges(adj)
    print("Nodes: ", adj_nodes)
    print("Edges: ", adj_edges)
    
    sample, energy = solve(adj_nodes, adj_edges)
    print("Solution: ", sample)
    print("Solution energy:", energy)
    
    valid = verify_solution(sample, adj_edges)
    print("Solution validity: ", valid)
    
 