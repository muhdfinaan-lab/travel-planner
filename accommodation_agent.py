import os
from groq import Groq
from dotenv import load_dotenv
from search_tool import web_search

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def accommodation_agent(destination: str, dates: str, budget: str) -> str:
    search_query = f"hotels in {destination} price per night"
    search_results = web_search(search_query)

    prompt = f"""You are an Accommodation Agent, part of a multi-agent travel planner.
Task: recommend places to stay, grounded in the real search results below.
Do not invent prices that aren't supported by the search results - if the
results only give rough starting prices, say so clearly.

Destination: {destination}
Dates: {dates}
Budget: {budget}

REAL SEARCH RESULTS:
{search_results}

Summarize 2-3 realistic options based on the above, cite which site each
price came from, and flag if anything is a starting price rather than a
confirmed rate for these dates."""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        max_completion_tokens=4096,
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    result = accommodation_agent("Tokyo", "Oct 10-17", "₹50,000")
    print(result)