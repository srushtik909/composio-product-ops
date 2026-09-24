import json
from pathlib import Path
from collections import Counter

INPUT = Path("output/research.json")
OUTPUT_DIR = Path("case-study")
OUTPUT = OUTPUT_DIR / "index.html"

OUTPUT_DIR.mkdir(exist_ok=True)

with open(INPUT, "r", encoding="utf-8") as f:
    apps = json.load(f)

total = len(apps)

buildability = Counter(
    app.get("buildability", "Unknown")
    for app in apps
)

mcp = Counter(
    app.get("mcp_availability", "Unknown")
    for app in apps
)

categories = Counter(
    app.get("category", "Unknown")
    for app in apps
)

rows = ""

for app in apps:
    evidence = app.get("evidence", [])

    evidence_html = "<br>".join(
        f'<a href="{src.get("url", "#")}" target="_blank">'
        f'{src.get("title", "Source")}</a>'
        for src in evidence[:5]
    )

    rows += f"""
    <tr>
        <td>{app.get("app", "")}</td>
        <td>{app.get("category", "")}</td>
        <td>{app.get("description", "")}</td>
        <td>{", ".join(app.get("auth_methods", []))}</td>
        <td>{app.get("access_model", "")}</td>
        <td>{", ".join(app.get("api_type", []))}</td>
        <td>{app.get("api_breadth", "")}</td>
        <td>{app.get("mcp_availability", "")}</td>
        <td>{app.get("buildability", "")}</td>
        <td>{app.get("main_blocker") or "None"}</td>
        <td>{evidence_html}</td>
    </tr>
    """

category_html = "".join(
    f"<li><strong>{category}</strong>: {count}</li>"
    for category, count in categories.items()
)

html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>AI Product Ops Research Case Study</title>

<style>
body {{
    font-family: Arial, sans-serif;
    margin: 0;
    background: #f5f7fb;
    color: #172033;
}}

.container {{
    max-width: 1400px;
    margin: auto;
    padding: 40px;
}}

.hero {{
    background: #111827;
    color: white;
    padding: 45px;
    border-radius: 18px;
    margin-bottom: 30px;
}}

.hero h1 {{
    font-size: 38px;
    margin-bottom: 10px;
}}

.cards {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 15px;
    margin: 25px 0;
}}

.card {{
    background: white;
    padding: 22px;
    border-radius: 14px;
    box-shadow: 0 2px 10px rgba(0,0,0,.06);
}}

.card h2 {{
    margin: 0;
    font-size: 30px;
}}

section {{
    background: white;
    padding: 30px;
    border-radius: 16px;
    margin: 25px 0;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
}}

th, td {{
    padding: 10px;
    border: 1px solid #ddd;
    vertical-align: top;
    text-align: left;
}}

th {{
    background: #eef2ff;
}}

a {{
    color: #2563eb;
}}

code {{
    background: #eef2ff;
    padding: 3px 6px;
    border-radius: 4px;
}}

@media(max-width: 900px) {{
    .cards {{
        grid-template-columns: repeat(2, 1fr);
    }}
}}

@media(max-width: 600px) {{
    .cards {{
        grid-template-columns: 1fr;
    }}

    .container {{
        padding: 15px;
    }}
}}
</style>
</head>

<body>

<div class="container">

<div class="hero">
<h1>AI Product Ops Research Agent</h1>
<p>
Automating research of SaaS applications for AI-agent integration
readiness.
</p>
<p>
The pipeline converts product/API research into structured,
verifiable data for product and engineering decisions.
</p>
</div>

<div class="cards">

<div class="card">
<p>Apps researched</p>
<h2>{total}</h2>
</div>

<div class="card">
<p>Buildable now</p>
<h2>{buildability.get("BUILDABLE NOW", 0)}</h2>
</div>

<div class="card">
<p>With constraints</p>
<h2>{buildability.get("BUILDABLE WITH CONSTRAINTS", 0)}</h2>
</div>

