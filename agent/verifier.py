import json
from pathlib import Path


def verify_app(research):

    issues = []
    fields_to_review = []
    recommended_changes = []

    buildability = str(
        research.get("buildability", "")
    ).upper()

    access_model = str(
        research.get("access_model", "")
    ).lower()

    blocker = str(
        research.get("main_blocker") or ""
    ).lower()

    notes = str(
        research.get("notes") or ""
    ).lower()

    confidence = research.get("confidence", 0)

    evidence = research.get("evidence", [])

    # --------------------------------------------------
    # 1. Check confidence
    # --------------------------------------------------

    if isinstance(confidence, (int, float)):

        if confidence < 0.7:
            issues.append(
                "Low research confidence."
            )

            fields_to_review.append(
                "confidence"
            )

    # --------------------------------------------------
    # 2. Check BUILDABLE NOW contradictions
    # --------------------------------------------------

    if buildability == "BUILDABLE NOW":

        restriction_words = [
            "contact sales",
            "partnership",
            "partner",
            "admin approval",
            "administrator approval",
            "paid plan required",
            "paid access",
            "special approval"
        ]

        found_restrictions = [
            word for word in restriction_words
            if word in blocker or word in notes
        ]

        if found_restrictions:

            issues.append(
                "Buildability is BUILDABLE NOW, "
                "but the notes/blocker mention access restrictions: "
                + ", ".join(found_restrictions)
            )

            fields_to_review.append(
                "buildability"
            )

            recommended_changes.append(
                "Review whether the app should be "
                "BUILDABLE WITH CONSTRAINTS or OUTREACH REQUIRED."
            )

    # --------------------------------------------------
    # 3. Check access model contradictions
    # --------------------------------------------------

    if access_model == "self-serve":

        if (
            "contact sales" in notes
            or "contact sales" in blocker
            or "partner-only" in notes
            or "partnership required" in notes
        ):

            issues.append(
                "Access model is Self-serve but notes "
                "mention sales or partnership requirements."
            )

            fields_to_review.append(
                "access_model"
            )

    # --------------------------------------------------
    # 4. Check MCP evidence
    # --------------------------------------------------

    mcp = str(
        research.get("mcp_availability", "")
    ).lower()

    if "official mcp" in mcp:

        official_sources = 0

        for source in evidence:

            title = str(
                source.get("title", "")
            ).lower()

            if any(
                domain in title
                for domain in [
                    ".com",
                    ".dev",
                    ".org"
                ]
            ):

                official_sources += 1

        if official_sources == 0:

            issues.append(
                "Official MCP is claimed but "
                "no obvious official source was found."
            )

            fields_to_review.append(
                "mcp_availability"
            )

    # --------------------------------------------------
    # 5. Check evidence count
    # --------------------------------------------------

    if len(evidence) == 0:

        issues.append(
            "No evidence sources were captured."
        )

        fields_to_review.append(
            "evidence"
        )

    elif len(evidence) > 10:

        issues.append(
            f"Too many evidence sources ({len(evidence)}). "
            "Research should be narrowed to the strongest sources."
        )

        fields_to_review.append(
            "evidence"
        )

        recommended_changes.append(
            "Keep approximately 3–5 strongest sources."
        )

    # --------------------------------------------------
    # 6. Check Google grounding URLs
    # --------------------------------------------------

    grounding_urls = 0

    for source in evidence:

        url = str(
            source.get("url", "")
        )

        if "vertexaisearch.cloud.google.com" in url:

            grounding_urls += 1

    if grounding_urls > 0:

        issues.append(
            "Evidence URLs are Google grounding redirects "
            "rather than direct source URLs."
        )

        fields_to_review.append(
            "evidence_urls"
        )

        recommended_changes.append(
            "Resolve grounding sources to direct official URLs "
            "for the final case study."
        )

    # --------------------------------------------------
    # 7. Remove duplicate field names
    # --------------------------------------------------

    fields_to_review = list(
        dict.fromkeys(fields_to_review)
    )

    # --------------------------------------------------
    # Final status
    # --------------------------------------------------

    if issues:

        status = "NEEDS_REVIEW"

    else:

        status = "PASS"

    if len(evidence) >= 3:

        evidence_quality = "MEDIUM"

    elif len(evidence) > 0:

        evidence_quality = "LOW"

    else:

        evidence_quality = "LOW"

    return {
        "verification_status": status,
        "evidence_quality": evidence_quality,
        "fields_to_review": fields_to_review,
        "contradictions": issues,
        "reason": (
            "Automated rule-based verification completed."
        ),
        "recommended_changes": recommended_changes
    }


def main():

    input_file = Path(
        "output/research.json"
    )

    output_file = Path(
        "output/verified_research.json"
    )

    with open(
        input_file,
        "r",
        encoding="utf-8"
    ) as file:

        research_data = json.load(file)

    verified_results = []

    for research in research_data:

        app = research.get(
            "app",
            "Unknown"
        )

        print(
            f"\nVerifying: {app}"
        )

        verification = verify_app(
            research
        )

        final_record = research.copy()

        final_record["verification"] = verification

        verified_results.append(
            final_record
        )

        print(
            f"✓ {app} → "
            f"{verification['verification_status']}"
        )

        if verification["fields_to_review"]:

            print(
                "  Review:",
                ", ".join(
                    verification[
                        "fields_to_review"
                    ]
                )
            )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            verified_results,
            file,
            indent=2,
            ensure_ascii=False
        )

    print("\n--------------------------------")
    print("Verification complete.")
    print(
        f"Results saved to: {output_file}"
    )
    print("--------------------------------")


if __name__ == "__main__":
    main()