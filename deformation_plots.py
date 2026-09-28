import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def get_coordinates_deformed(model,
                             global_displacement_vector):

    coordinates_undeformed = np.zeros(model.n_nodes * 2)
    coordinates_deformed = np.zeros(model.n_nodes * 2)

    for i in range(model.n_nodes):
        coordinates_undeformed[2*i]= model.nodes[i][0]
        coordinates_undeformed[2*i+1]= model.nodes[i][1]

    coordinates_deformed = coordinates_undeformed + global_displacement_vector


    return coordinates_undeformed, coordinates_deformed


def plot_coordinates(model,
                     coordinates_deformed,
                     coordinates_undeformed):

    cmatrix = model.connectivity_matrix

    plt.figure()


    for j in range(len(cmatrix)):
        n1 = cmatrix[j][0]
        n2 = cmatrix[j][1]

        x_vals_undeformed = [coordinates_undeformed[2*n1]*1000, coordinates_undeformed[2*n2]*1000]
        y_vals_undeformed = [coordinates_undeformed[2*n1+1]*1000, coordinates_undeformed[2*n2+1]*1000]
        x_vals_deformed = [coordinates_deformed[2*n1]*1000, coordinates_deformed[2*n2]*1000]
        y_vals_deformed = [coordinates_deformed[2*n1+1]*1000, coordinates_deformed[2*n2+1]*1000]

        plt.plot(x_vals_undeformed, y_vals_undeformed, 'bo', linestyle = '--')
        plt.plot(x_vals_deformed, y_vals_deformed, 'ro', linestyle = '--')

    plt.show()

    return

def print_results(model, elements, global_displacement_vector, strains, stresses, reaction_forces, show_results:bool):

    element_data = pd.DataFrame(columns = ['Element Number', 'strain', 'stress'])


    element_data = {'Element Number': [],  'strain [-]': [], 'stress [MPa]': []}
    node_data = {'Node Number': [], 'x-coord': [], 'y-coord': [], 'U1': [], 'U2': [], 'Reaction force x-dir': [], 'Reaction force y-dir': []}

    element_df = pd.DataFrame(element_data)
    node_df = pd.DataFrame(node_data)

    element_df['Element Number'] = element_df['Element Number'].astype(int)
    node_df['Node Number'] = node_df['Node Number'].astype(int)


    for element in elements:
        element_increment = {'Element Number': element.element_number + 1, 'strain [-]': strains[element.element_number], 'stress [MPa]': stresses[element.element_number]/1e6}
        element_df = pd.concat([element_df, pd.DataFrame([element_increment])], ignore_index=True)

    for i in range(len(model.nodes)):
        node_increment = {'Node Number': i+1, 'x-coord': model.nodes[i][0], 'y-coord': model.nodes[i][1], 'U1': global_displacement_vector[2*i], 'U2': global_displacement_vector[2*i+1], 'Reaction force x-dir': reaction_forces[2*i], 'Reaction force y-dir': reaction_forces[2*i+1]}
        node_df = pd.concat([node_df, pd.DataFrame([node_increment])], ignore_index=True)

    if show_results:
        print(element_df.to_string(index=False))
        print()
        print(node_df.to_string(index=False))


    return element_df, node_df
