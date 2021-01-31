from dimod import DiscreteQuadraticModel
from dwave.system import LeapHybridDQMSampler
from nsp2gc import nsp_to_graph_coloring, adj_to_nodes_and_edges
from params import *
from config import API_TOKEN

lagrange = LAGRANGE
lagrange2 = LAGRANGE2
nurses = NURSES
days = DAYS
shifts = SHIFTS
nurses_per_shift = NURSES_PER_SHIFT

def solve(adj_nodes, adj_edges):

    dqm = DiscreteQuadraticModel()

    for i in adj_nodes:
      dqm.add_variable(nurses, label=i)
    
    # classic graph coloring constraint that no two adjacent nodes have the same color
    for i0,i1 in adj_edges:
        dqm.set_quadratic(i0,i1, {(c,c): lagrange for c in range(nurses)})
    
    shifts_per_nurse = days * shifts // nurses
    
    # we should ensure that nurses get assigned a roughly equal amount of work
    for i in range(nurses):
        for index, j in enumerate(adj_nodes):
            
            dqm.set_linear_case(j, i, dqm.get_linear_case(j, i) - lagrange*(2*shifts_per_nurse+1))
            
            for k_index in range(index+1, len(adj_nodes)):
                k = adj_nodes[k_index]
                dqm.set_quadratic_case(j, i, k, i, lagrange*(dqm.get_quadratic_case(j, i, k, i) + 2))
    
    # some nurses may hate each other, so we should do out best to not put them in the same shift!
    for d in range(DAYS):
        for s in range(SHIFTS):
            for l1 in range(NURSES_PER_SHIFT):
                for l2 in range(l1+1, NURSES_PER_SHIFT):
                    
                    j = f"l{l1}_d{d}_s{s}"
                    k = f"l{l2}_d{d}_s{s}"
                    
                    for conflict in CONFLICTS:
                        
                        for n1 in conflict:
                            for n2 in conflict:
                                
                                if n1 == n2:
                                    continue
                                    
                                dqm.set_quadratic_case(j, n1, k, n2, lagrange2*(dqm.get_quadratic_case(j, n1, k, n2) + 10))


    sampler= LeapHybridDQMSampler(token=API_TOKEN)
    sampleset= sampler.sample_dqm(dqm, time_limit=10)
    sample=sampleset.first.sample
    energy = sampleset.first.energy
    
    return sample, energy

    
def verify_solution(sample, adj_edges):
    valid = True
    
    # makes sure nurses don't work more than one shift per day
    # as well as no back-to-back sessions
    for edge in adj_edges:
            i, j=edge
            if sample[i]== sample[j]:
                valid = False
                break
                
    freq = {}
    for var, nurse in sample.items():
        freq[nurse] = freq.get(nurse, 0) + 1
    
    # makes sure that workload is evenly distributed abong nurses
    for nurse, num_shifts in freq.items():
        if num_shifts < MIN_SHIFTS or num_shifts > MAX_SHIFTS:
            valid = False
            break
    
    return valid

def compress_solution(sample):
    compressed = {}
    for d in range(days):
        for s in range(shifts):
            
            day_and_shift = f"d{d}_s{s}"
            nurses = [sample[other_var] for other_var in [f"l{layer}_{day_and_shift}" for layer in range(nurses_per_shift)]]
            
            compressed[day_and_shift] = nurses
    return compressed


if __name__ == "__main__":
    adj = nsp_to_graph_coloring(NURSES, DAYS, SHIFTS, NURSES_PER_SHIFT)
    
    adj_nodes, adj_edges = adj_to_nodes_and_edges(adj)
    
    sample, energy = solve(adj_nodes, adj_edges)
    print("Solution: ", sample)
    print("Solution energy:", energy)
    
    valid = verify_solution(sample, adj_edges)
    print("Solution validity: ", valid)
    
    print("Compressed solution: ", compress_solution(sample))
    
    
    
 