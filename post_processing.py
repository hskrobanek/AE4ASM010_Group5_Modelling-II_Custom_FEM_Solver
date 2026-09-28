import numpy as np

def calculate_stress_strain(element_transformation_matrices,
                            u_global,
                            elements,
                            model):

    strains = []
    stresses = []

    for element in elements:
        n1 = element.node1_number
        n2 = element.node2_number

    # Find the element global displacement vector
        u_global_element = np.zeros(4)
        u_global_element[0] = u_global[2*n1]
        u_global_element[1] = u_global[2*n1 + 1]
        u_global_element[2] = u_global[2*n2]
        u_global_element[3] = u_global[2*n2 + 1]

        u_global_element = np.array([u_global_element]).T

    # Find the local displacements according to u_local = T-1 u_global
        T_inv = np.linalg.inv(element_transformation_matrices[element.element_number])
        u_local_element = T_inv @ u_global_element

    # Calculate the strain based on epsilon = (u2x - u1x) / 0
        dl = float((u_local_element[2] - u_local_element[0])[0])


        epsilon = float(dl/element.length_undeformed)


    # Calculate the stress based on sigma = E * epsilon
        sigma = float(element.elastic_modulus * epsilon)

    # Append the results to the lists
        strains.append(epsilon)
        stresses.append(sigma)

    return strains, stresses


def get_reaction_forces(global_stiffness_matrix,
                        global_displacement_vector,
                        applied_force_vector):

    global_displacement_vector = np.array([global_displacement_vector]).T

    reaction_forces = np.dot(global_stiffness_matrix, global_displacement_vector) - applied_force_vector.T

    return reaction_forces

