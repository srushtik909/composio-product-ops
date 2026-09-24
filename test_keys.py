import os
from dotenv import load_dotenv
from composio import Composio
from openai import OpenAI

load_dotenv()

composio_key = os.getenv("COMPOSIO_API_KEY")
openai_key = os.getenv("OPENAI_API_KEY")

print("Composio key loaded:", bool(composio_key))
print("OpenAI key loaded:", bool(openai_key))

if composio_key:
    composio = Composio(api_key=composio_key)
    print("Composio client created successfully")

if openai_key:
    client = OpenAI(api_key=openai_key)
    print("OpenAI client created successfully")