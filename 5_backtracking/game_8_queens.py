"""
performs backtracking to find all the possible solutions for eight queens game
"""
def solveQueenPositions(positions):
    # get current iteration row
    row = len(positions)

    # if current row index is 8 that means game has been completed
    if row == 8:
        global queenPositionsSolutions
        queenPositionsSolutions.append(positions)
        return
    
    # find all possible positions in current row
    posiblePositions = []

    for i in range(8):
        # flag that determines if queen can be added at current position
        flag = True

        # look for unattacked positions by queens
        for queen in positions:
            x, y = queen

            # queen is in current column
            if x == i:
                flag = False
                break

            # queen is in a diagonal
            if abs(y - row) == abs(x - i):
                flag = False
                break

        # current position is available
        if flag:
            posiblePositions.append(i)

    # perform backtracking to find solution
    for option in posiblePositions:
        newPositions = positions.copy()
        newPositions.append((option, row))

        solveQueenPositions(newPositions)


# array that stores all queen position solutions
# it is updated through global inside the function
queenPositionsSolutions = []
# call the function to look for positions
solveQueenPositions([])

print('total solutions:', len(queenPositionsSolutions))

# display all solutions
for positions in queenPositionsSolutions:
    print(positions)