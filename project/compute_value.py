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

# get the relative positions of the node
# and append to a list of neighbors if not outside the grid
#
def all_neighbors(node, grid):
    up = relative_location(node, delta[0])
    left = relative_location(node, delta[1])
    down = relative_location(node, delta[2])
    right = relative_location(node, delta[3])
    neighbors = []
    for i in [up,left,down,right]:
        if not -1 in i and not i[0] == len(grid) and not i[1] == len(grid[0]): neighbors.insert(0, i)
    return neighbors

def conditional_update(value_dict, n, current_value):
    if value_dict[n[0]][n[1]] > current_value:
        value_dict = update_dict(value_dict, n, (current_value+1))
    return value_dict

def compute_value(grid,goal,cost):
    current_node = goal
    # set value in value dict e.g. {3:{3:0}}
    # first level of dict are rows, second level columns
    value_dict = {current_node[0]: {current_node[1]: 0}}
    current_value = 1
    # next is up and left
    next_to_visit = all_neighbors(goal, grid)
    # update value dict
    visited = [current_node]
    for n in next_to_visit:
      if grid[n[0]][n[1]] == 0:
        value_dict = update_dict(value_dict, n, current_value)
      else:
        value_dict = update_dict(value_dict, n, 99)
    while len(next_to_visit) > 0:
        # next node to visit
        current_node = next_to_visit.pop(0)
        current_value = value_dict[current_node[0]][current_node[1]]
        # adds current node to end of visited
        visited.append(current_node)
        neighbors = all_neighbors(current_node, grid)
        # for each neighbor, update the value to the current step value plus one
        # unless it's already less than or equal to the current step value (i.e. closer to home)
        for n in neighbors:
            obstacle = grid[n[0]][n[1]] == 1
            if n not in visited:
                # only update if it's not an obstacle
                if not obstacle:
                  if n[0] in value_dict.keys() and n[1] in value_dict[n[0]].keys():
                      value_dict = conditional_update(value_dict, n, current_value)
                  else:
                      value_dict = update_dict(value_dict, n, current_value+1)
                  if not n == (0,0): next_to_visit.insert(0, n)
                else:
                    value_dict = update_dict(value_dict, n, 99)
            elif value_dict[n[0]][n[1]] > current_value:
                value_dict = conditional_update(value_dict, n, current_value)
                next_to_visit.insert(0, n)
    return value_dict # to bo value grid someday


res = compute_value(grid, goal, cost)
print(res)
