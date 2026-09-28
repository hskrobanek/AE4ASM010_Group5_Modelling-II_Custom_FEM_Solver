'''
PIJUS

Post-processing: Derived Results - Strains and Stresses. To find out the
elemental strains and stresses, the global results must be transformed back to the
local co-ordinate system for the elements.

'''

import numpy as np


def calculate_stress_strain(T, U, length_undeformed, elastic_modulus, n_elements):

    strains = np.zeros((n_elements, 2))
    stresses = np.zeros((n_elements, 2))

    for e in range(n_elements):

        # transform back to the local co-ordinate system: U_local = T^-1 U_global
        U_local_element = np.linalg.inv(T[e]) @ U

        # axial strain from the local axial displacements of both nodes
        epsilon = (U_local_element[2] - U_local_element[0]) / length_undeformed[e]

        sigma = elastic_modulus[e] * epsilon

        strains[e] = [e, epsilon]
        stresses[e] = [e, sigma]

    return strains, stresses



def get_reaction_forces(K, U, F):
    U = np.asarray(U, dtype=float).flatten()
    F = np.asarray(F, dtype=float).flatten() 

    R = K @ U - F

    return R



# TEST 1 - Call the function with example inputs

Ttest = np.array([[0.78087, -0.6247, 0.0,     0.0    ],
               [0.6247,   0.78087, 0.0,     0.0    ],
               [0.0,      0.0,     0.78087, -0.6247],
               [0.0,      0.0,     0.6247,  0.78087]])

  
T1 = [Ttest]                                   
U1 = np.array([0.0, 0.0, 0.223, -0.865])    
L1 = [160.08e-3]                            
E1 = [70e9]                                 

strains, stresses = calculate_stress_strain(T1, U1, L1, E1, 1)
print(strains)  
print(stresses)   

