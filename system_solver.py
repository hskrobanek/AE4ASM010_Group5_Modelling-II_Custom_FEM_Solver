import numpy as np

"""
System solver inputs
K   stiffness matrix [n, n]
BC  boundary conditions [n, 2] 
      first column 'boolean' (0=False 1=True)
      second column if first==True/1 --> 0 or bounded applied displacement
                    else if first==False/0 --> 0 no boundary (free)
F   forces [n]
"""
def sysSolver(K, BC, F):
# boundary conditions into boolean
    print("K=", K) # debug printouts
    print("BC=", BC)
    print("F=", F)
    
    bounded = BC[:, 0]==1 # all rows BC==1 --> bounded DOFs (into boolean array True)
    free = ~bounded  # all rows BC==0 --> free DOFs (into boolean array True)
    print("bounded=", bounded)
    print("free=", free)
    print(np.where(bounded), np.where(bounded)[0]) # np matrix of indices for True bounded, list of indices for True bounded
    print()
    
# modify F with applied dicplacement (not zero bounds)
    for i in np.where(bounded)[0]:
        b = BC[i, 1]  # applied dicplacement (bound value)
        if b != 0.0:  # if not zero, add column to F
            print("modify i=", i, " b=", b)
            F[free] -= K[free, i] * b # move applied displacement to the right of the equation (only the not reduced elements)
    
    redK = K[np.ix_(free, free)]  # ix_ extracts the non bounded columns and rows from K (reduction K in 2D)
    redF = F[free]  # extracts the non bounded nodes for F (reduction K in 1D)
    print("redK=", redK)
    print("redF=", redF)

# solve
    redU = np.linalg.solve(redK, redF) #solution of redF=redK*redU
    print("redU=", redU)

    # reconstruct global displacement vector
    U = np.zeros(len(F), dtype=float) # zero vector
    U[free] = redU  # solutions for not bounded nodes
    U[bounded] = BC[bounded, 1]  # boundary conditions set displacements    
    print("U=", U)

    return U