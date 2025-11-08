#!/usr/bin/env python3
"""CLI to run a named experiment using theranostics.experiments.run_experiment

Usage:
    python scripts/run_experiment.py --n 300
"""
import argparse
import json
import os
import sys

# Ensure repo root is on path when running directly
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from theranostics.experiments import run_experiment


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=200, help="number of synthetic patients to generate")
    parser.add_argument("--artifacts", type=str, default="artifacts/experiments", help="artifacts directory")
    args = parser.parse_args()

    res = run_experiment(params={"n": args.n}, artifacts_dir=args.artifacts)
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
