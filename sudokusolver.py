import copy, time

# default grid
GRID = [['5', '3', ' ', ' ', '7', ' ', ' ', ' ', ' '],
        ['6', ' ', ' ', '1', '9', '5', ' ', ' ', ' '],
        [' ', '9', '8', ' ', ' ', ' ', ' ', '6', ' '],
        ['8', ' ', ' ', ' ', '6', ' ', ' ', ' ', '3'],
        ['4', ' ', ' ', '8', ' ', '3', ' ', ' ', '1'],
        ['7', ' ', ' ', ' ', '2', ' ', ' ', ' ', '6'],
        [' ', '6', ' ', ' ', ' ', ' ', '2', '8', ' '],
        [' ', ' ', ' ', '4', '1', '9', ' ', ' ', '5'],
        [' ', ' ', ' ', ' ', '8', ' ', ' ', '7', '9']]

# spaces with numbers drawn in originally
FIXED = []

for i in range(9):
    for j in range(9):
        if GRID[i][j] != " ":
            FIXED.append((i, j))


class Sudoku():

    def __init__(self, grid=GRID, fixed=FIXED):
        self.grid = grid
        self.fixed = fixed  # keep track of which values were part of the original board
        self.choices = []  # a list of choices for each empty space
        for row in range(9):
            new_row = []
            for col in range(9):
                if (row, col) not in self.fixed:
                    new_row.append(self.available(row, col))
                else:
                    new_row.append([])
            self.choices.append(new_row)

    def __eq__(self, other):
        return self.grid == other.grid

    def __hash__(self):
        return hash(str(self.grid))

    # is this puzzle solved?
    def solved(self):
        for i in range(9):
            if " " in self.grid[i]:
                return False

        return self.conflicting() == 0

    # function for returning the positions in one box
    def box(self, row, col):
        positions = []
        for i in range(row, row + 3):
            for j in range(col, col + 3):
                positions.append((i, j))

        return positions

    def conflicting(self):
        conflicts = 0

        # row conflicts
        for row in range(9):
            row_seen = []
            for col in range(9):
                if self.grid[row][col] != " ":
                    if self.grid[row][col] in row_seen:
                        conflicts += 1
                    else:
                        row_seen.append(self.grid[row][col])

        # column conflicts
        for col in range(9):
            col_seen = []
            for row in range(9):
                if self.grid[row][col] != " ":
                    if self.grid[row][col] in col_seen:
                        conflicts += 1
                    else:
                        col_seen.append(self.grid[row][col])

        # box conflicts
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                box_seen = []
                positions = self.box(i, j)
                for pos in positions:
                    if self.grid[pos[0]][pos[1]] != " ":
                        if self.grid[pos[0]][pos[1]] in box_seen:
                            conflicts += 1
                        else:
                            box_seen.append(self.grid[pos[0]][pos[1]])

        return conflicts

    # print
    def display(self):
        # this puzzle will always be nine by nine
        for r in range(9):
            if r % 3 == 0:
                print("=========================")
            print("| ", end='')
            for c in range(9):
                if (r, c) in self.fixed:
                    # print a bold character for the fixed numbers
                    code = int(self.grid[r][c]) + 0x1D7CE
                    print("{:c}".format(code), end='')
                else:
                    # print a regular character for our guesses
                    print(self.grid[r][c], end='')
                if c % 3 == 2:
                    # put vertical bars between boxes so that they are easier to see
                    print(" | ", end='')
                else:
                    print(" ", end='')
            print()
        print("=========================")

    # return a new puzzle created by a move
    def neighbor(self, pos, num):
        new = copy.deepcopy(self.grid)
        new[pos[0]][pos[1]] = num
        return Sudoku(new, self.fixed)

    # return how many moves could be made for the given empty space
    def available(self, row, col):
        moves = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        if (row, col) not in self.fixed:  # just in case (we shouldn't call this method on a fixed square)
            # check for the conflicts
            for i in range(9):
                if self.grid[i][col] in moves:
                    moves.remove(self.grid[i][col])
                if self.grid[row][i] in moves:
                    moves.remove(self.grid[row][i])

            positions = self.box((row // 3) * 3, (col // 3) * 3)  # this is just the top left corner of the box to which the empty space belongs
            for pos in positions:
                if self.grid[pos[0]][pos[1]] in moves:
                    moves.remove(self.grid[pos[0]][pos[1]])

            return moves

    # get all empty spaces on the board
    def empty(self):
        moves = []
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == " ":
                    moves.append((i, j))

        return moves

    # returns box with minimum number of choices available to it
    def minimum(self):
        min = 10
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == " ":
                    choices = self.available(i, j)
                    if len(choices) < min:
                        min = len(choices)
                        min_pos = (i, j)

        return min_pos

    def solve(self):
        self.display()
        # start solving from space with smallest number of choices
        return self.inner_solve(self.minimum())

    def inner_solve(self, position):
        min_moves = self.choices[position[0]][position[1]]
        for move in min_moves:
            choice = self.neighbor(position, move)
            choice.display()
            time.sleep(.15)

            broken = False
            for i in range(9):
                for j in range(9):
                    if choice.grid[i][j] == " ":
                        if len(choice.choices[i][j]) == 0:
                            broken = True
                            break
                if broken:
                    break

            if not broken:
                if choice.solved():
                    return True
                # move to next minimum choice space
                result = choice.inner_solve(choice.minimum())
                if result:
                    return True
        return False


############################
#  M A I N  P R O G R A M  #
############################

puzzle = Sudoku()
result = puzzle.solve()
if result is False:
    print("Failed to solve.")
else:
    print("Puzzle solved! B)")
