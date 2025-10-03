# AGENTS.md

Instructions

    The user will provide a task.
    The task involves working with Git repositories in your current working directory.
    Wait for all terminal commands to be completed (or terminate them) before finishing.

Git instructions

If completing the user's task requires writing or modifying files:

    Do not create new branches.
    Use git to commit your changes.
    If pre-commit fails, fix issues and retry.
    Check git status to confirm your commit. You must leave your worktree in a clean state.
    Only committed code will be evaluated.
    Do not modify or amend existing commits.

Citations instructions

    If you browsed files or used terminal commands, you must add citations to the final response (not the body of the PR message) where relevant. Citations reference file paths and terminal outputs with the following formats:
        【F:<file_path>†L<line_start>(-L<line_end>)?】
        File path citations must start with F:. file_path is the exact file path of the file relative to the root of the repository that contains the relevant text.
        line_start is the 1-indexed start line number of the relevant output within that file.
        【<chunk_id>†L<line_start>(-L<line_end>)?】
        Where chunk_id is the chunk_id of the terminal output, line_start and line_end are the 1-indexed start and end line numbers of the relevant output within that chunk.
    Line ends are optional, and if not provided, line end is the same as line start, so only 1 line is cited.
    Ensure that the line numbers are correct, and that the cited file paths or terminal outputs are directly relevant to the word or clause before the citation.
    Do not cite completely empty lines inside the chunk, only cite lines that have content.
    Only cite from file paths and terminal outputs, DO NOT cite from previous pr diffs and comments, nor cite git hashes as chunk ids.
    Use file path citations that reference any code changes, documentation or files, and use terminal citations only for relevant terminal output.
    Prefer file citations over terminal citations unless the terminal output is directly relevant to the clauses before the citation, i.e. clauses on test results.
        For PR creation tasks, use file citations when referring to code changes in the summary section of your final response, and terminal citations in the testing section.
        For question-answering tasks, you should only use terminal citations if you need to programmatically verify an answer (i.e. counting lines of code). Otherwise, use file citations.

PR creation instructions

    If you are comitting changes to the repository, you MUST call the make_pr tool.
    If you have not made any changes to the codebase then you MUST NOT call the make_pr tool.
    I.e. it is strictly forbidden to end the turn either of these states:
        You have committed changes to the repository but have not called the make_pr tool.
        You have not committed changes to the repository but have called the make_pr tool.

Final message instructions

    For each test or check in your final message, prefix the exact command with an emoji: use ✅ for pass, ⚠️ for warning (environment limitation), or ❌ for fail (agent error).

Screenshot instructions

If you are making a front-end change and there are instructions on how to start a dev server, please take a screenshot using the browser_container tool. If the browser tool is not available DO NOT attempt to install a browser/screenshot simply skip this step.

If the browse tool failed or is not working please indicate that you tried but were unable to take a screenshot.

If you have connection issues with the browse tool, DO NOT attempt to install your own browser or playwright unless the user asked or its installed already. Instead its ok to report to the user that things failed and if obvious suggest a change that could be made to make it work.

Include a citation to the image using standard markdown syntax (e.g. ![screenshot description](<artifact_path>)).

Repo path: /workspace/basilisk-core
Environment guidelines

    Do not use ls -R or grep -R as they are slow in large codebases. Instead, always use ripgrep (rg).
    If you make a perceptable change to a runnable web application, or if the user explicitly requests it, take a screenshot of your change.
    This is a non-interactive environment. Never ask for permissions to run a command, just do it.

Final answer guidelines### Answering questions

If you are answering a question, you MUST cite the files referenced and terminal commands you used to answer the question. Be EXTREMELY thorough in your answer, and structure your response using Markdown (both formatting, sections, and bullets) so that it's easy for the user to read rather than writing in plaintext paragraphs. The user really likes detailed answers to questions--you should not be terse! Make sure to put the file citations after the period in sentences.
Writing code

When you make code changes, your final answer should look like this:
Summary

    Bulleted list of changes made, with file citations.

Testing

    Bulleted list of tests and programmatic checks you ran, with terminal citations.
    Each command is prefixed by ⚠️ , ✅, or ❌ to indicate success, failure, or a warning depending on the output of the command.
    Use the warning symbol only if there is an environment limitation that causes that particular command to fail, for example not having network access.

<EXAMPLE_FINAL_ANSWER> Summary

    Changed src/main.rs to add a new function add_two that adds two to a given number. 【F:src/main.rs†L21-L31】
    Changed src/lib.rs to add a new function add_two that adds two to a given number. 【F:src/lib.rs†L12-L22】

