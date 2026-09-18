from datetime import date

from src.course_qa import QuestionRequest, answer_question


class FakeClient:
    def embeddings(self, text):
        return [0.1, 0.2]

    def query(self, collection, embedding, top_k):
        return {"matches": [{"metadata": {"text": "Portfolio submission is due Friday."}}]}

    def rerank(self, query, candidates, top_k):
        return {"results": [{"text": candidates[0], "score": 0.97}]}


def test_deadline_report_marks_due_soon():
    result = answer_question(QuestionRequest("When is the portfolio due?", date(2026, 9, 6)), FakeClient())
    assert result["status"] == "due_soon"
    assert result["answer"] == "Portfolio submission is due Friday."

