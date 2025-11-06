"""Minimal DICOM ingestion utilities."""
from __future__ import annotations

from typing import List
import os
import csv
import pandas as pd

try:
    import pydicom
    from pydicom.dataset import Dataset
except Exception:  # pragma: no cover - optional dependency
    pydicom = None


def extract_metadata(dicom_path: str) -> dict:
    """Extract a small set of metadata from a DICOM file.

    Returns a dict with keys: StudyInstanceUID, SeriesInstanceUID, SOPInstanceUID,
    PatientID, Modality, StudyDate, Manufacturer.
    """
    if pydicom is None:
        raise RuntimeError("pydicom is required for DICOM ingestion")
    try:
        ds = pydicom.dcmread(dicom_path, stop_before_pixels=True)
    except pydicom.errors.InvalidDicomError:
        # Try to read non-conformant files
        ds = pydicom.dcmread(dicom_path, stop_before_pixels=True, force=True)
    return {
        "study_instance_uid": getattr(ds, "StudyInstanceUID", ""),
        "series_instance_uid": getattr(ds, "SeriesInstanceUID", ""),
        "sop_instance_uid": getattr(ds, "SOPInstanceUID", ""),
        "patient_id": getattr(ds, "PatientID", ""),
        "modality": getattr(ds, "Modality", ""),
        "study_date": getattr(ds, "StudyDate", ""),
        "manufacturer": getattr(ds, "Manufacturer", ""),
        "file_path": dicom_path,
    }


def ingest_directory(directory: str, out_path: str, to_parquet: bool = False) -> int:
    """Walk `directory`, extract DICOM metadata, and write to CSV or Parquet file `out_path`.
    If `to_parquet` is True, writes a parquet file (requires pyarrow or fastparquet).
    Returns number of files processed.
    """
    rows: List[dict] = []
    for root, _, files in os.walk(directory):
        for fn in files:
            path = os.path.join(root, fn)
            try:
                meta = extract_metadata(path)
                rows.append(meta)
            except Exception:
                # skip files that are not DICOM or can't be read
                continue

    if not rows:
        # write an empty file of the chosen format for downstream tooling
        df = pd.DataFrame()
        out_dir = os.path.dirname(out_path)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        if to_parquet:
            df.to_parquet(out_path)
        else:
            df.to_csv(out_path, index=False)
        return 0

    df = pd.DataFrame(rows)
    out_dir = os.path.dirname(out_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    if to_parquet:
        # prefer parquet; index=False keeps file tidy
        try:
            df.to_parquet(out_path, index=False)
        except Exception as exc:
            # parquet engine not available or failed; fallback to CSV
            # write alongside with .csv suffix for portability
            csv_path = out_path + '.csv'
            df.to_csv(csv_path, index=False)
    else:
        # fallback to csv
        df.to_csv(out_path, index=False)

    return len(rows)

