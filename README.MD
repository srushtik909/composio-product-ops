# AI Product Ops Research Agent
An automated research project that checks SaaS applications for AI-agent integration readiness.

## Problem
Checking whether an application can be used by an AI agent requires checking APIs, authentication, access restrictions, MCP availability, and integration limits. Doing this manually for many applications takes time and can give inconsistent results.

## Solution
This project uses a research agent to collect application and API information and convert it into structured data. A separate verification step checks the results for possible issues.

## Pipeline
100-app catalog → Research Agent → Source Discovery → Structured JSON → Verification → Analysis → HTML Case Study

## Research Fields
Each application contains:
- Application
- Category
- Description
- Authentication methods
- Access model
- API type
- API breadth
- MCP availability
- Buildability
- Main blocker
- Evidence
- Confidence
- Notes

## Buildability Framework
**BUILDABLE NOW:** Public API is available without a partnership or contact-sales requirement.
**BUILDABLE WITH CONSTRAINTS:** API exists but may require a paid plan, admin approval, extra permissions, or other restrictions.
**OUTREACH REQUIRED:** Integration requires sales, partnership, or special approval.
**BLOCKED:** No practical public integration path was identified.

## Research Scope
The research catalog contains 100 applications across 10 categories.
The automated research pipeline was executed and validated on 5 applications:
- Salesforce
- HubSpot
- Slack
- Shopify
- Stripe
The remaining applications are kept in the catalog and are not marked as researched without supporting evidence.

## Validation
The research output was checked using an independent validation sample.
- Applications checked: 5
- Fields checked: 7
- Passed: 7
- Failed: 0
- Final checked-field accuracy: 100%
This result applies only to the 7 checked fields and does not represent accuracy across all 100 applications.

## Key Observations
- API availability and MCP availability are separate checks.
- Applications use different authentication methods.
- Having an API does not always mean unrestricted access.
- Paid plans and admin approval can affect integration.
- Evidence and confidence are important for automated research.

## Technology
Python, Gemini API, Google Search grounding, Pandas, JSON, CSV, deterministic verification, HTML/CSS.

## Project Structure
```text
composio-product-ops/
├── agent/
│   ├── prompts.py
│   ├── schemas.py
│   ├── researcher.py
│   └── verifier.py
├── data/
│   └── apps.csv
├── output/
│   ├── research.json
│   └── verified_research.json
├── analysis/
│   └── analyze.py
├── case-study/
│   └── index.html
├── accuracy_validation.py
├── generate_case_study.py
├── test_composio.py
└── README.md