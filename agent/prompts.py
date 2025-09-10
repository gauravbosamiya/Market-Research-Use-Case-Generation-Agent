from langchain.prompts import PromptTemplate

def CompanyResearchPrompt() -> PromptTemplate:
    template = """You are an expert research analyst. Based on the provided search results, extract and structure the company information accurately.

Fill out each field precisely:
- Company: The exact company name
- Industry: The main industry (e.g., 'Automotive', 'Technology', 'Healthcare')  
- Segment: The primary business segment (e.g., 'Electric Vehicles', 'Cloud Computing')
- Key_Offerings: List the main products/services (3-5 items)
- Strategic_Focus_Areas: List key strategic priorities (3-5 items)
- Vision: The company's vision or mission statement

User Request: {input}

Search Results:
{search_results}

Based on this information, provide structured company research data."""

    prompt = PromptTemplate(
        template=template,
        input_variables=["input", "search_results"]
    )
    return prompt