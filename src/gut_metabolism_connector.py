class GutMetabolismConnector:

    def connect(self, pathways, kampo_list):
        result = []

        for k in kampo_list:
            result.append({
                "kampo": k["name_en"],
                "mbt55_strains": k["mbt55_optimization"]["recommended_strains"],
                "pathways": list(set([
                    p["pathway"] for p in k.get("phytochemicals", [])
                ]))
            })

        return result
