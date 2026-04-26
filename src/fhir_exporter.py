import json
from typing import Dict, Any

class FHIRExporter:
    """HealthBook inference result → FHIR R4 ClinicalImpression"""

    def build(self, result: Dict[str, Any]) -> Dict[str, Any]:
        disease_ranking = result.get("disease_ranking", [])
        kampo = result.get("kampo_recommendations", [])
        prevention = result.get("prevention_score", 100)

        return {
            "resourceType": "ClinicalImpression",
            "status": "completed",
            "summary": "HealthBook AI Metabolic Inference",
            "finding": [
                {
                    "itemCodeableConcept": {
                        "coding": [{"system": "http://hl7.org/fhir/sid/icd-10", "code": d["disease_id"], "display": d["disease_name"]}],
                        "text": d["disease_name"]
                    },
                    "basis": f"Risk Score: {d['score']:.2f}"
                }
                for d in disease_ranking[:10]
            ],
            "prognosisCodeableConcept": {
                "coding": [{"system": "http://snomed.info/sct", "code": "prevention-score", "display": f"Prevention Score: {prevention}"}],
                "text": f"Prevention Score: {prevention}"
            },
            "extension": [
                {
                    "url": "https://healthbook.ai/fhir/kampo-recommendations",
                    "valueString": json.dumps(kampo[:5], ensure_ascii=False)
                },
                {
                    "url": "https://healthbook.ai/fhir/mbt55-pathways",
                    "valueString": json.dumps(result.get("mbt55_pathways", {}), ensure_ascii=False)
                }
            ]
        }
