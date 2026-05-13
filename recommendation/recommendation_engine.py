import json

def recommend(pathway_scores, graph_file):
    with open(graph_file, "r", encoding="utf-8") as f:
        graph = json.load(f)

    recommendations = []

    for edge in graph:
        pathway = edge["target_pathway"]

        if pathway_scores.get(pathway, 1.0) < 0.4:
            recommendations.append({
                "substrate": edge["substrate"],
                "cluster": edge["microbial_cluster"],
                "metabolite": edge["final_metabolite"],
                "effect": edge["human_effect"]
            })

    return recommendations
