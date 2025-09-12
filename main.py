import streamlit as st
import json
from agent.graph import workflow
from agent.states import FinalProposal, ResourceAssets

# ---------------------------
# Streamlit Config
# ---------------------------
st.set_page_config(
    page_title="AI/ML Proposal Generator",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI/ML Implementation Proposal Generator")
st.write(
    "This app generates a **comprehensive AI/ML Implementation Proposal** "
    "with company research, market analysis, use cases, resource links, and next steps."
)

# ---------------------------
# Session State
# ---------------------------
if "result" not in st.session_state:
    st.session_state.result = None
if "user_prompt" not in st.session_state:
    st.session_state.user_prompt = ""

# ---------------------------
# User Input
# ---------------------------
with st.form("proposal_form"):
    st.session_state.user_prompt = st.text_input(
        "Enter company or industry details:",
        st.session_state.user_prompt,
        placeholder="Example: Tesla industry, key offerings, and strategic focus areas"
    )
    submitted = st.form_submit_button("🔍 Generate Proposal")

# ---------------------------
# Run Workflow
# ---------------------------
if submitted and st.session_state.user_prompt.strip():
    with st.spinner("Generating proposal... please wait ⏳"):
        st.session_state.result = workflow.invoke(
            {"user_prompt": st.session_state.user_prompt}
        )
    st.success("✅ Proposal Generated!")

# ---------------------------
# Display Results
# ---------------------------
if st.session_state.result:
    result = st.session_state.result

    # Debug Raw Output
    with st.expander("🔍 Debug: Raw Output"):
        st.json(result)

    # ---------------------------
    # Company Research
    # ---------------------------
    if "company_research" in result:
        st.subheader("🏢 Company Research")
        cr = result["company_research"]
        st.markdown(f"""
        - **Company**: {cr.Company}  
        - **Industry**: {cr.Industry}  
        - **Segment**: {cr.Segment}  
        - **Key Offerings**: {", ".join(cr.Key_Offerings) if cr.Key_Offerings else "N/A"}  
        - **Strategic Focus Areas**: {", ".join(cr.Strategic_Focus_Areas) if cr.Strategic_Focus_Areas else "N/A"}  
        - **Vision**: {cr.Vision or "N/A"}  
        """)

    # ---------------------------
    # Market Analysis
    # ---------------------------
    if "market_analysis" in result:
        st.subheader("📈 Market Analysis")
        ma = result["market_analysis"]

        st.write("**Industry Trends**")
        st.markdown("\n".join([f"- {t}" for t in ma.industry_trends]))

        st.write("**Industry Standards**")
        st.markdown("\n".join([f"- {s}" for s in ma.industry_standards]))

        st.write("**Competitor Analysis**")
        st.markdown("\n".join([f"- {c}" for c in ma.competitor_analysis]))

        st.write("**Market Opportunities**")
        st.markdown("\n".join([f"- {o}" for o in ma.market_opportunities]))

    # ---------------------------
    # Use Cases
    # ---------------------------
    if "use_cases" in result:
        st.subheader("💡 AI/ML Use Cases")
        uc_data = result["use_cases"]

        for i, uc in enumerate(uc_data.use_cases, 1):
            with st.expander(f"{i}. {uc.title} ({uc.category}, Complexity: {uc.implementation_complexity})"):
                benefits_text = "\n".join([f"- {b}" for b in uc.expected_benefits])
                st.markdown(f"""
                **Problem:** {uc.problem_statement}  
                **Solution:** {uc.ai_ml_solution}  

                **Expected Benefits:**  
                {benefits_text}
                """)

        st.subheader("🏆 Priority Ranking")
        st.markdown("\n".join([f"{i+1}. {p}" for i, p in enumerate(uc_data.priority_ranking)]))

    # ---------------------------
    # Resource Assets
    # ---------------------------
    if "resource_assets" in result:
        st.subheader("🔗 Resource Assets")
        ra: ResourceAssets = result["resource_assets"]

        for res in ra.use_case_resources:
            with st.expander(f"{res.use_case_title} ({res.category})"):
                st.markdown(f"**Focus:** {res.technology_focus}")
                if res.kaggle_datasets:
                    st.markdown("**Kaggle Datasets:** " + " | ".join([f"[{k}]({k})" for k in res.kaggle_datasets]))
                if res.huggingface_resources:
                    st.markdown("**HuggingFace Models:** " + " | ".join([f"[{h}]({h})" for h in res.huggingface_resources]))
                if res.github_repositories:
                    st.markdown("**GitHub Repos:** " + " | ".join([f"[{g}]({g})" for g in res.github_repositories]))
                if res.additional_resources:
                    st.markdown("**Additional Resources:** " + " | ".join([f"[{a}]({a})" for a in res.additional_resources]))

    # ---------------------------
    # Final Proposal
    # ---------------------------
    if "final_proposal" in result:
        st.subheader("📑 Final Proposal")
        fp = result["final_proposal"]

        st.markdown(f"**Executive Summary:** {fp.executive_summary}")

        # Show proposed use cases with references
        for puc in fp.top_use_cases:
            with st.expander(f"{puc.title} ({puc.category}, Priority: {puc.priority})"):
                benefits = "\n".join([f"- {b}" for b in puc.benefits])
                risks = "\n".join([f"- {r}" for r in puc.risk_factors])
                st.markdown(f"""
                **Problem:** {puc.problem_statement}  
                **Solution:** {puc.solution_approach}  
                - **Timeline:** {puc.timeline}  
                - **Investment:** {puc.investment_estimate}  
                - **Expected ROI:** {puc.expected_roi}  

                **Benefits:**  
                {benefits}

                **Risks:**  
                {risks}
                """)

                if puc.references:
                    st.markdown("**References:** " + " | ".join([f"[{r}]({r})" for r in puc.references]))

        # Business case summary
        st.subheader("📊 Business Case")
        bc = fp.business_case
        st.markdown(f"""
        - **Total Investment**: {bc.total_investment}  
        - **Expected ROI**: {bc.expected_roi}  
        - **Payback Period**: {bc.payback_period}  
        - **Risk Assessment**: {bc.risk_assessment}  
        """)

    # ---------------------------
    # Download Proposal
    # ---------------------------
    st.download_button(
        label="⬇️ Download Full Report (JSON)",
        data=json.dumps(result, indent=2, default=str),
        file_name="ai_ml_proposal.json",
        mime="application/json"
    )
