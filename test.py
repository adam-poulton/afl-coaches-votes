import unittest
from src.util import is_valid_sequence


class TestVoteSplitMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.input = [[10, 8, 6, 4, 2],
                      [10, 6, 4, 4, 3, 3]
                      ]
        self.output = [[[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)]],
                       [[(5, 5), (3, 3), (4, 0), (0, 4), (2, 1), (1, 2)],
                        [(5, 5), (4, 2), (4, 0), (1, 3), (3, 0), (2, 1)]]
                       ]
        self.bad_output = [[(5, 5), (5, 3), (3, 3), (2, 2), (1, 1)]]

    def test_is_valid_sequence_01(self):
        for case in self.output:
            for output in case:
                self.assertTrue(is_valid_sequence(output))

    def test_is_valid_sequence_02(self):
        for case in self.bad_output:
            self.assertFalse(is_valid_sequence(case))


if __name__ == "__main__":
    unittest.main()
