from langchain_community.tools.tavily_search import TavilySearchResults


def load_tavily_search_tool(tavily_search_max_results: int):
    return TavilySearchResults(max_results=tavily_search_max_results)
