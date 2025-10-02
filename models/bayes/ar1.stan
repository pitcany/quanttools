// AR(1) time series model (autoregressive of order 1)
// Data block: N observations of a univariate series y
data {
  int<lower=1> N;
  vector[N] y;
}
// Parameters: mean (mu), autoregressive coefficient (phi), and noise scale (sigma)
parameters {
  real mu;
  real<lower=-1,upper=1> phi;
  real<lower=0> sigma;
}
// Model block: priors and likelihood
model {
  // Priors
  mu ~ normal(0, 10);
  phi ~ uniform(-1, 1);
  sigma ~ cauchy(0, 5);

  // Likelihood: first observation and AR(1) recursion
  y[1] ~ normal(mu, sigma);
  for (n in 2:N)
    y[n] ~ normal(mu + phi * (y[n-1] - mu), sigma);
}
