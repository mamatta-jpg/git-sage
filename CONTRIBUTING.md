# Contributing to git-sage

Thanks for your interest in contributing!

## Getting started

```bash
git clone https://github.com/mamatta-jpg/git-sage
cd git-sage
pip install -e ".[dev]"
pytest tests/ -v
```

## Testing prompt changes

The core prompt lives in `git_sage/ai.py` inside `build_prompt()`. To test it against a real diff:

```bash
git add some_file.py
ANTHROPIC_API_KEY=sk-ant-... git-sage
```

## Running tests

```bash
pytest tests/ -v
```

## Pull requests

- Keep PRs focused — one change per PR
- All tests must pass
- If you change `build_prompt()`, add a test asserting the new behavior in `tests/test_prompt.py`

## Reporting a bad commit message

Open an issue with:
1. The git diff (redacted if needed)
2. The message that was generated
3. What you expected instead
