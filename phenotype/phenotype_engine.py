import json


class PhenotypeEngine:

    def __init__(self, matrix_path):

        with open(
            matrix_path,
            "r",
            encoding="utf-8"
        ) as f:

            self.matrix = json.load(f)

    def calculate_scores(self, answers):

        scores = {}

        for question_id, answer_value in answers.items():

            if question_id not in self.matrix:
                continue

            pathway_weights = self.matrix[question_id]

            for pathway, weight in pathway_weights.items():

                if pathway not in scores:
                    scores[pathway] = 0.5

                scores[pathway] += (
                    answer_value * weight
                )

        for pathway in scores:

            if scores[pathway] < 0:
                scores[pathway] = 0.0

            if scores[pathway] > 1:
                scores[pathway] = 1.0

            scores[pathway] = round(
                scores[pathway],
                2
            )

        return scores