<div class="card">
<p>Official MCP</p>
<h2>{mcp.get("Official MCP", 0)}</h2>
</div>

</div>

<section>

<h2>1. Problem</h2>

<p>
Evaluating whether an application can be integrated into an AI-agent
platform requires checking multiple sources including API documentation,
authentication requirements, access restrictions and MCP availability.
Doing this manually for many applications is repetitive and difficult
to keep consistent.
</p>

</section>

<section>

<h2>2. Research Approach</h2>

<ol>
<li>Start with a structured application list.</li>
<li>Collect API and authentication information.</li>
<li>Check access and commercial restrictions.</li>
<li>Check MCP availability separately from API availability.</li>
<li>Classify integration buildability.</li>
<li>Capture evidence sources.</li>
<li>Run deterministic verification checks.</li>
</ol>

</section>

<section>

<h2>3. Data Schema</h2>

<p>The research agent produces the following structured fields:</p>

<ul>
<li>Application</li>
<li>Category</li>
<li>Description</li>
<li>Authentication methods</li>
<li>Access model</li>
<li>API type</li>
<li>API breadth</li>
<li>MCP availability</li>
<li>Buildability</li>
<li>Main blocker</li>
<li>Evidence</li>
<li>Confidence</li>
<li>Notes</li>
</ul>

</section>

<section>

<h2>4. Buildability Framework</h2>

<ul>
<li>
<strong>BUILDABLE NOW:</strong>
Public API exists and developers can obtain access without a
partnership/contact-sales dependency.
</li>

<li>
<strong>BUILDABLE WITH CONSTRAINTS:</strong>
API exists but access requires additional permissions, paid plans,
administrative approval or similar restrictions.
</li>

<li>
<strong>OUTREACH REQUIRED:</strong>
Integration requires sales, partnership or special approval.
</li>

<li>
<strong>BLOCKED:</strong>
No practical public integration path was identified.
</li>
</ul>

</section>

<section>

<h2>5. Category Coverage</h2>

<ul>
{category_html}
</ul>

</section>

<section>

<h2>6. Automated Research Results</h2>

<div style="overflow-x:auto">

<table>

<thead>
<tr>
<th>App</th>
<th>Category</th>
<th>Description</th>
<th>Auth</th>
<th>Access</th>
<th>API</th>
<th>Breadth</th>
<th>MCP</th>
<th>Buildability</th>
<th>Blocker</th>
<th>Evidence</th>
</tr>
</thead>

<tbody>
{rows}
</tbody>

</table>

</div>

</section>

<section>

<h2>7. Quality Control</h2>

<p>
The pipeline uses deterministic verification rules to identify
low-confidence results, conflicting access restrictions, weak evidence
and unsupported MCP claims.
</p>

<p>
The verification layer is intentionally separate from the research
layer so that research generation and quality control can be evaluated
independently.
</p>

</section>

<section>

<h2>8. Key Observations</h2>

<ul>
<li>API availability and MCP availability must be evaluated separately.</li>
<li>Authentication requirements vary significantly between products.</li>
<li>Public APIs do not always mean unrestricted production access.</li>
<li>Administrative approval and paid plans can affect integration feasibility.</li>
<li>Evidence quality is important when automating product research.</li>
</ul>

</section>

<section>

<h2>9. Technology</h2>

<p>
Python · Gemini API · Google Search grounding · Composio SDK/MCP ·
JSON · CSV · deterministic verification · HTML/CSS
</p>

</section>

<section>

<h2>10. Project Structure</h2>

<pre>
composio-product-ops/
├── agent/
│   ├── researcher.py
│   └── verifier.py
├── data/
│   └── apps.csv
├── output/
│   ├── research.json
│   └── verified_research.json
├── case-study/
│   └── index.html
├── .env
└── README.md
</pre>

</section>

</div>

</body>
</html>
"""

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Case study created: {OUTPUT}")