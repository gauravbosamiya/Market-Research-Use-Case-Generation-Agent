from langchain_groq import ChatGroq
from dotenv import load_dotenv
from agent.prompts import *
from agent.states import *
from agent.tools import *
from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from datetime import datetime
import tiktoken
import re
import os
from urllib.parse import urlparse


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model="meta-llama/llama-4-maverick-17b-128e-instruct", api_key=api_key)

def count_tokens(text: str, model_name: str = "gpt-3.5-turbo") -> int:
    try:
        encoding = tiktoken.encoding_for_model(model_name)
        return len(encoding.encode(text))
    except:
        return len(text) // 4

def truncate_search_results(search_results: str, max_tokens: int = 1500) -> str:
    if count_tokens(search_results) <= max_tokens:
        return search_results
    
    lines = search_results.split('\n')
    truncated = []
    current_tokens = 0
    
    for line in lines:
        line_tokens = count_tokens(line)
        if current_tokens + line_tokens <= max_tokens:
            truncated.append(line)
            current_tokens += line_tokens
        else:
            break
    
    result = '\n'.join(truncated)
    if len(result) < len(search_results):
        result += "\n[... truncated for token limits ...]"
    
    return result

class ResearchState(TypedDict):
    user_prompt: str
    company_research: CompanyResearch
    market_analysis: MarketAnalysis
    use_cases: UseCases
    resource_assets: ResourceAssets
    final_proposal: FinalProposal

def company_researcher(state: ResearchState):
    user_prompt = state["user_prompt"]
    
    structured_llm = llm.with_structured_output(CompanyResearch)
    
    search_results = tavily_search.invoke(f"{user_prompt} company information")
    
    search_results = truncate_search_results(str(search_results), max_tokens=1000)
    
    prompt = CompanyResearchPrompt().format(
        input=user_prompt,
        search_results=search_results
    )
    
    company_research = structured_llm.invoke(prompt)
    
    return {"company_research": company_research}

def market_analyzer(state: ResearchState):
    company_research = state["company_research"]
    
    structured_llm = llm.with_structured_output(MarketAnalysis)
    
    search_query = f"{company_research.Industry} AI ML automation trends standards 2024 2025"
    search_results = tavily_search.invoke(search_query)
    
    competitor_search = tavily_search.invoke(f"{company_research.Industry} companies AI adoption case studies")
    
    search_results = truncate_search_results(str(search_results), max_tokens=1000)
    competitor_search = truncate_search_results(str(competitor_search), max_tokens=1000)
    
    prompt = MarketAnalysisPrompt().format(
        company=company_research.Company,
        industry=company_research.Industry,
        segment=company_research.Segment,
        search_results=search_results,
        competitor_search=competitor_search
    )
    
    market_analysis = structured_llm.invoke(prompt)
    
    return {"market_analysis": market_analysis}

def use_case_generator(state: ResearchState):
    company_research = state["company_research"]
    market_analysis = state["market_analysis"]
    
    structured_llm = llm.with_structured_output(UseCases)
    
    use_case_search = tavily_search.invoke(
        f"{company_research.Industry} AI ML use cases generative AI LLM applications"
    )
    
    use_case_search = truncate_search_results(str(use_case_search), max_tokens=1000)
    
    prompt = UseCaseGenerationPrompt().format(
        company=company_research.Company,
        industry=company_research.Industry,
        key_offerings=company_research.Key_Offerings,
        strategic_focus=company_research.Strategic_Focus_Areas,
        industry_trends=market_analysis.industry_trends,
        market_opportunities=market_analysis.market_opportunities,
        use_case_search=use_case_search
    )
    
    use_cases = structured_llm.invoke(prompt)
    
    return {"use_cases": use_cases}


def extract_real_urls(search_results: str, platform: str) -> list:
    urls = []
    lines = str(search_results).split('\n')
    
    platform_patterns = {
        'kaggle': r'https://www\.kaggle\.com/[^\s]+',
        'huggingface': r'https://huggingface\.co/[^\s]+',
        'github': r'https://github\.com/[^\s]+'
    }
    
    pattern = platform_patterns.get(platform.lower())
    if not pattern:
        return []
    
    for line in lines:
        found_urls = re.findall(pattern, line)
        for url in found_urls:
            clean_url = re.sub(r'[.,;)]+$', '', url)
            if clean_url not in [u['url'] for u in urls]:
                title = extract_title_from_line(line, clean_url)
                urls.append({
                    'url': clean_url,
                    'title': title,
                    'line_context': line[:200]
                })
    
    return urls[:5] 

