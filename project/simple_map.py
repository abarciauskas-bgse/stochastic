import itertools
import time 
execfile('optimum_policy.py')

grid = [[0,0,1],
        [1,0,0],
        [1,0,0]]

rows = range(len(grid))
cols = range(len(grid[0]))
# delta = orientation
states = list(itertools.product(rows,cols,range(len(delta))))
init = states[0][0:2]
goal = states[-1][0:2]
print(goal)
# determine optimal path
opt = optimum_policy(grid, init, cost)

# for each state in the map, the transition to every adjacent state has some probability,
# if there is a wall, the probability is 0
# if there is not a wall AND the direction of current orientation is the same as the fastest ascent,
# We give this tranisition the highest probability
# If we are oriented in the OPPOSITE DIRECTION of the fastest ascent, we give that a 0 probability (we encountered some obstacle)

# generate the transition matrix
# for every state in states
trans_p = {}
emit_p = {}
for state in states:
  trans_p[state] = {}
  emit_p[state] = {}
  x = state[0]
  y = state[1]
  o = state[2]
  # value of the current state
  current_value = opt[x][y]
  # for every delta in deltas
  for d in range(len(delta)):
    # should only check this possibility if we can move there
    x2 = x + delta[d][0]
    y2 = y + delta[d][1]
    if not x2 == -1 and not y2 == -1 and x2 < len(opt) and y2 < len(opt[1]):
      # check the gain of that transition
      gain = opt[x2][y2] - current_value
      # if gain is positive and in the same direction as current orientation, give high probability
      if gain == 1 and delta[o] == delta[d]:
        trans_p[state][(x2,y2,d)] = 0.8
        emit_p[state][d] = 0.8
      elif gain > 90:
        trans_p[state][(x2,y2,d)] = 0.0
        emit_p[state][d] = 0.0
      # if looking in opposite direction
      elif gain == 1 and delta[o] == delta[d-2]:
        trans_p[state][(x2,y2,d)] = 0.2
        emit_p[state][d] = 0.2
      elif (x2,y2) == goal:
        trans_p[state][(x2,y2,d)] = 0.8
        emit_p[state][d] = 0.8
      else:
        trans_p[state][(x2,y2,d)] = 0.2
        emit_p[state][d] = 0.2
  # but we need to have something for everybody
  # what states are we missing?
  missing_state_transitions = set(states).difference(set(trans_p[state].keys()))
  for missing_state in missing_state_transitions:
    trans_p[state][missing_state] = 0.0
  missing_deltas = set(range(len(delta))).difference(emit_p[state].keys())
  for missing_delta in missing_deltas:
    emit_p[state][missing_delta] = 0.0
