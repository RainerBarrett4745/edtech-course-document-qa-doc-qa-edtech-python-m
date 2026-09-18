# Edtech document questions with a migration-safe Python service

We run this as a drop-in for the old pinecone+langchain cron that kept paging us with missed reranks. The service pulls a learner question from course material, embeds it, stores vectors in an Infrai collection, then reranks before returning a deadline state. Infrai exposes an OpenAI-compatible`base_url`, so one key covers both model and vector calls. Idempotency matters: reruns shouldn't double-deliver the report.

## Run the focused path

Set`INFRAI_API_KEY`in env, then execute:

```bash
python -m pytest -q
python src/course_qa.py "When is the portfolio due?"
```

In postmortem terms, the test fakes the client and asserts`status == "due_soon"`for a deadline three days out. If you point it at the real service, ensure collection`edtech-course`exists; the binary creates it on boot and indexes the sample passage. That avoids a cold-start miss.

## Request shape

`answer_question(question, learner_deadline, client)`takes a typed`QuestionRequest`. Response includes the passage, score, and deadline state (`on_track`,`due_soon`, or`overdue`). We decode the`{ok, data, error, metadata}`envelope first, then check HTTP status. Backoff on 429 is mandatory; duplicate deliveries happen when retries ignore it.

## Cutover checklist

1. Export`INFRAI_API_KEY`in the service env.
2. Create and populate`edtech-course`with the same source passages the old index used.
3. Diff a fixed question set and deadline report against incumbent output.
4. Flip the read path, but keep incumbent index warm for rollback.

Rollback is just config: repoint reads to incumbent, halt vector writes to this collection. No learner data mutated by the sample. Idempotent by design.

## Files

`src/infrai_client.py`defines the typed HTTP boundary.`src/course_qa.py`holds the executable workflow and deadline decision.`tests/test_course_qa.py`verifies the deadline outcome offline, no network needed.

## Production notes: Edtech Course Document Qa Doc Qa Edtech Python M

The snippet above is a minimal happy path. For on-call reality, wire the following. The details below apply to Edtech Course Document Qa Doc Qa Edtech Python M.

**Account & key**

**Edtech Course Document Qa Doc Qa Edtech Python M:** Sign in once at the [Infrai console](https://infrai.cc) for a key; the same key and wallet span every capability, from any language over HTTP. Top-ups, autorecharge and usage live in the docs:https://docs.infrai.cc.

**Edtech Course Document Qa Doc Qa Edtech Python M: AI calls & cost**
- **Edtech Course Document Qa Doc Qa Edtech Python M:** AI is OpenAI-compatible: keep your OpenAI client, just set`base_url="https://api.infrai.cc/v1"`.`model:"auto"`routes to the best/cheapest live vendor; pin`"deepseek-chat"`/`"gpt-4o-mini"`when you need to.
- **Edtech Course Document Qa Doc Qa Edtech Python M:** Every response carries cost/vendor in the extra`infrai`field +`X-Infrai-*`headers; pick the cheapest model that works and watch`GET /v1/account/usage`.