def extract_title_from_line(line: str, url: str) -> str:
    line_without_url = line.replace(url, '').strip()

    title_patterns = [
        r'^([^-|•]+)[-|•]', 
        r'"([^"]+)"',        
        r'([A-Z][^.!?]*[.!?])', 
        r'^([^:]+):',        
    ]
    
    for pattern in title_patterns:
        match = re.search(pattern, line_without_url)
        if match:
            title = match.group(1).strip()
            if len(title) > 10 and len(title) < 100: 
                return title
    
    parsed = urlparse(url)
    path_parts = [part for part in parsed.path.split('/') if part]
    if path_parts:
        return path_parts[-1].replace('-', ' ').replace('_', ' ').title()
    
    return f"{parsed.netloc.replace('www.', '').title()} Resource"

def create_resource_description(title: str, platform: str, use_case_category: str) -> str:
    descriptions = {
        'kaggle': {
            'customer_experience': f"Dataset for {title} - Contains data relevant to customer behavior analysis and experience optimization",
            'operations': f"Operational dataset for {title} - Includes data for process optimization and operational efficiency",
            'marketing': f"Marketing dataset for {title} - Contains customer and market data for AI-driven campaigns",
            'default': f"Kaggle dataset: {title} - Structured data for machine learning model training"
        },
        'huggingface': {
            'customer_experience': f"Pre-trained model: {title} - Ready-to-use AI model for customer experience enhancement",
            'operations': f"AI model for {title} - Optimized for operational process automation",
            'marketing': f"Content generation model: {title} - AI model for marketing content creation",
            'default': f"HuggingFace model: {title} - Pre-trained AI/ML model with documentation"
        },
        'github': {
            'customer_experience': f"Implementation repository: {title} - Complete code implementation for customer experience AI solutions",
            'operations': f"Operations AI repository: {title} - Source code and implementation guides for operational AI",
            'marketing': f"Marketing AI toolkit: {title} - Open-source implementation for marketing AI solutions",
            'default': f"GitHub repository: {title} - Complete implementation with documentation and examples"
        }
    }
    
    platform_desc = descriptions.get(platform.lower(), {})
    return platform_desc.get(use_case_category.lower(), platform_desc['default'])

