import streamlit as st
import json
from agent.graph import workflow
from agent.states import FinalProposal, ResourceAssets
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.colors import HexColor, black, blue
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from io import BytesIO
from datetime import datetime
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()
def get_api_key():
    try:
        return st.secrets["GROQ_API_KEY"]
    except (KeyError, FileNotFoundError):
        pass
    
    api_key = os.getenv("GROQ_API_KEY")
    if api_key:
        return api_key
    
    st.error("GROQ_API_KEY not configured!")
    st.stop()

api_key = get_api_key()
llm = ChatGroq(
    model="meta-llama/llama-4-maverick-17b-128e-instruct",
    api_key=api_key
)

st.set_page_config(
    page_title="AI/ML Proposal Generator",
    page_icon="🤖",
    layout="wide"
)

def create_pdf_report(result_data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=HexColor('#2E86AB')
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        spaceBefore=20,
        textColor=HexColor('#2E86AB')
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=14,
        spaceAfter=8,
        spaceBefore=12,
        textColor=HexColor('#A23B72')
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,
        alignment=TA_JUSTIFY
    )
    
    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=styles['Normal'],
        fontSize=10,
        leftIndent=20,
        spaceAfter=4
    )
    
    story = []
    
    story.append(Paragraph("AI/ML Implementation Proposal", title_style))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y')}", normal_style))
    story.append(PageBreak())
    
    if "company_research" in result_data:
        story.append(Paragraph("🏢 Company Research", heading_style))
        cr = result_data["company_research"]
        
        company_data = [
            ['Field', 'Information'],
            ['Company', cr.Company or 'N/A'],
            ['Industry', cr.Industry or 'N/A'],
            ['Segment', cr.Segment or 'N/A'],
            ['Key Offerings', ', '.join(cr.Key_Offerings) if cr.Key_Offerings else 'N/A'],
            ['Strategic Focus Areas', ', '.join(cr.Strategic_Focus_Areas) if cr.Strategic_Focus_Areas else 'N/A'],
            ['Vision', cr.Vision or 'N/A']
        ]
        
        company_table = Table(company_data, colWidths=[2*inch, 4*inch])
        company_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2E86AB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#F8F9FA')),
            ('GRID', (0, 0), (-1, -1), 1, black)
        ]))
        
        story.append(company_table)
        story.append(Spacer(1, 0.3*inch))
    
    if "market_analysis" in result_data:
        story.append(Paragraph("📈 Market Analysis", heading_style))
        ma = result_data["market_analysis"]
        
        story.append(Paragraph("Industry Trends", subheading_style))
        for trend in ma.industry_trends:
            story.append(Paragraph(f"• {trend}", bullet_style))
        story.append(Spacer(1, 0.1*inch))
        
        story.append(Paragraph("Industry Standards", subheading_style))
        for standard in ma.industry_standards:
            story.append(Paragraph(f"• {standard}", bullet_style))
        story.append(Spacer(1, 0.1*inch))
        
        story.append(Paragraph("Competitor Analysis", subheading_style))
        for competitor in ma.competitor_analysis:
            story.append(Paragraph(f"• {competitor}", bullet_style))
        story.append(Spacer(1, 0.1*inch))
        
        story.append(Paragraph("Market Opportunities", subheading_style))
        for opportunity in ma.market_opportunities:
            story.append(Paragraph(f"• {opportunity}", bullet_style))
        story.append(Spacer(1, 0.2*inch))
    
    if "use_cases" in result_data:
        story.append(Paragraph("💡 AI/ML Use Cases", heading_style))
        uc_data = result_data["use_cases"]
        
        for i, uc in enumerate(uc_data.use_cases, 1):
            story.append(Paragraph(f"{i}. {uc.title}", subheading_style))
            story.append(Paragraph(f"<b>Category:</b> {uc.category} | <b>Complexity:</b> {uc.implementation_complexity}", normal_style))
            story.append(Paragraph(f"<b>Problem:</b> {uc.problem_statement}", normal_style))
            story.append(Paragraph(f"<b>Solution:</b> {uc.ai_ml_solution}", normal_style))
            
            story.append(Paragraph("<b>Expected Benefits:</b>", normal_style))
            for benefit in uc.expected_benefits:
                story.append(Paragraph(f"• {benefit}", bullet_style))
            story.append(Spacer(1, 0.15*inch))
        
        story.append(Paragraph("🏆 Priority Ranking", subheading_style))
        for i, priority in enumerate(uc_data.priority_ranking, 1):
            story.append(Paragraph(f"{i}. {priority}", bullet_style))
        story.append(Spacer(1, 0.2*inch))
    
    if "resource_assets" in result_data:
        story.append(Paragraph("🔗 Resource Assets", heading_style))
        ra = result_data["resource_assets"]
        
        for res in ra.use_case_resources:
            story.append(Paragraph(f"{res.use_case_title} ({res.category})", subheading_style))
            story.append(Paragraph(f"<b>Technology Focus:</b> {res.technology_focus}", normal_style))
            
            if res.kaggle_datasets:
                story.append(Paragraph("<b>Kaggle Datasets:</b>", normal_style))
                for dataset in res.kaggle_datasets:
                    story.append(Paragraph(f"• {dataset}", bullet_style))
            
            if res.huggingface_resources:
                story.append(Paragraph("<b>HuggingFace Resources:</b>", normal_style))
                for resource in res.huggingface_resources:
                    story.append(Paragraph(f"• {resource}", bullet_style))
            
            if res.github_repositories:
                story.append(Paragraph("<b>GitHub Repositories:</b>", normal_style))
                for repo in res.github_repositories:
                    story.append(Paragraph(f"• {repo}", bullet_style))
            
            if res.additional_resources:
                story.append(Paragraph("<b>Additional Resources:</b>", normal_style))
                for additional in res.additional_resources:
                    story.append(Paragraph(f"• {additional}", bullet_style))
            
            story.append(Spacer(1, 0.15*inch))
    
    if "final_proposal" in result_data:
        story.append(PageBreak())
        story.append(Paragraph("📋 Final Proposal", heading_style))
        fp = result_data["final_proposal"]
        
        story.append(Paragraph("Executive Summary", subheading_style))
        story.append(Paragraph(fp.executive_summary, normal_style))
        story.append(Spacer(1, 0.2*inch))
        
        story.append(Paragraph("Top Use Cases", subheading_style))
        for puc in fp.top_use_cases:
            story.append(Paragraph(f"<b>{puc.title}</b> ({puc.category}, Priority: {puc.priority})", subheading_style))
            story.append(Paragraph(f"<b>Problem:</b> {puc.problem_statement}", normal_style))
            story.append(Paragraph(f"<b>Solution:</b> {puc.solution_approach}", normal_style))
            story.append(Paragraph(f"<b>Timeline:</b> {puc.timeline}", normal_style))
            story.append(Paragraph(f"<b>Investment:</b> {puc.investment_estimate}", normal_style))
            story.append(Paragraph(f"<b>Expected ROI:</b> {puc.expected_roi}", normal_style))
            
            story.append(Paragraph("<b>Benefits:</b>", normal_style))
            for benefit in puc.benefits:
                story.append(Paragraph(f"• {benefit}", bullet_style))
            
            story.append(Paragraph("<b>Risk Factors:</b>", normal_style))
            for risk in puc.risk_factors:
                story.append(Paragraph(f"• {risk}", bullet_style))
            
            if puc.references:
                story.append(Paragraph("<b>References:</b>", normal_style))
                for ref in puc.references:
                    story.append(Paragraph(f"• {ref}", bullet_style))
            
            story.append(Spacer(1, 0.2*inch))
        
        story.append(Paragraph("📊 Business Case", subheading_style))
        bc = fp.business_case
        
        business_data = [
            ['Metric', 'Value'],
            ['Total Investment', bc.total_investment],
            ['Expected ROI', bc.expected_roi],
            ['Payback Period', bc.payback_period],
            ['Risk Assessment', bc.risk_assessment]
        ]
        
        business_table = Table(business_data, colWidths=[2.5*inch, 3.5*inch])
        business_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#A23B72')),
            ('TEXTCOLOR', (0, 0), (-1, 0), black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#F8F9FA')),
            ('GRID', (0, 0), (-1, -1), 1, black)
        ]))
        
        story.append(business_table)
    
    doc.build(story)
    buffer.seek(0)
    return buffer

