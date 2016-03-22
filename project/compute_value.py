import time

grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0]]
goal = (len(grid)-1, len(grid[0])-1)
cost = 1 # the cost associated with moving from a cell to an adjacent one

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

def relative_location(position, delta):
  return tuple([x + y for x, y in zip(position, delta)])

def update_dict(dicto, node, value):
    row = node[0]
    col = node[1]
    if row in dicto.keys():
        dicto[row][col] = value
    else:
        dicto[row] = {col: value}
    return dicto

def compute_value(grid,goal,cost):
    current_node = goal
    # set value in value dict e.g. {3:{3:0}}
    # first level of dict are rows, second level columns
    value_dict = {current_node[0]: {current_node[1]: 0}}
    current_value = 1
    # next is up and left
    up = relative_location(goal, delta[0])
    left = relative_location(goal, delta[1])
    next_to_visit = [up, left]
    # update value dict
    visited = [current_node]
    value_dict = update_dict(value_dict, up, current_value)
    value_dict = update_dict(value_dict, left, current_value)
    while len(next_to_visit) > 0:
        # next node to visit
        current_node = next_to_visit.pop(0)
        current_value = value_dict[current_node[0]][current_node[1]]
        # adds current node to end of visited
        visited.append(current_node)
        up = relative_location(current_node, delta[0])
        left = relative_location(current_node, delta[1])
        neighbors = []
        for i in [up,left]:
            if not -1 in i: neighbors.insert(0, i)
        for n in neighbors:
            if n not in visited:
                # ADD ME: CHECK IF EMPTY IN GRID OR OBSTACLE
                value_dict = update_dict(value_dict, n, current_value+1)
                next_to_visit.insert(0, n)
            elif value_dict[n[0]][n[1]] > (current_value+1):
                value_dict = update_dict(value_dict, n, (current_value+1))
    return value_dict # to bo value grid someday


res = compute_value(grid, goal, cost)
print(res)
