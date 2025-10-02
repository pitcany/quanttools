#!/usr/bin/env Rscript
#' Fit AR(1) time series model using cmdstanr
#'
#' @param series Numeric vector of time series observations.
#' @param iter_sampling Number of sampling iterations (default: 1000).
#' @param iter_warmup Number of warmup iterations (default: 500).
#' @return A CmdStanMCMC object with posterior samples.
#' @details
#' This function expects the Stan model file to be located at 'models/bayes/ar1.stan'
#' relative to the project root. It uses cmdstanr to compile and sample.
#' @examples
#' \dontrun{
#' library(cmdstanr)
#' source('src/r/bayes_ar1.R')
#' data <- rnorm(100)
#' fit <- fit_ar1_model(data)
#' print(fit$summary())
#' }
fit_ar1_model <- function(series, iter_sampling = 1000, iter_warmup = 500) {
  if (!requireNamespace('cmdstanr', quietly = TRUE)) {
    stop('Package "cmdstanr" is required for fitting Stan models.')
  }
  stan_file <- file.path('models', 'bayes', 'ar1.stan')
  if (!file.exists(stan_file)) {
    stop(sprintf('Stan model file not found: %s', stan_file))
  }
  model <- cmdstanr::cmdstan_model(stan_file)
  data_list <- list(N = length(series), y = as.numeric(series))
  fit <- model$sample(
    data = data_list,
    iter_sampling = iter_sampling,
    iter_warmup = iter_warmup
  )
  return(fit)
}
