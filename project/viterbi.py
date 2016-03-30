# States correspond to positions of Xavier
# TODO: Add orientations?
# State space S
states = (1,2,3,4)
# e.g. directives motivated by current belief state
# ADD MOVE UP
# Observation space O
obs = ('move left', 'move down', 'stay put', 'stay put')
# given the origin is 1 and the goal is 4, prefer to move left (when oriented down)
# chosen somewhat arbitrarily
# Transition matrix A
trans = {
    1: {1: 0.1, 2: 0.8, 3: 0.0, 4: 0.1},
    2: {1: 0.1, 2: 0.1, 3: 0.8, 4: 0.0},
    3: {1: 0.0, 2: 0.1, 3: 0.8, 4: 0.0},
    4: {1: 0.1, 2: 0.0, 3: 0.8, 4: 0.1}
}
# Probability of getting directive
# ADD MOVE UP
# Emission matrix B
emiss = {
    1: {'move left': 0.7, 'move right': 0.1, 'move down': 0.1, 'stay put': 0.1},
    2: {'move left': 0.1, 'move right': 0.1, 'move down': 0.7, 'stay put': 0.1},
    3: {'move left': 0.1, 'move right': 0.1, 'move down': 0.1, 'stay put': 0.7},
    4: {'move left': 0.7, 'move right': 0.1, 'move down': 0.1, 'stay put': 0.1}
}
# An initial array of probabilities of size K - e.g. the possible number of states
# Here, say it's known as the first state
# DATA STRUCTURES KNOWLEDGE: Tuples have structure, lists have order
# http://stackoverflow.com/questions/626759/whats-the-difference-between-list-and-tuples
piarr = (0.9,0.05,0.05,0)


def viterbi(states, piarr, trans, emiss, obs):
  # Initialize T1 and T2, which keep track of everything done so far
  # T1 - probability of most likely path so far
  T1 = [{}]
  # length of sequence
  T = len(obs)
  # init T1 and T2 for each state
  for s in range(0, len(states)):
    st = states[s]
    # s is 1-4, so subtract 1 for indexing into piarr
    T1[0][s] = piarr[s]*emiss[st][obs[0]]
  for t in range(1, T):
    T1.append({})
    for s in range(0, len(states)):
      st = states[s]
      # evaluate the probabilitiy of each possible state transition
      # on the basis of the transition probability and the current observation
      prob_each_step = [T1[(t-1)][y0]*trans[states[y0]][st]*emiss[st][obs[t]] for y0 in range(0,len(states))]
      maxprob = max(prob_each_step)
      argmaxk = prob_each_step.index(maxprob)
      T1[t][s] = maxprob
  for i in dptable(T1):
      print i
  # terminal state
  opt = []
  for j in T1:
    for x, y in j.items():
      if j[x] == max(j.values()):
        opt.append(x)
  # The highest probability
  h = max(T1[-1].values())
  return(opt)

def dptable(V):
    # Print a table of steps from dictionary
    yield " ".join(("%10d" % i) for i in range(len(V)))
    for y in V[0]:
        yield "%.7s: " % y+" ".join("%.7s" % ("%f" % v[y]) for v in V)

print(viterbi(states, piarr, trans, emiss, obs))

