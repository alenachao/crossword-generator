import requests

class Crossword:
    """
    One possible crossword puzzle from a list of words.

    Instance Variables:
    grid (list(list(str))): the grid containing the positioned words and empty spaces
    words_used (list(Word)): words successfully placed in grid with their position
    words_unused (list(str)): words that were not used in the grid
    score (int): a measure on how "good" the crossword is
    """

    def __init__(self, grid, words_used, words_unused):

        def score_crossword():
            """
            Returns how "good" the crossword is based on the following parameters:
                - Number of words placed (more is better)
                - Grid size actually used (less is better)
                - Ratio between height and width (close to 1 is better)
            """
            left = min([w.get_col() for w in words_used])
            right = max([w.get_col() + len(w.get_word()) if w.horizontal else w.get_col() for w in words_used ])
            top = min([w.get_row() for w in words_used])
            bottom = max([w.get_row() + len(w.get_word()) if not w.horizontal else w.get_row() for w in words_used])

            height = bottom - top
            width = right - left

            grid_score = height*width

            # get ratio_score
            ratio = height / width
            diff_from_one = abs(ratio - 1)

            if diff_from_one == 0:
                ratio_score = grid_score
            else:
                # calculate the score based on the reciprocal of the absolute difference
                ratio_score = 1 / diff_from_one

            return ratio_score - grid_score + len(words_used)
        
        self.grid = grid
        self.words_used = words_used
        self.words_unused = words_unused
        self.score = score_crossword()

    def print_crossword(self):
        """
        Print the grid, list of words used, lists of words unused, and score of the crossword
        """
        print(f'''Score: {self.score}
Words used: {[word.get_word() for word in self.words_used]}
Words unused: {self.words_unused}''')
        
        for row in self.grid:
            print(' '.join(row))

    def add_clue_numbers(self):
        # sort by col and row number and assign from there. python .sort() is stable
        self.words_used.sort(key=lambda x: x.get_col())
        self.words_used.sort(key=lambda x: x.get_row())

        # assign numbers
        curr_num = 1
        for i in range(len(self.words_used)):
            self.words_used[i].update_clue_number(curr_num)

            # if 2 words have the same position then they have the same number.
            if (i + 1 < len(self.words_used)) and \
                (self.words_used[i].get_row() == self.words_used[i + 1].get_row()) and \
                (self.words_used[i].get_col() == self.words_used[i + 1].get_col()):
                curr_num -= 1
            
            curr_num += 1

    
    def add_clues(self):
        for word in self.words_used:
            word.update_clue(self.get_word_definition(word))

    def get_word_definition(self, word):
        url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word.word}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()[0]
            if "meanings" in data:
                return data["meanings"][0]["definitions"][0]["definition"]
        return "Sorry, unable to generate clue..."

    def get_grid(self):
        return self.grid

    def get_words_used(self):
        return self.words_used
    
    def get_words_unused(self):
        return self.words_unused
    
    def get_score(self):
        return self.score