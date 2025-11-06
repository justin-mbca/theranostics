import os

import pytest

from theranostics.dicom_ingest import ingest_directory


def test_ingest_writes_parquet(tmp_path):
    # create a tiny DICOM using existing test helper pattern
    try:
        import pydicom
        from pydicom.dataset import Dataset, FileMetaDataset
        from pydicom.uid import ExplicitVRLittleEndian, generate_uid
    except Exception:
        pytest.skip("pydicom not installed")

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
    ds.PatientID = "P1"
    ds.Modality = "CT"
    ds.StudyDate = "20250101"
    ds.Manufacturer = "M1"
    dcm_path = tmp_path / "t1.dcm"
    ds.save_as(str(dcm_path))

    out_parquet = tmp_path / "out.parquet"
    n = ingest_directory(str(tmp_path), str(out_parquet), to_parquet=True)
    assert n >= 1
    # Accept either a parquet file or a CSV fallback when parquet engine is not installed
    parquet_exists = os.path.exists(str(out_parquet))
    csv_fallback = os.path.exists(str(out_parquet) + '.csv')
    assert parquet_exists or csv_fallback

