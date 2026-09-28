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
