from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_codeql_init_and_analyze_use_the_same_pinned_version() -> None:
    workflow = (ROOT / ".github" / "workflows" / "codeql.yml").read_text(encoding="utf-8")
    action_pins = re.findall(
        r"uses:\s*github/codeql-action/(?:init|analyze)@([0-9a-f]{40})",
        workflow,
    )

    assert len(action_pins) == 2
    assert action_pins[0] == action_pins[1]
