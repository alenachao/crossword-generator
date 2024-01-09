import random
from generator_classes.Crossword import Crossword

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
        Generate a possible crossword puzzle.
        """
        # helper functions
        def score_position(word, position):
            """
            Returns how "good" the word position is based on the following parameters:
                - How much it increases the grid size (less is better)
                - How many already placed words it overlaps with (more is better)
            """
            
            if position[2]:
                # get grid score
                # if horizontal we only care abt left and right 
                left = min(words_used.values(), key=lambda p: p[1])[1]
                right = max((p[1] + len(w) if p[2] else p[1] for w, p in words_used.items()))

                grid_score_left = min(position[1] - left, 0)
                grid_score_right = max(position[1] - right, 0)

                grid_score = grid_score_left + grid_score_right

                # get overlap score: we go along the adjacent tiles of the word. 
                # if there's a letter on one side then that's a corner, if there are letters on both sides thats a cross (cross is better)
                overlap_score = 0
                for i in range(len(word)):
                    if r > 0 and grid[r - 1][c + i] != "#":
                        overlap_score += 1
                    if r < self.grid_size - 1 and grid[r + 1][c + i] != "#":
                        overlap_score += 1

                return grid_score + overlap_score
            else:
                # get grid score
                # if vertical we only care abt up and down
                top = min(words_used.values(), key=lambda p: p[0])[0]
                bottom = max((p[0] if p[2] else p[0] + len(w) for w, p in words_used.items()))

                grid_score_top = min(position[0] - top, 0)
                grid_score_bottom = max(position[0] - bottom, 0)

                grid_score = grid_score_top + grid_score_bottom

                # get overlap score: we go along the adjacent tiles of the word. 
                # if there's a letter on one side then that's a corner, if there are letters on both sides thats a cross (cross is better)
                overlap_score = 0
                for i in range(len(word)):
                    if c > 0 and grid[r + i][c - 1] != "#":
                        overlap_score += 1
                    if c < self.grid_size - 1 and grid[r + i][c + 1] != "#":
                        overlap_score += 1

                return overlap_score - grid_score + len(words_used) - len(words_unused)


        def get_valid_position(word, position):
            """
            Returns a valid position we could place the word, if none then return None. 
            Note this is not the same as curr_position since any letter in word can match with the letter at curr_position.
            A valid position is one where:
                - for any overlaps, letter of word and letter already placed must match
                - the word does not go off the grid
            """
            position_row = position[0]
            position_col = position[1]
            direction = position[2]

            position_letter = grid[position_row][position_col]
            letter_in_word = [i for i, letter in enumerate(word) if letter == position_letter]

            for i in letter_in_word:
                if direction: # if the existing word was placed horizontally, we want our new word to be placed vertically
                    start_position = (position[0] - i, position[1], not position[2])
                    if start_position[0] < 0 or position[0] + len(word) > self.grid_size:
                        continue
                    for j in range(len(word) + 1):
                        if j == len(word):
                            return start_position
                        elif start_position[0] + j > self.grid_size or (grid[start_position[0] + j][start_position[1]] != "#" and word[j] != grid[start_position[0] + j][start_position[1]]):
                            break
                else:
                    start_position = (position[0], position[1] - i, not position[2])
                    if start_position[1] < 0 or position[1] + len(word) > self.grid_size:
                        continue
                    for j in range(len(word) + 1):
                        if j == len(word):
                            return start_position
                        elif start_position[1] + j > self.grid_size or (grid[start_position[0]][start_position[1] + j] != "#" and word[j] != grid[start_position[0]][start_position[1] + j]):
                            break

        def insert_word(word, position):
            """
            Place word onto grid.
            """
            r = position[0]
            c = position[1]
            direction = position[2]

            if direction:
                for i in range(len(word)):
                    grid[r][c + i] = word[i]
            else:
                for i in range(len(word)):
                    grid[r + i][c] = word[i]

        # keep track of words
        words_used = {} # { word (str): position (tuple) } where position is (r, c, true if horizontal and false otherwise)
        words_unused = [] # list(str)
        
        # initialize grid
        grid = [['#' for _ in range(self.grid_size)] for _ in range(self.grid_size)] # list(str) where each space is either # (empty space) or letter
        
        # place first word horizontally on the center of the grid
        first_word = words[0]
        r = self.grid_size // 2
        try:
            c = (self.grid_size // 2) -  (len(first_word) // 2)
        except c < 0:
            raise "grid_size needs to be larger than all words available"
        
        position = (r, c, True)
        insert_word(first_word, position)
        words_used[first_word] = position

        # try to place the rest of the words
        for word in words[1:]:

            potential_positions = {} # { score (int): position (tuple) } where position is (r, c, true if horizontal and false otherwise)
            # note: duplicate scores are okay since we simply care bout the best score, this makes it a bit nicer to grab best position

            # find potential positions
            for existing_word in words_used:
                start_position = words_used[existing_word]
                for i in range(len(existing_word)):
                    # get current position, if horizontal we add to start col else we add to start row
                    if start_position[2]:
                        curr_position = (start_position[0], start_position[1] + i, start_position[2])
                    else:
                        curr_position = (start_position[0] + i, start_position[1], start_position[2])
                
                    # if potential position is found, score and add to potential_positions
                    valid_position = get_valid_position(word, curr_position)
                    if valid_position:
                        potential_positions[score_position(word, valid_position)] = valid_position

            if not potential_positions:
                words_unused.append(word)
            else:
                # find best position and add to words_used and grid
                best_score = max(potential_positions.keys())
                best_position = potential_positions[best_score]
                insert_word(word, best_position)
                words_used[word] = best_position

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

    def print_crosswords(self, num_crosswords):
        """
        Print the top num_crosswords crosswords based on score.
        """
        if not self.crosswords:
            print("No crosswords generated.")
            return

        sorted_crosswords = sorted(self.crosswords, key=lambda crossword: crossword.score, reverse=True)

        print(f"Printing top {num_crosswords} crosswords:")
        for i, crossword in enumerate(sorted_crosswords[:num_crosswords], 1):
            print(f"Crossword #{i}")
            crossword.print_crossword()
            print("\n" + "-" * 20 + "\n")

    def get_crosswords(self):
        return self.crosswords


