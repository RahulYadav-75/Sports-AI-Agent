import os
from dotenv import load_dotenv
from tavily import TavilyClient
from retrieval.chroma_db import search_chroma
load_dotenv()
client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)
def search_sports(query, max_results=5):
    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=max_results
    )
    results = []
    for item in response["results"]:
        results.append({
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "content": item.get("content", "")
        })
    return results
def get_sports_context(query):
    search_results = search_sports(
        query,
        max_results=5
    )
    chroma_results = search_chroma(
        query,
        n_results=3
    )
    web_context = "\n\n".join(
        [
            f"WEB SOURCE: {r['title']}\n"
            f"URL: {r['url']}\n"
            f"Information: {r['content']}"
            for r in search_results
        ]
    )
    chroma_context = "\n\n".join(
        [
            f"HISTORICAL KNOWLEDGE: {fact}"
            for fact in chroma_results
        ]
    )
    context = f"""
WEB SEARCH INFORMATION:
{web_context}
HISTORICAL KNOWLEDGE FROM CHROMADB:
{chroma_context}
"""
    return context, search_results