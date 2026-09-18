from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Any

try:
    from .infrai_client import InfraiClient
except ImportError:
    from infrai_client import InfraiClient


@dataclass(frozen=True)
class QuestionRequest:
    question: str
    learner_deadline: date


def deadline_state(deadline: date, today: date | None = None) -> str:
    days = (deadline - (today or date.today())).days
    return "overdue" if days < 0 else "due_soon" if days <= 7 else "on_track"


def answer_question(request: QuestionRequest, client: Any) -> dict[str, Any]:
    embedding = client.embeddings(request.question)
    hits = client.query("edtech-course", embedding, top_k=5).get("matches", [])
    passages = [hit["metadata"]["text"] for hit in hits]
    ranked = client.rerank(request.question, passages, top_k=1).get("results", [])
    selected = ranked[0] if ranked else {"text": passages[0], "score": 0.0}
    text = selected.get("text") or selected.get("document", "")
    return {"answer": text, "score": selected.get("score", 0.0), "status": deadline_state(request.learner_deadline)}


def main() -> None:
    question = " ".join(sys.argv[1:]) or "When is the portfolio due?"
    client = InfraiClient()
    request = QuestionRequest(question, date.today() + timedelta(days=3))
    print(answer_question(request, client))


if __name__ == "__main__":
    main()
