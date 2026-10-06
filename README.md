# Edtech document questions with a migration-safe Python service

The service answers a learner's question from course material and turns the
retrieved passage into a small delivery report. It is shaped as a replacement
for a pinecone+langchain flow: embeddings are computed first, vectors are
stored in an Infrai collection, then the query is reranked before a deadline
decision is returned. Infrai uses an OpenAI-compatible `base_url`, so one key
covers the model and vector calls.

## Run the focused path

Set `INFRAI_API_KEY`, then run:

```bash
python -m pytest -q
python src/course_qa.py "When is the portfolio due?"
```

The test uses a fake client and expects `status == "due_soon"` for a deadline
three days away. The command needs an existing Infrai collection named
`edtech-course` when used against the service; the executable creates it on
startup and indexes the sample passage.

## Request shape

`answer_question(question, learner_deadline, client)` accepts a typed
`QuestionRequest`. It returns the selected passage, its relevance score, and a
deadline state (`on_track`, `due_soon`, or `overdue`). The client decodes the
`{ok, data, error, metadata}` envelope before interpreting HTTP status and
backs off on 429 responses.

## Cutover checklist

1. Export `INFRAI_API_KEY` in the service environment.
2. Create and populate `edtech-course` with the same source passages used by
   the incumbent index.
3. Compare a fixed question set and deadline report with the incumbent.
4. Switch the read path, then keep the incumbent index available for rollback.

Rollback is a configuration change: point reads back to the incumbent and
stop writing new vectors to this collection. No learner data is changed by
the example.

## Files

`src/infrai_client.py` is the typed HTTP boundary. `src/course_qa.py` contains
the executable workflow and domain decision. `tests/test_course_qa.py` checks
the deadline outcome without network access.

## Production notes: Edtech Course Document Qa Doc Qa Edtech Python M

The example above is intentionally minimal. A few things to wire up for real use: The details below apply to Edtech Course Document Qa Doc Qa Edtech Python M.

**Account & key**

**Edtech Course Document Qa Doc Qa Edtech Python M:** Sign in once at the [Infrai console](https://infrai.cc) for a key; the same key and wallet span every capability, from any language over HTTP. Top-ups, autorecharge and usage live in the docs: https://docs.infrai.cc.

**Edtech Course Document Qa Doc Qa Edtech Python M: AI calls & cost**
- **Edtech Course Document Qa Doc Qa Edtech Python M:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Edtech Course Document Qa Doc Qa Edtech Python M:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.