def resource_collector(state: ResearchState):
    use_cases = state["use_cases"]
    company_research = state["company_research"]
    
    structured_llm = llm.with_structured_output(ResourceAssets)
    
    limited_use_cases = use_cases.use_cases[:4]
    
    all_use_case_resources = []
    total_kaggle = 0
    total_huggingface = 0 
    total_github = 0
    
    for use_case in limited_use_cases:
        print(f"Searching resources for: {use_case.title}")
        
        kaggle_query = f"site:kaggle.com {use_case.category} {company_research.Industry} dataset {use_case.ai_ml_solution}"
        huggingface_query = f"site:huggingface.co {use_case.ai_ml_solution} {use_case.category} model"
        github_query = f"site:github.com {use_case.ai_ml_solution} {use_case.category} {company_research.Industry}"
        
        kaggle_results = tavily_search.invoke(kaggle_query)
        huggingface_results = tavily_search.invoke(huggingface_query)
        github_results = tavily_search.invoke(github_query)
        
        kaggle_urls = extract_real_urls(kaggle_results, 'kaggle')
        huggingface_urls = extract_real_urls(huggingface_results, 'huggingface')
        github_urls = extract_real_urls(github_results, 'github')
        
        kaggle_resources = []
        for url_data in kaggle_urls:
            kaggle_resources.append(ResourceLink(
                title=url_data['title'],
                url=url_data['url'],
                description=create_resource_description(url_data['title'], 'kaggle', use_case.category)
            ))
        
        huggingface_resources = []
        for url_data in huggingface_urls:
            huggingface_resources.append(ResourceLink(
                title=url_data['title'],
                url=url_data['url'],
                description=create_resource_description(url_data['title'], 'huggingface', use_case.category)
            ))
        
        github_resources = []
        for url_data in github_urls:
            github_resources.append(ResourceLink(
                title=url_data['title'],
                url=url_data['url'],
                description=create_resource_description(url_data['title'], 'github', use_case.category)
            ))
        
        use_case_resource = UseCaseResource(
            use_case_title=use_case.title,
            category=use_case.category,
            technology_focus=use_case.ai_ml_solution,
            kaggle_datasets=kaggle_resources,
            huggingface_resources=huggingface_resources,
            github_repositories=github_resources,
            additional_resources=[] 
        )
        
        all_use_case_resources.append(use_case_resource)
        
        total_kaggle += len(kaggle_resources)
        total_huggingface += len(huggingface_resources)
        total_github += len(github_resources)
        
        print(f"Found: {len(kaggle_resources)} Kaggle, {len(huggingface_resources)} HuggingFace, {len(github_resources)} GitHub")
    
    platform_summary = PlatformSummary(
        kaggle_count=total_kaggle,
        huggingface_count=total_huggingface,
        github_count=total_github,
        kaggle_recommendations=[f"{res.kaggle_datasets[0].title}" for res in all_use_case_resources if res.kaggle_datasets][:5],
        huggingface_recommendations=[f"{res.huggingface_resources[0].title}" for res in all_use_case_resources if res.huggingface_resources][:5],
        github_recommendations=[f"{res.github_repositories[0].title}" for res in all_use_case_resources if res.github_repositories][:5]
    )
    
    implementation_phases = [
        ImplementationPhase(
            phase_name="Quick Wins & Proof of Concept",
            timeline="6-12 weeks",
            priority="High",
            use_cases=[uc.title for uc in limited_use_cases[:2]],
            key_resources=["Data preparation", "Model selection", "Initial training"]
        ),
        ImplementationPhase(
            phase_name="Core Implementation",
            timeline="3-6 months", 
            priority="High",
            use_cases=[uc.title for uc in limited_use_cases[2:4]],
            key_resources=["Full model development", "Integration", "Testing"]
        ),
        ImplementationPhase(
            phase_name="Advanced Features & Scale",
            timeline="6-12 months",
            priority="Medium",
            use_cases=["Advanced analytics", "Performance optimization"],
            key_resources=["Optimization", "Monitoring", "Scaling infrastructure"]
        )
    ]
    
    resource_assets = ResourceAssets(
        use_case_resources=all_use_case_resources,
        platform_summary=platform_summary,
        implementation_roadmap=implementation_phases,
        total_resources_found=total_kaggle + total_huggingface + total_github
    )
    
    return {"resource_assets": resource_assets}


