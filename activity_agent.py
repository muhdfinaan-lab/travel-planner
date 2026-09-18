import os
import re
from datetime import datetime
from dateutil import parser as date_parser
from groq import Groq
from dotenv import load_dotenv
from search_tool import web_search

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def count_trip_days(dates: str) -> int | None:
    """Try to compute exact trip length from a string like 'Oct 10-17' or
    'Oct 10 - Oct 17, 2026'. Returns None if parsing isn't possible."""
    try:
        # Handle "Oct 10-17" style by splitting on the dash and reusing the month
        match = re.match(r"([A-Za-z]+)\s*(\d+)\s*-\s*(\d+)", dates.strip())
        if match:
            month, start_day, end_day = match.groups()
            start = date_parser.parse(f"{month} {start_day}")
            end = date_parser.parse(f"{month} {end_day}")
            return (end - start).days + 1

        # Fallback: try splitting on '-' or 'to' and parsing each side fully
        parts = re.split(r"\s*(?:-|to)\s*", dates.strip())
        if len(parts) == 2:
            start = date_parser.parse(parts[0])
            end = date_parser.parse(parts[1])
            return (end - start).days + 1
    except Exception:
        return None
    return None


def activity_agent(destination: str, dates: str, preferences: str) -> str:
    search_query = f"top things to do in {destination} {preferences}"
    search_results = web_search(search_query)

    num_days = count_trip_days(dates)

    if num_days:
        day_instruction = (
            f"This trip is EXACTLY {num_days} days long. You MUST produce "
            f"exactly {num_days} day sections, labeled 'Day 1' through "
            f"'Day {num_days}', in order, with no skipped or repeated numbers. "
            f"Do not create a Day {num_days + 1} or any day beyond that."
        )
    else:
        day_instruction = (
            "Number the days sequentially starting at Day 1, with no skipped "
            "or duplicate day numbers. Before finishing, count your day "
            "headers and make sure they are consecutive."
        )

    prompt = f"""You are an Activity Agent, part of a multi-agent travel planner.
Task: recommend things to do, grounded in the real search results below where
relevant. It's fine to add well-known general knowledge too, but prioritize
anything specific mentioned in the search results.

Destination: {destination}
Dates: {dates}
Preferences: {preferences}

{day_instruction}

REAL SEARCH RESULTS:
{search_results}

Give a day-by-day list of 2-3 activities per day, mixing well-known sights
with at least one less obvious pick, tailored to the preferences."""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        max_completion_tokens=4096,
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    result = activity_agent("Tokyo", "Oct 10-17", "food, culture, some nightlife")
    print(result)