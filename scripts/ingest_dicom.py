"""CLI to run DICOM directory ingest."""
import sys
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
