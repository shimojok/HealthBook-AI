class MetaboliteMapper:

    def __init__(self):

        # RF → 代謝物（因果ベース）
        self.mapping = {
            "糖質過多": ["butyrate"],
            "間食多い": ["butyrate"],
            "運動不足": ["butyrate"],

            "炎症": ["urolithin_A"],
            "ストレス": ["urolithin_A"],
            "免疫低下": ["urolithin_A"],

            "ホルモン異常": ["equol"],
            "更年期": ["equol"],
            "骨密度低下": ["equol"]
        }

        # 説明
        self.meta_info = {
            "butyrate": {
                "name": "酪酸",
                "mechanism": "SCFA → インスリン感受性改善・腸上皮修復"
            },
            "urolithin_A": {
                "name": "ウロリチンA",
                "mechanism": "ミトファジー活性化 → 炎症抑制"
            },
            "equol": {
                "name": "エクオール",
                "mechanism": "ERβ選択的作動 → ホルモン調整"
            }
        }

    def map(self, rf_scores):

        metabolite_scores = {}

        for rf, score in rf_scores.items():
            mets = self.mapping.get(rf, [])

            for m in mets:
                metabolite_scores[m] = metabolite_scores.get(m, 0) + score

        # 正規化
        total = sum(metabolite_scores.values()) or 1

        return {
            m: {
                "score": round(v / total, 3),
                **self.meta_info[m]
            }
            for m, v in metabolite_scores.items()
        }
