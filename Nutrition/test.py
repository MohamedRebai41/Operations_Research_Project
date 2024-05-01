import numpy as np
import scipy.optimize as opt
from testCases import tests
from model import optimize

def optimizeSimplex(names, cout, contraintesInf, contraintesSup):
    c= np.array(cout)
    # make array values all negative contraintesInf
    for i in range(len(contraintesInf)):
        contraintesInf[i] = [-x for x in contraintesInf[i]]
    A_ub = np.array(contraintesInf)[:, :-1]
    b_ub = np.array(contraintesInf)[:, -1]

    bounds = [(0, None) for _ in range(len(names))]
    for i in range(len(contraintesSup)):
        for j in range(len(contraintesSup[i]) - 1):
            if contraintesSup[i][j] == 1:
                bounds[j] = (0, contraintesSup[i][-1])
                break
            

    res = opt.linprog(c, A_ub=A_ub, b_ub=b_ub,bounds=bounds, method='highs')
    if res.success:
        return res
    else:
        return None

def main():
    for test in tests:
        names = test["names"]
        cout = test["cout"]
        contraintesInf = test["contraintesInf"]
        contraintesSup = test["contraintesSup"]
        resGurobi = optimize(len(names), names, cout, contraintesInf, contraintesSup)
        resSimplex = optimizeSimplex(names, cout, contraintesInf, contraintesSup)
        # compare the results
        if resSimplex and resGurobi:
            for var_name, var_value in zip(names, resSimplex.x):
                print(f"{var_name}: {var_value}")
            print("Optimal cost Simplex:", resSimplex.fun)
            for i in range(len(resGurobi)):
                print(f"{names[i]}: {resGurobi[i]}")


if __name__ == "__main__":
    main()