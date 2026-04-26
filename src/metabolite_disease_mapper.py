class MetaboliteDiseaseMapper:

    def map(self, disease_ranking, kampo_list):
        return [
            {
                "disease": d["disease_name"],
                "metabolites": self._extract_metabolites(kampo_list)
            }
            for d in disease_ranking[:10]
        ]

    def _extract_metabolites(self, kampo_list):
        mets = []
        for k in kampo_list:
            for p in k.get("phytochemicals", []):
                mets.append(p["name_en"])
        return list(set(mets))
