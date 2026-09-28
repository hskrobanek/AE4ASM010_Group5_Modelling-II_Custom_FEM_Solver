import numpy as np

def get_element_transformation_matrices(model, elements):
    rotation_angles = np.zeros(model.n_elements)
    transformation_matrices = np.zeros((model.n_elements, 4, 4))

    for element in elements:

        dx = element.node2_x - element.node1_x
        dy = element.node2_y - element.node1_y

        if dx == 0:
            if dy > 0:
                rotation_angle = np.pi/2
            if dy < 0:
                rotation_angle = -np.pi/2
            if dy == 0:
                raise ValueError("Element is a node: dx = dy = 0")
        else:
            rotation_angle = float(np.arctan2(dy, dx))

        transformation_matrix = np.array([[float(np.cos(rotation_angle)), float(-np.sin(rotation_angle)), 0.0, 0.0],
                                 [float(np.sin(rotation_angle)), float(np.cos(rotation_angle)), 0.0, 0.0],
                                 [0.0, 0.0, float(np.cos(rotation_angle)), float(-np.sin(rotation_angle))],
                                 [0.0, 0.0, float(np.sin(rotation_angle)), float(np.cos(rotation_angle))]])

        rotation_angles[element.element_number] = rotation_angle
        transformation_matrices[element.element_number] = transformation_matrix

    return rotation_angles, transformation_matrices

