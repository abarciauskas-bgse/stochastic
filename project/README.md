## The Viterbi Algorithm for HMMs and POMDPs (Partially Observable Markov Decision Processes)

Here lies the meat and potatoes of a stochastic modelling project exploring how the viterbi algorithm may be used to solve HMMs and POMDPs for autonomous robot navigation.

#### Simulating autonomous robot navigation

The process of simulation is as follows:

**1. Encode an "office map"**

```python
# see `simple_map.py`
# HERE IS THE MAP
grid = [[0,1,0,0],
        [0,0,1,0],
        [0,0,0,0],
        [0,0,1,0]]
```

**2. Declare a start and goal locations and determine the optimal path for the robot to travel from an arbitrary location**

```python
rows = range(len(grid))
cols = range(len(grid[0]))
states = list(itertools.product(rows,cols,range(len(delta))))
init = states[0][0:2]
goal = (0,2)

# see `optimum_policy.py`
opt = optimum_policy(grid, goal, cost)
for i in range(len(opt)):
    print(opt[i])
```

**3. Determine the transition and emission probabilities**

Code omitted, see [`simple_map.py`](simple_map.py).

The state space is not too big itself, it is the set of possible positions and orientations, i.e. `rows x cols x 4`. So for our simple 4 x 4 example, there are **64 possible states**.

But for the transitions matrix, we consider every possible state transition, so this is a pretty big space! It has dimension `(rows x cols x 4)^2` = **4096**

```python
# Did you think I was lying?
len(trans_p.values())*len(trans_p[(0, 0, 0)].values())
# 4096
```

```python
pp.pprint(trans_p)
{   (0, 0, 0): {   (0, 0, 0): 0.0,
                   (0, 0, 1): 0.0,
                   (0, 0, 2): 0.0,
                   (0, 0, 3): 0.0,
                   (0, 1, 0): 0.0,
                   (0, 1, 1): 0.0,
                   (0, 1, 2): 0.0,
                   (0, 1, 3): 0.1,
                   (0, 2, 0): 0.0,
                   (0, 2, 1): 0.0,
                   (0, 2, 2): 0.0,
                   (0, 2, 3): 0.0,
                   (0, 3, 0): 0.0,
                   (0, 3, 1): 0.0,
                   (0, 3, 2): 0.0,
                   (0, 3, 3): 0.0,
                   (1, 0, 0): 0.0,
                   (1, 0, 1): 0.0,
                   (1, 0, 2): 0.8,
                   (1, 0, 3): 0.0,
                   (1, 1, 0): 0.0,
                   (1, 1, 1): 0.0,
                   (1, 1, 2): 0.0,
                   (1, 1, 3): 0.0,
                   (1, 2, 0): 0.0,
                   (1, 2, 1): 0.0,
                   (1, 2, 2): 0.0,
                   (1, 2, 3): 0.0,
                   (1, 3, 0): 0.0,
                   (1, 3, 1): 0.0,
                   (1, 3, 2): 0.0,
                   (1, 3, 3): 0.0,
                   (2, 0, 0): 0.0,
                   (2, 0, 1): 0.0,
                   (2, 0, 2): 0.0,
                   (2, 0, 3): 0.0,
                   (2, 1, 0): 0.0,
                   (2, 1, 1): 0.0,
                   (2, 1, 2): 0.0,
                   (2, 1, 3): 0.0,
                   (2, 2, 0): 0.0,
                   (2, 2, 1): 0.0,
                   (2, 2, 2): 0.0,
                   (2, 2, 3): 0.0,
                   (2, 3, 0): 0.0,
                   (2, 3, 1): 0.0,
                   (2, 3, 2): 0.0,
                   (2, 3, 3): 0.0,
                   (3, 0, 0): 0.0,
                   (3, 0, 1): 0.0,
                   (3, 0, 2): 0.0,
                   (3, 0, 3): 0.0,
                   (3, 1, 0): 0.0,
                   (3, 1, 1): 0.0,
                   (3, 1, 2): 0.0,
                   (3, 1, 3): 0.0,
                   (3, 2, 0): 0.0,
                   (3, 2, 1): 0.0,
                   (3, 2, 2): 0.0,
                   (3, 2, 3): 0.0,
                   (3, 3, 0): 0.0,
                   (3, 3, 1): 0.0,
                   (3, 3, 2): 0.0,
                   (3, 3, 3): 0.0},
    (0, 0, 1): {   (0, 0, 0): 0.0,
                   ,,, },
    (3, 3, 3): {   (0, 0, 0): 0.0,
                   ... }}
```

