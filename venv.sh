#!/bin/bash
set -e

if test -d venv; then
  rm -rf venv
fi

python3 -m venv --system-site-packages venv
. "venv/bin/activate" && pip3 install -r requirements.txt
