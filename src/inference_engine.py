import json
from collections import defaultdict


class HealthBookInferenceEngine:

    def __init__(self, q_path, d_path, k_path):
        # 質問データ読み込み
        q_data = self._load_json(q_path)
        if isinstance(q_data, dict) and "questions" in q_data:
            self.Q = q_data["questions"]
        else:
            self.Q = q_data

        # 疾病データ読み込み
        d_data = self._load_json(d_path)
        if isinstance(d_data, dict) and "disease_matrix" in d_data:
            self.DM = d_data["disease_matrix"]
        else:
            self.DM = d_data

        # 漢方ライブラリ読み込み
        k_data = self._load_json(k_path)
        self.KL = k_data if isinstance(k_data, list) else k_data.get("kampo_formulas", [])

        self.kampo_dict = {k["id"]: k for k in self.KL}

    def _load_json(self, path):
        with open(path, "r", encoding="utf-8-sig") as f:
            return json.load(f)

    # -----------------------------
    # ① RF抽出（rf / risk_factors両対応）
    # -----------------------------
    def extract_active_risk_factors(self, answers):
        rf_scores = defaultdict(float)

        for qid, ans in answers.items():
            if ans == 0:
                continue

            q = self.Q.get(str(qid))
            if not q:
                continue

            weight = q.get("weight", 1.0)
            multiplier = 1.0 if ans == 2 else 0.5

            rf_list = q.get("risk_factors") or q.get("rf") or []

            for rf in rf_list:
                rf_scores[rf] += weight * multiplier

        return dict(rf_scores)

    # -----------------------------
    # ② 疾病スコア
    # -----------------------------
    def calculate_disease_risk(self, rf_scores):
        results = []

        for d in self.DM:
            disease_rf = d.get("risk_factors", [])
            if not disease_rf:
                continue

            match = sum(rf_scores.get(rf, 0) for rf in disease_rf)
            score = match / len(disease_rf)

            results.append({
                "disease_id": d["disease_id"],
                "disease_name": d["disease_name_ja"],
                "score": score,
                "recommended_kampo": d.get("recommended_kampo", [])
            })

        return sorted(results, key=lambda x: x["score"], reverse=True)

    # -----------------------------
    # ③ D2P正式実装
    # -----------------------------
    def calculate_mbt55_pathways(self, disease_scores):

        pathway_scores = defaultdict(float)

        for d in disease_scores[:10]:
            for kid in d["recommended_kampo"]:
                kampo = self.kampo_dict.get(kid)
                if not kampo:
                    continue

                # phytochemicals → pathway抽出
                for p in kampo.get("phytochemicals", []):
                    pathway = p.get("pathway")
                    if pathway:
                        pathway_scores[pathway] += d["score"]

        return dict(sorted(pathway_scores.items(),
                           key=lambda x: x[1], reverse=True))

    # -----------------------------
    # ④ 漢方
    # -----------------------------
    def match_kampo(self, disease_scores):
        seen = set()
        result = []

        for d in disease_scores[:10]:
            for kid in d["recommended_kampo"]:
                if kid not in seen and kid in self.kampo_dict:
                    result.append(self.kampo_dict[kid])
                    seen.add(kid)

        return result

    # -----------------------------
    # ⑤ 予防スコア
    # -----------------------------
    def calculate_prevention_score(self, disease_scores):
        if not disease_scores:
            return 100

        top10 = disease_scores[:10]
        avg = sum(d["score"] for d in top10) / len(top10)
        return round(100 * (1 - avg), 2)

    # -----------------------------
    # 🚀 runEngine
    # -----------------------------
    def run_engine(self, answers):

        rf_scores = self.extract_active_risk_factors(answers)
        disease_scores = self.calculate_disease_risk(rf_scores)
        pathways = self.calculate_mbt55_pathways(disease_scores)
        kampo = self.match_kampo(disease_scores)
        prevention = self.calculate_prevention_score(disease_scores)

        return {
            "risk_factors": rf_scores,
            "disease_ranking": disease_scores[:20],
            "mbt55_pathways": pathways,
            "kampo_recommendations": kampo,
            "prevention_score": prevention
        }
