import copy
execfile('simple_map.py')

def viterbi(states, piarr, trans_p, emit_p, obs):
  # Initialize T1 and T2, which keep track of everything done so far
  # T1 - probability of most likely path so far
  T1 = [{}]
  T2 = [{}]
  # length of sequence
  T = len(obs)
  # init T1 and T2 for each state
  for s in range(0, len(states)):
    st = states[s]
    if obs[0] in emit_p[st].keys():
      T1[0][s] = piarr[s]*emit_p[st][obs[0]]
    else:
      T1[0][s] = 0.0
  for t in range(1, T):
    T1.append({})
    T2.append({})
    for s in range(0, len(states)):
      st = states[s]
      # evaluate the probabilitiy of each possible state transition
      # on the basis of the transition probability and the current observation
      prob_each_step = [T1[(t-1)][y0]*trans_p[states[y0]][st]*emit_p[st][obs[t]] for y0 in range(0,len(states))]
      maxprob = max(prob_each_step)
      T1[t][s] = maxprob
      T2[t][s] = prob_each_step
  opt = []
  for j in T1:
    for x, y in j.items():
      if j[x] == max(j.values()):
        opt.append(x)
  # The highest probability
  h = max(T1[-1].values())
  return([opt,T1, T2])

def dptable(V):
    # Print a table of steps from dictionary
    yield " ".join(("%10d" % i) for i in range(len(V)))
    for y in V[0]:
        yield "%.7s: " % y+" ".join("%.7s" % ("%f" % v[y]) for v in V)

piarr = [0.0]*len(states)
piarr[0:2] = [0.05]*3
piarr[1] = 0.9
# grid = [[0,1],
#         [0,0]]
# last observation has to make sense for position
# obs = (2,3,1)
obs = (2,2,3,3,1)
vit = viterbi(states, piarr, trans_p, emit_p, obs)
path = vit[0]
print(path)

def dendro_dict(k):
  return {'name': str(k[0]), 'value': k[1], 'children': []}

def dendro_list(states):
  return [dendro_dict(k) for k in states]

trellis_for_vis = {'name': 't0', 'children': dendro_list(zip(states, vit[1][0].values()))}
# add first time period

# for s in range(len(states)):
#   moves = dendro_list(zip(states, vit[1][1].values()))
#   trellis_for_vis['children'][s]['children'] = moves
#   for s2 in range(len(states)):
#     moves = dendro_list(zip(states, vit[1][2].values()))
#     trellis_for_vis['children'][s]['children'][s2]['children'] = moves
# #
# import json
# with open('trellis.json', 'w') as outfile:
#     json.dump(trellis_for_vis, outfile, sort_keys = True, indent = 4, ensure_ascii=False)

grid_with_position = copy.deepcopy(grid)
for r in range(len(grid_with_position)):
  for c in range(len(grid_with_position[0])):
    if grid_with_position[r][c] == 0:
      grid_with_position[r][c] = ' '
    else:
      grid_with_position[r][c] = '|'

path_states = [states[step] for step in path]
import json
with open('path.json', 'w') as outfile:
    json.dump(path_states, outfile, sort_keys = True, indent = 4, ensure_ascii=False)

# for step in path:
#   state = states[step]
#   position_x = state[0]
#   position_y = state[1]
#   orientation = state[2]
#   grid_with_position[position_x][position_y] = delta_name[orientation]
#   for i in range(len(grid)):
#     print(grid_with_position[i])
#   grid_with_position[position_x][position_y] = ' '
#   print('\n')
#   time.sleep(1)
