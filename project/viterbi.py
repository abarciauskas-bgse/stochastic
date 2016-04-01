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
piarr[3] = 0.9
obs = (2,3,2,3,3,0,0,1,3)
vit = viterbi(states, piarr, trans_p, emit_p, obs)
path = vit[0]
path_states = [states[step] for step in path]
print(path_states)

import json
with open('path.json', 'w') as outfile:
    json.dump(path_states, outfile, sort_keys = True, indent = 4, ensure_ascii=False)

