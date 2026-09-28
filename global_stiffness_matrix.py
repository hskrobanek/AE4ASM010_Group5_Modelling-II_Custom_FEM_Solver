import numpy as np
import numpy.typing as npt

from .objects import Element, Assembly

Matrix = npt.NDArray[np.float64]

def get_global_stiffness_matrix(
        model, element_stiffness_matrices, element_transformation_matrices, connectivity_matrix
) -> Matrix:
    global_matrix: Matrix = np.zeros(model.n_elements, model.n_elements)  # GW Check

    elements = [Element(model, i) for i in range(model.n_elements)]

    for index, element in enumerate(elements):
        nodes_pair = connectivity_matrix[index]  # GW Check, assuming correct ordering of this matrix
        transformation_matrix = element_transformation_matrices[index]
        local_stiffness_matrix = element_stiffness_matrices[index]
        
        rotated_stiffness_matrix = transformation_matrix @ (local_stiffness_matrix @ transformation_matrix.T)  # GW superfluous () ?

        for local_row_index, row in enumerate(rotated_stiffness_matrix):
            local_node_index = local_row_index // 2  # GW Check whether this is floor division  # GW Don't hardcode 2
            dimension_index = local_row_index % 2  # GW Check
            global_node_index = nodes_pair[local_node_index]
            global_row_index = global_node_index * 2 + dimension_index

            for local_column_index, element in enumerate(row):
                local_node_index = local_column_index // 2
                dimension_index = local_column_index % 2
                global_node_index = nodes_pair[local_node_index]
                global_column_index = global_node_index * 2 + dimension_index

                global_matrix[global_row_index][global_column_index] += element

    if (not np.allclose(global_matrix, global_matrix.T)):
        raise RuntimeError("Global stiffness matrix is not symmetric. Check logic.")

    return global_matrix


# GW Todo
# - Put asserts for properties of the matrices
