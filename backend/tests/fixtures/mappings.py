import pytest


@pytest.fixture
def mappings():
    return {
        "limit": 20,
        "offset": 0,
        "total": 7,
        "items": [
            {
                "subject_id": "MONDO:0020121",
                "subject_label": "muscular dystrophy",
                "predicate_id": "skos:exactMatch",
                "object_id": "DOID:9884",
                "object_label": "muscular dystrophy",
                "mapping_justification": "semapv:UnspecifiedMatching",
                "id": "074f33ef-cab8-46e9-b535-5c637220dcd1",
            },
            {
                "subject_id": "MONDO:0020121",
                "subject_label": "muscular dystrophy",
                "predicate_id": "skos:exactMatch",
                "object_id": "ICD10CM:G71.0",
                "object_label": "Muscular dystrophy",
                "mapping_justification": "semapv:UnspecifiedMatching",
                "id": "575115b8-67a4-482d-88e7-1b1b60fdd99a",
            },
            {
                "subject_id": "MONDO:0020121",
                "subject_label": "muscular dystrophy",
                "predicate_id": "skos:exactMatch",
                "object_id": "MESH:D009136",
                "object_label": None,
                "mapping_justification": "semapv:UnspecifiedMatching",
                "id": "a2f1233e-1951-4f40-9a79-60f591a24bb5",
            },
            {
                "subject_id": "MONDO:0020121",
                "subject_label": "muscular dystrophy",
                "predicate_id": "skos:exactMatch",
                "object_id": "NCIT:C84910",
                "object_label": "Muscular Dystrophy",
                "mapping_justification": "semapv:UnspecifiedMatching",
                "id": "73eaeaef-9868-4e50-a4ed-aee537a830ae",
            },
            {
                "subject_id": "MONDO:0020121",
                "subject_label": "muscular dystrophy",
                "predicate_id": "skos:exactMatch",
                "object_id": "SCTID:73297009",
                "object_label": None,
                "mapping_justification": "semapv:UnspecifiedMatching",
                "id": "3f7aa4af-411c-47fe-9b3a-d8248484ea2d",
            },
            {
                "subject_id": "MONDO:0020121",
                "subject_label": "muscular dystrophy",
                "predicate_id": "skos:exactMatch",
                "object_id": "UMLS:C0026850",
                "object_label": None,
                "mapping_justification": "semapv:UnspecifiedMatching",
                "id": "f8d6fe34-2d2a-4ace-a314-f4def3070e3a",
            },
            {
                "subject_id": "MONDO:0020121",
                "subject_label": "muscular dystrophy",
                "predicate_id": "skos:exactMatch",
                "object_id": "Orphanet:98473",
                "object_label": None,
                "mapping_justification": "semapv:UnspecifiedMatching",
                "id": "63588ca1-4204-4143-88b3-152b31ea0c41",
            },
        ],
    }
