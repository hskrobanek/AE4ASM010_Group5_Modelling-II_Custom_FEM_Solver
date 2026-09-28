import numpy as np

def solve_system(global_stiffness_matrix,
                 boundary_conditions,
                 applied_force_vector):

    # Governing equation: K_global * u = F - u_known

    # Define the global displacement vector
    u_global = np.zeros_like(boundary_conditions)

    # Set up a list of coordinated corresponding to defined boundary conditions
    coords_del = []

    # Set up a list of deleted columns to move to construct u_known with
    bc_cols = []

    # Set up a list of coordinates to match the remaining displacements when assembling the global displacement vector later on
    coords_empty = np.arange(0,len(boundary_conditions))

    # Check for boundary conditions and apply them accordingly
    for i in range(len(boundary_conditions)):

        if boundary_conditions[i] == 0:
            u_global[i] = 0.0
            coords_del.append(i)

        elif boundary_conditions[i] is not None:
            u_global[i] = boundary_conditions[i]
            bc_cols.append([i, global_stiffness_matrix[:,[i]]])
            coords_del.append(i)

    # Update the list of displacements which still have to be calculated
    coords_empty = np.delete(coords_empty, coords_del)


    # Assemble the u_known vector:
    u_known = np.array([np.zeros(len(boundary_conditions))]).T

    for i in range(len(bc_cols)):
        id = bc_cols[i][0]
        u_known += boundary_conditions[id] * bc_cols[i][1]

    # Reduce the global stiffness matrix, applied force vector and u_known vector
    gsm_reduced_col = np.delete(global_stiffness_matrix, coords_del, 1)
    gsm_reduced_col_row = np.delete(gsm_reduced_col, coords_del, 0)

    applied_force_vector_reduced = np.delete(applied_force_vector.T, coords_del, 0)

    u_known_reduced = np.delete(u_known, coords_del, 0)

    # Assemble the RHS of the governing equation
    RHS = applied_force_vector_reduced + u_known_reduced

    # Solve the remaining system
    solution = np.linalg.solve(gsm_reduced_col_row, RHS)

    # Assemble the global displacement vector
    for i in range(len(solution)):
        id = coords_empty[i]
        u_global[id] = float(solution[i][0])

    return u_global
