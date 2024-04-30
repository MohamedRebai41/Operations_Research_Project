import time

import numpy as np
import model as md
import naive as nv
import matplotlib.pyplot as plt
from test_service import nx_generate_testcases
from tqdm import tqdm


def benchmark(schedule_,graph_type, nb_testcases, threshhold,priority=False):
    results = []
    n=2
    while True:
        n+=1
        print(f"[N={n}]")
        current_results = []
        testcases = nx_generate_testcases(n,nb_testcases,graph_type,priority)
        for testcase in tqdm(testcases):
            start_time = time.perf_counter()
            priority_graph = [] if not priority else testcase[2]
            schedule_(testcase[0],testcase[1],priority_graph)
            end_time = time.perf_counter()
            current_results.append(end_time - start_time)
        mean = np.mean(current_results)
        print(f"Average Runtime: {mean}")
        results.append(mean)
        if(mean > threshhold):
            break
    return results


def plot_benchmarks(nv_benchmark, md_benchmark):
    plt.figure(figsize=(10, 6))    
    plt.plot(range(3,len(nv_benchmark) + 3), nv_benchmark , label='naive algorithm', marker='s', linestyle='--') 
    plt.plot(range(3,len(md_benchmark) + 3), md_benchmark, label='solver Algorithm', marker='o', linestyle='-')  
    plt.title('Comparison of Average Runtimes') 
    plt.xlabel('Size of Input (n)') 
    plt.ylabel('Average Runtime (seconds)') 
    plt.legend() 
    plt.grid(True)  
    plt.show()  


def compare(graph_type="normal",nb_testcases=20,threshold=5,priority='False'):
    nv_benchmarks= benchmark(nv.schedule_,graph_type,nb_testcases,threshold,priority)
    md_benchmarks = benchmark(md.schedule_,graph_type,nb_testcases,threshold,priority)
    plot_benchmarks(nv_benchmarks,md_benchmarks)








