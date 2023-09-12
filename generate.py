# Faiyaz Hasan 
import sys

from crossword import *
import itertools
import copy

class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # accessing the words in the domain 
        for domain_value in self.domains: 
            # empty set stores words that don't meet the unary constraint 
            inconsistent_words = set()
            
            # checking if the unary constraint is met
            for word in self.domains[domain_value]: 
                if len(word) != domain_value.length: 
                    inconsistent_words.add(word)

            # removing the inconsistent words from the domain
            for word in inconsistent_words:
                self.domains[domain_value].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.
        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False

        # tuple (i, j) where x's ith character overlaps y's jth character
        overlap_loc = self.crossword.overlaps[x, y]

        # checking if there is an overlapping cell between x and y  
        if overlap_loc is not None:
            inconsistent_words = set()
            
            # for words in the x domain 
            for x_word in self.domains[x]:
                # accessing the (i,j) overlapping tuple, where the i'th character represents x 
                x_overlap_char = x_word[overlap_loc[0]]
                y_overlap_chars = []
                # finding all corresponding characters in the y domain that can go in the sane cell 
                for y_word in self.domains[y]:
                    y_overlap_chars.append(y_word[overlap_loc[1]])
                # if there are no matching characters for the corresponding char in x 
                # then remove that word from x domain
                if x_overlap_char not in y_overlap_chars:
                    inconsistent_words.add(x_word)
                    revised = True
            
            # removing the inconsistent words 
            for word in inconsistent_words:
                self.domains[x].remove(word)
        
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.
        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
         # checking for if the arc is empty  
        if arcs is None:
            queue = []
            for var1 in self.crossword.variables: 
                for var2 in self.crossword.variables: 
                    # checking for if var1 is not equal to var2 and there is an overlap between var1 and var 2
                    if var1 != var2 and self.crossword.overlaps[var1, var2] is not None: 
                        # appending to the queue
                        queue.append((var1, var2))
        else:
            queue = arcs
        
        # checking whether the queue is not empty 
        while len(queue) != 0: 
            x, y = queue.pop(0)

            if self.revise(x, y):
                if len(self.domains[x]) == 0: 
                    # it is impossible to solve problem since there are no values left in domain
                    return False
                
                # adding neighbors of x to the list since x changed 
                for z in (self.crossword.neighbors(x) - {y}): 
                    queue.append((z, x))

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # checking if all assignment keys are valid variables and assigned a value 
        if set(assignment.keys()) == self.crossword.variables and all(assignment.values()):
            return True
        else:
            return False
        
    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # checking that all words are distinct
        unique_values = set(assignment.values())
        if len(unique_values) != len(set(assignment.keys())):
            return False

        # checking that all values are the correct length
        for key, value in assignment.items(): 
            if key.length != len(value): 
                return False 
        
        # checking that there are no conflicts between neighboring variables
        for key, value in assignment.items():
            known_neighbors = self.crossword.neighbors(key).intersection(assignment.keys())
            for neighbor in known_neighbors:
                # (i, j) tuple where key's ith character overlaps neighbor's jth character
                overlap_loc = self.crossword.overlaps[key, neighbor]
                
                # there is a conflict if the ith value in the first word is not equal to 
                # the jth value in the second word
                if value[overlap_loc[0]] != assignment[neighbor][overlap_loc[1]]:
                    return False
        
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # initializing all restrictions to zero
        num_restrictions = {} 
        for elem in self.domains[var]: 
            num_restrictions[elem] = 0 
        
        # finding unassigned neighbors 
        unassigned_neighbors = self.crossword.neighbors(var) - assignment.keys()

        # looking for overlaps in relation to the unassigned neighbord 
        for word_var_d in self.domains[var]:
            for neighbor in unassigned_neighbors:
                overlap_loc = self.crossword.overlaps[var, neighbor]

                # if the i'th value not equal to the j'th value, 
                # then add to the value of num_restrictions because of conflict 
                for word_neighbor_d in self.domains[neighbor]:
                    if word_var_d[overlap_loc[0]] != word_neighbor_d[overlap_loc[1]]:
                        num_restrictions[word_var_d] += 1
        
        # the sorted list 
        sorted_lst = sorted(num_restrictions.items(), key=lambda x: x[1])

        return [elem[0] for elem in sorted_lst]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        
        # finding the unassigned variables 
        unassigned_vars = self.crossword.variables - assignment.keys()

        # dictionary with the variables as the keys and the corresponding number of 
        # elements in their domains as values
        num_values = {}
        for var in unassigned_vars:
            num_values[var] = len(self.domains[var])

        # sort based on number of values in domain
        sorted_num_values = sorted(num_values.items(), key=lambda x: x[1])

        # no tie if there is only one element
        if len(sorted_num_values) == 1 or (sorted_num_values[0][1] != sorted_num_values[1][1]):
            return sorted_num_values[0][0]
        else:
            # find the variables that tie based on the number of remaining values
            ties = []
            tie_val = sorted_num_values[0][1]
            for i in range(len(sorted_num_values)):
                if sorted_num_values[i][1] == tie_val:
                    ties.append(sorted_num_values[i])
                elif sorted_num_values[i][1] > tie_val:
                    break
            ties = dict(ties)

            # break tie based on the variable among the tied variables that has the largest degree
            num_degrees = {}
            for var in ties.keys():
                num_degrees[var] = len(self.crossword.neighbors(var))
            sorted_num_degrees = sorted(num_degrees.items(), key=lambda x: x[1], reverse=True)
            return sorted_num_degrees[0][0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.
        `assignment` is a mapping from variables (keys) to words (values).
        If no assignment is possible, return None.
        """
        # checking if the assignment is complete
        if self.assignment_complete(assignment): 
            return assignment 

        # for unassignment variables 
        unassigned_var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(unassigned_var, assignment): 

            # making a deepcopy of the assignment 
            assignment_copy = copy.deepcopy(assignment) 
            assignment_copy[unassigned_var] = value 

            # checking if the assignment copy is consistent 
            if self.consistent(assignment_copy): 

                # then unassigned variable is given this assignment 
                assignment[unassigned_var] = value 
                result = self.backtrack(assignment) 
                if result is not None: 
                    return result 

                assignment.pop(unassigned_var, None)  
        return None 

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()