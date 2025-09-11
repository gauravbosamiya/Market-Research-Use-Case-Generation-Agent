import streamlit as st
from agent.graph import workflow, print_results

from agent.states import CompanyResearch, MarketAnalysis, UseCases
from agent.prompts import *

# ---------------------------
# Streamlit App
# ---------------------------
st.set_page_config(
    page_title="AI Use Case Generator",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Use Case Generation Agent")
st.write(
    "This tool performs **company research**, analyzes **market trends**, and "
    "generates **AI/ML use cases** using LangGraph."
)

# ---------------------------
# Session State Initialization
# ---------------------------
if "result" not in st.session_state:
    st.session_state.result = None
if "user_prompt" not in st.session_state:
    st.session_state.user_prompt = ""

# ---------------------------
# User Input
# ---------------------------
with st.form("research_form"):
    st.session_state.user_prompt = st.text_input(
        "Enter company or industry details:",
        st.session_state.user_prompt,
        placeholder="Example: Tesla industry, key offerings, and strategic focus areas"
    )
    submitted = st.form_submit_button("🔍 Run Analysis")

# ---------------------------
# Run Workflow
# ---------------------------
if submitted and st.session_state.user_prompt.strip():
    with st.spinner("Running workflow... please wait ⏳"):
        st.session_state.result = workflow.invoke(
            {"user_prompt": st.session_state.user_prompt}
        )
    st.success("✅ Workflow completed!")

# ---------------------------
# Display Results
# ---------------------------
if st.session_state.result:
    result = st.session_state.result

    st.subheader("📊 Company Research")
    company: CompanyResearch = result["company_research"]
    st.markdown(f"""
    - **Company**: {company.Company}  
    - **Industry**: {company.Industry}  
    - **Segment**: {company.Segment}  
    - **Key Offerings**: {", ".join(company.Key_Offerings)}  
    - **Strategic Focus Areas**: {", ".join(company.Strategic_Focus_Areas)}  
    - **Vision**: {company.Vision}  
    """)

    st.subheader("📈 Market Analysis")
    market: MarketAnalysis = result["market_analysis"]
    st.write("**Industry Trends**")
    st.write("\n".join([f"• {t}" for t in market.industry_trends]))

    st.write("**Industry Standards**")
    st.write("\n".join([f"• {s}" for s in market.industry_standards]))

    st.write("**Competitor Analysis**")
    st.write("\n".join([f"• {c}" for c in market.competitor_analysis]))

    st.write("**Market Opportunities**")
    st.write("\n".join([f"• {o}" for o in market.market_opportunities]))

    st.subheader("💡 Generated Use Cases")
    use_cases: UseCases = result["use_cases"]
    for i, use_case in enumerate(use_cases.use_cases, 1):
        with st.expander(f"{i}. {use_case.title}"):
            st.markdown(f"""
            - **Category**: {use_case.category}  
            - **Problem**: {use_case.problem_statement}  
            - **Solution**: {use_case.ai_ml_solution}  
            - **Complexity**: {use_case.implementation_complexity}  
            - **Expected Benefits**:  
              {chr(10).join([f"- {b}" for b in use_case.expected_benefits])}
            """)

    st.subheader("🏆 Priority Ranking")
    st.write("\n".join([f"{i+1}. {p}" for i, p in enumerate(use_cases.priority_ranking)]))
