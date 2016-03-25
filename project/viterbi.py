# States correspond to positions of Xavier
# TODO: Add orientations?
# State space S
states = (1,2,3,4)
# e.g. directives motivated by current belief state
# ADD MOVE UP
# Observation space O
obs = ('move left', 'move right', 'move down', 'move left', 'stay put')
start_probability = {1: 1, 2: 0, 3: 0, 4: 0}
# given the origin is 1 and the goal is 4, prefer to move left (when oriented down)
# chosen somewhat arbitrarily
# Transition matrix A
trans = {
    1: {1: 0.1, 2: 0.8, 3: 0.1, 4: 0.0},
    2: {1: 0.1, 2: 0.1, 3: 0.0, 4: 0.8},
    3: {1: 0.1, 2: 0.0, 3: 0.1, 4: 0.8},
    4: {1: 0.0, 2: 0.1, 3: 0.1, 4: 0.8}
}
# Probability of getting directive
# ADD MOVE UP
# Emission matrix B
emiss = {
    1: {'move left': 0.7, 'move right': 0.1, 'move down': 0.1, 'stay put': 0.1},
    2: {'move left': 0.1, 'move right': 0.1, 'move down': 0.7, 'stay put': 0.1},
    3: {'move left': 0.7, 'move right': 0.1, 'move down': 0.1, 'stay put': 0.1},
    4: {'move left': 0.1, 'move right': 0.1, 'move down': 0.1, 'stay put': 0.7}
}
# An initial array of probabilities of size K - e.g. the possible number of states
# Here, say it's known as the first state
# DATA STRUCTURES KNOWLEDGE: Tuples have structure, lists have order
# http://stackoverflow.com/questions/626759/whats-the-difference-between-list-and-tuples
piarr = (0.9,0.05,0.05,0)


def viterbi(states, piarr, trans, emiss, obs):
  # Initialize T1 and T2, which keep track of everything done so far
  # T1 - probability of most likely path so far
  T1 = dict(zip(states, [[]]*4))
  # T2 - which state was most likely one step prior
  T2 = dict(zip(states, [[]]*4))
  # length of sequence
  T = len(obs)
  # init T1 and T2 for each state
  for s in states:
    # s is 1-4, so subtract 1 for indexing into piarr
    T1[s] = [piarr[s-1]*emiss[s][obs[0]]]
    T2[s] = [0]
  for i in range(2, T+1):
    for sidx in range(0, len(states)):
      s = states[sidx]
      # max probability last state
      # i - 2 because we are looking for i - 1 with - 1 for python indexing from 0
      prob_each_step = [T1[k][i-2]*trans[s][k]*emiss[s][obs[i-1]] for k in T1.keys()]
      maxprob = max(prob_each_step)
      argmaxk = prob_each_step.index(maxprob)
      T1[s].insert(i-1, maxprob)
      T2[s].insert(i-1, argmaxk)
  # terminal state
  probs = [T1[k][T-1] for k in T1.keys()]
  maxprob = max(probs)
  # initialize the most likely sequence of our POMDP
  Z = [0]*T
  X = [0]*T
  # terminal
  Z[T-1] = probs.index(maxprob)
  X[T-1] = states[Z[T-1]]
  for i in range(1,T)[::-1]:
    Z[i-1] = T2[Z[i]+1][i]
    X[i-1] = states[Z[i-1]]

