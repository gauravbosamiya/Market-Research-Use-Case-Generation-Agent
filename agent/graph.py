from langchain_groq import ChatGroq
from dotenv import load_dotenv
from agent.prompts import *
from agent.states import *
from agent.tools import *

from langgraph.graph import StateGraph, START, END
from typing import TypedDict

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile")

# Extended State for both tasks
class ExtendedResearchState(TypedDict):
    user_prompt: str
    company_research: CompanyResearch
    market_analysis: MarketAnalysis
    use_cases: UseCases

def company_researcher(state: ExtendedResearchState):
    """Task 1: Research the Industry or Company"""
    user_prompt = state["user_prompt"]
    
    structured_llm = llm.with_structured_output(CompanyResearch)
    
    search_results = tavily_search.invoke(f"{user_prompt} company information")
    
    # Fixed: Call the function to get PromptTemplate
    prompt = CompanyResearchPrompt().format(
        input=user_prompt,
        search_results=search_results
    )
    
    company_research = structured_llm.invoke(prompt)
    
    return {"company_research": company_research}

def market_analyzer(state: ExtendedResearchState):
    """Task 2a: Analyze Market Standards and Industry Trends"""
    company_research = state["company_research"]
    
    structured_llm = llm.with_structured_output(MarketAnalysis)
    
    # Search for industry-specific AI trends and standards
    search_query = f"{company_research.Industry} AI ML automation trends standards 2024 2025"
    search_results = tavily_search.invoke(search_query)
    
    # Additional search for competitor analysis
    competitor_search = tavily_search.invoke(f"{company_research.Industry} companies AI adoption case studies")
    
    # Fixed: Call the function to get PromptTemplate
    prompt = MarketAnalysisPrompt().format(
        company=company_research.Company,
        industry=company_research.Industry,
        segment=company_research.Segment,
        search_results=search_results,
        competitor_search=competitor_search
    )
    
    market_analysis = structured_llm.invoke(prompt)
    
    return {"market_analysis": market_analysis}

def use_case_generator(state: ExtendedResearchState):
    """Task 2b: Generate AI/ML Use Cases"""
    company_research = state["company_research"]
    market_analysis = state["market_analysis"]
    
    structured_llm = llm.with_structured_output(UseCases)
    
    # Search for specific use cases in the industry
    use_case_search = tavily_search.invoke(
        f"{company_research.Industry} AI ML use cases generative AI LLM applications"
    )
    
    # Fixed: Call the function to get PromptTemplate
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

# Create the extended workflow graph
graph = StateGraph(ExtendedResearchState)

# Add nodes for all tasks
graph.add_node("company_researcher", company_researcher)
graph.add_node("market_analyzer", market_analyzer)
graph.add_node("use_case_generator", use_case_generator)

# Define the workflow edges
graph.add_edge(START, "company_researcher")
graph.add_edge("company_researcher", "market_analyzer")
graph.add_edge("market_analyzer", "use_case_generator")
graph.add_edge("use_case_generator", END)

# Compile and run the workflow
workflow = graph.compile()

# def print_results(result):
#     print("=" * 80)
#     print("COMPREHENSIVE AI USE CASE GENERATION REPORT")
#     print("=" * 80)
    
#     # Task 1 Results
#     print("\n📊 COMPANY RESEARCH (TASK 1)")
#     print("-" * 50)
#     company = result['company_research']
#     print(f"Company: {company.Company}")
#     print(f"Industry: {company.Industry}")
#     print(f"Segment: {company.Segment}")
#     print(f"Key Offerings: {', '.join(company.Key_Offerings)}")
#     print(f"Strategic Focus Areas: {', '.join(company.Strategic_Focus_Areas)}")
#     print(f"Vision: {company.Vision}")
    
#     # Task 2a Results
#     print("\n📈 MARKET ANALYSIS (TASK 2A)")
#     print("-" * 50)
#     market = result['market_analysis']
    
#     print("🔍 Industry Trends:")
#     for trend in market.industry_trends:
#         print(f"  • {trend}")
    
#     print("\n📋 Industry Standards:")
#     for standard in market.industry_standards:
#         print(f"  • {standard}")
    
#     print("\n🏢 Competitor Analysis:")
#     for competitor in market.competitor_analysis:
#         print(f"  • {competitor}")
    
#     print("\n🚀 Market Opportunities:")
#     for opportunity in market.market_opportunities:
#         print(f"  • {opportunity}")
    
#     # Task 2b Results
#     print("\n💡 GENERATED USE CASES (TASK 2B)")
#     print("-" * 50)
#     use_cases = result['use_cases']
    
#     for i, use_case in enumerate(use_cases.use_cases, 1):
#         print(f"\n{i}. {use_case.title}")
#         print(f"   Category: {use_case.category}")
#         print(f"   Problem: {use_case.problem_statement}")
#         print(f"   Solution: {use_case.ai_ml_solution}")
#         print(f"   Complexity: {use_case.implementation_complexity}")
#         print("   Benefits:")
#         for benefit in use_case.expected_benefits:
#             print(f"     • {benefit}")
    
#     print("\n🏆 PRIORITY RANKING")
#     print("-" * 50)
#     for i, priority in enumerate(use_cases.priority_ranking, 1):
#         print(f"{i}. {priority}")
    
#     print("=" * 80)

# Run the workflow
# if __name__ == "__main__":
#     result = workflow.invoke({"user_prompt": "Apple industry, key offerings, and strategic focus areas"})
#     print_results(result)