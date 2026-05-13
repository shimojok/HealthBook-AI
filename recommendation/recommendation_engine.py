import json


class RecommendationEngine:

    def __init__(self, mapping_path):

        with open(
            mapping_path,
            "r",
            encoding="utf-8"
        ) as f:

            self.mapping = json.load(f)

    def recommend(self, pathways):

        recommendations = []

        for pathway in pathways:

            if pathway in self.mapping:

                recommendations.append({
                    "pathway": pathway,
                    "foods": self.mapping[pathway]
                })

        return recommendations
