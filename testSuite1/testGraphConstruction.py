
from graphConstructor import get_neighbors, sobel_filters, construct_graph_with_gradients
import unittest
from PIL import Image
import numpy as np
import sys
import os
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)


class TestImageProcessing(unittest.TestCase):

    def setUp(self):
        self.test_image = np.array(
            [[100, 100, 100], [150, 150, 150], [200, 200, 200]])
        # Expected outputs for sobel_filters
        self.expected_Gx = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        self.expected_Gy = np.array([[-200, -200, -200],
                                     [-400, -400, -400],
                                     [-200, -200, -200]])
        self.expected_G = np.sqrt(self.expected_Gx**2 + self.expected_Gy**2)

    def test_get_neighbors(self):
        rows, cols = self.test_image.shape
        neighbors = get_neighbors(1, 1, rows, cols)
        self.assertEqual(sorted(neighbors), [(0, 1), (1, 0), (1, 2), (2, 1)])
        print("Test get_neighbors: passed")

    def test_sobel_filters(self):
        Gx, Gy, G = sobel_filters(self.test_image)
        print("Gx: ", Gx)
        print("Gy: ", Gy)
        np.testing.assert_array_almost_equal(Gx, self.expected_Gx)
        np.testing.assert_array_almost_equal(Gy, self.expected_Gy)
        np.testing.assert_array_almost_equal(G, self.expected_G)
        print("Test sobel_filters: passed")

    def test_construct_graph_with_gradients(self):
        G = np.sqrt(self.expected_Gx**2 + self.expected_Gy**2)
        graph = construct_graph_with_gradients(self.test_image, G)
        # Test some specific nodes and weights in the graph
        self.assertIn((0, 1), graph[(1, 1)])
        self.assertIn((1, 0), graph[(1, 1)])
        self.assertIn((1, 2), graph[(1, 1)])
        self.assertIn((2, 1), graph[(1, 1)])
        print("Test construct_graph_with_gradients: passed")


if __name__ == '__main__':
    unittest.main()
