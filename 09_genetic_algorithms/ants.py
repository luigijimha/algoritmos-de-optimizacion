from copy import deepcopy
import random

"""
initializes a path of N steps followed by an ant
@return     returns an array of STEPS length simulating the path followed by the ant
"""
def initializePath():
    return [random.randint(0, 3) for _ in range(STEPS)]

"""
validates how much food did the ant eat
@param{List} ant     list with steps followed by ant
@return              count of food eaten by ant
"""
def fitness(ant):
    coords = STARTING_COORDS
    newMap = deepcopy(MAP)
    food = 0

    for move in ant:
        # validate ant movement is within map boundaries
        new_coords = (coords[0] + MOVEMENTS[move][0], coords[1] + MOVEMENTS[move][1])
        if 0 <= new_coords[0] < len(newMap) and 0 <= new_coords[1] < len(newMap[0]):
            if newMap[new_coords[0]][new_coords[1]] == 1:
                # if current field has food on it, increase counter and remove food from field
                food += 1
                newMap[new_coords[0]][new_coords[1]] = 0
            coords = new_coords

    return food

"""
creates a new ant based on random its parent genes
@param{List} A     parent ant path data
@param{List} B     parent ant path data
@return            returns new generated ant
"""
def mating(A, B):
    new_entity = []

    # generate a random child from parent genes
    for gene_A, gene_B in zip(A, B):
        new_entity.append(random.choice([gene_A, gene_B]))

    return new_entity

"""
performs mutations to an ant
@param{List} entity     ant path data who is goint to mutate
@return                 ant with mutated genes
"""
def mutate(entity):
    for i in range(len(entity)):
        # randomly decide if a gen must mutate or not
        if random.random() <= MUTATION_PROBABILITY:
            entity[i] = random.randint(0, 3)

    return entity

"""
calculates population descendency
@param{List} population     list with all the ants in the current generation
@return                     new list with ants for next generation
"""
def descendency(population):
    new_population = []
    survivors = []
    roulette = {}

    # create a roulette to select ants from the population
    for ant in population:
        fit = fitness(ant)
        if roulette.get(fit) is None:
            # if it is the first time a fit value was found, initialize an array
            roulette[fit] = []
        # add ant to group
        roulette[fit].append(ant)

    # order fit values from highest to smallest
    groupIndexes = sorted(roulette, key=lambda k: k, reverse=True)

    # randomly select half of the population as survivors
    for _ in range(TOTAL_ANTS // 2):
        # randomly select a group based on ants fitness
        groupIndex = 0
        p = random.random()
        lastIndex = len(groupIndexes) - 1

        # find elected value by roulette
        while p > ROULETTE_PROPORTION and groupIndex < lastIndex:
            groupIndex += 1
            p *= ROULETTE_PROPORTION

        # pick up selected survivor
        survivor = random.choice(roulette[groupIndexes[groupIndex]])
        roulette[groupIndexes[groupIndex]].remove(survivor)
        survivors.append(survivor)

        # remove group from roulette if it is now empty
        if len(roulette[groupIndexes[groupIndex]]) == 0:
            del groupIndexes[groupIndex]

    # reproduce survivors to create new population
    while len(new_population) < TOTAL_ANTS:
        mom = random.choice(survivors)
        dad = random.choice(survivors)
        kid = mating(mom, dad)
        kid = mutate(kid)
        new_population.append(kid)

    return survivors + new_population

def main():
    population = [initializePath() for _ in range(TOTAL_ANTS)]

    for _ in range(GENERATIONS_LIMIT):
        new_generation = descendency(population)
        population = new_generation

    best = max(population, key=fitness)
    print('Best solution:', best, ', Food:', fitness(best))


STARTING_COORDS = (0, 0)

MOVEMENTS = {
    0: (-1, 0),  # move up
    1: (0, 1),  # move right
    2: (1, 0),  # move down
    3: (0, -1)  # move left
}

TOTAL_ANTS = 10
STEPS = 10
GENERATIONS_LIMIT = 1000
MUTATION_PROBABILITY = 0.1
ROULETTE_PROPORTION = 0.8

MAP = [
    [0, 0, 1, 0, 1, 1],
    [0, 1, 1, 0, 0, 1],
    [0, 1, 0, 0, 1, 0],
    [1, 1, 0, 0, 0, 1],
    [0, 0, 0, 1, 1, 0],
    [1, 0, 1, 0, 1, 0]
]

main()