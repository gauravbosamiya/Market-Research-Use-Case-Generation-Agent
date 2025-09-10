from langchain_groq import ChatGroq
from dotenv import load_dotenv
from prompts import *
from states import *
from tools import *
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

load_dotenv()

llm = ChatGroq(model="deepseek-r1-distill-llama-70b")

class ResearchState(TypedDict):
    user_prompt: str
    company_research: CompanyResearch

def company_researcher(state: ResearchState):
    user_prompt = state["user_prompt"]
    
    structured_llm = llm.with_structured_output(CompanyResearch)
    
    search_results = tavily_search.invoke(f"{user_prompt} company information")
    
    prompt = CompanyResearchPrompt().format(
        input=user_prompt,
        search_results=search_results
    )
    
    company_research = structured_llm.invoke(prompt)
    
    return {"company_research": company_research}

graph = StateGraph(ResearchState)
graph.add_node("company_researcher", company_researcher)
graph.add_edge(START, "company_researcher")
graph.add_edge("company_researcher", END)

workflow = graph.compile()
result = workflow.invoke({"user_prompt": "Apple industry, key offerings, and strategic focus areas"})

print("=" * 60)
print("COMPANY RESEARCH REPORT")
print("=" * 60)
print(f"Company: {result['company_research'].Company}")
print(f"Industry: {result['company_research'].Industry}")
print(f"Segment: {result['company_research'].Segment}")
print(f"Key Offerings: {result['company_research'].Key_Offerings}")
print(f"Strategic Focus Areas: {result['company_research'].Strategic_Focus_Areas}")
print(f"Vision: {result['company_research'].Vision}")
print("=" * 60)