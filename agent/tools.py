from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from dotenv import load_dotenv

load_dotenv()

class SafeTavilySearch(TavilySearch):
    """Wrapper around TavilySearch to safely catch API errors."""
    def invoke(self, input_str: str, **kwargs) -> str:
        try:
            return super().invoke(input_str, **kwargs)
        except Exception as e:
            return f"[Tavily API Error: {str(e)}]"

@tool("tavily_search")
def tavily_search(query: str, max_results: int = 5) -> str:
    """ Perform a Tavily search for a given query. 
    
    Args: 
        query (str): The search query. 
        max_results (int, optional): Maximum number of results to return. Defaults to 5. 
    
    Returns:
        str: Search results from Tavily, or error message if API fails. """
    safe_tavily = SafeTavilySearch(max_results=max_results)
    return safe_tavily.invoke(query)