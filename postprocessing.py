'''
PIJUS

Post-processing: Derived Results - Strains and Stresses. To find out the
elemental strains and stresses, the global results must be transformed back to the
local co-ordinate system for the elements.

'''

import numpy as np


def calculate_stress_strain(element_transformation_matrices, global_displacement_vector, elements, model):

    strains = np.zeros((model.n_elements, 2))
    stresses = np.zeros((model.n_elements, 2))

    U_global = np.asarray(global_displacement_vector, dtype=float).flatten()

    for e in range(model.n_elements):

        # pick out the 4 global DOFs of this element: [u1, v1, u2, v2]
        node1 = elements[e].node1_number
        node2 = elements[e].node2_number
        element_dofs = [2*node1, 2*node1 + 1, 2*node2, 2*node2 + 1]
        U_global_element = U_global[element_dofs]

        # transform back to the local co-ordinate system: U_local = T^-1 U_global (T is orthogonal, so T^-1 = T^T)
        U_local_element = element_transformation_matrices[e].T @ U_global_element

        # axial strain from the local axial displacements of both nodes
        epsilon = (U_local_element[2] - U_local_element[0]) / elements[e].length_undeformed

        sigma = elements[e].elastic_modulus * epsilon

        strains[e] = [e, epsilon]
        stresses[e] = [e, sigma]

    return strains, stresses



def get_reaction_forces(global_stiffness_matrix, global_displacement_vector, model):
    U = np.asarray(global_displacement_vector, dtype=float).flatten()
    F = np.asarray(model.applied_forces, dtype=float).flatten() 

    R = global_stiffness_matrix @ U - F

    return R
