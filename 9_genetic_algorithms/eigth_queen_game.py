from queue import PriorityQueue
import random

"""
initialize a game with random positions
@return     game board with pieces randomly positioned
"""
def initializeGame():
    game = [i for i in range(8)]
    random.shuffle(game)
    return game

"""
fitness function that validates how many queens are not being attacked
@param {List}     board data
@return           metric for unattacked queens
"""
def fitness(positions):
    score: int = 8

    # compare each queen with each other
    for row in range(8):
        column = positions[row]
        
        for x in range(row+1, 8):
            # diminish score if queen is in a diagonal
            if abs(row - x) == abs(column - positions[x]):
                score -= 1

            # there is no need to look for horizontal and vertical lines since board structure prevents these problem

    return score

"""
calculates the next generation of a population
@param {List}     population list
@return           new population for next iteration
"""
def descendency(population):
    pq = PriorityQueue()
    new_population = []

    # shuffle population and estratificate it in groups
    random.shuffle(population)

    for i in range(0, POPULATION_SIZE, POPULATION_GRUOP_SIZE):
        population_group = population[i: i+POPULATION_GRUOP_SIZE]

        # insert positions inside the pq based on its fitness
        for position in population_group:
            pq.put((fitness(position), position))

        # keep half of the population
        for _ in range(int(POPULATION_GRUOP_SIZE/2)):
            # half of the population survives
            _, positions = pq.get()
            new_population.append(positions)

            # this algorithm uses asymetric reproduction xD, skip mating process
            # create descendency for each chromosome with mutations
            new_population.append(mutate(positions))

    return new_population

"""
mutates an board by performing a random shuffle inside the board
@param {List}     board data
@return           mutated board
"""
def mutate(positions):
    a = random.randint(0, len(positions) - 2)
    b = random.randint(a + 1, len(positions) - 1)

    left = positions[:a]
    mutation = positions[a:b+1]
    right = positions[b+1:]
    
    random.shuffle(mutation)

    return left + mutation + right

"""
returns a solution if current population has one
@param {List}     list with current population
@return           entity that solves problem or an empty list of no one solves the problem
"""
def findSolution(population):
    for positions in population:
        if fitness(positions) == 8:
            return positions
        
    return []

def main():
    population = [initializeGame() for _ in range(int(POPULATION_SIZE))]
    limit: int = 0
    solution = findSolution(population)

    while solution == [] and limit < ITERATIONS_LIMIT:
        population = descendency(population)
        solution = findSolution(population)
        limit += 1

    if solution != []:
        print('solution found:', solution)
        print('iterations:', limit)
    else:
        print('solution not found')


POPULATION_SIZE = 100
POPULATION_GRUOP_SIZE = 10
ITERATIONS_LIMIT = 1000

# note: the board is a list that represents the coordinates where the queens should be placed
#       the index is the row and the value is the column
main()