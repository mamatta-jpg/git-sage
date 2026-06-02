import pytest

from git_sage.ai import build_prompt, MAX_DIFF_CHARS

SAMPLE_DIFF = """\
diff --git a/auth.py b/auth.py
index abc1234..def5678 100644
--- a/auth.py
+++ b/auth.py
@@ -10,6 +10,12 @@ def login(user, password):
+    if not user or not password:
+        raise ValueError("Credentials required")
+
     token = generate_token(user)
     return token
"""


# --- build_prompt() ---

def test_returns_string():
    result = build_prompt(SAMPLE_DIFF, ["auth.py"])
    assert isinstance(result, str)


def test_non_empty():
    result = build_prompt(SAMPLE_DIFF, ["auth.py"])
    assert len(result.strip()) > 50


def test_contains_diff_content():
    result = build_prompt(SAMPLE_DIFF, ["auth.py"])
    assert "auth.py" in result or "Credentials" in result or "diff" in result.lower()


def test_includes_file_list():
    result = build_prompt(SAMPLE_DIFF, ["auth.py", "tests/test_auth.py"])
    assert "auth.py" in result


def test_handles_empty_files_list():
    result = build_prompt(SAMPLE_DIFF, [])
    assert isinstance(result, str)
    assert len(result.strip()) > 0


def test_handles_empty_diff():
    result = build_prompt("", ["README.md"])
    assert isinstance(result, str)


def test_handles_large_diff_truncation():
    large_diff = "+" + "x" * (MAX_DIFF_CHARS + 500)
    result = build_prompt(large_diff, ["big_file.py"])
    assert isinstance(result, str)


def test_prompt_mentions_commit():
    result = build_prompt(SAMPLE_DIFF, ["auth.py"])
    assert "commit" in result.lower()


def test_prompt_references_imperative_or_conventional():
    result = build_prompt(SAMPLE_DIFF, ["auth.py"])
    keywords = ["imperative", "feat", "fix", "conventional", "subject"]
    assert any(kw in result.lower() for kw in keywords)
