from prompt import SYSTEM_PROMPT
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def _format_sources(sources):
    if isinstance(sources, str):
        return sources

    if isinstance(sources, dict):
        items = []
        for key, value in sources.items():
            items.append(f"{key}: {value}")
        return "\n".join(items)

    if isinstance(sources, (list, tuple)):
        formatted = []
        for index, item in enumerate(sources, start=1):
            if isinstance(item, dict):
                title = item.get("title", "No title")
                url = item.get("url", "")
                snippet = item.get("snippet", "").strip()
                content = item.get("content", "").strip()
                section = [f"Source {index}", f"Title: {title}", f"URL: {url}"]
                if snippet:
                    section.append("\nSnippet:")
                    section.append(snippet)
                if content:
                    section.append("\nContent:")
                    section.append(content)
                formatted.append("\n".join(section).strip())
            else:
                formatted.append(str(item).strip())
        return "\n\n".join(formatted)

    return str(sources)


def investigate(topic, sources):
    """
    Builds the final prompt for the LLM.

    Parameters:
        topic (str): Investigation topic.
        sources (str): Search results collected from the web.

    Returns:
        str: Complete prompt to send to the LLM.
    """

    sources = _format_sources(sources)

    prompt = f"""
{SYSTEM_PROMPT}

========================================
INVESTIGATION TOPIC
========================================

{topic}

========================================
SEARCH RESULTS
========================================

{sources}

========================================
INSTRUCTIONS
========================================

Analyze all the above search results carefully.

Generate a complete OSINT Investigation Report using ONLY the supplied evidence.

Remember:

- Do not invent facts.
- Cite every important claim.
- Mention conflicting evidence.
- Mention if evidence is insufficient.
- Provide a confidence score.
"""

    if client is None:
        return prompt

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=1500
    )

    return response.choices[0].message.content