import streamlit as st
import plotly.graph_objects as go

from phenotype.phenotype_engine import (
    PhenotypeEngine
)

from api.disease_engine_api import (
    infer_disease
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


phenotype_engine = PhenotypeEngine(
    "phenotype/questionnaire_pathway_matrix.json"
)


st.header("Questionnaire Input")

questions = {
    "Q001": "Do you skip breakfast frequently?",
    "Q002": "Do you suffer from constipation?",
    "Q003": "Do you experience bloating after meals?",
    "Q004": "Do you have sleep disturbances?",
    "Q005": "Do you often feel fatigue?"
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

    if len(scores) == 0:

        st.error(
            "No pathway scores generated"
        )

        st.stop()

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

    st.header("DISEASE RISKS")

    disease_results = infer_disease(
        scores
    )

    if len(disease_results) == 0:

        st.success(
            "No major disease risks detected"
        )

    else:

        for item in disease_results:

            st.markdown(f"""
            - {item['disease']}
              : {item['risk_score']}
            """)
