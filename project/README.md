## The Viterbi Algorithm for HMMs and POMDPs (Partially Observable Markov Decision Processes)

Here lies the meat and potatoes of a stochastic modelling project exploring how the viterbi algorithm may be used to solve HMMs and POMDPs for autonomous robot navigation.

#### Simulating autonomous robot navigation

The process of simulation is as follows:

1. Encode an "office map"

```python
# see `simple_map.py`
# HERE IS THE MAP
grid = [[0,1,0,0],
        [0,0,1,0],
        [0,0,0,0],
        [0,0,1,0]]
```

2. Declare a start and goal locations and determine the optimal path for the robot to travel from an arbitrary location

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

3. Determine the transition and emission probabilities
