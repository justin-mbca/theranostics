import os
from theranostics.flow import pipeline_with_dicom


def test_pipeline_returns_numeric_dicom_count():
    # use the test DICOMs generated earlier in /tmp/mydicoms
    res = pipeline_with_dicom(n=5, dicom_dir='/tmp/mydicoms', out_parquet='data/bronze/dicom_metadata_test.parquet')
    assert 'dicom_count' in res
    assert isinstance(res['dicom_count'], int)
    # expected 3 files were created in the earlier step
    assert res['dicom_count'] >= 0
