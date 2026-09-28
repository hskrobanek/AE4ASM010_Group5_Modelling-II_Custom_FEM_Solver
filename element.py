# calculate the element stiffness matrix in local coordinate system
# stiffness matrix is 4 x 4 size
# code for main:
from element import local_stiffness_matrices

Ke = local_stiffness_matrices(model, model.n_elements, model.cross_section_area)
import numpy as np
from objects import *



def calculate_stiffness_matrix(elastic_modulus: float, cross_sectional_area: float, length_element: float) -> float:
    k = elastic_modulus * cross_sectional_area / length_element
    return k


def local_stiffness_matrices(model, n_elements: int, elastic_modulus_array, cross_sectional_area_array) -> list:
    # make list to be returned with all the local stiffness matrices for each element
    K_e = []
    
    # for loop 0 to number of elements - 1
    for e in range(n_elements):  
        # find equivalent stiffness of element
        elementclass = Element(model, e)
        k = calculate_stiffness_matrix(
            elastic_modulus_array[e],
            cross_sectional_area_array[e],
            elementclass.length_undeformed
        )

        # make the 4x4 local stiffness matrix
        stiffness_matrix = np.array([
            [ k, 0, -k, 0],
            [ 0, 0,  0, 0],
            [-k, 0,  k, 0],
            [ 0, 0,  0, 0]
        ])

        # put the matrix in a list so it can be returned with the other ones 
        K_e.append(stiffness_matrix)

    return K_e


if __name__ == "__main__":
    # define inputs
    n_elements = 4
    elastic_modulus_array = [10, 10, 10, 10]
    cross_sectional_area_array = [20, 20, 20, 20]
    length_array = [1, 1, 1, 1]

    # get all local stiffness matrices in a list
    K_e = local_stiffness_matrices(
        n_elements,
        elastic_modulus_array,
        cross_sectional_area_array,
        length_array
    )

    # obtain the individual matrices from the list so they can be used individually
    for e in range(n_elements):
        local_stiffness_matrix = K_e[e]
        print(local_stiffness_matrix)