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



def print_results_tables(global_displacement_vector, strains, stresses, reaction_forces, model):
    U = np.asarray(global_displacement_vector, dtype=float).flatten()
    R = np.asarray(reaction_forces, dtype=float).flatten()

    # nodal displacements
    print("\nNODAL DISPLACEMENTS")
    print(f"{'Node':>6} {'U1 [m]':>15} {'U2 [m]':>15}")
    for n in range(model.n_nodes):
        print(f"{n:>6} {U[2*n]:>15.6e} {U[2*n + 1]:>15.6e}")

    # element strains and stresses
    print("\nELEMENT STRAINS AND STRESSES")
    print(f"{'Element':>7} {'Nodes':>7} {'Strain [-]':>15} {'Stress [Pa]':>15}")
    for e in range(model.n_elements):
        node1, node2 = model.connectivity_matrix[e]
        print(f"{e:>7} {f'{node1}-{node2}':>7} {strains[e][1]:>15.6e} {stresses[e][1]:>15.6e}")

    # reaction forces, only at constrained DOFs (free DOFs are zero up to round-off)
    print("\nREACTION FORCES")
    print(f"{'Node':>6} {'RF1 [N]':>15} {'RF2 [N]':>15}")
    for n in range(model.n_nodes):
        rf = []
        for dof in (2*n, 2*n + 1):
            rf.append(f"{R[dof]:>15.6e}" if model.boundary_conditions[dof] is not None else f"{'-':>15}")
        print(f"{n:>6} {rf[0]} {rf[1]}")
    print()
