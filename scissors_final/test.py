import unittest
import numpy as np
from livewire import Livewire


class LivewireTests(unittest.TestCase):

    def setUp(self):
        # Sample image for testing
        self.image = np.array(
            [[10, 20, 30], [40, 50, 60], [70, 80, 90]], dtype=np.uint8)
        self.lw = Livewire(self.image)

    def test_get_grad(self):
        grad_x, grad_y, grad_mag = self.lw._get_grad(self.image)
        assertions_count = 0

        # Check if gradients are not None
        self.assertIsNotNone(grad_x)
        assertions_count += 1
        self.assertIsNotNone(grad_y)
        assertions_count += 1
        self.assertIsNotNone(grad_mag)
        assertions_count += 1

        # Check for correct shapes of gradients
        self.assertEqual(grad_x.shape, self.image.shape)
        assertions_count += 1
        self.assertEqual(grad_y.shape, self.image.shape)
        assertions_count += 1
        self.assertEqual(grad_mag.shape, self.image.shape)
        assertions_count += 1

        # Check for correct data type
        self.assertIsInstance(grad_x, np.ndarray)
        assertions_count += 1
        self.assertIsInstance(grad_y, np.ndarray)
        assertions_count += 1
        self.assertIsInstance(grad_mag, np.ndarray)
        assertions_count += 1

        # Check gradient values are within expected range
        self.assertTrue(np.all(grad_x >= -1) and np.all(grad_x <= 1))
        assertions_count += 1
        self.assertTrue(np.all(grad_y >= -1) and np.all(grad_y <= 1))
        assertions_count += 1
        self.assertTrue(np.all(grad_mag >= 0))
        assertions_count += 1

        print(f"Testing get gradients: {assertions_count} tests passed")

    # less tests for this as it's a simpler function also tested in initial implementations

    def test_get_neighbors(self):
        neighbors = self.lw._get_neighbors((1, 1))
        expected_neighbors = [(0, 0), (0, 1), (0, 2),
                              (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]
        self.assertEqual(sorted(neighbors), sorted(expected_neighbors))
        print("Testing get neighbors: passed ")

    def test_get_grad_direction_cost(self):
        p = (1, 1)
        q = (2, 2)
        cost = self.lw._get_grad_direction_cost(p, q)
        assertions_count = 0

        # Check if the cost is a float
        self.assertIsInstance(cost, float)
        assertions_count += 1

        # Check if the cost is non-negative
        self.assertGreaterEqual(cost, 0)
        assertions_count += 1

        print(
            f"Testing get_grad_direction_cost: {assertions_count} tests passed")

    def test_local_cost(self):
        p = (1, 1)
        q = (2, 2)
        cost = self.lw._local_cost(p, q)
        assertions_count = 0

        # Check if the cost is a float
        self.assertIsInstance(cost, float)
        assertions_count += 1

        # Check if the cost is non-negative
        self.assertGreaterEqual(cost, 0)
        assertions_count += 1

        print(f"Testing local_cost: {assertions_count} tests passed")

    def test_get_path_matrix(self):
        seed = (0, 0)
        paths = self.lw.get_path_matrix(seed)
        assertions_count = 0

        # Check if paths is a dictionary
        self.assertIsInstance(paths, dict)
        assertions_count += 1

        # Check if the seed point is not in paths
        self.assertNotIn(seed, paths)
        assertions_count += 1

        # Check if keys in paths are valid coordinates
        for key in paths.keys():
            self.assertIsInstance(key, tuple)
            self.assertTrue(0 <= key[0] < self.image.shape[0]
                            and 0 <= key[1] < self.image.shape[1])
            assertions_count += 1

        # Check if values in paths are valid coordinates
        for value in paths.values():
            self.assertIsInstance(value, tuple)
            self.assertTrue(
                0 <= value[0] < self.image.shape[0] and 0 <= value[1] < self.image.shape[1])
            assertions_count += 1

        # Check for non-empty paths
        self.assertTrue(len(paths) > 0)
        assertions_count += 1

        # Additional checks can be added here based on expected behavior

        print(f"Testing get_path_matrix: {assertions_count} tests passed")


if __name__ == '__main__':
    unittest.main()
