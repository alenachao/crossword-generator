import unittest
from generator_classes.Crossword import Crossword
import io
from unittest.mock import patch

class TestCrossword(unittest.TestCase):
    def setUp(self):
        grid = [['#', '#', 'h', '#', '#'],
                ['#', '#', 'e', '#', '#'],
                ['#', '#', 'l', '#', '#'],
                ['#', '#', 'l', '#', '#'],
                ['#', '#', 'o', '#', '#']]
        words_used = {'hello': (0, 2, True)}
        words_unused = ['world']

        self.sample_crossword = Crossword(grid, words_used, words_unused)

    def test_score_crossword(self):
        # Test the score_crossword method
        expected_score = 2.0 
        self.assertEqual(self.sample_crossword.score, expected_score)

    def test_print_crossword(self):
        # Test the print_crossword method
        with unittest.mock.patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.sample_crossword.print_crossword()
            output = mock_stdout.getvalue().strip()

        expected_output = """Crossword with a score of 2.0
Words used: ['hello']
Words unused: ['world']
# # h # #
# # e # #
# # l # #
# # l # #
# # o # #"""

        self.assertEqual(output, expected_output)

if __name__ == '__main__':
    unittest.main()