"""Tests that validate code blocks embedded in the lesson and slide Markdown files.

Each YAML and TOML fenced code block is extracted and parsed.  A parse error
means the snippet shown to learners is broken, so we want to catch that early.
"""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).parent.parent
MARKDOWN_DIRS = [REPO_ROOT / "lessons", REPO_ROOT / "slides"]

# Matches any fenced code block, capturing the language tag and body.
_FENCE_RE = re.compile(r"```(\w+)\n(.*?)```", re.DOTALL)


def _collect_all_blocks() -> tuple[list[tuple[str, int, str]], list[tuple[str, int, str]]]:
    """Walk every Markdown file once and return (yaml_blocks, toml_blocks).

    Each element is a list of (relative_path, block_index, block_text) tuples
    where block_index counts blocks of that language within the file.
    """
    yaml_blocks: list[tuple[str, int, str]] = []
    toml_blocks: list[tuple[str, int, str]] = []
    yaml_counters: dict[str, int] = {}
    toml_counters: dict[str, int] = {}

    for directory in MARKDOWN_DIRS:
        for md_file in sorted(directory.rglob("*.md")):
            rel = str(md_file.relative_to(REPO_ROOT))
            text = md_file.read_text(encoding="utf-8")
            for lang, body in _FENCE_RE.findall(text):
                if lang in ("yaml", "yml"):
                    yaml_counters[rel] = yaml_counters.get(rel, 0) + 1
                    yaml_blocks.append((rel, yaml_counters[rel], body))
                elif lang == "toml":
                    toml_counters[rel] = toml_counters.get(rel, 0) + 1
                    toml_blocks.append((rel, toml_counters[rel], body))

    return yaml_blocks, toml_blocks


def _block_id(val: tuple[str, int, str]) -> str:
    path, idx, _ = val
    return f"{path}::block{idx}"


YAML_BLOCKS, TOML_BLOCKS = _collect_all_blocks()


@pytest.mark.parametrize("path,idx,block", YAML_BLOCKS, ids=[_block_id(b) for b in YAML_BLOCKS])
def test_yaml_block_is_valid(path: str, idx: int, block: str) -> None:
    """Every YAML code block in the lessons/slides must be syntactically valid."""
    try:
        yaml.safe_load(block)
    except yaml.YAMLError as exc:
        pytest.fail(f"{path} block {idx}: invalid YAML — {exc}")


@pytest.mark.parametrize("path,idx,block", TOML_BLOCKS, ids=[_block_id(b) for b in TOML_BLOCKS])
def test_toml_block_is_valid(path: str, idx: int, block: str) -> None:
    """Every TOML code block in the lessons/slides must be syntactically valid."""
    try:
        tomllib.loads(block)
    except tomllib.TOMLDecodeError as exc:
        pytest.fail(f"{path} block {idx}: invalid TOML — {exc}")
