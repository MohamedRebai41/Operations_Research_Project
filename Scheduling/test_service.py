import random
import networkx as nx
import naive as nv
import model as md
from tqdm import tqdm

def nx_generate_testcases(nb_nodes,nb_testcases,type="normal",priority=False):
    testcases = []
    if type == "dense": 
        p = 0.9
    elif type == "normal":
        p = 0.1
    elif type == "sparse":
        p=0.01
    for t in range(nb_testcases):
        graph = nx.gnp_random_graph(nb_nodes, p)
        if priority:
            top_graph = nx.gnp_random_graph(nb_nodes, 0.01)
            testcases.append((nb_nodes,graph.edges(),top_graph.edges()))
        else:
            testcases.append((nb_nodes,graph.edges()))
    return testcases


def test_topological_sort(priority_edges, assignment):
    for i,j in priority_edges:
        if assignment[i] > assignment[j]: 
            return False
    return True

def test_correctness(n,edge_list,priority_edges):
    md_result = md.schedule_(n,edge_list,priority_edges)
    nv_result = nv.schedule_(n,edge_list, priority_edges) 
    if (md_result == False):
        return True
    return test_topological_sort(priority_edges,md_result["assignment"]) and md_result["nb_colors"] == nv_result["nb_colors"]

def test(nb_testcases,priority):
    correct = 0
    wrong = 0
    for i in tqdm(range(nb_testcases)):
        n = random.randint(3,20)
        edge_list = nx_generate_testcases(n,1,"normal")[0][1]
        priority_edges = []
        if priority:
            priority_edges = nx_generate_testcases(n,1,"sparse")[0][1]
        if(test_correctness(n,edge_list,priority_edges)):
            correct+=1
        else:
            wrong+=1
    print(f"[Correct Testcases]: [{correct}/{nb_testcases}]")
    print(f"[Wrong Testcases]: [{wrong}/{nb_testcases}]")
    
