from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from scripts.acaf_ambigator import require_clean_baseline, snapshot_tracked
from scripts.acaf_meaning_matrix import snapshot_tracked as matrix_snapshot


def _repo(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    (root / "sub").mkdir(parents=True)
    (root / "README.md").write_text("tracked\n", encoding="utf-8")
    (root / "sub" / "rule.txt").write_text("tracked\n", encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)
    # run artifacts written after checkout: must never reach the fuzzed workspace
    (root / "acaf.json").write_text('{"leak": "retired wording"}\n', encoding="utf-8")
    (root / "sub" / "rule.txt").write_text("edited in working tree\n", encoding="utf-8")
    return root


@pytest.mark.parametrize("snapshot", [snapshot_tracked, matrix_snapshot])
def test_snapshot_excludes_untracked_run_artifacts(tmp_path: Path, snapshot) -> None:
    dest = tmp_path / "snap"
    snapshot(_repo(tmp_path), dest)
    assert not (dest / "acaf.json").exists()
    assert (dest / "README.md").is_file()
    assert (dest / "sub" / "rule.txt").read_text(encoding="utf-8") == "edited in working tree\n"


def test_failing_baseline_is_refused_not_scored(tmp_path: Path) -> None:
    with pytest.raises(RuntimeError, match="baseline fails"):
        require_clean_baseline(tmp_path, lambda _root: (True, "Rule 0 contract failed: leak"))
    require_clean_baseline(tmp_path, lambda _root: (False, "PASS"))
