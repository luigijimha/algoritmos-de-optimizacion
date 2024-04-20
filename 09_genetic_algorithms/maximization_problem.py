from queue import PriorityQueue
import random

"""
finds craft limits for production
@return     list with craft limits for each craft
"""
def findCraftLimits():
    global crafts, resources
    limits = []
    for craft in crafts:
        min = float('inf')

        # find the maximum craft you can product based on available materials
        for i in range(len(craft)):
            material_limit = resources[i]
            materials_per_unit = craft[i]
            limit = material_limit // materials_per_unit
            # update production limit
            min = limit if limit < min else min
        
        # add limit found to array
        # note: this limit represents the maximum crafts possible if you production is oriented to produce an specific product only
        limits.append(min)

    return limits

"""
create a random gen value
@param{int} start     lower limit for random value
@param{int} end       upper limit for random value
@return               random value for gen
"""
def randomizeGen(start, end):
    rand = random.uniform(start, end)
    return  float(PRECISION.format(rand))

"""
intializes an entity representing the production goals for a production
@param {List} limits     list with the individual production limits
@return                  list with randomly generated production goals
"""
def initializeEntity():
    global limits
    entity = []

    for limit in limits:
        # add random production goal for current entity
        entity.append(randomizeGen(0, limit))

    return entity
        

"""
calculates efficiency of the entity to solve the problem
@param {List} entity             produced crafts array
@return                          gain for current entity to solve problem
"""
def fitness(entity):
    global restrictions, crafts, crafts_gain, resources

    score = 0
    resource_usage = [0 for _ in range(len(crafts_gain))]

    # count resource usage
    for i in range(len(crafts)):
        craft = crafts[i]
        for j in range(len(craft)):
            resource_usage[j] += craft[j] * entity[i]

    # verify if resource usage was exceded
    for i in range(len(resource_usage)):
        if resource_usage[i] > resources[i]:
            # usage was exceded, solution is invalid
            return 0

    # find which custom production restrictions are being violated
    for restriction in restrictions:
        sum = 0

        # sum the values in each restriction equation
        for i in range(len(restriction)-1):
            sum += entity[i] * restriction[i]

        # verify if the restriction equation was violated
        if sum > restriction[len(restriction)-1]:
            # restriction is being violated, set score to 0. invalid result
            return 0

    # calculate gain for current entity
    for i in range(len(crafts_gain)):
        score += crafts_gain[i] * entity[i]

    return score

"""
calculates population descendency
@param{List} population     list with all the entities in the current generation
@return                     new list with entities for next generation
"""
def descendency(population):
    pq = PriorityQueue()
    survivors = []
    new_population = []

    # insert all the population in the pq based on its fitness
    for entity in population:
        fit = fitness(entity)
        pq.put((-fit, entity)) # use - simbol to order DESC

    # look for the survivors
    for _ in range(int(POPULATION_SIZE/2)):
        _, entity = pq.get()
        survivors.append(entity)

    # kill remaining population
    del pq

    # reproduce survivors
    for _ in range(int(POPULATION_SIZE/2)):
        mom = random.choice(survivors)
        dad = random.choice(survivors)
        kid = mating(mom, dad)

        # mutate kid
        kid = mutate(kid)
        new_population.append(kid)

    return survivors + new_population

"""
creates a new ant based on random its parent genes
@param{List} A     parent entity data
@param{List} B     parent entity data
@return            returns new generated entity
"""
def mating(A, B):
    newEntity = []

    # randomly select gens from parents to use in the new identity
    for i in range(len(A)):
        r = random.randint(0, 1)
        gen = A[i] if r == 0 else B[i] 
        newEntity.append(gen)
    
    return newEntity

"""
performs a mutations to an entity
@param{List} entity     ant path data who is goint to mutate
@return                 ant with mutated genes
"""
def mutate(entity):
    global limits

    for i in range(len(entity)):
        p = random.random()
        if p <= MUTATION_PROBABILITY:
            mutation = randomizeGen(0, limits[i])
            entity[i] = mutation

    return entity

def main():
    # randomly generate an starting population
    population = [initializeEntity() for _ in range(POPULATION_SIZE)]

    # perform N iterations to find best subject
    for _ in range(GENERATIONS_LIMIT):
        newGeneration = descendency(population)
        population = newGeneration

    # print one of the best solutions found
    best = population[0]

    print('best solution:', best, ', gain:', fitness(best))
    

# the different type of primary resources you have
n_resources = 2
# arr of length n_resources, contains the available quantity for each resources
resources = [24, 6]


# the different things you can craft with those primary resources
n_crafts = 2
# arr of length n_crafts. each subarray is of length n_resources
# contains the amount of resources required to produce each craft
crafts = [
    [6, 1],
    [4, 2]
]
# arr of length n_crafts, contains the gain for producing each craft
crafts_gain = [5, 4]


# the total custom restrictions for your problem
n_restrictions = 2
# arr of length n_restrictions, each subarray of of len n_resources + 1
# contains specified restrictions for crafts
restrictions = [
    [0, 1, 2],
    [-1, 1, 1]
]

# find production limits
limits = findCraftLimits()

POPULATION_SIZE = 100
GENERATIONS_LIMIT = 10000
MUTATION_PROBABILITY = 0.1

# set working precision
PRECISION = "{:.1f}"

main()