

import unittest
import numpy as np
import sys
import os
from dijkstra import dijkstra_with_predecessors, backtrack_path, draw_path_on_image


class TestDijkstraAlgorithms(unittest.TestCase):

    def setUp(self):
        # Create a simple test graph
        self.graph = {
            'A': {'B': 1, 'C': 4},
            'B': {'A': 1, 'C': 2, 'D': 5},
            'C': {'A': 4, 'B': 2, 'D': 1},
            'D': {'B': 5, 'C': 1}
        }
        self.start = 'A'
        self.end = 'D'

    def test_dijkstra_with_predecessors(self):
        distances, predecessors = dijkstra_with_predecessors(
            self.graph, self.start)
        self.assertEqual(distances, {'A': 0, 'B': 1, 'C': 3, 'D': 4})
        self.assertEqual(
            predecessors, {'A': None, 'B': 'A', 'C': 'B', 'D': 'C'})

    def test_backtrack_path(self):
        _, predecessors = dijkstra_with_predecessors(self.graph, self.start)
        path = backtrack_path(predecessors, self.start, self.end)
        self.assertEqual(path, ['A', 'B', 'C', 'D'])

    def test_draw_path_on_image(self):
        # Create a simple test image (2x2 pixels)
        test_image = np.zeros((2, 2, 3), dtype=np.uint8)
        path = [(0, 0), (1, 1)]
        color_value = (255, 255, 255)  # White color

        modified_image = draw_path_on_image(test_image, path, color_value)
        expected_image = np.zeros((2, 2, 3), dtype=np.uint8)
        expected_image[0, 0] = color_value
        expected_image[1, 1] = color_value

        np.testing.assert_array_equal(modified_image, expected_image)


if __name__ == '__main__':
    unittest.main()
