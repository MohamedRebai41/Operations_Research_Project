from gurobipy import Model, GRB


def schedule(nb_tasks,nb_resources,tasks,priorities):
    """
        - The input should be of the following format:
            - tasks should be a matrix: Each array in the matrix the represents the resources of that task
            - priorities: Each element is an array of two elements
    """
    validate_input(nb_tasks,nb_resources,tasks,priorities)
    edge_list = build_graph(tasks)
    return get_session_plan(schedule_(nb_tasks,edge_list,priorities))


def build_graph(tasks):
    resources=len(tasks)*[[]]
    for i in range(len(tasks)):
        for res in tasks[i]:
            resources[res].append(i)
    edge_list = []
    #Building the graph
    for resource in resources:
        for i in range(len(resource)):
            for j in range(i+1,len(resource)):
                edge_list.append([i,j])
    return edge_list

def validate_input(nb_tasks,nb_resources,tasks,priorities):
    if(len(tasks) !=nb_tasks):
        raise Exception("The data is incomplete")
    for task in tasks:
        for x in task:
            if(x<0 or x>=nb_resources):
                raise Exception(f"The resource {x} does not exist")
    for pr in priorities:
        if(len(pr)!=2):
            raise Exception("Incorrect input at priorities")
        if(pr[0]<0 or pr[0]>=nb_tasks):
            raise Exception(f"The task {pr[0]} does not exist")
        if(pr[0]<0 or pr[0]>=nb_tasks):
            raise Exception(f"The task {pr[1]} does not exist")

def schedule_(n,edge_list,priority_edges=[]):
    """
        - The Problem is defined using two graphs:
            - A graph that defines the coloring problem: edge_list
            - A graph that defines the topological sort: priority_edges
        - The number of nodes in both graphs is n
        - The nodes should be zero-indexed
        - Returns false if there is no solution => There is a cycle in the second graph
        - Returns a dictionary that has two fields: number of colors and assignment
    """
    m = Model("graph_coloring")
    m.setParam('OutputFlag', 0)
    # Create variables
    x = m.addVars(n,n, vtype=GRB.BINARY, name = "x")
    w = m.addVars(n, vtype=GRB.BINARY, name = "w")




    # Set objective: Minimizing the number of colors used
    m.setObjective(sum(w[c] for c in range(n)), GRB.MINIMIZE)
    # Add constraints
    # One color per node
    for i in range(n):
        m.addConstr(sum(x[i,c] for c in range(n))==1)
    #No two adjacent nodes have the same color
    for i,j in edge_list:
        for c in range(n):
            m.addConstr(x[i,c] + x[j,c] <= w[c])
    #Pick only the first colors in a sequence
    for c in range(1,n):
        m.addConstr(w[c-1]>=w[c])
    #Topological sort constraints
    for i,j in priority_edges:
        for c in range(n):
            m.addConstr(sum(x[i,k] for k in range(c)) >= sum(x[j,k] for k in range(c)))
    for i,j in priority_edges:
        for c in range(n):
            m.addConstr(x[i,c] + x[j,c] <= w[c])
    # Optimize model
    m.optimize()
    if m.status != GRB.OPTIMAL:
        return False
    return format_results(m,n)


def format_results(model,n):
    nb_colors = 0
    assignment = [-1]*n
    for i in range(n):
        for j in range(n):
            if(model.getVarByName(f"x[{i},{j}]").X == 1):
                assignment[i]=j
                nb_colors = max(nb_colors,j+1)
                break
    return {
        'nb_colors':nb_colors,
        'assignment': assignment
    }

def get_session_plan(data):
    plan = [[] for _ in range(data["nb_colors"])]
    for i in range(len(data["assignment"])):
        plan[data["assignment"][i]].append(i)
    return {
        'plan': plan
    }

