# Alumnium Tests

AI-driven UI test framework, built on
[Playwright](https://playwright.dev/python/), [Alumnium](https://alumnium.ai/)
and pytest. Runs on **Windows 10/11**.

## Requirements

- Windows 10/11
- Python 3.12
- [uv](https://docs.astral.sh/uv/) — install with `pip install uv` or `winget install astral-sh.uv`

## Step-by-step guide

### 1. Check prerequisites

You need Python 3.12 and uv. Check uv is available:

```powershell
uv --version
```

If that errors ("not recognized"), install uv first:

```powershell
pip install uv
```

### 2. Create / sync the virtual environment

`uv sync` reads `pyproject.toml`, creates the `.venv` folder if missing, and
installs all dependencies (pytest, playwright, alumnium, etc.) into it:

```powershell
uv sync
```

Then install the Chromium browser Playwright needs:

```powershell
uv run playwright install chromium
```

> **Note:** you don't manually activate the venv. `uv run <cmd>` automatically
> runs the command inside `.venv` for you.

### 3. Set up your API key (.env)

Create your local `.env` from the template and add your OpenAI key:

```powershell
copy .env.example .env
notepad .env
```

Make sure it contains a real key — a line like `OPENAI_API_KEY=sk-...`. Save and
close.

`.env` is gitignored — never commit real secrets.

### 4. Run the tests

All tests (headed — browser window visible):

```powershell
uv run pytest -v
```

All tests (headless — no browser window):

```powershell
$env:HEADLESS = "1"; uv run pytest -v
```

Just one scenario folder:

```powershell
uv run pytest tests/scenario_1 -v
```

A single test file (e.g. your new one):

```powershell
uv run pytest tests/scenario_1/testManyElements.py -v
```

### 5. Check the output

After a run:

- **Videos** — one `.webm` per test in the `videos/` folder, recorded by
  Playwright's built-in recorder. The folder is cleared at the start of each run.
- **Logs** — a JSON run report per session in the `logs/` folder.
