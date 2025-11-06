import json

import pytest

from theranostics.fhir_ingest import fetch_patients


def make_patient(uid: str):
    return {"resourceType": "Patient", "id": uid, "identifier": [{"value": uid}]}


def test_fetch_patients_monkeypatch(tmp_path, monkeypatch):
    base = "http://fhir.test"
    bundle = {
        "resourceType": "Bundle",
        "type": "searchset",
        "entry": [{"resource": make_patient("p1")}, {"resource": make_patient("p2")}],
    }

    class DummyResp:
        def __init__(self, json_data):
            self._json = json_data

        def raise_for_status(self):
            return None

        def json(self):
            return self._json

    def fake_get(url, timeout=10):
        return DummyResp(bundle)

    monkeypatch.setattr('theranostics.fhir_ingest.requests.get', fake_get)
    out = tmp_path / "patients.ndjson"
    n = fetch_patients(base, str(out))
    assert n == 2
    lines = out.read_text(encoding='utf-8').strip().splitlines()
    assert len(lines) == 2
    data = [json.loads(l) for l in lines]
    assert data[0]["id"] == "p1"


def test_fetch_patients_csv(tmp_path, monkeypatch):
    base = "http://fhir.test"
    bundle = {
        "resourceType": "Bundle",
        "type": "searchset",
        "entry": [{"resource": make_patient("p1")}, {"resource": make_patient("p2")}],
    }

    class DummyResp:
        def __init__(self, json_data):
            self._json = json_data

        def raise_for_status(self):
            return None

        def json(self):
            return self._json

    def fake_get(url, timeout=10):
        return DummyResp(bundle)

    monkeypatch.setattr('theranostics.fhir_ingest.requests.get', fake_get)
    out = tmp_path / "patients.csv"
    from theranostics.fhir_ingest import fetch_patients

    n = fetch_patients(base, str(out), to_csv=True)
    assert n == 2
    txt = out.read_text(encoding='utf-8')
    assert 'patient_id' in txt