Testing

    ✅ cargo test 【154bd0†L1-L24】
    ⚠️ pyright 【84b85d-L24】(warning due to missing dependencies) </EXAMPLE_FINAL_ANSWER>

PR guidelines

When calling make_pr on a follow-up task, your PR message on follow-ups should reuse the original PR message as much as possible and only edit it if there is a meaningful change from your follow-up, i.e. a major feature that should be added to the summary section. For example, if the original task asked you to make a Sudoku app from scratch, and then the user follows up and asks you to make a "Restart" button, your PR message should reflect that you made a Sudoku app with a Restart button, not just the Restart button. Do NOT add trivial changes to the PR message, i.e. if the user asks you to remove a comment you don't need to update the message. Assume that the user only sees the PR message for the cumulative diff after all follow-ups have been completed, so don't reference things that don't exist in your change.
Code style guidelines

    Never put try/catch blocks around imports.

Internet access

Internet access is ON. You can try installing dependencies and making curl requests.
Tools

Tools are grouped by namespace where each namespace has one or more tools defined. By default, the input for each tool call is a JSON object. If the tool schema has the word 'FREEFORM' input type, you should strictly follow the function description and instructions for the input format. It should not be JSON unless explicitly instructed by the function description or system/developer instructions.
Namespace: container
Target channel: commentary

