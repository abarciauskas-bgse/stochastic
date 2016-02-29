# setwd('~/Box Sync/abarciausksas/myfiles/stochastic/')

source('travellingSalesman.R')
cities <- as.matrix(read.csv('uruguay.tsv', sep = ' ', header = FALSE))
path <- travelling.salesman(cities)

# references:
# https://en.wikipedia.org/wiki/Held–Karp_algorithm
# http://www.personal.kent.edu/~rmuhamma/Compgeometry/MyCG/CG-Applets/TSP/notspcli.htm
# http://www.math.uwaterloo.ca/tsp/world/uytour.html
# this greedy solution returns a distance of 96514.81
# current optimal distance is 79114
#