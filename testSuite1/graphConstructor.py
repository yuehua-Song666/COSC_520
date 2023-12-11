from PIL import Image
import numpy as np
from scipy.ndimage import convolve


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


def sobel_filters(image):
    # Sobel kernels for x and y directions
    sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    # Convolution
    Gx = convolve(image, sobel_x)
    Gy = convolve(image, sobel_y)
    # Gradient magnitude
    G = np.sqrt(Gx**2 + Gy**2)
    return Gx, Gy, G


def construct_graph_with_gradients(image, G):
    """
    Construct an undirected weighted graph using the gradient magnitudes.

    Args:
    - image (np.array): Grayscale image.
    - G (np.array): Gradient magnitude for each pixel.

    Returns:
    - dict: Graph represented as a dictionary.
    Time complexity is O(4*n*m) where n is the number of rows and m is the number of columns.
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
