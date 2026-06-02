# git-sage

> AI-powered commit message generator. Stage your changes, run `git-sage`, get a great commit message.

[![PyPI](https://img.shields.io/pypi/v/git-sage)](https://pypi.org/project/git-sage/)
[![Python](https://img.shields.io/pypi/pyversions/git-sage)](https://pypi.org/project/git-sage/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Install

```bash
pip install git-sage
```

Set one of:

```bash
export ANTHROPIC_API_KEY=sk-ant-...   # uses claude-sonnet-4-6
export OPENAI_API_KEY=sk-...          # uses gpt-4o-mini
```

## Usage

```bash
# Stage changes, then:
git add -A

# Preview the generated message
git-sage

# Generate and commit immediately
git-sage --commit

# Generate, review in your editor, then commit
git-sage --edit --commit
```

## Example

```bash
$ git add src/auth.py tests/test_auth.py
$ git-sage

feat: add JWT refresh token rotation with sliding expiration

Tip: run with --commit to use this message directly.
```

## Works with both Claude and OpenAI

`git-sage` checks for `ANTHROPIC_API_KEY` first, then `OPENAI_API_KEY`. No config file needed.

## Git alias (optional)

Add to `~/.gitconfig` for a one-keystroke workflow:

```ini
[alias]
  ai = !git-sage --commit
```

Then: `git add -A && git ai`

## License

MIT
