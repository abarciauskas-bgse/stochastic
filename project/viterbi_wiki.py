def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    for i in states:
        V[0][i] = start_p[i]*emit_p[i][obs[0]]
    # Run Viterbi when t > 0
    for t in range(1, len(obs)):
        V.append({})
        for y in states:
            prob = max(V[t - 1][y0]*trans_p[y0][y]*emit_p[y][obs[t]] for y0 in states)
            V[t][y] = prob
    for i in dptable(V):
        print i
    opt = []
    for j in V:
      for x, y in j.items():
        if j[x] == max(j.values()):
          opt.append(x)
    # The highest probability
    h = max(V[-1].values())
    print(opt)
    #print 'The steps of states are ' + ' '.join(opt) + ' with highest probability of %s'%h 

def dptable(V):
    # Print a table of steps from dictionary
    yield " ".join(("%10d" % i) for i in range(len(V)))
    for y in V[0]:
        yield "%.7s: " % y+" ".join("%.7s" % ("%f" % v[y]) for v in V)


states = [0,1,2,3]
obs = ['move left', 'move down', 'stay put', 'stay put']
trans_p = {
    0: {0: 0.1, 1: 0.8, 2: 0.0, 3: 0.1},
    1: {0: 0.1, 1: 0.1, 2: 0.8, 3: 0.0},
    2: {0: 0.0, 1: 0.1, 2: 0.8, 3: 0.0},
    3: {0: 0.1, 1: 0.0, 2: 0.8, 3: 0.1}
}
emit_p = {
    0: {'move left': 0.7, 'move right': 0.1, 'move down': 0.1, 'stay put': 0.1},
    1: {'move left': 0.1, 'move right': 0.1, 'move down': 0.7, 'stay put': 0.1},
    2: {'move left': 0.1, 'move right': 0.1, 'move down': 0.1, 'stay put': 0.7},
    3: {'move left': 0.7, 'move right': 0.1, 'move down': 0.1, 'stay put': 0.1}
}
start_p = (0.9,0.05,0.05,0)

viterbi(obs, states, start_p, trans_p, emit_p)
