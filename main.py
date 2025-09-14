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

st.set_page_config(
    page_title="AI/ML Proposal Generator",
    page_icon="🤖",
    layout="wide"
)

def create_pdf_report(result_data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    # Define styles
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
        story.append(Paragraph("Company Research", heading_style))
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
        story.append(Paragraph("Market Analysis", heading_style))
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
        story.append(Paragraph("AI/ML Use Cases", heading_style))
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
        
        story.append(Paragraph("Priority Ranking", subheading_style))
        for i, priority in enumerate(uc_data.priority_ranking, 1):
            story.append(Paragraph(f"{i}. {priority}", bullet_style))
        story.append(Spacer(1, 0.2*inch))
    
    
    if "final_proposal" in result_data:
        story.append(PageBreak())
        story.append(Paragraph("Final Proposal", heading_style))
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
            
            if hasattr(puc, 'references') and puc.references:
                story.append(Paragraph("<b>References:</b>", normal_style))
                for ref in puc.references:
                    story.append(Paragraph(f"• {ref}", bullet_style))
            
            story.append(Spacer(1, 0.2*inch))
        
        story.append(Paragraph("Business Case", subheading_style))
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

def display_resources_flexible(resources, resource_type_name):
    if not resources:
        st.info(f"No {resource_type_name} available")
        return
    
    st.markdown(f"**{resource_type_name}:**")
    for resource in resources:
        if isinstance(resource, str):
            st.markdown(f"- [{resource}]({resource})")
        elif isinstance(resource, dict):
            url = resource.get('url', '')
            title = resource.get('title', resource.get('name', 'Resource'))
            description = resource.get('description', '')
            
            if url:
                st.markdown(f"- [{title}]({url})")
                if description:
                    st.markdown(f"  *{description}*")
            else:
                st.markdown(f"- {title}")
        elif hasattr(resource, 'url'):
            title = getattr(resource, 'title', getattr(resource, 'name', 'Resource'))
            url = resource.url
            description = getattr(resource, 'description', '')
            
            st.markdown(f"- [{title}]({url})")
            if description:
                st.markdown(f"  *{description}*")
        else:
            st.markdown(f"- {str(resource)}")

st.title("AI/ML Implementation Proposal Generator")
st.write(
    "This app generates a comprehensive AI/ML Implementation Proposal "
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
    submitted = st.form_submit_button("Generate Proposal")

if submitted and st.session_state.user_prompt.strip():
    with st.spinner("Generating proposal... please wait it will take 3-5 minutes ⌛"):
        try:
            st.session_state.result = workflow.invoke(
                {"user_prompt": st.session_state.user_prompt}
            )
        except Exception as e:
            st.error(f"Workflow execution failed: {str(e)}")
            st.write("Error details:", str(e))
            import traceback
            st.code(traceback.format_exc())
    st.success("Proposal Generated!")

if st.session_state.result:
    result = st.session_state.result

    if "company_research" in result:
        st.subheader("Company Research")
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
        st.subheader("Market Analysis")
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
        st.subheader("AI/ML Use Cases")
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

        st.subheader("Priority Ranking")
        st.markdown("\n".join([f"{i+1}. {p}" for i, p in enumerate(uc_data.priority_ranking)]))

    if "resource_assets" in result:
        st.subheader("Resource Assets")
        ra = result["resource_assets"]

        if hasattr(ra, 'total_resources_found'):
            st.write(f"**Total Resources Found:** {ra.total_resources_found}")
        
        if hasattr(ra, 'platform_summary'):
            ps = ra.platform_summary
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Kaggle", getattr(ps, 'kaggle_count', 0))
            with col2:
                st.metric("HuggingFace", getattr(ps, 'huggingface_count', 0))
            with col3:
                st.metric("GitHub", getattr(ps, 'github_count', 0))
        
        st.write("---")


        if hasattr(ra, 'implementation_roadmap') and ra.implementation_roadmap:
            st.subheader("Implementation Roadmap")
            for phase in ra.implementation_roadmap:
                with st.expander(f"Phase: {phase.phase_name} ({phase.timeline})"):
                    st.markdown(f"**Priority:** {phase.priority}")
                    st.markdown(f"**Use Cases:** {', '.join(phase.use_cases)}")
                    st.markdown(f"**Key Resources:** {', '.join(phase.key_resources)}")

    if "final_proposal" in result:
        st.subheader("Final Proposal")
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

                if hasattr(puc, 'references') and puc.references:
                    st.markdown("**References:**")
                    for ref in puc.references:
                        if isinstance(ref, str):
                            if ref.startswith("title="):
                                try:
                                    import re
                                    title_match = re.search(r"title='([^']*)'", ref)
                                    url_match = re.search(r"url='([^']*)'", ref)
                                    desc_match = re.search(r"description='([^']*)'", ref)
                                    
                                    if title_match and url_match:
                                        title = title_match.group(1)
                                        url = url_match.group(1)
                                        description = desc_match.group(1) if desc_match else ""
                                        
                                        st.markdown(f"- [{title}]({url})")
                                        if description:
                                            st.markdown(f"  *{description}*")
                                    else:
                                        st.markdown(f"- {ref}")
                                except:
                                    st.markdown(f"- {ref}")
                            else:
                                if ref.startswith('http'):
                                    st.markdown(f"- [{ref}]({ref})")
                                else:
                                    st.markdown(f"- {ref}")
                        elif hasattr(ref, 'url') and hasattr(ref, 'title'):
                            title = getattr(ref, 'title', 'Reference')
                            url = getattr(ref, 'url', '')
                            description = getattr(ref, 'description', '')
                            
                            if url:
                                st.markdown(f"- [{title}]({url})")
                                if description:
                                    st.markdown(f"  *{description}*")
                            else:
                                st.markdown(f"- {title}")
                        elif isinstance(ref, dict):
                            title = ref.get('title', 'Reference')
                            url = ref.get('url', '')
                            description = ref.get('description', '')
                            
                            if url:
                                st.markdown(f"- [{title}]({url})")
                                if description:
                                    st.markdown(f"  *{description}*")
                            else:
                                st.markdown(f"- {title}")
                        else:
                            st.markdown(f"- {str(ref)}")

        st.subheader("Business Case")
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
            label="Download Complete Proposal (PDF)",
            data=pdf_buffer.getvalue(),
            file_name=f"AI_ML_Proposal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf"
        )
        
    except Exception as e:
        st.error(f"Error generating PDF: {str(e)}")
        st.write("Error details:", str(e))
        st.write("Falling back to JSON download:")
        st.download_button(
            label="Download Full Report (JSON)",
            data=json.dumps(result, indent=2, default=str),
            file_name="ai_ml_proposal.json",
            mime="application/json"
        )