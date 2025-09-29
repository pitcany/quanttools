#!/usr/bin/env bash
rm -rf .venv poetry.lock && poetry env list --full-path | awk '{print $1}' | xargs -r poetry env remove && poetry cache clear PyPI --all
