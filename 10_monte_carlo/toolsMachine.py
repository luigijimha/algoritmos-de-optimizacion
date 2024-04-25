from random import random

"""
randomly determines the time it will take for a tool to break
@param {List} times     list with different time endurances
@return                 time taken for a tool to break
"""
def randomizeBreak(times):
    r = random()
    # both problem arrays have the same probabilities for different time groups,
    # that's why I'm using static values here
    index = 0 if r < 0.05 else 1 if r < 0.2 else 2 if r < 0.35 else 3 if r < 0.55 else 4 if r < 0.75 else 5 if r < 0.9 else 6
    return times[index]

def main():
    # counts how many hours have passed in the simulation
    t = 0
    # counts cost produced by single tool replacement
    singleChangeCost = 0
    # counts cost produced by full tool replacement
    fullChangeCost = 0

    # first perform simulation for single tool replacement
    # randomly initialize endurance time values for machine
    toolRemainingHours = [randomizeBreak(SINGLE_CHANGE_INTERVALS) for _ in range(FULL_CHANGE_TOOLS)]

    while True:
        # get breaking time for next tool
        minTime = min(toolRemainingHours)

        # end loop if next tool breaks after simulation time ended
        if t + minTime >= SIMULATION_TIME:
            break

        for i in range(FULL_CHANGE_TOOLS):
            # update break times for tools
            toolRemainingHours[i] -= minTime
            # change tools who broke
            if toolRemainingHours[i] == 0:
                # calculate new break time for tool
                toolRemainingHours[i] = randomizeBreak(SINGLE_CHANGE_INTERVALS)
                # update cost for changing tool
                singleChangeCost += TOOL_CHANGE_COST

        # increase timer by time passed
        t += minTime + SINGLE_CHANGE_TIME
        # increase cost by machine inactivity
        singleChangeCost += SINGLE_CHANGE_TIME * HOUR_COST

    # perform simulation for full tool replacement
    t = 0
    while True:
        # simulate new tools remaining life time
        toolRemainingHours = [randomizeBreak(SINGLE_CHANGE_INTERVALS) for _ in range(FULL_CHANGE_TOOLS)]
        # get next tool break time
        minTime = min(toolRemainingHours)

        # end loop if next tool breaks after simulation time ended
        if t + minTime >= SIMULATION_TIME:
            break

        # increase timer by time passed
        t += minTime + FULL_CHANGE_TIME
        # increase cost by machine inactivity
        fullChangeCost += FULL_CHANGE_TIME * HOUR_COST + TOOL_CHANGE_COST * FULL_CHANGE_TOOLS

    print('single change cost:', singleChangeCost)
    print('full change cost', fullChangeCost)

# arrays with endurance time probability for tools
# probability in this problem is static,
# it is code embed in randomizeBreak function
SINGLE_CHANGE_INTERVALS = [20, 30, 40, 50, 60, 70, 80]
FULL_CHANGE_INTERVALS = [30, 40, 50, 60, 70, 80, 90]

# hours needed to perform single and full replacements in machine
SINGLE_CHANGE_TIME = 1
FULL_CHANGE_TIME = 2

# cost for stopping machine for 1 hour
HOUR_COST = 100
# cost for buying a new tool
TOOL_CHANGE_COST = 10
# total tools machinery has
FULL_CHANGE_TOOLS = 6

# simulation time in hours
SIMULATION_TIME = 24*7*365

main()