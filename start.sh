#!/bin/bash
set -euo pipefail
echo "Downloading"
python3 downloader.py
echo "Preprocessing"
python3 preprocess.py
