class CascadeConnector:

    def __init__(self):

        # PATH → カスケード寄与
        self.cascade_map = {
            "PATH_01": {"stage1": 0.6, "stage2": 0.2, "stage3": 0.2},
            "PATH_02": {"stage1": 0.3, "stage2": 0.5, "stage3": 0.2},
            "PATH_03": {"stage1": 0.2, "stage2": 0.3, "stage3": 0.5},
            "PATH_04": {"stage1": 0.4, "stage2": 0.3, "stage3": 0.3},
            "PATH_05": {"stage1": 0.2, "stage2": 0.4, "stage3": 0.4}
        }

        self.stage_meaning = {
            "stage1": "加水分解（0-6h）糖鎖・タンパク分解",
            "stage2": "変換（6-24h）アグリコン化",
            "stage3": "再合成（24-72h）シグナル分子生成"
        }

    def connect(self, pathway_scores):

        result = {}

        for path, score in pathway_scores.items():

            cascade = self.cascade_map.get(path, {})

            result[path] = {
                stage: round(score * weight, 3)
                for stage, weight in cascade.items()
            }

        return {
            "cascade_scores": result,
            "stage_meaning": self.stage_meaning
        }
