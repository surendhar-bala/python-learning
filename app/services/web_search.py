import os
from tavily import TavilyClient

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_company(company_name: str):

    response = client.search(
        query=f"{company_name} company official website headquarters industry",
        search_depth="basic",
        max_results=5,
        include_answer=False
    )

    text = ""

    for item in response["results"]:
        text += f"""
Title: {item['title']}
URL: {item['url']}
Content:
{item['content']}

--------------------
"""

    return text