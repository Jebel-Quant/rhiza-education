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


def _collect_code_blocks(lang: str) -> list[tuple[str, int, str]]:
    """Return a list of (relative_path, block_index, block_text) for *lang*."""
    pattern = re.compile(rf"```{lang}\n(.*?)```", re.DOTALL)
    results: list[tuple[str, int, str]] = []
    for directory in MARKDOWN_DIRS:
        for md_file in sorted(directory.rglob("*.md")):
            rel = md_file.relative_to(REPO_ROOT)
            text = md_file.read_text(encoding="utf-8")
            for idx, block in enumerate(pattern.findall(text), start=1):
                results.append((str(rel), idx, block))
    return results


def _block_id(val: tuple[str, int, str]) -> str:
    path, idx, _ = val
    return f"{path}::block{idx}"


YAML_BLOCKS = _collect_code_blocks("yaml") + _collect_code_blocks("yml")
TOML_BLOCKS = _collect_code_blocks("toml")


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
