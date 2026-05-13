import streamlit as st

from phenotype.phenotype_engine import PhenotypeEngine
from recommendation.recommendation_engine import RecommendationEngine


st.set_page_config(
    page_title="HealthBook Metabolic OS",
    layout="wide"
)

st.title("HealthBook Metabolic OS")

st.markdown(
    """
    Ecological Metabolic Intelligence Platform
    """
)

answers = {
    "Q001": st.slider("Skip breakfast", 0.0, 1.0, 0.5),
    "Q002": st.slider("Constipation", 0.0, 1.0, 0.5),
    "Q003": st.slider("Bloating", 0.0, 1.0, 0.5),
    "Q004": st.slider("Sleep disturbance", 0.0, 1.0, 0.5),
    "Q005": st.slider("Fatigue", 0.0, 1.0, 0.5),
}

phenotype_engine = PhenotypeEngine(
    "phenotype/questionnaire_pathway_matrix.json"
)

scores = phenotype_engine.calculate_scores(answers)

st.subheader("PATHWAY SCORES")

st.json(scores)

recommendation_engine = RecommendationEngine(
    "graphs/substrate_metabolite_graph.json"
)

recommendations = recommendation_engine.generate_recommendations(
    scores
)

st.subheader("RECOMMENDATIONS")

for rec in recommendations:

    st.markdown(f"""
    ### {rec['substrate']}

    - Pathway: {rec['pathway']}
    - MBT Cluster: {rec['cluster']}
    - Intermediate: {rec['intermediate']}
    - Final Metabolite: {rec['metabolite']}
    - Expected Effect: {rec['effect']}
    """)
