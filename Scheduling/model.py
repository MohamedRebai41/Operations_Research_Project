from gurobipy import Model, GRB




def schedule(n,edge_list,priority_edges):
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
        for c in range(n-1):
            m.addConstr(sum(x[i,k] for k in range(c+1) ) <= sum(x[j,k] for k in range(c)))
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
