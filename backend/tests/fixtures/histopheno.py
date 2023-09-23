import pytest


@pytest.fixture
def histopheno():
    return {
        "id": "MONDO:0020121",
        "items": [
            {"label": "musculature", "count": 962, "id": "HP:0003011"},
            {"label": "nervous_system", "count": 628, "id": "HP:0000707"},
            {"label": "head_neck", "count": 366, "id": "HP:0000152"},
            {"label": "skeletal_system", "count": 244, "id": "HP:0000924"},
            {"label": "eye", "count": 191, "id": "HP:0000478"},
            {"label": "respiratory", "count": 177, "id": "HP:0002086"},
            {"label": "metabolism_homeostasis", "count": 126, "id": "HP:0001939"},
            {"label": "blood", "count": 113, "id": "HP:0001871"},
            {"label": "cardiovascular_system", "count": 96, "id": "HP:0001626"},
            {"label": "connective_tissue", "count": 87, "id": "HP:0003549"},
            {"label": "digestive_system", "count": 68, "id": "HP:0025031"},
            {"label": "neoplasm", "count": 68, "id": "HP:0002664"},
            {"label": "integument", "count": 20, "id": "HP:0001574"},
            {"label": "ear", "count": 19, "id": "HP:0000598"},
            {"label": "genitourinary_system", "count": 18, "id": "HP:0000119"},
            {"label": "growth", "count": 14, "id": "HP:0001507"},
            {"label": "immune_system", "count": 12, "id": "HP:0002715"},
            {"label": "prenatal_or_birth", "count": 10, "id": "HP:0001197"},
            {"label": "endocrine", "count": 8, "id": "HP:0000818"},
            {"label": "breast", "count": 0, "id": "HP:0000769"},
        ],
    }
