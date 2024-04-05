import math
import tkinter as tk

class ConvexHull:
    # list that stores all points coordinates
    points: list

    def __init__(self, points):
        self.points = points
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack()


    """
    transforms rectangular coordinates to polar coordinates
    @param {Pair} A     rectangular coordinates
    @return {Pair}      polar coordinates
    """
    def transformToPolarCoordinates(self, A):
        x, y = A
        r = math.sqrt(x**2 + y**2)
        theta = math.atan2(y, x)
        return (r, theta)


    """
    performs vectorial reduction operation
    @param {Pair} A     initial point
    @param {Pair} A     final point
    @return {Pair}      resultant vector
    """
    def vectorialReduction(self, A, B):
        Ax, Ay = A
        Bx, By = B
        x = Bx - Ax
        y = By - Ay
        return (x, y)
    

    """
    finds next border point
    @param {int} current      index to current point in self.points
    @param {double} theta     angle of current iteration
    @return {Pair}             index of next border point in self.points and last angle of calculus
    """
    def findNextPoint(self, current, theta):
        currentPoint = self.points[current]
        
        # look for the largest smaller angle than theta
        # store latest candidate polar coordinates value and index
        maxA = -9999
        minR = 9999
        nextIndex = None

        # iterate until a candidate point has been found
        while  nextIndex == None:
            for i in range(len(self.points)):
                # skip current iteration point
                if i == current: continue

                point = self.points[i]
                r, a = self.transformToPolarCoordinates(self.vectorialReduction(currentPoint, point))

                # new candidate point found
                if a <= theta and (a > maxA or a == maxA and r < minR):
                    maxA = a
                    minR = r
                    nextIndex = i
            
            # increase theta value to solve 3rd quartet gap problem
            theta += 2 * math.pi

        return nextIndex, maxA
    

    """
    run program and find convex area
    @return {list}     list with node connections indexes for convex area
    """
    def run(self):
        # find initial node and set starting values
        initialNode = self.findInitialNode()
        it = initialNode
        theta = math.pi/2
        answer = [it]

        # do while
        it, theta = self.findNextPoint(it, theta)
        while it != initialNode:
            answer.append(it)
            it, theta = self.findNextPoint(it, theta)

        answer.append(initialNode)
        return answer
    
    """
    finds the initial node for algorithm, the node that is at the left lower corner
    @return {int}     index of the initial node
    """
    def findInitialNode(self):
        minX = 9999
        minY = 9999
        index = None
        for i in range(len(self.points)):
            x, y = self.points[i]
            if x < minX or x == minX and y < minY:
                minX = x
                minY = y
                index = i

        return index

    """
    plot envolvent convex with Tkinter
    """
    #! this function is still not complete yet
    def graphPoints(self):
        pointIndexes = self.run()

        # plot envolvent convex
        for i in range(len(pointIndexes) - 1):
            A = self.points[pointIndexes[i]]*10
            B = self.points[pointIndexes[i+1]]*10

            # plot a line between A and B
            self.canvas.create_line(A[0], A[1], B[0], B[1], fill="blue")

        # plot points
        for point in self.points:
            self.canvas.create_oval(point[0]-30, point[1]-30, point[0]+30, point[1]+30, fill="red")

        self.root.mainloop()



# run code

# read and store points data
coords = input('insert points: ')
coords = coords.split(', ')
points = []
for coord in coords:
    x, y = coord.split(' ')
    x = int(x)
    y = int(y)
    points.append((x, y))

# initialize object
convex = ConvexHull(points)

# get convex indexes
pointIndexes = convex.run()
# print convex indexes
print('convex area node indexes:', pointIndexes)

# retreive and print point coordinates
pointCoordinates = []
for index in pointIndexes:
    pointCoordinates.append(convex.points[index])
print('convex area node coordinates:', pointCoordinates)

#convex.graphPoints()


""" ----------------------- sample inputs ----------------------- """

# sample input
"""
7 6, 8 4, 7 2, 3 2, 1 6, 1 8, 4 9
"""
# output (convex point indexes, the index depends in the order points were inserted)
"""
4 5 6 0 1 2 3 4
"""


# input
"""
3 8, 1 6, 6 2, 7 6, 5 5, 8 4, 6 8
"""
# output
"""
1 0 6 3 5 2 1
"""


# input
"""
1 2, 3 4, 5 6, 7 8
"""
# output
"""
0 1 2 3 2 1 0
"""