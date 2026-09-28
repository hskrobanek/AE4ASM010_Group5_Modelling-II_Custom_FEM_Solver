import numpy as np

# Define the truss model to be analysed by the FEM software

class Model_1:
    def __init__(self):

        # Define node cooridnates [x, y] based on a chosen origin point
        self.nodes = [[0.100, 0.0],
                      [0.0, 0.100],
                      [0.100, 0.150],
                      [0.200, 0.050]]

        # Define the connectivity matrix based on the structure diagram
        self.connectivity_matrix = [[0, 1],
                                    [1, 2],
                                    [2, 3],
                                    [3, 0],
                                    [0, 2]]

        # Define element data based on available structure description
        self.elastic_modulus = [70e9, 70e9, 70e9, 70e9, 70e9]
        self.poisson_ratio = [0.3, 0.3, 0.3, 0.3, 0.3]
        self.cross_section_area = [0.000010, 0.000010, 0.000010, 0.000010, 0.000020]

        # Define the applied force vector based on the structure diagram
        self.applied_forces = np.array([[0.0, 0.0,
                               0.0, 0.0,
                               1500.0, -2500.0,
                               0.0, 0.0]])

        # Define boundary conditions based on the structural supports
        self.boundary_conditions = [0.0, 0.0,
                                    0.0, None,
                                    None, None,
                                    0.0, None]


        # Get the number of nodes and elements for the analysed structure
        self.n_nodes = len(self.nodes)
        self.n_elements = len(self.connectivity_matrix)





class Model_2:
    def __init__(self):

        # Define node cooridnates [x, y] based on a chosen origin point
        self.nodes = [[0.100, 0.0],
                      [0.0, 0.100],
                      [0.100, 0.150],
                      [0.200, 0.050]]

        # Define the connectivity matrix based on the structure diagram
        self.connectivity_matrix = [[0, 1],
                                    [1, 2],
                                    [3, 2],
                                    [0, 3],
                                    [0, 2]]

        # Define element data based on available structure description
        self.elastic_modulus = [70e9, 70e9, 70e9, 70e9, 70e9]
        self.poisson_ratio = [0.3, 0.3, 0.3, 0.3, 0.3]
        self.cross_section_area = [0.000010, 0.000010, 0.000010, 0.000010, 0.000020]

        # Define the applied force vector based on the structure diagram
        self.applied_forces = np.array([[0.0, 0.0,
                               0.0, 0.0,
                               1500.0, -2500.0,
                               0.0, 0.0]])

        # Define boundary conditions based on the structural supports
        self.boundary_conditions = [0.0, 0.0,
                                    0.0, 0.00001,
                                    None, None,
                                    0.0, None]


        # Get the number of nodes and elements for the analysed structure
        self.n_nodes = len(self.nodes)
        self.n_elements = len(self.connectivity_matrix)





class Model_3:
    def __init__(self):

        # Define node cooridnates [x, y] based on a chosen origin point
        self.nodes = [[1.250, 0.750],
                      [2.000, 0.0],
                      [0.750, 0.0],
                      [0.0, 0.0],
                      [0.500, 0.500]]

        # Define the connectivity matrix based on the structure diagram
        self.connectivity_matrix = [[1, 0],
                                    [2, 4],
                                    [3, 4],
                                    [4, 0]]

        # Define element data based on available structure description
        self.elastic_modulus = [70e9, 70e9, 70e9, 70e9]
        self.poisson_ratio = [0.3, 0.3, 0.3, 0.3]
        self.cross_section_area = [0.000050, 0.000030, 0.000030, 0.000050]

        # Define the applied force vector based on the structure diagram
        self.applied_forces = np.array([[0.0, 0.0,
                               1500.0, 0.0,
                               0.0, 0.0,
                               -500.0, 0.0,
                               0.0, 0.0]])

        # Define boundary conditions based on the structural supports
        self.boundary_conditions = [0.0, 0.0,
                                    None, 0.0,
                                    0.0, 0.0,
                                    None, 0.0,
                                    None, None]


        # Get the number of nodes and elements for the analysed structure
        self.n_nodes = len(self.nodes)
        self.n_elements = len(self.connectivity_matrix)




