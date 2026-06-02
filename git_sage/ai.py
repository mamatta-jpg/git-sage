import os

MAX_DIFF_CHARS = 8000  # Truncate huge diffs to stay within token limits


def build_prompt(diff: str, files: list[str]) -> str:
    # TODO(human): Design the prompt that turns a git diff into a commit message.
    # This function receives the staged diff and a list of changed filenames.
    # Return a single string (the full prompt) to send to the AI.
    #
    # Things to consider:
    #   - Should you use a system prompt + user message, or a single string?
    #     (This wrapper sends one combined string, so keep it as one block)
    #   - Should you enforce conventional commits format (feat:, fix:, etc.)?
    #   - How much of the diff should you include? (hint: MAX_DIFF_CHARS is already applied below)
    #   - Should you tell the model to output ONLY the message, or explain its reasoning?
    #   - What tone/length constraints matter? (subject line ≤ 72 chars is a git best practice)
    pass


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
