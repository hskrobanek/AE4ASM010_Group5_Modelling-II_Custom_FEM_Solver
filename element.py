# calculate the element stiffness matrix in local coordinate system
# stiffness matrix is node x node size
import numpy as np


def calculate_stiffness_matrix(elastic_modulus: float, cross_sectional_area: float, length_element:float)->float:
    k = elastic_modulus * cross_sectional_area / length_element
    return k


def local_stiffness_matrices(n_elements: int, elastic_modulus_array, cross_sectional_area_array, length_array)->list:
    # make list to be returned with all the local stiffness matrices for each element
    return_list = []
    
    # for loop 0 to number of elements - 1
    for e in range(n_elements):  
        # find equivalent stiffness of element
        k = calculate_stiffness_matrix(elastic_modulus_array[e], cross_sectional_area_array[e], length_array[e])

        # make an node x node size matrix
        stiffness_matrix = np.zeros((n_elements + 1, n_elements + 1))

        # change the corresponding zeroes to the k, -k, -k, k matrix
        stiffness_matrix[e, e] = k  # top left value of corresponding local matrix
        stiffness_matrix[e, e + 1] = -k  # top right of local matrix
        stiffness_matrix[e + 1, e] = -k  # bottom left of local matrix
        stiffness_matrix[e + 1, e + 1] = k  # bottom right of local matrix

        # put the matrix in a list so it can be returned with the other ones 
        return_list.append(stiffness_matrix)
    return return_list


if __name__ == "__main__":
    # define inputs
    n_elements = 4
    elastic_modulus_array = [10, 10, 10, 10]
    cross_sectional_area_array = [20, 20, 20, 20]
    length_array = [1, 1, 1, 1]
    # get all local stiffnes matrices in a list
    return_list = local_stiffness_matrices(n_elements, elastic_modulus_array, cross_sectional_area_array, length_array)

    # obtain the individual matrices from the list so they can be used individually
    for e in range(n_elements):
        local_stiffness_matrix = return_list[e]
        print(local_stiffness_matrix)

    # for the successor:)
    return_list = local_stiffness_matrices(n_elements, elastic_modulus_array, cross_sectional_area_array, length_array)
    
    for e in range(n_elements):
        local_stiffness_matrix = return_list[e]
        print(local_stiffness_matrix)
