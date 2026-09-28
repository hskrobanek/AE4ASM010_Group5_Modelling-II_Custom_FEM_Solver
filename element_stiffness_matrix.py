import numpy as np

def get_element_stiffness_matrices(model, elements):
    element_stiffness_matrices = np.zeros((model.n_elements, 4, 4))


    for element in elements:
        elastic_modulus = float(element.elastic_modulus)
        cross_section_area = float(element.cross_section_area)
        length_undeformed = float(element.length_undeformed)

        k_eq = elastic_modulus * cross_section_area / length_undeformed

        element_stiffness_matrix = np.array([[k_eq, 0.0, -k_eq, 0.0],
                                    [0.0, 0.0, 0.0, 0.0],
                                    [-k_eq, 0.0, k_eq, 0.0],
                                    [0.0, 0.0, 0.0, 0.0]])

        element_stiffness_matrices[element.element_number] = element_stiffness_matrix


    return element_stiffness_matrices