namespace container {

// Open a new interactive exec session in a container. // Normally used for launching an interactive shell. Multiple sessions may // be running at a time. type new_session = (_: { // Unique name for the session session_name: string, }) => any;

// Feed characters to a session's STDIN. // After feeding characters, wait some amount of time, flush // STDOUT/STDERR, and show the results. Note that a minimum of 250 ms is enforced, so // if a smaller value is provided, it will be overridden with 250 ms. type feed_chars = (_: { // Session to feed characters to session_name: string, // Characters to feed; may be empty chars: string, // How long to wait in milliseconds before flushing STDOUT/STDERR yield_time_ms?: number, // default: 250 }) => any;

type make_pr = (_: { // Title of the pull request title: string, // Body message of the pull request body: string, }) => any;

} // namespace container
Namespace: browser_container

namespace browser_container {

// Execute a python playwright script in an attached browser container. // Use this to drive a browser to interact with services started in the container tool. // Do not start the webserver in this script, it should connect to a running server that is // bound to the interface 0.0.0.0. You can then instruct chromium, firefox or webkit to // connect to localhost: of your service. // We can only connect to ports you specify as ports_to_forward so include anything you need // for the app to work. Any images or output you wish to save should be output to a relatvie // local path like my/artifact.png and not /tmp/artifact.png. The full path of artifacts // will be returned by this function. type run_playwright_script = (_: { // A Playwright script to run. Written in python, and preferring asyncio apis. script: string, // List of TCP ports that to which need to connect. This is important as the browser will not be able to connect to localhost:PORT without this specified ports_to_forward: number[], // Number of seconds to wait for your script to complete. If this is omitted 30s is used as the default timeout_s?: number, // default: 30 }) => any;

// Opens an image artifact produced by a previous invocation of run_playwright_script. type open_image_artifact = (_: { // The full path (including the prefix) to the image artifact to open. Paths are returned by the run_playwright_script tool. path: string, }) => any;

} // namespace browser_container
Valid channels: analysis, commentary, final. Channel must be included for every message.
Juice: 240

## Purpose
This document defines how automated agents, assistants, and contributors should interact with this project.  
The focus is on workflows in **R**, **Python**, and **C++**, which are the project’s primary languages.  
The end goal is a reproducible, modular framework for **automated trading strategies**.

---

## General Principles
- **Reproducibility First**: All changes must be traceable, testable, and reproducible on a clean machine.  
- **Language-Aware Contributions**: Follow idioms of each language (tidyverse in R, PEP-8 in Python, RAII in C++).  
- **Minimal Surprises**: Avoid clever hacks unless explicitly requested. Clarity beats compactness.  
- **Version Pinning**: Always document version requirements for packages, libraries, or compilers.  
- **Domain Awareness**: Trading-related code must document assumptions (market, asset class, data frequency, slippage, etc.).  

---

## Python Rules
- Use **Poetry** or **Conda** for environment management.  
- Format code with **black** + **ruff**.  
- Provide **docstrings** for all functions/classes.  
- Group dependencies logically (core, ML, dev, viz, optim).  
- Write unit tests with **pytest**.  

### Optimization with Gurobi
- Use **gurobipy** for portfolio optimization, execution scheduling, and risk constraints.  
- Clearly annotate constraints/objectives in math and code.  
- Encapsulate models in reusable functions/classes.  
- Always call `.dispose()` in long sessions to avoid memory leaks.  
- Provide toy test cases under `tests/optimization/` (e.g., small mean-variance problems).  

---

## R Rules
- Use **tidyverse** for wrangling, **ggplot2** for visualization.  
- Document functions with `roxygen2`.  
- Use **renv** for reproducibility.  
- Supply **RMarkdown notebooks** for exploratory analysis and reporting.  

### Bayesian Inference with Stan / R
- Use **cmdstanr** for Bayesian time series and regime-switching models.  
- Store `.stan` models under `models/`.  
- Document priors explicitly in comments.  
- Run posterior checks (`R-hat`, ESS, traceplots).  
- Provide test datasets to validate models.  

---

## C++ Rules
- Target **C++17 or later**.  
- Use **CMake** for builds.  
- RAII patterns for memory safety.  
- Unit tests with **Catch2** or **GoogleTest**.  
- Prefer STL over hand-rolled utilities.  

### GPU Acceleration in C++
- Use **CUDA** kernels for backtesting acceleration (e.g., Monte Carlo simulations).  
- Provide CPU fallbacks.  
- Benchmark under `/benchmarks/`.  
- Document memory assumptions (FP32 vs FP64).  
- Toggle builds with `-DENABLE_CUDA=ON`.  

---

## Cross-Language Integration
- R ↔ Python: use **reticulate** for data pipelines.  
- Python ↔ C++: use **pybind11** for performance-critical code (e.g., fast order book simulation).  
- Document data types and ownership rules at boundaries.  

---

## Project Structure (Boilerplate)
quanttools/
├── data/ # Raw + processed datasets (never commit large raw data)
│ ├── raw/
│ └── processed/
├── models/ # ML, Bayesian, optimization, and fundamental-analysis models
│ ├── bayes/       # Stan models (.stan)
│ ├── dl/          # Deep learning (PyTorch/TensorFlow)
│ ├── trees/       # XGBoost, LightGBM, CatBoost
│ ├── fundamental/ # Fundamental-analysis pipelines (e.g., earnings, ratios)
│ └── optim/       # Gurobi, CVXPY, scheduling
├── src/ # Core source code
│ ├── python/ # Python modules
│ ├── r/ # R scripts
│ └── cpp/ # C++ code (with optional CUDA kernels)
├── notebooks/ # Jupyter/RMarkdown for research & reporting
├── benchmarks/ # Performance benchmarks (C++, GPU, backtesting)
├── tests/ # Unit + integration tests
│ ├── test_data/ # Small fixtures
│ ├── optimization/
│ └── bayes/
├── config/ # Config files (YAML/JSON for strategies/envs)
├── results/ # Saved model artifacts, logs, reports
├── scripts/ # Utility scripts (data download, cron jobs, etc.)
├── README.md
├── AGENTS.md
├── pyproject.toml # Poetry config
├── renv.lock # R reproducibility
└── CMakeLists.txt # C++ builds


---

## Dependency Groups (Poetry)

- **core**: always installed → numpy, pandas, scipy, scikit-learn, matplotlib, seaborn, jupyterlab, notebook, ipykernel.  
- **dl**: deep learning frameworks → torch/vision/audio, flax, optax, tensorflow, jax.  
- **trees**: gradient boosting frameworks → xgboost, lightgbm, catboost.  
- **fundamental**: fundamental-analysis → yfinance, pandas-datareader, openpyxl.  
- **bayes**: Bayesian inference → pymc, numpyro, cmdstanpy, arviz.  
- **nlp**: NLP stack → transformers, datasets, tokenizers, spacy, sentencepiece.  
- **cv**: computer vision → timm, opencv-python, (optionally detectron2/mmcv/mmdet).  
- **time**: time-series modeling → statsmodels, darts, prophet.  
- **optim**: optimization/experimentation → optuna, ray, mlflow, onnxruntime.  
- **dev**: developer tools → pytest, black, ruff.  

When running Poetry commands:
- `poetry install --with bayes` → installs only `core + bayes`.  
- `poetry install --without cv` → skips `cv` dependencies.  

---

## Agent Workflow Examples

- **Optimization (Python)**: Use `gurobipy` to maximize portfolio Sharpe ratio subject to risk/turnover constraints.  
- **Bayesian Calibration (R/Stan)**: Fit state-space volatility models and validate with posterior predictive checks.  
- **GPU Acceleration (C++)**: Implement Monte Carlo simulations with CUDA kernels, benchmark against CPU fallback.  

---
