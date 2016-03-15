if (!require('assertthat')) install.packages('asserthat')
if (!require('matrixcalc')) install.packages('matrixcalc')
if (!require('mvtnorm')) install.packages('mvtnorm')
if (!require('Matrix')) install.packages('Matrix')

# Initial values for x, A, B, C and R
N = 101 # go to 101 since R's indexing starts at 1
# the first element of everything is associted with t = 0, and the last element (the 101th element) with t = 100
x0 = c(1,1)
A = matrix(c(0,1,2,0), nrow = 2, ncol = 2)
B = matrix(c(2,0,5,3), nrow = 2, ncol = 2)
are_equal(rankMatrix(cbind(A, A%*%B))[1], max(nrow(A), ncol(A)))
C = c(2,1)
Q = C %*% t(C)
R = diag(x = c(2,3))
assert_that(is.positive.definite(R))
# 100 disturbances
ws = rmvnorm(N-1, mean = c(0,0), sigma = diag(x = c(0.1,0.2)))

# Initialize stores for x, L and K
x.mat <- matrix(NA, nrow = N, ncol = length(x0))
# store the initial state x0 as the first element in x
x.mat[1,] <- x0
#L.mat <- matrix(NA, nrow = N, ncol = length(x0))
L.list <- list()
# K's are (length of C) x (length of C), e.g. NxN
K.list <- list()

# Terminal K_N = C'C
K.list[[N]] <- Q

# for t = 99 to 0, solve for K and L
# R indices 100 to 1
for (t in (N-1):1) {
  K.tplus1 <- K.list[t+1][[1]]
  K.list[[t]] <- t(A) %*% (K.tplus1 - K.tplus1%*%B%*% solve(R + t(B)%*%K.tplus1%*%B) %*% t(B) %*% K.tplus1) %*% A + Q
  L.list[[t]] <- -solve(R + t(B)%*%K.tplus1%*%B) %*% t(B) %*% K.tplus1 %*% A
}

# Use L's to solve for optimal control
# from t = 1 to 100 (e.g. R indices 2 to 101)
# first component of xs is x0 -> x0, so need to index from t+1
for (t in 2:N) {
  lastperiod <- t-1
  x.lastperiod <- x.mat[lastperiod,]
  L.lastperiod <- L.list[[lastperiod]]
  w.lastperiod <- ws[lastperiod,]
  # solve for x_{k+1}
  x.mat[t,] <- A %*% x.lastperiod + B %*% (L.lastperiod %*% x.lastperiod) + w.lastperiod
}

# final x.mat will be matrix of our states
