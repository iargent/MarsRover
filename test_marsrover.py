import unittest
from marsrover import direction_change, go_forward, do_move

class TestMarsRover(unittest.TestCase):
    def test_left_from_west(self):
        dirs=['N', 'E', 'S', 'W']
        self.assertEqual(direction_change(dirs, 'W', False), 'S')

    def test_left_from_north(self):
        dirs=['N', 'E', 'S', 'W']
        self.assertEqual(direction_change(dirs, 'N', False), 'W')

    def test_right_from_west(self):
        dirs=['N', 'E', 'S', 'W']
        self.assertEqual(direction_change(dirs, 'W', True), 'N')

    def test_right_from_north(self):
        dirs=['N', 'E', 'S', 'W']
        self.assertEqual(direction_change(dirs, 'N', True), 'E')

    def test_go_north_from_origin(self):
        (x, y) = go_forward(0, 0, 'N')
        self.assertEqual(x, 0)
        self.assertEqual(y, 1)

    def test_go_east_from_origin(self):
        (x, y) = go_forward(0, 0, 'E')
        self.assertEqual(x, 1)
        self.assertEqual(y, 0)

    def test_go_south_from_origin(self):
        (x, y) = go_forward(0, 0, 'S')
        self.assertEqual(x, 0)
        self.assertEqual(y, -1)

    def test_go_west_from_origin(self):
        (x, y) = go_forward(0, 0, 'W')
        self.assertEqual(x, -1)
        self.assertEqual(y, 0)

    def test_from_spec_1(self):
        self.assertEqual(do_move(2, 3, 'E', 4, 8, 'LFRFF'), '(4, 4, E)')

    def test_from_spec_2(self):
        self.assertEqual(do_move(0, 2, 'N', 4, 8, 'FFLFRFF'), '(0, 4, W) LOST')
        
if __name__ == "__main__":
    unittest.main()
