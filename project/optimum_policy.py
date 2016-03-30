# ----------
# User Instructions:
# 
# Write a function optimum_policy that returns
# a grid which shows the optimum policy for robot
# motion. This means there should be an optimum
# direction associated with each navigable cell from
# which the goal can be reached.
# 
# Unnavigable cells as well as cells from which 
# the goal cannot be reached should have a string 
# containing a single space (' '), as shown in the 
# previous video. The goal cell should have '*'.
# ----------

# grid = [[0, 1, 0, 0, 0, 0],
#         [0, 1, 1, 0, 1, 0],
#         [0, 0, 0, 0, 1, 0],
#         [0, 1, 1, 1, 1, 0],
#         [0, 1, 0, 1, 1, 0]]
grid = [[1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1]]
init = [4, 3]
goal = [2,0]
init = [0,0]
#goal = [len(grid)-1, len(grid[0])-1]
cost = 1 # the cost associated with moving from a cell to an adjacent one

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']


def relative_location(position, delta):
  return tuple([x + y for x, y in zip(position, delta)])

# look at all the neighbors and return the direction of fastest descent
def min_neighbor(node, value):
    firstdir = relative_location(node, delta[0])
    if node[0] == 0: firstdir = relative_location(node, delta[1])
    minv = value[firstdir[0]][firstdir[1]]
    mindir = 0
    for i in range(1,4):
        rel_loc = relative_location(node, delta[i])
        if -1 not in rel_loc and rel_loc[0] < len(value) and rel_loc[1] < len(value[0]):
            newv = value[rel_loc[0]][rel_loc[1]]
            if newv < minv:
                minv = newv
                mindir = i
    return mindir


def optimum_policy(grid,goal,cost):
    # ----------------------------------------
    # modify code below
    # ----------------------------------------
    value = [[99 for row in range(len(grid[0]))] for col in range(len(grid))]
    change = True

    while change:
        change = False

        for x in range(len(grid)):
            for y in range(len(grid[0])):
                if goal[0] == x and goal[1] == y:
                    if value[x][y] > 0:
                        value[x][y] = 0

                        change = True

                elif grid[x][y] == 0:
                    for a in range(len(delta)):
                        x2 = x + delta[a][0]
                        y2 = y + delta[a][1]

                        if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]) and grid[x2][y2] == 0:
                            v2 = value[x2][y2] + cost

                            if v2 < value[x][y]:
                                change = True
                                value[x][y] = v2

    # for each position in the value matrix,
    # move in the direction of nearest return
    # find the least neighbor and putted to that
    policy = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]
    for x in range(len(value)):
        for y in range(len(value[0])):
            # if not an obstacle
            if not value[x][y] == 99 and not [x,y] == goal and not [x,y] == [0,0]:
                mindirection = min_neighbor([x,y], value)
                policy[x][y] = delta_name[mindirection]
    #return value
    return policy


pol = optimum_policy(grid, goal, cost)
for i in range(0, len(pol)):
    print(pol[i])

