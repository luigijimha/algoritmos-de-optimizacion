class LifeGame:
    # height size of board
    height: int
    # width size of board
    width: int
    # list of height*width size which stores initial board with cell states
    # 1 means it is an alive cell
    # 0 means it is a dead cell
    board: list

    def __init__(self, board=[], height=0, width=0):
        self.board = board
        self.height = height
        self.width = width

    """
    counts alive neighbors around a cell
    @param {int} index    index of cells you want to verify its neighbor status
    @return {int}         total alive neighbors around the cell
    """
    def findAliveNeighbors(self, index):
        alive_neighbors = 0
        # calculate current row and column
        row, col = index // self.width, index % self.width

        # look neighbors around cell
        for i in range(-1, 2):
            for j in range(-1, 2):
                # skip the cell itself
                if i == 0 and j == 0:
                    continue

                # calculate neighbor's row and column
                neighbor_row, neighbor_column = row + i, col + j

                # verify row and column are within the board boundaries
                if 0 <= neighbor_row < self.height and 0 <= neighbor_column < self.width:
                    # verify if neighbor is alive
                    if self.board[neighbor_row * self.width + neighbor_column] == 1:
                        alive_neighbors += 1

        return alive_neighbors

    """
    executes the life game loop for certain amount of time
    @param {int} time    the amount of time the life game will be executed
    """
    def play(self, time):
        print('time 0')
        self.printBoard()

        for t in range(time):
            # initialize new board
            new_board = [-1] * (self.height * self.width)

            # update board cell status
            for i in range(self.height):
                for j in range(self.width):
                    index = i * self.width + j

                    # count cell alive neighbors
                    alive_neighbors = self.findAliveNeighbors(index)
                    
                    # conway life game rules
                    if self.board[index] == 1:
                        # cell survives if it is surrounded by 2 or 3 alive cells
                        if alive_neighbors in [2, 3]:
                            new_board[index] = 1
                        # cell dies due to underpopulation or overpopulation
                        else:
                            new_board[index] = 0
                    else:
                        # dead cell revives if it is surrounded by exactly 3 cells
                        if alive_neighbors == 3:
                            new_board[index] = 1
                        # dead cell cannot revive
                        else:
                            new_board[index] = 0

            self.board = new_board

            print('time', t+1)
            self.printBoard()

    """
    setter for new board game
    @param {list} board    new initial board for cells
    @param {int} height    height of new board
    @param {int} width     width of new board
    """
    def setBoard(self, board, height, width):
        self.board = board
        self.height = height
        self.width = width

    """
    prints board number
    """
    def printBoard(self):
        for i in range(self.height):
            for j in range(self.width):
                print(self.board[i * self.width + j], end=" ")
            print()
        print('\n')

"""
board = [
    1, 0, 1, 1, 0,
    0, 1, 1, 0, 1,
    0, 1, 0, 0, 0,
    0, 0, 1, 1, 0,
    0, 1, 1, 0, 1,
    0, 0, 0, 1, 0
]
"""

"""
board = [
    1, 1, 1, 1, 1,
    1, 1, 1, 1, 1,
    1, 1, 1, 1, 1,
    1, 1, 1, 1, 1,
    1, 1, 1, 1, 1,
    1, 1, 1, 1, 1
]
"""

"""
board = [
    1, 0, 1, 0, 1,
    0, 1, 0, 1, 0,
    1, 0, 1, 0, 1,
    0, 1, 0, 1, 0,
    1, 0, 1, 0, 1,
    0, 1, 0, 1, 0
]
"""
"""
board = [
    1, 1, 0, 0, 1,
    1, 1, 0, 0, 1,
    0, 0, 1, 1, 0,
    0, 0, 1, 1, 0,
    1, 1, 0, 0, 1,
    1, 1, 0, 0, 1
]
"""

board = [
    1, 1, 1, 0, 0,
    1, 1, 1, 0, 0,
    1, 1, 1, 0, 0,
    0, 0, 0, 1, 1,
    0, 0, 0, 1, 1,
    0, 0, 0, 1, 1
]

game = LifeGame(board, 6, 5)

game.play(20)