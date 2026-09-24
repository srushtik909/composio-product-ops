import os
from dotenv import load_dotenv
from composio import Composio

load_dotenv()

api_key = os.getenv("COMPOSIO_API_KEY")

if not api_key:
    raise ValueError("COMPOSIO_API_KEY not found in .env")

composio = Composio(api_key=api_key)

print("Composio client created successfully.")

tools = composio.tools.get_raw_composio_tools(
    search="search web",
    limit=5
)

print(f"Tools found: {len(tools)}")

for tool in tools:
    print("-", tool.slug)