"""Minimal FHIR ingestion utilities."""
from __future__ import annotations

import json
from typing import List

import requests


def fetch_patients(base_url: str, out_path: str, page_size: int = 50) -> int:
    """Fetch Patient resources from a FHIR server (Bundle paging) and write a ndjson file.

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

    # write newline-delimited json
    out_dir = out_path.rsplit('/', 1)[0] if '/' in out_path else ''
    if out_dir:
        import os

        os.makedirs(out_dir, exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        for p in patients:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")
    return len(patients)
