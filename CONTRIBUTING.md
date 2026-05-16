# Contributing to MaintainerCopilot

Thank you for your interest in contributing! This guide covers everything you need to get from zero to a merged PR.

---

## Development Environment

### Prerequisites

- Python 3.11+
- Docker + Docker Compose (for integration testing)
- A GitHub account with access to create a GitHub App (for full end-to-end testing)

### Setup

```bash
# Clone the repo
git clone https://github.com/your-org/maintainer-copilot.git
cd maintainer-copilot

# Create a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dev dependencies
pip install -r requirements-dev.txt

# Copy and configure environment
cp .env.example .env
# Edit .env — you need at minimum NVIDIA_API_KEY for AI features
```

---

## Running Tests

```bash
# Run all tests
pytest

# Run a specific test file
pytest tests/test_triage.py -v

# Run with coverage
pytest --cov=app --cov-report=term-missing
```

Tests use mocks for the GitHub API and NVIDIA NIM API — no real credentials are needed to run the test suite.

---

## Linting

```bash
# Check for issues
ruff check app/ tests/

# Fix auto-fixable issues
ruff check --fix app/ tests/
```

All PRs must pass `ruff check` with zero warnings.

---

## Project Structure

```
app/
├── agent/        # Agentic loop, tool definitions, prompts, safety guardrails
├── features/     # One file per feature (triage, reproduction, onboarding, pr_review, release_notes)
├── github/       # GitHub API client and authentication
├── config.py     # Settings loaded from .env
├── main.py       # FastAPI entry point
├── security.py   # Webhook signature verification
└── webhook.py    # Event router
```

---

## Adding a New Feature

1. Create `app/features/your_feature.py` with an async `run(data: dict) -> str` function.
2. Add a system prompt to `app/agent/prompts.py` — never inline prompts in feature files.
3. Wire the feature into `app/webhook.py` (add an event trigger or a `/copilot` command).
4. Add a feature flag to `app/config.py` and `.env.example`.
5. Write tests in `tests/test_your_feature.py` — mock the GitHub client and agent.
6. Update `README.md` with a description of the new feature.

---

## Code Style

- **Type hints** on every function signature.
- **Docstrings** on every class and public function — one concise sentence explaining the purpose.
- No bare `except:` — always catch specific exceptions.
- No hardcoded strings — use `app/config.py` or constants.
- All async functions properly `await`ed.
- `ruff check` passes with zero warnings.

---

## Submitting a Pull Request

1. Fork the repo and create a branch: `git checkout -b feature/my-feature`
2. Make your changes and add tests.
3. Ensure `pytest` and `ruff check` both pass.
4. Open a PR against `main` with a clear description of what changed and why.
5. Reference any related issues in the PR body.

A maintainer will review your PR, run it against a test repository, and merge it if everything looks good.

---

## Questions?

Open an issue with the `question` label, or drop a comment on an existing issue. MaintainerCopilot itself will help triage it!
