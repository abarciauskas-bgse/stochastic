setwd('~/Box Sync/abarciausksas/second_term/stochastic/ps4')
source('get.states.R')

# final x.mat will be matrix of our states
# test default is not broken
res <- get.states()

# (i) Fix R and x0, and compare the behavior of the system for two covariance matrices for the disturbances,
# one “much larger” than the other, under optimal control (given by the discrete-time Riccati equation)
# small
first.q.small <- get.states()
# explicitly state N for clarity
N = 101
first.q.large <- get.states(N = N, ws = rmvnorm(N-1, mean = c(0,0), sigma = diag(x = c(1.2,3.2))))

min.x1 <- min(first.q.large$x.matrix[,1])
max.x1 <- max(first.q.large$x.matrix[,1])
plot(first.q.small$x.matrix[,1],
     type = 'l',
     col = 'blue',
     ylim = c(min.x1, max.x1),
     ylab = 'x1')
lines(first.q.large$x.matrix[,1], type = 'l', col = 'red')

min.x2 <- min(first.q.large$x.matrix[,2])
max.x2 <- max(first.q.large$x.matrix[,2])
plot(first.q.small$x.matrix[,2],
     type = 'l',
     col = 'blue',
     ylim = c(min.x2, max.x2),
     ylab = 'x2')
lines(first.q.large$x.matrix[,2], type = 'l', col = 'red')

# (ii) Fix R and D, and compare the behavior of the system for two initial conditions,
# one "much larger" than the other, under optimal control;
second.q.small <- get.states()
second.q.large <- get.states(x0 = c(21,43))
min.x1 <- min(second.q.small$x.matrix[,1])
max.x1 <- max(second.q.large$x.matrix[,1])
plot(second.q.small$x.matrix[,1],
     type = 'l',
     col = 'blue',
     ylim = c(min.x1-2, max.x1),
     ylab = 'x1')
lines(second.q.large$x.matrix[,1], type = 'l', col = 'red')

min.x2 <- min(second.q.small$x.matrix[,2])
max.x2 <- max(second.q.large$x.matrix[,2])
plot(second.q.small$x.matrix[,2],
     type = 'l',
     col = 'blue',
     ylim = c(min.x2-10, max.x2),
     ylab = 'x2')
lines(second.q.large$x.matrix[,2], type = 'l', col = 'red')

# (iii) Fix x0 and D, and compare the behavior of the system for two input-cost matrices,
# one "much larger" than the other, under optimal control;
third.q.small <- get.states()
third.q.large <- get.states(R = diag(x = c(99,23)))
min.x1 <- min(third.q.small$x.matrix[,1])
max.x1 <- max(third.q.large$x.matrix[,1])
plot(third.q.small$x.matrix[,1],
     type = 'l',
     col = 'blue',
     ylim = c(min.x1, max.x1),
     ylab = 'x1')
lines(third.q.large$x.matrix[,1], type = 'l', col = 'red')

min.x2 <- min(third.q.small$x.matrix[,2])
max.x2 <- max(third.q.large$x.matrix[,2])
plot(third.q.small$x.matrix[,2],
     type = 'l',
     col = 'blue',
     ylim = c(min.x2, max.x2),
     ylab = 'x2')
lines(third.q.large$x.matrix[,2], type = 'l', col = 'red')

# (iv) Fix R, x0, and D, and compare the behavior of the system under optimal control vs. steady-state control
# (given by the algebraic Riccati equation).
source('get.states.R')
fourth.q.normal <- get.states(riccardi = FALSE)
fourth.q.riccardi <- get.states(riccardi = TRUE)
plot(fourth.q.normal$x.matrix[,1],
     type = 'l',
     col = 'blue',
     ylab = 'x1')
lines(fourth.q.riccardi$x.matrix[,1], type = 'l', col = 'red')

plot(fourth.q.normal$x.matrix[,2],
     type = 'l',
     col = 'blue',
     ylab = 'x2')
lines(fourth.q.riccardi$x.matrix[,2], type = 'l', col = 'red')
