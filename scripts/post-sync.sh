#!/usr/bin/env bash
# Reinstall spaCy models after uv sync --upgrade.
# Models are installed via direct URL (not managed by uv.lock),
# so any full sync wipes them. Run this script to restore.
set -euo pipefail

echo "Installing spaCy models..."
uv pip install \
  en_core_web_sm@https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl \
  ja_core_news_sm@https://github.com/explosion/spacy-models/releases/download/ja_core_news_sm-3.8.0/ja_core_news_sm-3.8.0-py3-none-any.whl
echo "spaCy models installed."
