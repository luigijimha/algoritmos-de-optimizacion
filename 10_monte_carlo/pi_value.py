from random import uniform

"""
generates random coords inside square
@return     tuple with (x, y) coodinates
"""
def randomizeCoords():
    x = uniform(-RADIUS, RADIUS)
    y = uniform(-RADIUS, RADIUS)
    return (x, y)
    
"""
determines if coordinates are within the circle
@param {Tuple} coords     coordinates to evaluate
@return                   returns 1 if coords are inside circle, else 0
"""
def targetHit(coords):
    x, y = coords
    return 1 if x**2 + y**2 <= RADIUS**2 else 0

def main():
    success = 0
    for _ in range(N):
        coords = randomizeCoords()
        success += targetHit(coords)

    print('Pi value', 4 * success/N)

RADIUS = 5
N = 1_000_000

main()