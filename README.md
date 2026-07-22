# GenZ Bible semantic search agent

A conversational RAG agent over [genz.bible](https://genz.bible), a Gen-Z paraphrase of
scripture presented alongside the traditional English text. Ask a plain-language question,
get back the relevant passages in both wordings.

Built as a team hackathon project (team of 4, 200-minute sprint) for **CEU Data
Engineering 4 — AI Engineering and LLM Integration**, Spring 2026.

## What's here

This repository holds the parts I wrote, extracted from a working copy of the course
repository so they exist somewhere durable and attributable.

| Path | What it does |
| --- | --- |
| `scripts/test_scraping_data.py` | The scraper. Walks every book of genz.bible and emits verse-level chunks ready for ChromaDB ingestion. |
| `scripts/intercept_api.py` | Playwright driver that intercepts the site's internal JSON API rather than parsing rendered HTML — faster and far less brittle than DOM scraping. |
| `validate_counts.py` | Checks scraped chapter counts against the canonical Protestant Bible book/chapter counts, so a silently truncated scrape fails loudly. |
| `validate_books.py`, `parse_test.py`, `scripts/test_parse.py`, `run_test_single.py`, `run_eval.py` | Parser and scrape-integrity checks used while iterating on the extractor. |
| `scripts/request_bedrock_quotas.py` | CLI to list and request AWS Bedrock quota increases across the models used. |
| `notebooks/guardrails.ipynb` | Input and output guardrails (see below). Derived from course material — see Attribution. |
| `start_on_render.sh` | Entrypoint used to deploy the Chainlit app to Render. |

## Approach

**Scraping.** genz.bible renders client-side, so rather than fight the DOM the scraper
intercepts the site's own JSON API with Playwright. Output is one chunk per verse, each
carrying the traditional English text, the Gen-Z paraphrase, and book/chapter/verse/testament
metadata. The result was 30,591 verse-level chunks.

**Validation.** Scrapers fail quietly, so chapter counts are checked against the canonical
Protestant canon before anything is indexed — a missing or truncated book surfaces as an
error rather than as a thin retrieval index nobody notices.

**Retrieval and serving.** Chunks are embedded into a ChromaDB vector store and wrapped as
an OpenAI Agents SDK agent behind a Chainlit chat UI, backed by AWS Bedrock models
(Amazon Nova, Claude 3 Haiku) through litellm. The app was deployed to Render and
demonstrated running live at the end of the sprint. That deployment was for the
assignment and is no longer up.

**Guardrails** (my main contribution to the agent itself, in `notebooks/guardrails.ipynb`):

- an *input* guardrail — a small classifier agent returning a typed `ValidBibleQuery`
  (`is_valid_query`, topic, reason) that trips a tripwire on off-topic requests. A prompt
  like "write a python script to scan a network port" is refused with the reason surfaced
  rather than silently answered;
- an *output* guardrail — a typed `SafeOutput` carrying a `redacted_response`, screening
  generated text for offensive or inappropriate content before it reaches the user.

## Running it

Requires an `.env` with `OPENAI_API_KEY` and AWS credentials for Bedrock. Nothing in this
repository contains credentials.

```bash
python -m playwright install chromium
python scripts/test_scraping_data.py    # regenerates genz_bible_data/
python validate_counts.py               # verify the scrape is complete
```

The scraped corpus and the ChromaDB store are both gitignored: the text belongs to
genz.bible and is not mine to redistribute, and both are reproducible from the scripts here.

## Attribution

The course scaffolding this was built on — the Chainlit app skeleton and the notebook
`notebooks/guardrails.ipynb` is derived from — comes from
[zoltanctoth/ceu-ai-engineering-class](https://github.com/zoltanctoth/ceu-ai-engineering-class),
licensed **CC BY-NC 4.0**. That notebook is a modified version: the guardrail agents,
typed schemas and Bedrock/litellm wiring described above are my additions. The remaining
files in this repository are my own work.

The GenZ Bible text itself is the property of genz.bible and is neither included nor
redistributed here.
