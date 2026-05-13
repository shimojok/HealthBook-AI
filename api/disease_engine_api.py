def infer_disease(scores):

    results = []

    for pathway, value in scores.items():

        if value < 0.4:

            results.append({
                "disease": f"{pathway}_Suppression",
                "risk_score": round(
                    1 - value,
                    2
                )
            })

    return results
