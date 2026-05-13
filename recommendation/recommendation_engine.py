from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List


class RecommendationEngine:

    def __init__(self, graph_path: str | Path):

        self.graph_path = Path(graph_path)

        if not self.graph_path.exists():
            raise FileNotFoundError(
                f"Metabolic graph not found: {self.graph_path}"
            )

        with open(self.graph_path, "r", encoding="utf-8") as f:
            self.graph = json.load(f)

    def generate_recommendations(
        self,
        pathway_scores: Dict[str, float],
        threshold: float = 0.40
    ) -> List[Dict]:

        recommendations = []

        for edge in self.graph:

            pathway = edge.get("target_pathway")

            if pathway is None:
                continue

            score = pathway_scores.get(pathway, 1.0)

            if score < threshold:

                recommendations.append({
                    "pathway": pathway,
                    "substrate": edge.get("substrate"),
                    "cluster": edge.get("microbial_cluster"),
                    "intermediate": edge.get("intermediate_metabolite"),
                    "metabolite": edge.get("final_metabolite"),
                    "effect": edge.get("human_effect")
                })

        return recommendations
