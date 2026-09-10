# Alumnium Tests

AI-driven UI test framework, built on
[Playwright](https://playwright.dev/python/), [Alumnium](https://alumnium.ai/)
and pytest. Runs on **Windows 10/11**.

## Requirements

- Windows 10/11
- Python 3.12
- [uv](https://docs.astral.sh/uv/) — install with `pip install uv` or `winget install astral-sh.uv`

## Setup

```powershell
uv sync
uv run playwright install chromium
```

Create your local `.env` from the template and add your OpenAI key:

```powershell
copy .env.example .env
# then edit .env and set OPENAI_API_KEY=sk-...
```

`.env` is gitignored — never commit real secrets.

## Running tests

```powershell
uv run pytest -v                          # headed (default)
$env:HEADLESS = "1"; uv run pytest -v     # headless
```

Run a single scenario:

```powershell
uv run pytest tests/scenario_1 -v
```

## Output

- **Videos** — one `.webm` per test in `videos/`, recorded by Playwright's
  built-in recorder. The folder is cleared at the start of each run.
- **Logs** — a JSON run report per session in `logs/`.
