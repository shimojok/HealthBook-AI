import json

PATHWAYS = [
    "PATH_00",
    "PATH_01",
    "PATH_02",
    "PATH_03",
    "PATH_04",
    "PATH_05",
    "PATH_06"
]

def calculate_pathway_scores(answers, matrix_file):
    with open(matrix_file, "r", encoding="utf-8") as f:
        matrix = json.load(f)

    scores = {p: 0.0 for p in PATHWAYS}

    for qid, answer_value in answers.items():
        if qid not in matrix:
            continue

        weights = matrix[qid]["weights"]

        for pathway, weight in weights.items():
            scores[pathway] += answer_value * weight

    normalized = {}
    for pathway, value in scores.items():
        normalized[pathway] = round(max(0, min(1, 0.5 + value)), 2)

    return normalized
