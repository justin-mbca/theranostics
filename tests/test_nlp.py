from theranostics.nlp import extract_entities


def test_extract_entities_blank():
    text = "Patient has metastatic lung cancer and SOB."
    ents = extract_entities(text)
    # blank model has no trained NER, so ents should be a list (possibly empty)
    assert isinstance(ents, list)
