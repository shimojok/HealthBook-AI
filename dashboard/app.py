import streamlit as st
import json
import sys
from pathlib import Path

# パス設定
sys.path.append(str(Path(__file__).parent.parent))

from src.inference_engine import HealthBookInferenceEngine
from src.metabolite_mapper import MetaboliteMapper
from src.cascade_connector import CascadeConnector
from src.fhir_exporter import FHIRExporter  # 既存想定

# -----------------------------
# 初期化
# -----------------------------
@st.cache_resource
def load_engine():
    return HealthBookInferenceEngine(
        "data/questionnaire_200_jp.new.json",
        "data/disease_matrix_137.json",
        "data/kampo_metabolic_library.json"
    )

engine = load_engine()
mapper = MetaboliteMapper()
cascade = CascadeConnector()

# -----------------------------
# 言語切替
# -----------------------------
lang = st.sidebar.selectbox("Language / 言語", ["JP", "EN"])

q_file = "data/questionnaire_200_jp.new.json" if lang == "JP" else "data/questionnaire_200_en.new.json"

with open(q_file, "r", encoding="utf-8") as f:
    Q = json.load(f)["questions"]

# -----------------------------
# 問診UI
# -----------------------------
st.title("HealthBook AI Dashboard")

categories = {}
for qid, q in Q.items():
    cat = q.get("category", "Other")
    categories.setdefault(cat, []).append((qid, q))

answers = {}

tabs = st.tabs(list(categories.keys()))

for i, (cat, qs) in enumerate(categories.items()):
    with tabs[i]:
        for qid, q in qs:
            answers[int(qid)] = st.selectbox(
                q["question"],
                [0, 1, 2],
                format_func=lambda x: ["No", "Sometimes", "Often"][x],
                key=f"q_{qid}"
            )

# -----------------------------
# 実行
# -----------------------------
if st.button("Analyze / 分析実行"):

    result = engine.run_engine(answers)

    metabolites = mapper.map(result["risk_factors"])
    cascade_result = cascade.connect(result["mbt55_pathways"])
    fhir = FHIRExporter().build(result)

    # -----------------------------
    # 結果タブ
    # -----------------------------
    tabs = st.tabs([
        "Disease",
        "Kampo",
        "MBT55 Pathway",
        "Metabolites",
        "FHIR"
    ])

    # ① 疾病
    with tabs[0]:
        for d in result["disease_ranking"]:

            highlight = (
                d["disease_id"] in ["D002", "D012"]
            )

            st.write(
                f"{'🔴' if highlight else ''} "
                f"{d['disease_name']} : {round(d['score'],2)}"
            )

    # ② 漢方
    with tabs[1]:
        for k in result["kampo_recommendations"]:
            with st.expander(k["name_en"]):
                st.json(k)

    # ③ PATH
    with tabs[2]:
        st.bar_chart(result["mbt55_pathways"])

    # ④ 代謝
    with tabs[3]:
        st.json(metabolites)

    # ⑤ FHIR
    with tabs[4]:
        st.json(fhir)
