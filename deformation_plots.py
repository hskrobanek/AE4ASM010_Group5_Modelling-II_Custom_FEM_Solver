import matplotlib.pyplot as plt
import numpy as np

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