st.title("🤖 AI/ML Implementation Proposal Generator")
st.write(
    "This app generates a **comprehensive AI/ML Implementation Proposal** "
    "with company research, market analysis, use cases, resource links, and next steps."
)

if "result" not in st.session_state:
    st.session_state.result = None
if "user_prompt" not in st.session_state:
    st.session_state.user_prompt = ""

with st.form("proposal_form"):
    st.session_state.user_prompt = st.text_input(
        "Enter company or industry details:",
        st.session_state.user_prompt,
        placeholder="Example: Tesla industry, key offerings, and strategic focus areas"
    )
    submitted = st.form_submit_button("🔍 Generate Proposal")

if submitted and st.session_state.user_prompt.strip():
    with st.spinner("Generating proposal... please wait it will take 3-5 minutes⏳"):
        st.session_state.result = workflow.invoke(
            {"user_prompt": st.session_state.user_prompt}
        )
    st.success("✅ Proposal Generated!")

if st.session_state.result:
    result = st.session_state.result

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

    if "final_proposal" in result:
        st.subheader("📋 Final Proposal")
        fp = result["final_proposal"]

        st.markdown(f"**Executive Summary:** {fp.executive_summary}")

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

        st.subheader("📊 Business Case")
        bc = fp.business_case
        st.markdown(f"""
        - **Total Investment**: {bc.total_investment}  
        - **Expected ROI**: {bc.expected_roi}  
        - **Payback Period**: {bc.payback_period}  
        - **Risk Assessment**: {bc.risk_assessment}  
        """)

    try:
        pdf_buffer = create_pdf_report(result)
        
        st.download_button(
            label="📄 Download Complete Proposal (PDF)",
            data=pdf_buffer.getvalue(),
            file_name=f"AI_ML_Proposal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf"
        )
            
    except Exception as e:
        st.error(f"Error generating PDF: {str(e)}")
        st.write("Falling back to JSON download:")
        st.download_button(
            label="⬇️ Download Full Report (JSON)",
            data=json.dumps(result, indent=2, default=str),
            file_name="ai_ml_proposal.json",
            mime="application/json"
        )
        
      
# AI Planet industry, key offerings, and strategic focus areas