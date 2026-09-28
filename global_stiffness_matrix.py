import numpy as np

def get_global_stiffness_matrix(model,
                                elements,
                                element_stiffness_matrices,
                                element_transformation_matrices,
                                connectivity_matrix):

    gsm = np.zeros((model.n_nodes * 2, model.n_nodes * 2))

    for element in elements:
        n1 = element.node1_number
        n2 = element.node2_number

        K_local_element = element_stiffness_matrices[element.element_number]
        T_element = element_transformation_matrices[element.element_number]
        T_element_inv = np.linalg.inv(T_element)

        K_global_element = T_element @ K_local_element @ T_element_inv

        gsm[n1*2][n1*2] += K_global_element[0][0]
        gsm[n1*2][n1*2+1] += K_global_element[0][1]
        gsm[n1*2 + 1][n1*2] += K_global_element[1][0]
        gsm[n1*2 + 1][n1*2 + 1] += K_global_element[1][1]

        gsm[n2*2][n2*2] += K_global_element[2][2]
        gsm[n2*2][n2*2+1] += K_global_element[2][3]
        gsm[n2*2+1][n2*2 + 1] += K_global_element[3][3]
        gsm[n2*2+1][n2*2] += K_global_element[3][2]

        gsm[n1*2][n2*2] += K_global_element[0][2]
        gsm[n1*2+1][n2*2] += K_global_element[1][2]
        gsm[n1*2][n2*2+1] += K_global_element[0][3]
        gsm[n1*2+1][n2*2+1] += K_global_element[1][3]

        gsm[n2*2][n1*2] += K_global_element[2][0]
        gsm[n2*2][n1*2+1] += K_global_element[2][1]
        gsm[n2*2+1][n1*2] += K_global_element[3][0]
        gsm[n2*2+1][n1*2+1] += K_global_element[3][1]





    return gsm


