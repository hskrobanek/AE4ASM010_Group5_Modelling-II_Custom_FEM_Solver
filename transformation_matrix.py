import numpy as np


def get_element_transformation_matrices(model, elements):

#empty matrices for angles and transformation matrices
    angles = np.zeros(model.n_elements)
    transformation_matrices = np.zeros((model.n_elements, 4, 4))

    for i, element in enumerate(elements):
        dx = element.node2_x - element.node1_x
        dy = element.node2_y - element.node1_y
        theta = np.arctan2(dy, dx)
        c = np.cos(theta)
        s = np.sin(theta)

        T = np.array([
            [c, -s, 0,  0],
            [s,  c, 0,  0],
            [0,  0, c, -s],
            [0,  0, s,  c]
        ])

        angles[i] = theta
        transformation_matrices[i] = T

    return angles, transformation_matrices


def get_global_stiffness_matrix(
        model,
        element_stiffness_matrices,
        element_transformation_matrices):

    n_dof = model.n_nodes * 2

    K_global = np.zeros((n_dof, n_dof))

    K_global_contributions = np.zeros(
        (model.n_elements, n_dof, n_dof)
    )

    for i in range(model.n_elements):

        K_local = element_stiffness_matrices[i]

        T = element_transformation_matrices[i]

        K_element_global = T @ K_local @ T.T

        node1 = model.connectivity_matrix[i][0]
        node2 = model.connectivity_matrix[i][1]

        dof = [
            2 * node1,
            2 * node1 + 1,
            2 * node2,
            2 * node2 + 1
        ]

        K_global_contribution = np.zeros(
            (n_dof, n_dof)
        )

        for row in range(4):
            for column in range(4):

                K_global_contribution[
                    dof[row],
                    dof[column]
                ] = K_element_global[row, column]

        K_global_contributions[i] = K_global_contribution

        K_global += K_global_contribution

    return K_global, K_global_contributions

###OUTPUT: total global stiffness matrix