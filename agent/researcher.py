import csv
import json
import os
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=GEMINI_API_KEY)


# --------------------------------------------------
# SOURCE FILTERING
# --------------------------------------------------

def get_domain_from_title(title):
    """
    Try to identify a domain from the grounding source title.
    """

    if not title:
        return ""

    title = title.lower().strip()

    # Remove common prefixes
    title = title.replace("www.", "")

    return title


def is_official_source(title, website):
    """
    Check whether a grounding source appears to belong
    to the application's official website.
    """

    if not title or not website:
        return False

    official_domain = urlparse(website).netloc.lower()

    official_domain = official_domain.replace(
        "www.",
        ""
    )

    source_title = title.lower().replace(
        "www.",
        ""
    )

    return (
        official_domain in source_title
        or source_title in official_domain
    )


def extract_grounding_sources(response, website):
    """
    Extract and filter Google Search grounding sources.

    Priority:
    1. Official sources
    2. Developer/documentation sources
    3. Other sources

    Maximum: 5 sources.
    """

    sources = []

    try:

        metadata = response.candidates[0].grounding_metadata

        if not metadata or not metadata.grounding_chunks:
            return sources

        seen_titles = set()

        official_sources = []
        developer_sources = []
        other_sources = []

        for index, chunk in enumerate(
            metadata.grounding_chunks
        ):

            if not chunk.web:
                continue

            title = chunk.web.title or ""
            url = chunk.web.uri or ""

            title_key = title.lower().strip()

            # Remove duplicate source titles
            if title_key in seen_titles:
                continue

            seen_titles.add(title_key)

            source = {
                "source_id": index,
                "title": title,
                "url": url,
                "domain": chunk.web.domain
            }

            title_lower = title.lower()

            # ------------------------------------------
            # Official source
            # ------------------------------------------

            if is_official_source(
                title,
                website
            ):

                official_sources.append(
                    source
                )

            # ------------------------------------------
            # Developer/documentation source
            # ------------------------------------------

            elif any(
                keyword in title_lower
                for keyword in [
                    "developer",
                    "developers",
                    "api",
                    "docs",
                    "documentation",
                    "github",
                    "mcp"
                ]
            ):

                developer_sources.append(
                    source
                )

            # ------------------------------------------
            # Other reliable sources
            # ------------------------------------------

            else:

                other_sources.append(
                    source
                )

        # ------------------------------------------
        # Prioritize official sources
        # ------------------------------------------

        for source in official_sources:

            if len(sources) >= 5:
                break

            sources.append(source)

        # ------------------------------------------
        # Then developer/documentation sources
        # ------------------------------------------

        for source in developer_sources:

            if len(sources) >= 5:
                break

            sources.append(source)

        # ------------------------------------------
        # Finally other sources
        # ------------------------------------------

        for source in other_sources:

            if len(sources) >= 5:
                break

            sources.append(source)

    except Exception as error:

        print(
            "Could not extract grounding sources:",
            error
        )

    return sources


# --------------------------------------------------
# RESEARCH APP
# --------------------------------------------------

def research_app(
    app,
    category,
    website
):

    prompt = f"""
You are an AI Product Operations research agent.

Research this application:

Application: {app}
Category: {category}
Official website: {website}

Your goal is to determine whether this application
can be integrated into an AI agent toolkit.

IMPORTANT RESEARCH RULES:

- Prefer official developer/API documentation.
- Prefer official authentication documentation.
- Prefer official pricing/access documentation.
- Prefer official MCP documentation or official GitHub repositories.
- Do not guess.
- If something cannot be verified, use "Unknown".
- API availability and MCP availability are DIFFERENT.
- Do not assume that having an API means the app has MCP.
- Distinguish between public/self-serve access and gated access.

RESEARCH THESE FIELDS:

1. description

One simple sentence explaining what the application does.

2. auth_methods

Choose only from:

- OAuth2
- API Key
- Basic Auth
- Token
- JWT
- Other
- Unknown

Return a list.

3. access_model

Choose the most accurate value:

- Self-serve
- Free trial
- Paid plan required
- Admin approval
- Contact sales
- Partner-only
- Unknown

4. api_type

Choose from:

- REST
- GraphQL
- SOAP
- Other
- Unknown

Return a list if multiple API types exist.

5. api_breadth

Choose:

- Broad
- Moderate
- Limited
- Unknown

Think about how much of the product can realistically
be controlled through the public API.

6. mcp_availability

Choose:

- Official MCP
- Community MCP
- No MCP found
- Unknown

7. buildability

Use these rules:

BUILDABLE NOW:
Public API exists AND developers can obtain access
without a partnership/contact-sales dependency.

BUILDABLE WITH CONSTRAINTS:
API exists but requires admin approval, paid access,
special permissions, or similar restrictions.

OUTREACH REQUIRED:
Access requires sales, partnership, or special approval.

BLOCKED:
No usable public API or no practical integration path.

8. main_blocker

If there is an important restriction, explain it briefly.

If there is no major blocker, return null.

9. confidence

Return a number between 0 and 1.

10. notes

Add important context or uncertainty.

DO NOT RETURN SOURCE URLs.

The program will collect Google Search grounding
sources separately.

Return ONLY valid JSON with these fields:

app
category
description
auth_methods
access_model
api_type
api_breadth
mcp_availability
buildability
main_blocker
confidence
notes

Do not include source URLs in the JSON.
"""

    response = client.models.generate_content(

        model="gemini-3.5-flash-lite",

        contents=prompt,

        config=types.GenerateContentConfig(

            tools=[
                types.Tool(
                    google_search=types.GoogleSearch()
                )
            ]

        )
    )

    text = response.text.strip()

    # Remove accidental markdown fences

    if text.startswith("```"):

        text = text.replace(
            "```json",
            ""
        )

        text = text.replace(
            "```",
            ""
        )

        text = text.strip()

    result = json.loads(text)

    # Capture filtered grounding sources

    sources = extract_grounding_sources(
        response,
        website
    )

    result["evidence"] = sources

    return result


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    input_file = Path(
        "data/apps.csv"
    )

    output_dir = Path(
        "output"
    )

    output_dir.mkdir(
        exist_ok=True
    )

    results = []

    with open(
        input_file,
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(
            file
        )

        for row in reader:

            print(
                f"\nResearching: {row['app']}"
            )

            try:

                result = research_app(
                    row["app"],
                    row["category"],
                    row["website"]
                )

                results.append(
                    result
                )

                print(
                    f"✓ Completed: {row['app']}"
                )

                print(
                    f"  Sources kept: "
                    f"{len(result.get('evidence', []))}"
                )

            except Exception as error:

                print(
                    f"✗ Failed: {row['app']}"
                )

                print(error)

    output_file = (
        output_dir /
        "research.json"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=2,
            ensure_ascii=False
        )

    print(
        "\n--------------------------------"
    )

    print(
        "Research complete."
    )

    print(
        f"Results saved to: {output_file}"
    )

    print(
        "--------------------------------"
    )


if __name__ == "__main__":
    main()