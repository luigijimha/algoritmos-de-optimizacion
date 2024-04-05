import numpy as np


grid = [[8,0,0,0,0,7,0,9,0],
        [0,2,9,0,0,4,0,0,6],
        [3,0,0,2,0,0,0,0,0],
        [0,0,0,0,0,6,5,0,0],
        [0,1,7,4,0,0,0,3,0],
        [2,0,0,0,0,0,0,0,0],
        [0,9,4,1,0,0,0,7,0],
        [0,0,8,0,0,0,0,0,0],
        [0,0,0,0,7,0,0,0,3]]

def possible(row, column, number):
    global grid
    # ¿Aparece el número en la fila dada?
    for i in range(0,9):
        if grid[row][i] == number:
            return False

    # ¿Aparece el número en la columna dada?
    for i in range(0,9):
        if grid[i][column] == number:
            return False

    # ¿Aparece el número en el cuadrado dado?
    x0 = (column // 3) * 3
    y0 = (row // 3) * 3
    for i in range(0,3):
        for j in range(0,3):
            if grid[y0+i][x0+j] == number:
                return False

    return True


def print_sudoku():
   for i, row in enumerate(grid):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - - -")
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if row[j] == 0:
                print(". ", end="")
            else:
                print(f"{row[j]} ", end="")
        print()


def solve():
    global grid
    for row in range(0,9):
        for column in range(0,9):
            # current tuple needs an algorithm to be found
            if grid[row][column] == 0:
                for number in range(1,10):
                    if possible(row, column, number):
                        grid[row][column] = number
                        #print_sudoku()
                        solve()
                        grid[row][column] = 0

                return
    print_sudoku()

    #print(np.matrix(grid))
    #input('Generar otra posible solución (presione Enter para salir)')




print_sudoku()
print("="*30)

solve()