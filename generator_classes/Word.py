class Word:
    """
    A word in a crossword.

    Instance Variables:
    word (str): word the object represents
    row (int): row on the crossword grid of the first letter
    col (int): column on the crossword grid of the first letter
    horizontal (bool): true if the word is placed horizontally and false if vertically
    clue (str): clue associated with the word
    clue_number (int): the number of the word on the board
    """

    def __init__(self, word, row, col, horizontal):
        self.word = word
        self.row = row
        self.col = col
        self.horizontal = horizontal
        self.clue = ""
        self.clue_number = 0

    def get_word(self):
        return self.word
    
    def get_row(self):
        return self.row
    
    def get_col(self):
        return self.col
    
    def get_hor(self):
        return self.horizontal
    
    def get_clue(self):
        return self.clue
    
    def get_clue_number(self):
        return self.clue_number
    
    def update_clue_number(self, num):
        self.clue_number = num

    def update_clue(self, clue):
        self.clue = clue