class Crossword:
    """
    One possible crossword puzzle from a list of words.

    Instance Variables:
    grid (list(list(str))): the grid containing the positioned words and empty spaces
    words_used (dict(str:tuple(int,int,bool))): words successfully placed in grid with their position
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
            left = min(words_used.values(), key=lambda p: p[1])[1]
            right = max((p[1] + len(w) if p[2] else p[1] for w, p in words_used.items()))
            top = min(words_used.values(), key=lambda p: p[0])[0]
            bottom = max((p[0] if p[2] else p[0] + len(w) for w, p in words_used.items()))
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

            return ratio_score - grid_score + len(words_used.keys())
        
        self.grid = grid
        self.words_used = words_used
        self.words_unused = words_unused
        self.score = score_crossword()

        


    def print_crossword(self):
        """
        Print the grid, list of words used, lists of words unused, and score of the crossword
        """
        print(f'''Crossword with a score of {self.score}
Words used: {[word for word in self.words_used.keys()]}
Words unused: {self.words_unused}''')
        
        for row in self.grid:
            print(' '.join(row))