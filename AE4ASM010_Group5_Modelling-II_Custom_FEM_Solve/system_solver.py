import numpy as np
DEBUG = False #if true debug prints active
# inputs from models.py BC and F
# inputs from global_stiffness_matrix.py K
# output for postprocessing.py U 
#                                nparray vector (not the same as F from models which is a matrix)

"""
System solver inputs
K   stiffness matrix [n, n]
BC  boundary conditions list [n] 
        0 or applied displacement (bounded)
        None no boundary (free)
F   forces array matrix [1, n]
"""
def solve_system(K, BC, F):
# transform F from applied forces matrix [1, n] to array list [n]
    """
    Fa applied forces list [n]
    """
    Fa = F.flatten()
# transform BC into np array
    """
    BC boundary conditions into np array [n]
    """
    BC = np.array(BC) 
# debug printouts
    if DEBUG:
        print("K=", K)
        print("BC=", BC)
        print("Fa=", Fa)

# boundary conditions into boolean bounded and free
    bounded = BC != None # all elements Not None --> bounded DOFs (into boolean array True)
    free = ~bounded  # all elements None --> free DOFs (into boolean array True)
# debug printouts
    if DEBUG:
        print("bounded=", bounded)
        print("free=", free)
        print(np.where(bounded), np.where(bounded)[0]) # np matrix of indices for True bounded, list of indices for True bounded
        print()
    
# modify F with applied dicplacement (not zero bounds)
    for i in np.where(bounded)[0]:
        b = BC[i]  # applied dicplacement (bound value)
        if b != 0.0:  # if not zero, add column to F
            # debug printouts
            if DEBUG:
                print("modify i=", i, " b=", b)
            Fa[free] -= K[free, i] * b # move applied displacement to the right of the equation (only the not reduced elements)
#  Get reduced matrices K and F
    redK = K[np.ix_(free, free)]  # ix_ extracts the non bounded columns and rows from K (reduction K in 2D)
    redF = Fa[free]  # extracts the non bounded nodes for F (reduction K in 1D)
# debug printouts
    if DEBUG:
        print("redK=", redK)
        print("redF=", redF)

# solve
    redU = np.linalg.solve(redK, redF) # solution of redF=redK*redU
# debug printouts
    if DEBUG:
        print("redU=", redU)

    # reconstruct global displacement vector
    U = np.zeros(len(Fa), dtype=float) # zero vector
    U[free] = redU  # solutions for not bounded nodes
    U[bounded] = BC[bounded]  # boundary conditions set displacements 
# return printout
    if DEBUG:
        print("U=", U)

    return U 