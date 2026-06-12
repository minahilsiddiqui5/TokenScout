# Import the search tool from the ddgs library
from ddgs import DDGS


# This function searches the web for a topic and gives back clean results
def web_search(query, max_results=4):
    # An empty list where we will collect the results
    results = []

    # Open a DuckDuckGo search connection (it closes itself when done)
    with DDGS() as ddgs:
        # Run the search, then go through each result one by one
        for r in ddgs.text(query, max_results=max_results):
            # From each result, keep only the 3 things we need
            results.append({
                "title": r.get("title", ""),    # the page title
                "url": r.get("href", ""),        # the link
                "snippet": r.get("body", ""),    # a short summary text
            })

    # Send the full list of results back to whoever called this function
    return results


# This part runs ONLY when you run this file directly (it's just for testing)
if __name__ == "__main__":
    # Search a sample topic
    found = web_search("what is prompt caching in LLMs")

    # Print each result with a number in front
    for i, r in enumerate(found, 1):
        print(f"[{i}] {r['title']}")            # number + title
        print(f"    {r['snippet'][:120]}...")   # first 120 letters of the summary
        print(f"    {r['url']}\n")              # the link