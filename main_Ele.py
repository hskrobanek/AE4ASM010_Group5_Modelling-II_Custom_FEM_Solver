from models import Model_1, Model_2, Model_3
from objects import Element, Assembly
from global_stiffness_matrix import get_global_stiffness_matrix
from system_solver import *
from element_transformation_matrix import *
from postprocessing import *
from element import *
from deformation_plots import *


import numpy as np

model_id = input("Choose Verification Model (1-3): ")

if model_id == "1":
    model = Model_1()

elif model_id == '2':
    model = Model_2()

elif model_id == '3':
    model = Model_3()

else:
    raise ValueError('Invalid model choice.')



assembly = Assembly(model, Element)

elements = assembly.create_assembly_elements()

element_stiffness_matrices = local_stiffness_matrices(model, model.n_elements, model.elastic_modulus, model.cross_section_area)

element_rotation_angles, element_transformation_matrices = get_element_transformation_matrices(model, elements)

global_stiffness_matrix = get_global_stiffness_matrix(model, element_stiffness_matrices, element_transformation_matrices)

global_displacement_vector = solve_system(global_stiffness_matrix, model.boundary_conditions, model.applied_forces)

strains, stresses = calculate_stress_strain(element_transformation_matrices, global_displacement_vector, elements, model)

reaction_forces = get_reaction_forces(global_stiffness_matrix, global_displacement_vector, model)

coordinates_undeformed, coordinates_deformed = get_coordinates_deformed(model, global_displacement_vector)

print_results_tables(global_displacement_vector, strains, stresses, reaction_forces, model)

plot_coordinates(model, coordinates_deformed, coordinates_undeformed)
