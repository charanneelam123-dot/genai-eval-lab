# GenAI Eval Lab

[![Checks](https://github.com/charanneelam123-dot/genai-eval-lab/actions/workflows/tests.yml/badge.svg)](https://github.com/charanneelam123-dot/genai-eval-lab/actions/workflows/tests.yml)

Compare prompt variants using reproducible cases, deterministic grading, latency, and token usage reports.

A focused evaluation example. For the larger deployed application, see [llm-evaluation-mlops](https://github.com/charanneelam123-dot/llm-evaluation-mlops).

Project by Charan Neelam. Python 3.11+; no third-party packages required.
All bundled business data is fictional.

## Quick start

```bash
git clone https://github.com/charanneelam123-dot/genai-eval-lab.git
cd genai-eval-lab
python evaluate.py --output runs/demo
python -m unittest discover -s tests -v
```

## Optional live model

Set environment variables in your shell; `.env.example` documents the names
but `.env` files are not automatically loaded. Choose a chat/tool-compatible
model available to your API account.

```powershell
$env:OPENAI_API_KEY = "your-key"
$env:OPENAI_MODEL = "your-model-id"
```

Append `--live` to the demo command. Live mode sends question/context data to
OpenAI and incurs API usage. Missing credentials cause an explicit error.
The adapter uses the [Chat Completions API](https://developers.openai.com/api/reference/resources/chat).

## How it works

```mermaid
flowchart LR
    A[Versioned test cases] --> B[Prompt variants]
    B --> C[Fixture or live provider]
    C --> D[Deterministic graders]
    D --> E[JSON CSV Markdown reports]
```

Six synthetic cases cover facts, missing information, prompt injection, numeric
answers, and negation. Each case has required and forbidden terms. Use
`--cases file.json` for another dataset and `--repeats 3` for repeated samples.
Reports include each answer, grading checks, provider errors, latency, and token
usage. Fixture mode tests reporting using authored answers; it is not a model
benchmark. `--live` calls the configured model for both prompts.

## Design decisions and limitations

Term checks are cheap and deterministic but cannot measure semantic truth.
For example, a wrong sentence containing the required words can pass. Six cases
are too few for general quality claims. Expand with domain-reviewed cases and
human grading before making comparisons. Fixture latency measures local
execution only. Live token usage is reported without invented dollar pricing.
Live calls are sequential, and failed requests are recorded without retries.

## Interview walkthrough

Open report.json to inspect individual failures, then compare report.md.
Explain dataset leakage, repeated sampling, and why fixture pass rates cannot
be presented as measured model improvements.

## Validation

Unit tests run without API credentials and include mocked provider behavior.
GitHub Actions runs tests on Python 3.11–3.14. See `docs/validation.md` for the
local validation record. Live provider behavior has not been validated with a
paid API call.

## Portfolio talking point

See `docs/linkedin-draft.md` for an editable project announcement. Use only
results you have reproduced and can explain. Licensed under MIT.
