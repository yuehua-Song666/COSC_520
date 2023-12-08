from PIL import Image
import numpy as np


def pad_with_zeros(image, pad_width):
    return np.pad(image, pad_width, mode='constant', constant_values=0)


def apply_convolution(image, filter):
    # Padded image
    # Padding width is 1 for a 3x3 filter
    padded_image = pad_with_zeros(image, 1)
    rows, cols = image.shape
    convolved_image = np.zeros_like(image)

    # Applying the filter
    for i in range(rows):
        for j in range(cols):
            window = padded_image[i:i+3, j:j+3]
            convolved_value = np.sum(window * filter)
            convolved_image[i, j] = convolved_value

    return convolved_image


def energy_filter(image):
    # Sobel filters
    sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

    # Applying convolution
    Gx = apply_convolution(image, sobel_x)
    Gy = apply_convolution(image, sobel_y)

    # magnitude
    G = np.sqrt(Gx**2 + Gy**2)

    # Edge angle and energy function
    edge_angle = np.arctan2(Gy, Gx)
    Ex = G * np.cos(edge_angle + np.pi / 2.0)
    Ey = G * np.sin(edge_angle + np.pi / 2.0)

    return Gx, Gy, G, Ex, Ey


def get_neighbors(row, col, rows, cols):
    # 4-way connectivity
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))
    if row < rows - 1:
        neighbors.append((row + 1, col))
    if col > 0:
        neighbors.append((row, col - 1))
    if col < cols - 1:
        neighbors.append((row, col + 1))
    return neighbors


def construct_graph_with_gradients(image, G):
    """
    Construct an undirected weighted graph using the gradient magnitudes.
    """
    rows, cols = image.shape
    graph = {}

    for row in range(rows):
        for col in range(cols):
            graph[(row, col)] = {}
            for neighbor in get_neighbors(row, col, rows, cols):
                # Use inverse of gradient magnitude as weight
                # Adding a small constant to avoid division by zero
                weight = 1 / (G[neighbor] + 1e-5)
                graph[(row, col)][neighbor] = weight

    return graph
