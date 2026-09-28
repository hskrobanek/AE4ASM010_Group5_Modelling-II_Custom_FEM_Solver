import numpy as np


def get_element_transformation_matrices(model, elements):

    angles = np.zeros(model.n_elements)

    transformation_matrices = np.zeros(
        (model.n_elements, 4, 4)
    )

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


def transform_stiffness_matrices(
        element_stiffness_matrices,
        element_transformation_matrices):

    n_elements = len(element_stiffness_matrices)

    global_element_stiffness_matrices = np.zeros(
        (n_elements, 4, 4)
    )

    for i in range(n_elements):

        # Extract k from teammate's matrix
        k = element_stiffness_matrices[i][i, i]

        # Build the 4x4 local truss stiffness matrix
        K_local = np.array([
            [ k, 0, -k, 0],
            [ 0, 0,  0, 0],
            [-k, 0,  k, 0],
            [ 0, 0,  0, 0]
        ])

        # Transformation matrix for same element
        T = element_transformation_matrices[i]

        # Transform local -> global
        global_element_stiffness_matrices[i] = (
            T @ K_local @ T.T
        )

    return global_element_stiffness_matrices