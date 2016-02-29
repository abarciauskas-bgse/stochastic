if (!require('Rcpp')) install.packages('Rcpp')
Rcpp::sourceCpp('distance.cpp')

# Calculate the euclidean distance between every row in a matrix
distances <- function(matrix) {
  n <- nrow(matrix)
  dist.matrix <- matrix(NA, n, n)
  for (idx in 1:n) {
    x.current <- matrix[idx,]
    x.current.expanded <- matrix(x.current, nrow = n, ncol = 2, byrow = TRUE)
    dist.matrix[idx, ] <- calcDist(matrix, x.current.expanded, 2)
  }
  return(dist.matrix)
}