def final_proposal_generator(state: ResearchState):
    company_research = state["company_research"]
    market_analysis = state["market_analysis"]
    use_cases = state["use_cases"]
    resource_assets = state["resource_assets"]
    
    structured_llm = llm.with_structured_output(FinalProposal)
    
    business_case_search = tavily_search.invoke(
        f"{company_research.Industry} AI ROI business case implementation costs"
    )
    business_case_search = truncate_search_results(str(business_case_search), max_tokens=800)
    
    detailed_use_cases = []
    for i, use_case in enumerate(use_cases.use_cases[:5]):
        resource_data = None
        for uc_resource in resource_assets.use_case_resources:
            if uc_resource.use_case_title == use_case.title:
                resource_data = uc_resource
                break
        
        references = []
        if resource_data:
            for dataset in resource_data.kaggle_datasets[:2]: 
                references.append(ResourceLink(
                    title=dataset.title,
                    url=dataset.url,
                    description=dataset.description
                ))
            
            for hf_resource in resource_data.huggingface_resources[:2]:
                references.append(ResourceLink(
                    title=hf_resource.title,
                    url=hf_resource.url,
                    description=hf_resource.description
                ))
            
            for repo in resource_data.github_repositories[:2]:
                references.append(ResourceLink(
                    title=repo.title,
                    url=repo.url,
                    description=repo.description
                ))
        
        priority_level = "High" if i < 2 else "Medium" if i < 4 else "Low"
        timeline_map = {"High": "8-12 weeks", "Medium": "12-16 weeks", "Low": "16-24 weeks"}
        investment_map = {"High": "$300,000-500,000", "Medium": "$500,000-800,000", "Low": "$800,000-1,200,000"}
        roi_map = {"High": "25-40%", "Medium": "20-30%", "Low": "15-25%"}
        
        detailed_use_case = {
            "title": use_case.title,
            "category": use_case.category,
            "priority": priority_level,
            "timeline": timeline_map[priority_level],
            "investment_estimate": investment_map[priority_level],
            "expected_roi": roi_map[priority_level],
            "problem_statement": use_case.problem_statement,
            "solution_approach": use_case.ai_ml_solution,
            "benefits": use_case.expected_benefits,
            "success_metrics": [
                f"Improvement in {use_case.category.lower()} metrics by 20-40%",
                "User adoption rate > 80%",
                "ROI achievement within projected timeline"
            ],
            "risk_factors": [
                "Data quality and availability",
                "Integration complexity with existing systems", 
                "User adoption challenges",
                f"Technical complexity: {use_case.implementation_complexity}"
            ],
            "references": references,
            "resource_count": len(references)
        }
        detailed_use_cases.append(detailed_use_case)
    
    use_case_summaries = []
    for uc in detailed_use_cases:
        summary = f"""
        USE CASE: {uc['title']}
        Category: {uc['category']}
        Priority: {uc['priority']}
        Problem: {uc['problem_statement'][:150]}...
        Solution: {uc['solution_approach'][:150]}...
        Benefits: {', '.join(uc['benefits'][:3])}
        Resources Found: {uc['resource_count']} (Kaggle datasets, HuggingFace models, GitHub repos)
        Investment: {uc['investment_estimate']}
        Expected ROI: {uc['expected_roi']}
        Timeline: {uc['timeline']}
        """
        use_case_summaries.append(summary)
    
    enhanced_prompt = f"""
    You are creating a comprehensive AI/ML implementation proposal for {company_research.Company}.
    
    COMPANY CONTEXT:
    Company: {company_research.Company}
    Industry: {company_research.Industry}
    Key Offerings: {', '.join(company_research.Key_Offerings[:3])}
    Strategic Focus: {', '.join(company_research.Strategic_Focus_Areas[:3])}
    Vision: {company_research.Vision[:300]}
    
    MARKET INTELLIGENCE:
    Industry Trends: {', '.join(market_analysis.industry_trends[:4])}
    Market Opportunities: {', '.join(market_analysis.market_opportunities[:4])}
    Competitive Landscape: {', '.join(market_analysis.competitor_analysis[:3])}
    
    DETAILED USE CASES WITH RESOURCES:
    {chr(10).join(use_case_summaries)}
    
    RESOURCE AVAILABILITY:
    Total Resources Found: {resource_assets.total_resources_found}
    - Kaggle Datasets: {resource_assets.platform_summary.kaggle_count}
    - HuggingFace Models: {resource_assets.platform_summary.huggingface_count}
    - GitHub Repositories: {resource_assets.platform_summary.github_count}
    
    IMPLEMENTATION ROADMAP:
    Phase 1 (Quick Wins): {resource_assets.implementation_roadmap[0].timeline}
    Phase 2 (Core Implementation): {resource_assets.implementation_roadmap[1].timeline}
    Phase 3 (Advanced Features): {resource_assets.implementation_roadmap[2].timeline}
    
    BUSINESS RESEARCH:
    {business_case_search[:800]}
    
    Create a comprehensive final proposal with:
    1. Executive summary highlighting key opportunities
    2. Top 5 use cases with detailed implementation plans
    3. 3-phase implementation roadmap with specific deliverables
    4. Business case with realistic ROI projections
    5. Strategic alignment with company goals
    6. Next steps with clear ownership and timelines
    
    Focus on practical, implementable solutions backed by available resources.
    """
    
    final_proposal = structured_llm.invoke(enhanced_prompt)
    
    if hasattr(final_proposal, 'top_use_cases'):
        for i, proposed_uc in enumerate(final_proposal.top_use_cases):
            if i < len(detailed_use_cases):
                proposed_uc.references = detailed_use_cases[i]['references']
    
    return {"final_proposal": final_proposal}


# ---------------------------------------------------------------------------------

graph = StateGraph(ResearchState)

graph.add_node("company_researcher", company_researcher)
graph.add_node("market_analyzer", market_analyzer)
graph.add_node("use_case_generator", use_case_generator)
graph.add_node("resource_collector", resource_collector)
graph.add_node("final_proposal_generator", final_proposal_generator)

graph.add_edge(START, "company_researcher")
graph.add_edge("company_researcher", "market_analyzer")
graph.add_edge("market_analyzer", "use_case_generator")
graph.add_edge("use_case_generator", "resource_collector")
graph.add_edge("resource_collector", "final_proposal_generator")
graph.add_edge("final_proposal_generator", END) 

workflow = graph.compile()
