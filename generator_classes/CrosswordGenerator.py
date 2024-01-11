import random
from generator_classes.Crossword import Crossword
from generator_classes.Word import Word

class CrosswordGenerator:
    """
    Collection of crosswords generated from list of words

    Instance Variables:
    grid_size (int): length of each side of grid
    word_list (list(str)): list of available words to use
    num_return (int): how many top crossword boards to return
    """
    def __init__(self, word_list):

        self.grid_size = max([len(word) for word in word_list]) + 5
        self.word_list = word_list
        self.crosswords = []

    def generate_crossword(self, words):
        """
        Generate a possible crossword puzzle.
        """
        # helper functions
        def score_position(word):
            """
            Returns how "good" the word position is based on the following parameters:
                - How much it increases the grid size (less is better)
                - How many already placed words it overlaps with (more is better)
            """
            
            if word.get_hor():
                # get grid score
                # if horizontal we only care abt left and right 
                left = min([w.get_col() for w in words_used])
                right = max([w.get_col() + len(w.get_word()) if w.get_hor() else w.get_col() for w in words_used ])

                grid_score_left = min(word.get_col() - left, 0)
                grid_score_right = max((word.get_col() + len(word.get_word())) - right, 0)

                grid_score = grid_score_left + grid_score_right

                # get overlap score: we go along the adjacent tiles of the word. 
                # if there's a letter on one side then that's a corner, if there are letters on both sides thats a cross (cross is better)
                overlap_score = 0
                for i in range(len(word.get_word())):
                    if r > 0 and grid[r - 1][c + i] != "#":
                        overlap_score += 1
                    if r < self.grid_size - 1 and grid[r + 1][c + i] != "#":
                        overlap_score += 1

                return grid_score + overlap_score
            else:
                # get grid score
                # if vertical we only care abt up and down
                top = min([w.get_row() for w in words_used])
                bottom = max([w.get_row() + len(w.get_word()) if not w.get_hor() else w.get_row() for w in words_used])

                grid_score_top = min(word.get_row() - top, 0)
                grid_score_bottom = max((word.get_row() + len(word.get_word())) - bottom, 0)

                grid_score = grid_score_top + grid_score_bottom

                # get overlap score: we go along the adjacent tiles of the word. 
                # if there's a letter on one side then that's a corner, if there are letters on both sides thats a cross (cross is better)
                overlap_score = 0
                for i in range(len(word.get_word())):
                    if c > 0 and grid[r + i][c - 1] != "#":
                        overlap_score += 1
                    if c < self.grid_size - 1 and grid[r + i][c + 1] != "#":
                        overlap_score += 1

                return overlap_score - grid_score + len(words_used) - len(words_unused)


        def get_valid_position(word):
            """
            Returns a valid position we could place the word, if none then return None. 
            Note this is not the same as curr_position since any letter in word can match with the letter at curr_position.
            Note that the direction is the direction of the word we are placing which is perpendicular to the existing word.
            A valid position is one where:
                - for any overlaps, letter of word and letter already placed must match
                - the word does not go off the grid
                - there are no adjacent letters unless it is an overlap
            """
            position_letter = grid[word.get_row()][word.get_col()]
            letter_in_word = [i for i, letter in enumerate(word.get_word()) if letter == position_letter]

            for i in letter_in_word:
                if word.get_hor(): # if word is going to be placed horizontally
                    start_position = Word(word.get_word(), word.get_row(), word.get_col() - i, word.get_hor())
                    if start_position.get_col() < 0 or start_position.get_col() + len(word.get_word()) > self.grid_size:
                        continue
                    for j in range(len(word.get_word()) + 1):
                        if j == len(word.get_word()):
                            return start_position
                        elif (grid[start_position.get_row()][start_position.get_col() + j] != "#" and word.get_word()[j] != grid[start_position.get_row()][start_position.get_col() + j]) or \
                            ((grid[start_position.get_row()][start_position.get_col() + j] == "#") and \
                            ((start_position.get_row() > 0 and grid[start_position.get_row() - 1][start_position.get_col() + j] != "#" ) or \
                            (start_position.get_row() < self.grid_size - 1 and grid[start_position.get_row() + 1][start_position.get_col() + j] != "#" ))):
                            break
                else:
                    start_position = Word(word.get_word(), word.get_row() - i, word.get_col(), word.get_hor())
                    if start_position.get_row() < 0 or start_position.get_row() + len(word.get_word()) > self.grid_size:
                        continue
                    for j in range(len(word.get_word()) + 1):
                        if j == len(word.get_word()):
                            return start_position
                        elif (grid[start_position.get_row() + j][start_position.get_col()] != "#" and word.get_word()[j] != grid[start_position.get_row() + j][start_position.get_col()]) or \
                            ((grid[start_position.get_row() + j][start_position.get_col()] == "#") and \
                            ((start_position.get_col() > 0 and grid[start_position.get_row() + j][start_position.get_col() - 1] != "#" ) or \
                            (start_position.get_col() < self.grid_size - 1 and grid[start_position.get_row() + j][start_position.get_col() + 1] != "#" ))):
                            break
                    

        def insert_word(word):
            """
            Place word onto grid.
            """
            if word.get_hor():
                for i in range(len(word.get_word())):
                    grid[word.get_row()][word.get_col() + i] = word.get_word()[i]
            else:
                for i in range(len(word.get_word())):
                    grid[word.get_row() + i][word.get_col()] = word.get_word()[i]

        # keep track of words
        words_used = [] # list(Word)
        words_unused = [] # list(str)
        
        # initialize grid
        grid = [['#' for _ in range(self.grid_size)] for _ in range(self.grid_size)] # list(str) where each space is either # (empty space) or letter
        
        # place first word horizontally on the center of the grid
        r = self.grid_size // 2
        c = (self.grid_size // 2) -  (len(words[0]) // 2)
        first_word = Word(words[0], r, c, True)
        insert_word(first_word)
        words_used.append(first_word)

        # try to place the rest of the words
        for word in words[1:]:
            potential_positions = {} # { score (int): word (Word) } where position is (r, c, true if horizontal and false otherwise)
            # note: duplicate scores are okay since we simply care bout the best score, this makes it a bit nicer to grab best position

            # find potential positions
            for existing_word in words_used:
                for i in range(len(existing_word.get_word())):
                    # create our potential positions
                    if existing_word.get_hor():
                        curr_position = Word(word, existing_word.get_row(), existing_word.get_col() + i, False)
                    else:
                        curr_position = Word(word, existing_word.get_row() + i, existing_word.get_col(), True)
                
                    # if potential position is found, score and add to potential_positions
                    valid_position = get_valid_position(curr_position)
                    if valid_position:
                        potential_positions[score_position(valid_position)] = valid_position

            if not potential_positions:
                words_unused.append(word)
            else:
                # find best position and add to words_used and grid
                best_score = max(potential_positions.keys())
                best_position = potential_positions[best_score]
                insert_word(best_position)
                words_used.append(best_position)

        return Crossword(grid, words_used, words_unused)

    def generate_crosswords(self, num_iter):
        """
        Attempt to generate num_iter crosswords. Assign these crosswords to self.crosswords.
        """
        crosswords = []
        for i in range(num_iter):
            # shuffle words to get a different board (using sample instead of shuffle to avoid in-place operations)
            shuffled_words = random.sample(self.word_list, len(self.word_list))
            # generate crossword and add to list of crosswords
            crosswords.append(self.generate_crossword(shuffled_words))

        self.crosswords = crosswords

    def print_crosswords(self):
        """
        Print crosswords sorted by score.
        """
        if not self.crosswords:
            print("No crosswords generated.")
            return

        sorted_crosswords = sorted(self.crosswords, key=lambda crossword: crossword.get_score(), reverse=True)

        for i, crossword in enumerate(sorted_crosswords, 1):
            print(f"Crossword #{i} with a score of {crossword.get_score()}")
            crossword.print_crossword()
            print("\n" + "-" * 20 + "\n")

    def get_crosswords(self):
        return self.crosswords
    
    def get_grid_size(self):
        return self.grid_size
    
    def get_word_list(self):
        return self.word_list