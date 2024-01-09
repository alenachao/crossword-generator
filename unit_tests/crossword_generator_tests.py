import unittest
from generator_classes.CrosswordGenerator import CrosswordGenerator

class TestCrosswordGenerator(unittest.TestCase):
    def test_generate_crosswords(self):
        # set up parameters
        word_list = ["hello", "world", "python"]
        grid_size = 20
        generator = CrosswordGenerator(grid_size, word_list)

        # test
        generator.generate_crosswords(5)
        self.assertEqual(len(generator.crosswords), 5)

if __name__ == '__main__':
    unittest.main()