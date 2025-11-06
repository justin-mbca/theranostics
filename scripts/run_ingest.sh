#!/usr/bin/env bash
# Wrapper to run the DICOM ingest with the repository on PYTHONPATH
set -euo pipefail
REPO_ROOT=$(cd "$(dirname "$0")/.." && pwd)
export PYTHONPATH="$REPO_ROOT"
if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <dicom_dir> <out_path>"
  exit 2
fi
python "$REPO_ROOT/scripts/ingest_dicom.py" "$1" "$2"
