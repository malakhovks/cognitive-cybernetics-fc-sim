def normalize_doi(doi: str) -> str:
    return doi.strip().lower().replace('https://doi.org/', '')
