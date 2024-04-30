def get_adj_list(n,edge_list):
    adj_list = [[] for _ in range(n)]
    for i,j in edge_list:
        adj_list[i].append(j)
        adj_list[j].append(i)
    return adj_list

def is_safe(v, graph, top_graph, color, c):
    for x in graph[v]:
        if c == color[x]:
            return False
    for x in top_graph[v]:
        if color[x] != -1 and c >= color[x]:
            return False

    return True

def graph_coloring(n, graph,top_graph, m, color, v):
    # Base case: If all vertices are assigned a color, return true
    if v == n:
        return True
    # Try different colors for the current vertex 'v'
    for c in range(0, m):
        # Check if assignment of color 'c' to 'v' is fine
        if is_safe(v, graph, top_graph, color, c):
            color[v] = c
            # Recur to assign colors to the rest of the vertices
            if graph_coloring(n,graph, top_graph, m, color, v + 1):
                return True
            # If assigning color 'c' doesn't lead to a solution, remove it
            color[v] = -1
    # If no color can be assigned to this vertex, return false
    return False



def schedule_(n,edge_list,priority_edges=[]):
    graph = get_adj_list(n,edge_list)
    top_graph = get_adj_list(n,priority_edges)
    for i in range(1,n+1):
        color = [-1]*n
        if graph_coloring(n,graph,top_graph,i,color,0):
            return {"nb_colors": i}
    return -1 




