import itertools
execfile('optimum_policy.py')
grid = [[0,0],
        [0,0]]

rows = range(len(grid))
cols = range(len(grid[0]))
# delta = orientation
states = list(itertools.product(rows,cols,range(len(delta))))
print(states)
init = states[0]
goal = states[-1]

# determine optimal path
opt = optimum_policy(grid, goal, cost)
for i in range(0,len(opt)):
  print(opt[i])

# for each state in the map, the transition to every adjacent state has some probability,
# if there is a wall, the probability is 0
# if there is not a wall AND the direction of current orientation is the same as the fastest ascent,
# We give this tranisition the highest probability
# If we are oriented in the OPPOSITE DIRECTION of the fastest ascent, we give that a 0 probability (we encountered some obstacle)

# generate the transition matrix
# for every state in states
trans_p = {}
for state in states:
  trans_p[state] = {}
  x = state[0]
  y = state[1]
  o = state[2]
  # value of the current state
  current_value = opt[x][y]
  # for every delta in deltas
  for d in range(len(delta)):
    x2 = x + delta[d][0]
    y2 = y + delta[d][1]
    if not x2 == -1 and not y2 == -1 and x2 < len(opt) and y2 < len(opt[1]):
      # check the gain of that transition
      gain = opt[x2][y2] - current_value
      # if gain is positive and in the same direction as orientation, give high probability
      if gain == 1 and delta[o] == delta[d]:
        trans_p[state][(x2,y2,d)] = 0.9
      elif gain > 90:
        trans_p[state][(x2,y2,d)] = 0.0
      # if looking in opposite direction
      elif gain == 1 and delta[o] == delta[d-2]:
        trans_p[state][(x2,y2,d)] = 0.0
      else:
        trans_p[state][(x2,y2,d)] = 0.2

print trans_p
      # if orientation is in direction of highest gain, weight that probablitiy very high
#   if orientation is in opposite direction of highest gain, weight that probability 0
#   weight other directions corresponding to gain of that move
#