For the emissions space, things are less expansive. The set of possible emissions is the state space times the observation space, which in our case is the set of every possible move in 4 directions. 

```python
len(emit_p.values())*len(emit_p[(0,0,0)].values())
# 256
```

You probably didn't ask me to, but I'm going to print the whole thing because I can.

```python
{   (0, 0, 0): {   0: 0.0, 1: 0.0, 2: 0.8, 3: 0.1},
    (0, 0, 1): {   0: 0.0, 1: 0.0, 2: 0.8, 3: 0.1},
    (0, 0, 2): {   0: 0.0, 1: 0.0, 2: 0.8, 3: 0.1},
    (0, 0, 3): {   0: 0.0, 1: 0.0, 2: 0.8, 3: 0.1},
    (0, 1, 0): {   0: 0.0, 1: 0.2, 2: 0.2, 3: 0.2},
    (0, 1, 1): {   0: 0.0, 1: 0.2, 2: 0.2, 3: 0.2},
    (0, 1, 2): {   0: 0.0, 1: 0.2, 2: 0.2, 3: 0.2},
    (0, 1, 3): {   0: 0.0, 1: 0.2, 2: 0.2, 3: 0.2},
    (0, 2, 0): {   0: 0.0, 1: 0.1, 2: 0.1, 3: 0.2},
    (0, 2, 1): {   0: 0.0, 1: 0.1, 2: 0.1, 3: 0.2},
    (0, 2, 2): {   0: 0.0, 1: 0.1, 2: 0.1, 3: 0.2},
    (0, 2, 3): {   0: 0.0, 1: 0.1, 2: 0.1, 3: 0.2},
    (0, 3, 0): {   0: 0.0, 1: 0.8, 2: 0.2, 3: 0.0},
    (0, 3, 1): {   0: 0.0, 1: 0.8, 2: 0.2, 3: 0.0},
    (0, 3, 2): {   0: 0.0, 1: 0.8, 2: 0.2, 3: 0.0},
    (0, 3, 3): {   0: 0.0, 1: 0.8, 2: 0.2, 3: 0.0},
    (1, 0, 0): {   0: 0.2, 1: 0.0, 2: 0.8, 3: 0.8},
    (1, 0, 1): {   0: 0.2, 1: 0.0, 2: 0.8, 3: 0.8},
    (1, 0, 2): {   0: 0.2, 1: 0.0, 2: 0.8, 3: 0.8},
    (1, 0, 3): {   0: 0.2, 1: 0.0, 2: 0.8, 3: 0.8},
    (1, 1, 0): {   0: 0.1, 1: 0.2, 2: 0.8, 3: 0.1},
    (1, 1, 1): {   0: 0.1, 1: 0.2, 2: 0.8, 3: 0.1},
    (1, 1, 2): {   0: 0.1, 1: 0.2, 2: 0.8, 3: 0.1},
    (1, 1, 3): {   0: 0.1, 1: 0.2, 2: 0.8, 3: 0.1},
    (1, 2, 0): {   0: 0.2, 1: 0.2, 2: 0.2, 3: 0.2},
    (1, 2, 1): {   0: 0.2, 1: 0.2, 2: 0.2, 3: 0.2},
    (1, 2, 2): {   0: 0.2, 1: 0.2, 2: 0.2, 3: 0.2},
    (1, 2, 3): {   0: 0.2, 1: 0.2, 2: 0.2, 3: 0.2},
    (1, 3, 0): {   0: 0.8, 1: 0.1, 2: 0.2, 3: 0.0},
    (1, 3, 1): {   0: 0.8, 1: 0.1, 2: 0.2, 3: 0.0},
    (1, 3, 2): {   0: 0.8, 1: 0.1, 2: 0.2, 3: 0.0},
    (1, 3, 3): {   0: 0.8, 1: 0.1, 2: 0.2, 3: 0.0},
    (2, 0, 0): {   0: 0.2, 1: 0.0, 2: 0.2, 3: 0.8},
    (2, 0, 1): {   0: 0.2, 1: 0.0, 2: 0.2, 3: 0.8},
    (2, 0, 2): {   0: 0.2, 1: 0.0, 2: 0.2, 3: 0.8},
    (2, 0, 3): {   0: 0.2, 1: 0.0, 2: 0.2, 3: 0.8},
    (2, 1, 0): {   0: 0.2, 1: 0.2, 2: 0.2, 3: 0.8},
    (2, 1, 1): {   0: 0.2, 1: 0.2, 2: 0.2, 3: 0.8},
    (2, 1, 2): {   0: 0.2, 1: 0.2, 2: 0.2, 3: 0.8},
    (2, 1, 3): {   0: 0.2, 1: 0.2, 2: 0.2, 3: 0.8},
    (2, 2, 0): {   0: 0.1, 1: 0.2, 2: 0.1, 3: 0.8},
    (2, 2, 1): {   0: 0.1, 1: 0.2, 2: 0.1, 3: 0.8},
    (2, 2, 2): {   0: 0.1, 1: 0.2, 2: 0.1, 3: 0.8},
    (2, 2, 3): {   0: 0.1, 1: 0.2, 2: 0.1, 3: 0.8},
    (2, 3, 0): {   0: 0.8, 1: 0.2, 2: 0.2, 3: 0.0},
    (2, 3, 1): {   0: 0.8, 1: 0.2, 2: 0.2, 3: 0.0},
    (2, 3, 2): {   0: 0.8, 1: 0.2, 2: 0.2, 3: 0.0},
    (2, 3, 3): {   0: 0.8, 1: 0.2, 2: 0.2, 3: 0.0},
    (3, 0, 0): {   0: 0.8, 1: 0.0, 2: 0.0, 3: 0.8},
    (3, 0, 1): {   0: 0.8, 1: 0.0, 2: 0.0, 3: 0.8},
    (3, 0, 2): {   0: 0.8, 1: 0.0, 2: 0.0, 3: 0.8},
    (3, 0, 3): {   0: 0.8, 1: 0.0, 2: 0.0, 3: 0.8},
    (3, 1, 0): {   0: 0.8, 1: 0.2, 2: 0.0, 3: 0.1},
    (3, 1, 1): {   0: 0.8, 1: 0.2, 2: 0.0, 3: 0.1},
    (3, 1, 2): {   0: 0.8, 1: 0.2, 2: 0.0, 3: 0.1},
    (3, 1, 3): {   0: 0.8, 1: 0.2, 2: 0.0, 3: 0.1},
    (3, 2, 0): {   0: 0.2, 1: 0.2, 2: 0.0, 3: 0.2},
    (3, 2, 1): {   0: 0.2, 1: 0.2, 2: 0.0, 3: 0.2},
    (3, 2, 2): {   0: 0.2, 1: 0.2, 2: 0.0, 3: 0.2},
    (3, 2, 3): {   0: 0.2, 1: 0.2, 2: 0.0, 3: 0.2},
    (3, 3, 0): {   0: 0.8, 1: 0.1, 2: 0.0, 3: 0.0},
    (3, 3, 1): {   0: 0.8, 1: 0.1, 2: 0.0, 3: 0.0},
    (3, 3, 2): {   0: 0.8, 1: 0.1, 2: 0.0, 3: 0.0},
    (3, 3, 3): {   0: 0.8, 1: 0.1, 2: 0.0, 3: 0.0}}
```

**4. Once we get a set of observations, we use viterbie to solve for the most likely path:**

```python
def viterbi(states, piarr, trans_p, emit_p, obs):
  # Initialize T1, which keep track of everything done so far
  # T1 - probability of most likely path so far
  T1 = [{}]
  T2 = [{}]
  # length of sequence
  T = len(obs)
  # init T1 for each state
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

# Prior probability of state space
piarr = [0.0]*len(states)
piarr[0:2] = [0.05]*3
piarr[3] = 0.9
# observations: down, right, down, right, right, etc.
obs = (2,3,2,3,3,0,0,1,3)
vit = viterbi(states, piarr, trans_p, emit_p, obs)
path = vit[0]
path_states = [states[step] for step in path]
print(path_states)
```


