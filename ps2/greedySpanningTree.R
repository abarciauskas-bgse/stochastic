# `greedy.spanning.tree`
#
#  greedy.spanning.tree greedily finds a minimized cost path from origin node to every other node (w/o cycles)
#   but this is not the minimal cost
#
# Naming is purposefully generic, to facilitate use outside of the travelling salesman problem
#  Although, given it computes a complete path from origin to return, does seem to purposed for solving that problem
#
# greedy.spanning.tree takes 2 arguments:
#   `origin.node`: the index of the origin node
#   `costs`: a matrix of dimension of the number of nodes in the graph
#      indiciating the cost to travel from each node to any other nodes in the graph
#
# greedy.spanning.tree returns a list with elements
#   `path`: an ordered list of nodes visited
#   `total.distance`: the total distance from the first node through each subsequent node
#
greedy.spanning.tree <- function(origin.node = 1, costs = matrix()) {
  current.node <- origin.node
  total.distance <- 0
  num.nodes <- nrow(costs)
  visited <- c(origin.node)

  while (length(visited) < num.nodes) {
    ordered.costs <- order(costs[,current.node])
    nearest.neighbor <- ordered.costs[which(!(ordered.costs %in% visited))][1]
    total.distance <- total.distance + costs[current.node, nearest.neighbor]
    visited <- append(visited, nearest.neighbor)
    current.node <- nearest.neighbor
  }

  # Add final distance from last node to return ot the origin node
  final.distance <- total.distance + costs[origin.node, visited[num.nodes]]
  return(list(total.distance = final.distance, path = visited))
}
