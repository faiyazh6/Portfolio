import itertools
import random
import copy 


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j] 

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count 

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self): 
        """ 
        Returns the set of all cells in self.cells known to be mines.
        """ 
        if len(self.cells) == self.count: 
            return self.cells 
        else: 
            return set() 

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0: 
            return self.cells 
        else: 
            return set() 

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.count -= 1 
            self.cells.remove(cell) 

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells: 
            self.cells.remove(cell) 

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell): 
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """ 
        self.mines.add(cell) 
        for sentence in self.knowledge: 
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count): 
        """ 
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made 
            2) mark the cell as safe 
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge 
        """ 
        # step 1 
        self.moves_made.add(cell) 

        # step 2 
        self.mark_safe(cell)

        # step 3 
        i, j = cell
        cells_to_add = []
        for row in range(i-1, i+2, 1):
            for col in range(j-1, j+2, 1): 
                if not row < 0 and not col < 0 and not row >= self.width and not col >= self.height and not (row == i and col == j):
                    cell_to_check = (row, col)
                    if not cell_to_check in self.moves_made:
                        if cell_to_check in self.mines:
                            count -= 1
                        elif cell in self.safes:  
                            continue 
                        else:
                            cells_to_add.append((row, col))
        self.knowledge.append(Sentence(set(cells_to_add), count)) 

        knowledge_copy = copy.deepcopy(self.knowledge) 
        for sentence in knowledge_copy:
            if len(sentence.known_safes()) != 0:
                for safe_cell in sentence.cells:
                    self.mark_safe(safe_cell)
            elif len(sentence.known_mines()) != 0:
                for mine_cell in sentence.cells:
                    self.mark_mine(mine_cell)
                    
        # steps 3 and 4
        i, j = cell
        cells_to_add = []
        for row in range(i-1, i+2, 1):
            for col in range(j-1, j+2, 1): 
                # make sure the i and j are within the height by width 
                # (row, col) != cell 
                cell_to_check = (row, col)
                if not row < 0 and not col < 0 and not row >= self.width and not col >= self.height and not (row == i and col == j):
                    if not cell_to_check in self.moves_made:  
                        if cell_to_check in self.mines:  
                            count -= 1 
                            # self.knowledge.mark_mine(Sentence(set(cells_to_add), count))  
                        elif cell_to_check in self.safes:  
                            continue 
                        else: 
                            cells_to_add.append((row, col)) 
        self.knowledge.append(Sentence(set(cells_to_add), count)) 
        
        # step 5 
        # make a copy of the knowledge base, and then iterate through the copy 
        # keep track of new sentences in the KB 
        # every time somethign new in og KB, keep making a new copy and then iterate through it --> use a while loop.  
        change = True  
        while change:  
            change = False   
            knowledge_copy = copy.deepcopy(self.knowledge) 
            for sentence in knowledge_copy: 
                # sentence.cells => set 
                # sentence.count => count
                # write a method where we find if sentence.cells is a subset of any other sentence's cells 
                # keep track of every inference until you can't do anything - keep track of every sentence being added, and then go back and create another copy
                # iterating over cells, and seeing if those cells are in self.safes, if the sentence's safe cells not in self.sales, update self.cells to add these cell sin self.sales
                safe_cells = list(sentence.known_safes())
                mines = list(sentence.known_mines()) 
                for cell in safe_cells: 
                    if cell not in self.safes: 
                        self.mark_safe(cell) 
                        change = True 
                for cell in mines: 
                    if cell not in self.mines: 
                        self.mark_mine(cell)   
                        change = True     
                for other_sentence in knowledge_copy: 
                    if other_sentence != sentence: 
                        if sentence.cells: 
                            if sentence.cells.issubset(other_sentence.cells): 
                                new_sentence = Sentence(other_sentence.cells.difference(sentence.cells), other_sentence.count - sentence.count)
                                if new_sentence not in self.knowledge: 
                                    self.knowledge.append(new_sentence)  
                                    change = True 

    # iterate through every sentence in self.knowledge and see if it has safe cells that is not in AI's self.safe variable --> do it for mines as well 
    # keep track of self.safes and self.mines updating 

    def make_safe_move(self): 
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values. 
        """         
        for cell in self.safes: 
            if cell not in self.moves_made:  
                return cell 
        # Ask what to return if no more safe moves 
        return None 

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        board = []
        for i in range(self.height):
            for j in range(self.width):
                board.append((i, j))

        board = set(board) 
        excluded_moves = self.moves_made.union(self.mines)
        relevant_moves = board.difference(excluded_moves)

        if len(relevant_moves) == 0:
            return None 

        relevant_moves = list(relevant_moves) 
        idx = random.randint(0, len(relevant_moves) - 1) 
        return relevant_moves[idx] 