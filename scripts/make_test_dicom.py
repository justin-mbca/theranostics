#!/usr/bin/env python3
"""Write minimal DICOM files for local testing.

Usage:
  python scripts/make_test_dicom.py /tmp/mydicoms --count 3
"""
from pathlib import Path
import argparse


def make_minimal_dicom(path: Path):
    try:
        import pydicom
        from pydicom.dataset import Dataset, FileMetaDataset
        from pydicom.uid import ExplicitVRLittleEndian, generate_uid
    except Exception as e:
        raise RuntimeError("pydicom is required to run this script") from e

    file_meta = FileMetaDataset()
    file_meta.MediaStorageSOPClassUID = generate_uid()
    file_meta.MediaStorageSOPInstanceUID = generate_uid()
    file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

    ds = Dataset()
    ds.file_meta = file_meta
    ds.is_little_endian = True
    ds.is_implicit_VR = False
    ds.SOPInstanceUID = generate_uid()
    ds.StudyInstanceUID = generate_uid()
    ds.SeriesInstanceUID = generate_uid()
    ds.PatientID = "TESTPATIENT"
    ds.Modality = "CT"
    ds.StudyDate = "20250101"
    ds.Manufacturer = "TESTMANU"
    ds.save_as(str(path))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("out_dir", help="directory to write DICOM files")
    p.add_argument("--count", type=int, default=1, help="number of files to create")
    args = p.parse_args()
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    for i in range(args.count):
        pth = out / f"test_{i+1}.dcm"
        make_minimal_dicom(pth)
        print("Wrote", pth)


if __name__ == '__main__':
    main()
