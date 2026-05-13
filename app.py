import streamlit as st
import plotly.graph_objects as go

from phenotype.phenotype_engine import (
    PhenotypeEngine
)

from recommendation.recommendation_engine import (
    RecommendationEngine
)

from api.disease_engine_api import (
    infer_disease
)

from api.strain_api import (
    recommend_strains
)

from api.metabolic_graph_engine_api import (
    get_path
)


phenotype_engine = PhenotypeEngine(
    "phenotype/questionnaire_pathway_matrix.json"
)

recommendation_engine = RecommendationEngine(
    "recommendation/pathway_food_map.json"
)


st.set_page_config(
    page_title="HealthBook Metabolic OS",
    layout="wide"
)

st.title("HealthBook Metabolic OS")

st.markdown("""
HealthBook is an Ecological Metabolic OS
that models how microbial ecosystems transform
organic matter into human metabolic outcomes.
""")


st.header("Questionnaire Input")

questions = {
    "Q1": "Do you skip breakfast?",
    "Q2": "Do you feel chronic fatigue?",
    "Q3": "Do you have constipation?",
    "Q4": "Do you have sleep problems?",
    "Q5": "Do you consume fermented foods?"
}

answers = {}

for qid, text in questions.items():

    answers[qid] = st.slider(
        text,
        0.0,
        1.0,
        0.5
    )


if st.button("Analyze"):

    scores = phenotype_engine.calculate_scores(
        answers
    )

    st.header("PATHWAY SCORES")

    categories = list(scores.keys())

    values = list(scores.values())

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill='toself'
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )
        ),
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.header("PATHWAY DETAILS")

    for pathway, score in scores.items():

        st.markdown(f"""
        - {pathway}: {score}
        """)

    disease_results = infer_disease(scores)

    st.header("TOP DISEASE RISKS")

    for item in disease_results:

        st.markdown(f"""
        - {item['disease']}
          : {item['risk_score']}
        """)

    low_pathways = []

    for key, value in scores.items():

        if value < 0.5:

            low_pathways.append(key)

    recommendations = recommendation_engine.recommend(
        low_pathways
    )

    st.header("RECOMMENDED SUBSTRATES")

    for item in recommendations:

        st.markdown(f"""
        ## {item['pathway']}

        {", ".join(item['foods'])}
        """)

    strain_results = recommend_strains(
        low_pathways
    )

    st.header("MBT55 STRAIN RECOMMENDATIONS")

    for item in strain_results:

        st.markdown(f"""
        ### {item['strain']}

        - Cluster: {item['cluster']}
        - Pathways: {", ".join(item['matched_pathways'])}
        - Metabolites: {", ".join(item['metabolites'])}
        """)

    st.header("METABOLIC PATH TRACE")

    source = st.text_input(
        "Source Compound",
        "Puerarin"
    )

    target = st.text_input(
        "Target Metabolite",
        "Equol"
    )

    path = get_path(
        source,
        target
    )

    if path:

        st.success(
            " → ".join(path)
        )

    else:

        st.warning(
            "No pathway found"
        )
