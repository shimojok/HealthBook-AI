class FHIRClinicalDecisionSupport:

    def build(self, inference_result):
        return {
            "resourceType": "ClinicalImpression",
            "status": "completed",
            "summary": "HealthBook AI Inference",
            "finding": [
                {
                    "itemCodeableConcept": {
                        "text": d["disease_name"]
                    },
                    "basis": f"Risk Score: {d['score']:.2f}"
                }
                for d in inference_result["disease_ranking"][:10]
            ],
            "prognosisCodeableConcept": {
                "text": f"Prevention Score: {inference_result['prevention_score']}"
            }
        }
