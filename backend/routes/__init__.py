import re

from flask import Blueprint, jsonify, request

try:
    from backend.investigate import investigate
except ImportError:  # pragma: no cover - support running from backend folder
    from investigate import investigate

try:
    from backend.services import search_topic
except ImportError:  # pragma: no cover - support running from backend folder
    from services import search_topic

api = Blueprint("api", __name__)


@api.route("/hello", methods=["GET"])
def hello():
    return jsonify({"message": "Hello from OSINT backend routes."})


def _normalize_report(report, topic, sources):
    if isinstance(report, dict):
        key_findings = report.get("key_findings") or report.get("findings") or report.get("summary") or ["No key findings provided."]
        if isinstance(key_findings, str):
            key_findings = [line.strip() for line in key_findings.splitlines() if line.strip()]
        references = report.get("references") or report.get("sources") or []
        if isinstance(references, str):
            references = [line.strip() for line in references.splitlines() if line.strip()]
        return {
            "confidence": report.get("confidence") or report.get("confidence_score") or report.get("score") or "Based on available evidence",
            "key_findings": key_findings,
            "final_conclusion": report.get("final_conclusion") or report.get("conclusion") or report.get("summary") or "No conclusion provided.",
            "references": references,
        }

    report_text = str(report or "").strip()
    lines = [line.strip() for line in report_text.splitlines() if line.strip()]
    normalized = {
        "confidence": "Based on available evidence",
        "key_findings": [],
        "final_conclusion": "",
        "references": [],
    }

    current_heading = None
    for line in lines:
        lower_line = line.lower()
        if lower_line.startswith("# given query"):
            current_heading = "given_query"
            continue
        if lower_line.startswith("# confidence score"):
            current_heading = "confidence"
            continue
        if lower_line.startswith("# key findings"):
            current_heading = "key_findings"
            continue
        if lower_line.startswith("# final conclusion"):
            current_heading = "final_conclusion"
            continue
        if lower_line.startswith("# references"):
            current_heading = "references"
            continue

        if current_heading == "confidence":
            if normalized["confidence"] == "Based on available evidence":
                normalized["confidence"] = line
            else:
                normalized["confidence"] += " " + line
        elif current_heading == "key_findings":
            if line.startswith("*") or line.startswith("-"):
                normalized["key_findings"].append(re.sub(r"^[-*]\s*", "", line))
            else:
                normalized["key_findings"].append(line)
        elif current_heading == "final_conclusion":
            if normalized["final_conclusion"]:
                normalized["final_conclusion"] += " " + line
            else:
                normalized["final_conclusion"] = line
        elif current_heading == "references":
            if line.startswith("*") or line.startswith("-"):
                normalized["references"].append(re.sub(r"^[-*]\s*", "", line))
            else:
                normalized["references"].append(line)

    if not normalized["final_conclusion"]:
        normalized["final_conclusion"] = report_text
    if not normalized["key_findings"]:
        normalized["key_findings"] = ["No key findings available."]
    return normalized


@api.route("/investigate", methods=["POST"])
def investigate_route():
    payload = request.get_json(silent=True) or {}
    topic = payload.get("topic") or payload.get("query")

    if not topic:
        return jsonify({"error": "A topic or query is required."}), 400

    search_data = search_topic(topic)
    report = investigate(search_data.get("topic", topic), search_data.get("sources", []))

    return jsonify({
        "topic": search_data.get("topic", topic),
        "sources": search_data.get("sources", []),
        "report": report,
    })


@api.route("/verify-credibility", methods=["POST"])
def verify_credibility():
    payload = request.get_json(silent=True) or {}
    topic = payload.get("topic") or payload.get("query") or payload.get("claim") or payload.get("newsInput") or ""

    if not topic or not str(topic).strip():
        return jsonify({"error": "A topic, claim, or news input is required."}), 400

    try:
        search_data = search_topic(str(topic).strip())
        report = investigate(search_data.get("topic", topic), search_data.get("sources", []))
        normalized = _normalize_report(report, search_data.get("topic", topic), search_data.get("sources", []))
    except Exception as exc:  # pragma: no cover - defensive fallback
        return jsonify({
            "topic": str(topic).strip(),
            "verdict": "Investigation Failed",
            "confidence": "Backend error",
            "summary": f"Unable to investigate the topic right now: {exc}",
            "sources": [],
        }), 500

    return jsonify({
        "topic": search_data.get("topic", topic),
        "given_query": search_data.get("topic", topic),
        "confidence_score": normalized.get("confidence"),
        "key_findings": normalized.get("key_findings"),
        "final_conclusion": normalized.get("final_conclusion"),
        "references": normalized.get("references"),
        "sources": search_data.get("sources", []),
    })
