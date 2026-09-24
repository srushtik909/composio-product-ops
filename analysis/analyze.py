import json
from collections import Counter

with open("output/research.json", "r", encoding="utf-8") as f:
    apps = json.load(f)

print("\n=== Research Analysis ===")
print(f"Total researched records: {len(apps)}")

print("\n=== Buildability ===")
for key, value in Counter(
    app.get("buildability", "Unknown") for app in apps
).items():
    print(f"{key}: {value}")

print("\n=== MCP Availability ===")
for key, value in Counter(
    app.get("mcp_availability", "Unknown") for app in apps
).items():
    print(f"{key}: {value}")

print("\n=== Categories ===")
for key, value in Counter(
    app.get("category", "Unknown") for app in apps
).items():
    print(f"{key}: {value}")

print("\n=== Confidence ===")
if apps:
    confidences = [
        app.get("confidence")
        for app in apps
        if isinstance(app.get("confidence"), (int, float))
    ]

    if confidences:
        print(f"Average confidence: {sum(confidences) / len(confidences):.2f}")
        print(f"Records with confidence: {len(confidences)}")
    else:
        print("No numeric confidence values found.")
else:
    print("No research records found.")

print("\n=== App Results ===")
for app in apps:
    print(
        f"{app.get('app', 'Unknown')} | "
        f"{app.get('buildability', 'Unknown')} | "
        f"MCP={app.get('mcp_availability', 'Unknown')} | "
        f"Confidence={app.get('confidence', 'Unknown')}"
    )