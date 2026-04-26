import json
from collections import defaultdict
from typing import Dict, List, Any


class HealthBookInferenceEngine:

    def __init__(self, questionnaire_path, disease_matrix_path, kampo_library_path):
        self.Q = self._load_json(questionnaire_path)["questions"]
        self.DM = self._load_json(disease_matrix_path)["disease_matrix"]
        self.KL = self._load_json(kampo_library_path)

        # インデックス構築
        self.disease_rf_map = self._build_disease_rf_map()
        self.kampo_dict = {k["id"]: k for k in self.KL}

    def _load_json(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _build_disease_rf_map(self):
        """
        disease_name → risk_factor list
        """
        rf_map = {}
        for d in self.DM:
            rf_map[d["disease_id"]] = {
                "name": d["disease_name_ja"],
                "rf": d.get("risk_factors", []),  # 拡張対応
                "kampo": d.get("recommended_kampo", [])
            }
        return rf_map

    # -----------------------------
    # ① アクティブリスク因子抽出
    # -----------------------------
    def extract_active_risk_factors(self, answers: Dict[int, int]):
        """
        answers: {question_id: 0/1/2} (No / Sometimes / Often)
        """
        rf_scores = defaultdict(float)

        for qid, ans in answers.items():
            if ans == 0:
                continue

            q = self.Q[str(qid)]
            weight = q["weight"]

            # スコア係数
            multiplier = 1.0 if ans == 2 else 0.5

            for rf in q["risk_factors"]:
                rf_scores[rf] += weight * multiplier

        return dict(rf_scores)

    # -----------------------------
    # ② 疾病リスクスコア算出
    # -----------------------------
    def calculate_disease_risk(self, rf_scores):
        disease_scores = []

        for d in self.DM:
            disease_id = d["disease_id"]
            disease_name = d["disease_name_ja"]

            disease_rf = d.get("risk_factors", [])

            if not disease_rf:
                continue

            match_score = 0
            total_weight = 0

            for rf in disease_rf:
                total_weight += 1
                if rf in rf_scores:
                    match_score += rf_scores[rf]

            if total_weight == 0:
                continue

            score = match_score / total_weight

            disease_scores.append({
                "disease_id": disease_id,
                "disease_name": disease_name,
                "score": score
            })

        return sorted(disease_scores, key=lambda x: x["score"], reverse=True)

    # -----------------------------
    # ③ MBT55 経路優先度
    # -----------------------------
    def calculate_mbt55_pathways(self, top_diseases):
        """
        仮実装: disease → pathway マッピング必要
        """
        pathway_scores = defaultdict(float)

        # 仮: disease_id のプレフィックスで分岐
        for d in top_diseases[:10]:
            did = d["disease_id"]
            score = d["score"]

            if did.startswith("D00"):
                pathway_scores["PATH_01"] += score
            elif did.startswith("D01"):
                pathway_scores["PATH_02"] += score
            elif did.startswith("D02"):
                pathway_scores["PATH_03"] += score
            elif did.startswith("D03"):
                pathway_scores["PATH_04"] += score
            else:
                pathway_scores["PATH_05"] += score

        return dict(sorted(pathway_scores.items(), key=lambda x: x[1], reverse=True))

    # -----------------------------
    # ④ 漢方マッチング
    # -----------------------------
    def match_kampo(self, top_diseases):
        kampo_set = []
        seen = set()

        for d in top_diseases[:10]:
            for kid in d.get("recommended_kampo", []):
                if kid not in seen and kid in self.kampo_dict:
                    kampo_set.append(self.kampo_dict[kid])
                    seen.add(kid)

        return kampo_set

    # -----------------------------
    # ⑤ 予防スコア
    # -----------------------------
    def calculate_prevention_score(self, top_diseases):
        if not top_diseases:
            return 100

        top10 = top_diseases[:10]
        avg_risk = sum(d["score"] for d in top10) / len(top10)

        return round(100 * (1 - avg_risk), 2)

    # -----------------------------
    # 🚀 runEngine
    # -----------------------------
    def run_engine(self, answers: Dict[int, int]):

        # ① リスク因子
        rf_scores = self.extract_active_risk_factors(answers)

        # ② 疾病スコア
        disease_scores = self.calculate_disease_risk(rf_scores)

        # ③ 経路優先度
        pathway_scores = self.calculate_mbt55_pathways(disease_scores)

        # ④ 漢方
        kampo = self.match_kampo(disease_scores)

        # ⑤ 予防スコア
        prevention_score = self.calculate_prevention_score(disease_scores)

        return {
            "risk_factors": rf_scores,
            "disease_ranking": disease_scores[:20],
            "mbt55_pathways": pathway_scores,
            "kampo_recommendations": kampo,
            "prevention_score": prevention_score
        }
