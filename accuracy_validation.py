import json

with open("output/research.json", "r", encoding="utf-8") as f:
    results = json.load(f)

# Independently verified expected values for the validation sample.
expected = {
    "Salesforce": {
        "auth_methods": ["OAuth2", "JWT", "Other"],
        "mcp_availability": "Official MCP",
    },
    "HubSpot": {
        "auth_methods": ["OAuth2", "Token"],
        "mcp_availability": "Official MCP",
    },
    "Slack": {
        "auth_methods": ["OAuth2", "Token"],
    },
    "Shopify": {
        "auth_methods": ["OAuth2", "API Key"],
    },
    "Stripe": {
        "auth_methods": ["API Key", "OAuth2", "Basic Auth", "Token"],
    },
}

total = 0
passed = 0

print("\n=== Accuracy Validation ===")

for app in results:
    name = app.get("app")

    if name not in expected:
        continue

    for field, expected_value in expected[name].items():
        actual_value = app.get(field)

        if isinstance(expected_value, list):
            actual_set = set(actual_value or [])
            expected_set = set(expected_value)
            match = actual_set == expected_set
        else:
            match = actual_value == expected_value

        total += 1

        if match:
            passed += 1
            status = "PASS"
        else:
            status = "FAIL"

        print(
            f"{name} | {field} | {status}"
            f"\n  Expected: {expected_value}"
            f"\n  Actual:   {actual_value}"
        )

accuracy = (passed / total * 100) if total else 0

print("\n=== Result ===")
print(f"Verified fields: {total}")
print(f"Passed fields: {passed}")
print(f"Failed fields: {total - passed}")
print(f"Final verified accuracy: {accuracy:.1f}%")