import numpy as np


# Derive an element description from the global model definition
class Element:
    def __init__(self, model: AbstractModule, element_number: int):

        # Initialise model and element number values
        self.model = model
        self.element_number = element_number

        # Get the element node numbers from the model
        self.node1_number = model.connectivity_matrix[element_number][0]
        self.node2_number = model.connectivity_matrix[element_number][1]

        # Get x, y coordinates of element nodes
        self.node1_x = model.nodes[self.node1_number][0]
        self.node1_y = model.nodes[self.node1_number][1]
        self.node2_x = model.nodes[self.node2_number][0]
        self.node2_y = model.nodes[self.node2_number][1]

        # Get information about the element's elastic modulus and cross-sectional area
        self.cross_section_area = model.cross_section_area[element_number]
        self.elastic_modulus = model.elastic_modulus[element_number]

        # Calculate the undeformed length of the element
        self.length_undeformed = np.sqrt((self.node2_x - self.node1_x)**2 + (self.node2_y - self.node1_y)**2)



    # OPTIONAL: print information about the element to double-check with the diagram

    def get_element_info(self):
        print(f"Element number (system): {self.element_number}")
        print(f'Element number (drawing): {self.element_number + 1}')
        print(f'Node 1 (undeformed) [mm]: {self.node1_x * 1000, self.node1_y * 1000}')
        print(f'Node 2 (undeformed) [mm]: {self.node2_x * 1000, self.node2_y * 1000}')
        print(f'Undeformed element length [mm]: {self.length_undeformed * 1000}')
        print(f'Cross-sectional area [mm2]: {self.cross_section_area * 1e6}')
        print(f'Elastic Modulus [GPa]: {self.elastic_modulus / 1e9}\n')

        if self.model.boundary_conditions[2 * self.node1_number] == None:
            print("Node 1 free in x-direction")
        else:
            print(f'Node 1 constrained U1 = {self.model.boundary_conditions[2 * self.node1_number] * 1000} mm')
        if self.model.boundary_conditions[2 * self.node1_number + 1] == None:
            print("Node 1 free in y-direction")
        else:
            print(f'Node 1 constrained U2 = {self.model.boundary_conditions[2 * self.node1_number + 1] * 1000} mm')

        if self.model.boundary_conditions[2 * self.node2_number] == None:
            print("Node 2 free in x-direction")
        else:
            print(f'Node 2 constrained U1 = {self.model.boundary_conditions[2 * self.node2_number] * 1000} mm')
        if self.model.boundary_conditions[2 * self.node2_number + 1] == None:
            print("Node 2 free in y-direction")
        else:
            print(f'Node 2 constrained U2 = {self.model.boundary_conditions[2 * self.node2_number + 1] * 1000} mm')

        print("\n")

# Define an assembly class to create the structural elements
class Assembly:
    def __init__(self, model, element_constructor):
        self.model = model
        self.element_constructor = element_constructor

    # Return an array of elements based on model specification
    def create_assembly_elements(self):
        return [self.element_constructor(self.model, i) for i in range(self.model.n_elements)]



