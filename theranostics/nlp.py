"""Simple NLP helpers for clinical notes."""
from __future__ import annotations

from typing import List, Dict

try:
    import spacy
except Exception:  # pragma: no cover - optional dependency
    spacy = None


def extract_entities(text: str, model: str | None = None) -> List[Dict[str, str]]:
    """Extract named entities from `text` using a spaCy model.

    If spaCy is not installed, returns an empty list so tests and CI remain lightweight.
    """
    if spacy is None:
        return []
    if model:
        nlp = spacy.load(model)
    else:
        nlp = spacy.blank("en")
    doc = nlp(text)
    ents: List[Dict[str, str]] = []
    for ent in doc.ents:
        ents.append({"text": ent.text, "label": ent.label_})
    return ents
