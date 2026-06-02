import os

MAX_DIFF_CHARS = 8000  # Truncate huge diffs to stay within token limits


def build_prompt(diff: str, files: list[str]) -> str:
    file_list = "\n".join(f"- {path}" for path in files) if files else "- (unknown files)"
    return f"""You write excellent git commit messages.

Write a single commit message for the staged changes below.

Requirements:
- Output only the commit message, with no explanation, quotes, or code fences.
- Use imperative mood.
- Keep the first line as a concise subject line, ideally 72 characters or fewer.
- Prefer a conventional commit prefix when it clearly fits (for example: feat:, fix:, docs:, refactor:, test:, chore:), but do not force one if it would be misleading.
- If useful, include a blank line followed by a short body that explains the why or highlights important changes.
- Use the file list and diff to infer the main purpose of the change.
- Be specific and avoid vague subjects like 'update files' or 'misc changes'.

Changed files:
{file_list}

Diff:
{diff}
"""


def generate_message(diff: str, files: list[str]) -> str:
    truncated_diff = diff[:MAX_DIFF_CHARS] + ("\n[diff truncated]" if len(diff) > MAX_DIFF_CHARS else "")
    prompt = build_prompt(truncated_diff, files)

    if not prompt:
        raise RuntimeError("build_prompt() returned an empty string — implement it first.")

    if os.environ.get("ANTHROPIC_API_KEY"):
        return _call_claude(prompt)
    if os.environ.get("OPENAI_API_KEY"):
        return _call_openai(prompt)
    raise RuntimeError("Set ANTHROPIC_API_KEY or OPENAI_API_KEY in your environment.")


def _call_claude(prompt: str) -> str:
    import anthropic
    client = anthropic.Anthropic()
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text.strip()


def _call_openai(prompt: str) -> str:
    from openai import OpenAI
    client = OpenAI()
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content.strip()
