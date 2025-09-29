#!/usr/bin/env bash
rm -rf .venv poetry.lock && \
poetry env list --full-path --quiet | xargs -r -n1 poetry env remove && \
poetry cache clear PyPI --all
