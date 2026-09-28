from models import Model_1, Model_2, Model_3
from objects import Element, Assembly
from global_stiffness_matrix import get_global_stiffness_matrix
from system_solver import *
from element_transformation_matrix import *
from postprocessing import *
from element import *
'''
Example imports from files:

from element_stiffness_matrix import get_element_stiffness_matrices
from element_transformation_matrix import get_element_transformation_matrices
from global_stiffness_matrix import get_global_stiffness_matrix
from solve_system_global import solve_system
from post_processing import calculate_stress_strain, get_reaction_forces
from deformation_plots import get_coordinates_deformed, plot_coordinates
'''

import numpy as np

model = Model_1()

'''
Example main structure:

assembly = Assembly(model, Element)

elements = assembly.create_assembly_elements()

element_stiffnes_matrices = get_element_stiffness_matrices(model, elements)

element_rotation_angles, element_transformation_matrices = get_element_transformation_matrices(model, elements)

global_stiffness_matrix = get_global_stiffness_matrix(
        model, element_stiffness_matrices, element_transformation_matrices
)

global_displacement_vector = solve_system(global_stiffness_matrix, model.boundary_conditions, model.applied_forces)

strains, stresses = calculate_stress_strain(element_transformation_matrices, global_displacement_vector, elements, model)

reaction_forces = get_reaction_forces(global_stiffness_matrix, global_displacement_vector, model.applied_forces)

coordinates_undeformed, coordinates_deformed = get_coordinates_deformed(model, global_displacement_vector)

plot_coordinates(model, coordinates_deformed, coordinates_undeformed)
'''

assembly = Assembly(model, Element)

elements = assembly.create_assembly_elements()

element_stiffnes_matrices = local_stiffness_matrices(model, elements)

element_rotation_angles, element_transformation_matrices = get_element_transformation_matrices(model, elements)

global_stiffness_matrix = get_global_stiffness_matrix(
        model, element_stiffness_matrices, element_transformation_matrices
)

global_displacement_vector = solve_system(global_stiffness_matrix, model.boundary_conditions, model.applied_forces)

strains, stresses = calculate_stress_strain(element_transformation_matrices, global_displacement_vector, elements, model)

reaction_forces = get_reaction_forces(global_stiffness_matrix, global_displacement_vector, model.applied_forces)

# coordinates_undeformed, coordinates_deformed = get_coordinates_deformed(model, global_displacement_vector)

# plot_coordinates(model, coordinates_deformed, coordinates_undeformed)