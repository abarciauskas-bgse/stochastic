import copy
import itertools
import time
import json
import pprint
execfile('optimum_policy.py')

# HERE IS THE MAP
grid = [[0,1,0,0],
        [0,0,1,0],
        [0,0,0,0],
        [0,0,1,0]]

# WHERE DO WE WANT XAVIER TO GO?
rows = range(len(grid))
cols = range(len(grid[0]))
states = list(itertools.product(rows,cols,range(len(delta))))
init = states[0][0:2]
goal = (0,2)


# GIVE THE ROBOT A SET OF INSTRUCTIONS
opt = optimum_policy(grid, goal, cost)
# NOW WE TELL XAVIER TO GO TOWARDS THE GOAL UNLESS SOMETHING COMES IN HIS PATH

# for json
map_arr = []
for r in range(len(grid)):
  for c in range(len(grid[0])):
      map_arr.append([r,c,opt[r][c]])

# MAKE SURE YOU ARE IN THE RIGHT DIRECTORY
with open('site/public/js/map.json', 'w') as outfile:
    json.dump(map_arr, outfile, sort_keys = True, indent = 4, ensure_ascii=False)

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
  # tally up non-normalized probabilities
  total_probs = 0
  # for every delta in deltas
  for d in range(len(delta)):
    # should only check this possibility if we can move there
    x2 = x + delta[d][0]
    y2 = y + delta[d][1]
    if not x2 == -1 and not y2 == -1 and x2 < len(opt) and y2 < len(opt[1]):
      # check the gain of that transition
      gain = opt[x2][y2] - current_value
      # if gain is negative, we are going in the right direction
      if gain == -1:
        trans_p[state][(x2,y2,d)] = 0.8
        emit_p[state][d] = 0.8
        total_probs = total_probs + 0.8
      elif gain > 90:
        trans_p[state][(x2,y2,d)] = 0.1
        # small probability we get the wrong idea
        emit_p[state][d] = 0.1
        total_probs = total_probs + 0.1
      else:
        trans_p[state][(x2,y2,d)] = 0.2
        emit_p[state][d] = 0.2
        total_probs = total_probs + 0.2
  # normalize
  for d in range(len(delta)):
    x2 = x + delta[d][0]
    y2 = y + delta[d][1]
    if not x2 == -1 and not y2 == -1 and x2 < len(opt) and y2 < len(opt[1]):
      trans_p[state][(x2,y2,d)] = round(trans_p[state][(x2,y2,d)]/total_probs,3)
      emit_p[state][d] = round(emit_p[state][d]/total_probs,3)
  # but we need to have something for everybody
  # what states are we missing?
  missing_state_transitions = set(states).difference(set(trans_p[state].keys()))
  for missing_state in missing_state_transitions:
    trans_p[state][missing_state] = 0.0
  missing_deltas = set(range(len(delta))).difference(emit_p[state].keys())
  for missing_delta in missing_deltas:
    emit_p[state][missing_delta] = 0.0

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(emit_p)

trans_p_json = {}
for k,v in trans_p.iteritems():
  val = {str(k1): v1 for k1, v1 in trans_p[k].iteritems()}
  trans_p_json[str(k)] = val

with open('site/public/js/transitions_matrix.json', 'w') as outfile:
    json.dump(trans_p_json, outfile, sort_keys = True, indent = 4, ensure_ascii=False)
