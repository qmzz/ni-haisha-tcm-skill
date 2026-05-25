#!/bin/bash
cd "$(dirname "$0")/.."
python3 -m unittest discover -s tests -p 'test_*.py' -v 2>&1 | tail -20
