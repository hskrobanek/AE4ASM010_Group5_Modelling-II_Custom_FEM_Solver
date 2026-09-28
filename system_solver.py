import numpy as np

#inputs from models BC and F
#inputs from Gideon K
#output for Pijus U nparray vector (not the same as F from models which is a matrix)

"""
System solver inputs
K   stiffness matrix [n, n]
BC  boundary conditions list [n] 
        0 or applied displacement (bounded)
        None no boundary (free)
F   forces array matrix [1, n]
"""
def sysSolver(K, BC, F):
#transform BC from boundary conditions list [n] to array [n,2] with column if bounded and boundary value
    BCc = [] #list boundary conditions construction (will become list of list)
    for i in range(len(BC)): #build and append rows of np boundary condition array
        BCrow = [] #start from empty list
        #build 2 columns for each row (0=no boundary or 1=boundary, applied boundary)
        BCrow.append(0.0 if BC[i] == None else 1.0)
        BCrow.append(0.0 if BC[i] == None else BC[i])
        BCc.append(BCrow)
    """
    npBC  boundary conditions nparray matrix
        first column 'boolean' (0=False 1=True)
            second column if first==True/1 --> 0 or bounded applied displacement
                            else if first==False/0 --> 0 no boundary (free)
    """
    npBC = np.array(BCc) #build np array out of constructed BCc
#transform F from applied forces matrix [1, n] to array list [n]
    """
    Fa applied forces list [n]
    """
    Fa = F.flatten()

# debug printouts
    print("K=", K)
    print("npBC=", npBC)
    print("Fa=", Fa)

    # boundary conditions into boolean bounded and free
    bounded = npBC[:, 0]==1 # all rows BC==1 --> bounded DOFs (into boolean array True)
    free = ~bounded  # all rows BC==0 --> free DOFs (into boolean array True)
    print("bounded=", bounded)
    print("free=", free)
    print(np.where(bounded), np.where(bounded)[0]) # np matrix of indices for True bounded, list of indices for True bounded
    print()
    
# modify F with applied dicplacement (not zero bounds)
    for i in np.where(bounded)[0]:
        b = npBC[i, 1]  # applied dicplacement (bound value)
        if b != 0.0:  # if not zero, add column to F
            print("modify i=", i, " b=", b)
            Fa[free] -= K[free, i] * b # move applied displacement to the right of the equation (only the not reduced elements)
    
    redK = K[np.ix_(free, free)]  # ix_ extracts the non bounded columns and rows from K (reduction K in 2D)
    redF = Fa[free]  # extracts the non bounded nodes for F (reduction K in 1D)
    print("redK=", redK)
    print("redF=", redF)

# solve
    redU = np.linalg.solve(redK, redF) #solution of redF=redK*redU
    print("redU=", redU)

    # reconstruct global displacement vector
    U = np.zeros(len(Fa), dtype=float) # zero vector
    U[free] = redU  # solutions for not bounded nodes
    U[bounded] = npBC[bounded, 1]  # boundary conditions set displacements    
    print("U=", U)

    return U 