source('distances.R')
source('greedySpanningTree.R')

# Find a minimal path from any origin to return without visiting a city twice
#
travelling.salesman <- function(cities) {
  # Initialize the number of cities to work through and distances between them
  num.cities <- nrow(cities)
  distances <- distances(cities)

  # initialize data objects for storing distances and paths to enable returning the best solution
  all.distances <- rep(0, length(num.cities))
  # paths is a matrix to store each path returned from greedy spanning tree
  # will be a matrix num.cities x num.cities matrix, each city having itself as the origin
  # and a greedy path stemming from it
  all.paths <- matrix(0, nrow = num.cities, ncol = num.cities)

  # Loop through each city, find a greedy spanning tree
  # add it's total distance and path to all.distances and all.paths
  for (i in 1:num.cities) {
    greedy.path <- greedy.spanning.tree(i, distances)
    all.distances[i] <- greedy.path[['total.distance']]
    all.paths[i,] <- greedy.path[['path']]
  }

  min.distance.idx <- which.min(all.distances)
  min.distance <- all.distances[min.distance.idx]
  min.path <- all.paths[min.distance.idx,]
  return(list(min.path = min.path, min.distance = min.distance))
}
