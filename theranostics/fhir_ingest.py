"""Minimal FHIR ingestion utilities."""
from __future__ import annotations

import json
from typing import List, Dict

import requests


def normalize_patient(resource: dict) -> Dict[str, str]:
    """Return a small flattened patient dict for modeling/storage."""
    pid = resource.get('id') or resource.get('identifier', [{}])[0].get('value', '')
    name = ''
    if resource.get('name'):
        name_parts = resource['name'][0].get('given', []) + [resource['name'][0].get('family', '')]
        name = ' '.join([p for p in name_parts if p])
    birthDate = resource.get('birthDate', '')
    return {'patient_id': pid, 'name': name, 'birthDate': birthDate}


def fetch_patients(base_url: str, out_path: str, page_size: int = 50, to_csv: bool = False) -> int:
    """Fetch Patient resources from a FHIR server (Bundle paging) and write to ndjson or CSV.

    If `to_csv` is True, writes a flattened CSV with one row per patient.
    Returns number of patient resources fetched.
    """
    patients: List[dict] = []
    url = f"{base_url.rstrip('/')}/Patient?_count={page_size}"
    while url:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        entries = data.get('entry', [])
        for e in entries:
            resource = e.get('resource')
            if resource and resource.get('resourceType') == 'Patient':
                patients.append(resource)
        # next link
        url = None
        for link in data.get('link', []):
            if link.get('relation') == 'next':
                url = link.get('url')
                break

    out_dir = out_path.rsplit('/', 1)[0] if '/' in out_path else ''
    if out_dir:
        import os

        os.makedirs(out_dir, exist_ok=True)

    if to_csv:
        import csv

        keys = ['patient_id', 'name', 'birthDate']
        with open(out_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            for p in patients:
                writer.writerow(normalize_patient(p))
    else:
        with open(out_path, 'w', encoding='utf-8') as f:
            for p in patients:
                f.write(json.dumps(p, ensure_ascii=False) + "\n")
    return len(patients)
