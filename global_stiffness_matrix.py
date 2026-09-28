from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import numpy.typing as npt

Matrix = npt.NDArray[np.float64]

DOFS_PER_NODE = 2  # 2D truss: x and y displacement

if TYPE_CHECKING:
    from models import AbstractModule

def get_global_stiffness_matrix(
        model: AbstractModule, element_stiffness_matrices: list[Matrix], element_transformation_matrices: list[Matrix]
) -> Matrix:
    connectivity_matrix = model.connectivity_matrix
    
    total_degrees_of_freedom = DOFS_PER_NODE * model.n_nodes
    global_matrix = np.zeros((total_degrees_of_freedom, total_degrees_of_freedom))  # GW Check

    # Iterate over the elements
    for element_index in range(model.n_elements):
        # Get info of this element
        nodes_pair = connectivity_matrix[element_index]  # GW Check, assuming correct ordering of this matrix
        transformation_matrix = element_transformation_matrices[element_index]
        local_stiffness_matrix = element_stiffness_matrices[element_index]
        
        rotated_stiffness_matrix = transformation_matrix @ local_stiffness_matrix @ transformation_matrix.T 

        add_local_matrix_to_global(rotated_stiffness_matrix, nodes_pair, global_matrix)

    if (not np.allclose(global_matrix, global_matrix.T)):
        raise RuntimeError("Global stiffness matrix is not symmetric. Check logic.")

    return global_matrix

def add_local_matrix_to_global(rotated_stiffness_matrix: Matrix, nodes_pair: list[int], global_matrix: Matrix) -> None:
    for local_row_index, row in enumerate(rotated_stiffness_matrix):
        local_node_index = local_row_index // DOFS_PER_NODE  # GW Check whether this is floor division
        dimension_index = local_row_index % DOFS_PER_NODE  # GW Check
        global_node_index = nodes_pair[local_node_index]
        global_row_index = global_node_index * DOFS_PER_NODE + dimension_index

        for local_column_index, stiffness in enumerate(row):
            local_node_index = local_column_index // DOFS_PER_NODE
            dimension_index = local_column_index % DOFS_PER_NODE
            global_node_index = nodes_pair[local_node_index]
            global_column_index = global_node_index * DOFS_PER_NODE + dimension_index

            # numpy arrays are mutable so this in place addition will persist
            global_matrix[global_row_index][global_column_index] += stiffness


# GW Todo
# - Put asserts for properties of the matrices
