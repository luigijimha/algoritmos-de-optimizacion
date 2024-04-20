from random import uniform

"""
generates random coords inside cube
@return     tuple with (x, y) coodinates
"""
def randomizeCoords():
    x = uniform(-RADIUS, RADIUS)
    y = uniform(-RADIUS, RADIUS)
    z = uniform(-RADIUS, RADIUS)
    return (x, y, z)
    
"""
determines if coordinates are within the sphere
@param {Tuple} coords     coordinates to evaluate
@return                   returns 1 if coords are inside the sphere, else 0
"""
def targetHit(coords):
    x, y, z = coords
    return 1 if x**2 + y**2 + z**2 <= RADIUS**2 else 0

def main():
    success = 0
    for _ in range(N):
        coords = randomizeCoords()
        success += targetHit(coords)

    print('sphere area:', success/N * 24 * RADIUS**2)
    print('sphere volume:', success/N * 8 * RADIUS**3)

RADIUS = 7.5
N = 1_000_000

main()