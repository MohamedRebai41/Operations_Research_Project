import gurobipy as gp
from gurobipy import GRB



def add_variable(model,names):
    x = []
    for i in range(len(names)):
        x.append(model.addVar(vtype=GRB.CONTINUOUS, name=names[i]))
    return x

def set_objective(model,x,cout):
    model.setObjective(sum(cout[i]*x[i] for i in range(len(x))),GRB.MINIMIZE)

def add_constraint_Sup(model,x,contraintes):
    for i in range(len(contraintes)):
        lhs = sum(contraintes[i][j]*x[j] for j in range(len(x)))
        rhs = contraintes[i][-1]
        model.addConstr(lhs <= rhs)

def add_constraint_Inf(model,x,contraintes):
    for i in range(len(contraintes)):
        lhs = sum(contraintes[i][j]*x[j] for j in range(len(x)))
        rhs = contraintes[i][-1]
        model.addConstr(lhs >= rhs)

def validate_input(nb_items,names,cout,contraintesInf,contrainteSup):
    if(len(names) !=nb_items):
        raise Exception("The data is incomplete names")
    if(len(cout) !=nb_items):
        raise Exception("The data is incomplete cout")
    for contrainte in contraintesInf:
        if(len(contrainte) != nb_items+1):
            raise Exception("The data is incomplete")
    for contrainte in contrainteSup:
        if(len(contrainte) != nb_items+1):
            raise Exception("The data is incomplete")

def format_result(x):
    result = []
    for i in range(len(x)):
        result.append(x[i].x)
    return result

def optimize(nb_items,names,cout,contraintesInf,contrainteSup):
    model = gp.Model("optimization-model")
    validate_input(nb_items,names,cout,contraintesInf,contrainteSup)
    x = add_variable(model,names)
    model.update()
    set_objective(model,x,cout)
    model.update()
    add_constraint_Inf(model,x,contraintesInf)
    add_constraint_Sup(model,x,contrainteSup)
    model.update()
    model.optimize()
    if(model.status == GRB.OPTIMAL):
        print("Optimal solution found using Gurobi")
        return format_result(x)
    else:
        print("No solution found")
        return None
