class Crossword:
    """
    One possible crossword puzzle from a list of words.

    Instance Variables:
    grid (list(list(str))): the grid containing the positioned words and empty spaces
    words_used (list(str)): words successfully placed in grid
    words_unused (list(str)): words that were not used in the grid
    score (int): a measure on how "good" the crossword is
    """

    def __init__(self, grid, words_used, words_unused):
        self.grid = grid
        self.words_used = words_used
        self.words_unused = words_unused
        self.score = score_crossword()

        def score_crossword():
            """
            Returns how "good" the crossword is based on the following parameters:
            - Number of words placed (more is better)
            - Grid size actually used (less is better)
            - Ratio between height and width (close to 1 is better)
            """

    def print_crossword(self):
        """
        Print the grid, list of words used, lists of words unused, and score of the crossword
        """
        print(f'Crossword with a score of {self.score}. n/
              Words used: {self.words_used} n/
              Words unused: {self.words_unused}')
        
        for row in self.grid:
            print(' '.join(row))

class CrosswordGenerator:
    """
    Collection of crosswords generated from list of words

    Instance Variables:
    grid_size (int): length of each side of grid
    word_list (list(str)): list of available words to use
    num_return (int): how many top crossword boards to return
    """
    def __init__(self, grid_size, word_list):
        self.grid_size = grid_size
        self.word_list = word_list
        self.crosswords = []

    def generate_crossword(self, words):
        """
        Generate a possible crossword puzzle with at least 3 words.
        """

        words_used = [] # list of tuples where each tuple is (word, position) and the position is (r, c, v/h)
        words_unused = [] # list of strs
        grid = [] # list of strs where each space is either # (empty space) or letter

        # initialize grid

        # place first word on the center of the grid

        # try to place the rest of the words
        for word in words[1:]:
            potential_positions = [] # list of tuples where each tuple is (score, position) and the position is (r, c, v/h)

            # find potential positions
            for ...
                for ...
                    position = ...
                    # if potential position is found, score and add to potential_positions
                    if ...
                        potential_positions.append((score_position(word, position), position))

            if not potential_positions:
                words_used.append(word)
            else:
                # find best position and add to words_used and grid


        def score_position(word, position):
            """
            Returns how "good" the word position is based on the following parameters:
            - How much it increases the grid size (less is better)
            - How many already placed words it overlaps with (more is better)
            """

    def generate_crosswords(self, num_iter):
        """
        Attempt to generate num_iter crosswords. Assign these crosswords to self.crosswords.
        """
        crosswords = []
        for i in range(num_iter):
            # shuffle words to get a different board
            shuffled_words = ...
            # generate crossword and add to list of crosswords
            crosswords.append(self.generate_crossword(shuffled_words))

        self.crosswords = crosswords

    def print_crosswords(self, num_crosswords):
        """
        Print the top num_crosswords crosswords based on score.
        """
        for crossword in self.crosswords[:num_crosswords]:
            crossword.print_crossword()
            print(" ")