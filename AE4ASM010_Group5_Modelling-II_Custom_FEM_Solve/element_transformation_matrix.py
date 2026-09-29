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


