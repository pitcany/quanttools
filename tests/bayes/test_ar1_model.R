# Basic test for AR1 Stan model using testthat
library(testthat)

test_that("AR1 Stan model compiles and samples", {
  skip_if_not_installed("cmdstanr")
  source("src/r/bayes_ar1.R")
  # generate toy data
  data <- rnorm(30)
  fit <- fit_ar1_model(data, iter_sampling = 20, iter_warmup = 10)
  expect_s3_class(fit, "CmdStanMCMC")
  # check posterior summary contains parameters
  summary_df <- fit$summary()
  expect_true(all(c("mu", "phi", "sigma") %in% summary_df$variable))
})
