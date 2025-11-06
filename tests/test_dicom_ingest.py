import os

import pytest

from theranostics.dicom_ingest import extract_metadata, ingest_directory


def make_minimal_dicom(path: str):
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
    ds.PatientID = "TESTPATIENT"
    ds.Modality = "CT"
    ds.StudyDate = "20250101"
    ds.Manufacturer = "TESTMANU"
    ds.save_as(path)


def test_extract_metadata_and_ingest(tmp_path):
    dcm_path = tmp_path / "test.dcm"
    make_minimal_dicom(str(dcm_path))
    meta = extract_metadata(str(dcm_path))
    assert meta["patient_id"] == "TESTPATIENT"
    out_csv = tmp_path / "out.csv"
    n = ingest_directory(str(tmp_path), str(out_csv))
    assert n >= 1
    assert os.path.exists(out_csv)
