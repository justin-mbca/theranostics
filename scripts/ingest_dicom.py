"""CLI to run DICOM directory ingest."""
import sys
from pathlib import Path

# ensure the repo root is on sys.path so this script can be run directly
repo_root = str(Path(__file__).resolve().parents[1])
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from theranostics.dicom_ingest import ingest_directory


def main():
    if len(sys.argv) < 3:
        print("Usage: ingest_dicom.py <dicom_dir> <out_csv>")
        sys.exit(2)
    dicom_dir = sys.argv[1]
    out_csv = sys.argv[2]
    n = ingest_directory(dicom_dir, out_csv)
    print(f"Processed {n} DICOM files, wrote {out_csv}")


if __name__ == "__main__":
    main()
