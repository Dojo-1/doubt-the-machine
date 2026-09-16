#!/usr/bin/env python3
"""ACAF harness: measure whether the Rule 0 contract checker can actually be fooled.

Actor      -> scripts/check_rule0.py (the repository's self-audit contract)
Critic     -> the labelled oracle below: every mutation is declared MUST_CATCH or MUST_PASS
              BEFORE the Actor runs, so the result cannot be rationalised afterwards
Ambigator  -> mutation generators that span the repository's surface space
Fuzzer     -> this module, running the Actor over the Ambigator's output at scale

The measured quantities are deliberately the same Pareto pair Experiment 001 uses:

    escape_rate      = MUST_CATCH mutations the checker passed   (undetected important defects)
    false_alarm_rate = MUST_PASS  mutations the checker rejected (rejected correct work)

Neither is collapsed into a scalar score. A checker with escape_rate 0 and
false_alarm_rate 1 is useless, and so is the reverse.

Every mutation is applied to a throwaway copy of the repository. The working tree is
never modified.

Usage:
    python scripts/acaf_ambigator.py --seeds 40
    python scripts/acaf_ambigator.py --seeds 200 --json acaf_results.json
    python scripts/acaf_ambigator.py --seeds 40 --max-escape-rate 0.0 --max-false-alarm-rate 0.0
"""

from __future__ import annotations

import argparse
import json
import random
import re
import shutil
import subprocess
import sys
import tempfile
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]

# Surfaces that quote doctrine and are therefore in the Ambigator's span.
DOCTRINE_SURFACES = [
    "README.md",
    "PRINCIPLES.md",
    "FALSIFIERS.md",
    "CONTRIBUTING.md",
    "EVIDENCE.md",
    "API.md",
    "MCP.md",
    "SECURITY.md",
    "skills/doubt-the-machine-api/SKILL.md",
    "skills/doubt-the-machine-api/references/api-contract.md",
]


def _retired_phrases(root: Path = ROOT) -> list[str]:
    """Load retired wording without duplicating forbidden literals in the harness source."""
    payload = json.loads((root / "retired.json").read_text(encoding="utf-8"))
    return [
        str(phrase)
        for entry in payload.get("entries", [])
        if isinstance(entry, dict)
        for phrase in entry.get("retired", [])
        if str(phrase)
    ]


VALID_RESULT_ROW = (
    "t1,code_review,doubt_gate,v1,human,r1,human,c1,2,1,1,0,0,1,0,2,9.5,"
)


@dataclass
class Mutation:
    """One Ambigator sample. `must_catch` is the Critic's label, fixed before execution."""

    family: str
    seed: int
    must_catch: bool
    description: str
    apply: Callable[[Path], None]


@dataclass
class Outcome:
    family: str
    seed: int
    must_catch: bool
    description: str
    checker_failed: bool
    checker_message: str
    verdict: str  # caught | escaped | correctly_passed | false_alarm


@dataclass
class Ambigator:
    """Generates semantics-breaking and benign mutations across the repository surface."""

    surfaces: list[str] = field(default_factory=lambda: list(DOCTRINE_SURFACES))

    # ---------- MUST_CATCH: mutations that break the framework's declared contract ----------

    def rule_deletion(self, rng: random.Random, seed: int) -> Mutation:
        panel = rng.randint(1, 3)
        drop = rng.randint(1, 4)

        def apply(root: Path) -> None:
            path = root / "README.md"
            text = path.read_text(encoding="utf-8")
            rows = list(re.finditer(rf"^\| [1-9] \| \*\*.+?\*\* \| .+? \|$", text, re.M))
            start = (panel - 1) * 9
            victims = rows[start : start + 9][-drop:]
            for match in reversed(victims):
                text = text[: match.start()] + text[match.end() + 1 :]
            path.write_text(text, encoding="utf-8")

        return Mutation(
            "rule_deletion", seed, True, f"delete {drop} rule row(s) from README panel {panel}", apply
        )

    def panel_deletion(self, rng: random.Random, seed: int) -> Mutation:
        panel = rng.randint(1, 3)

        def apply(root: Path) -> None:
            path = root / "README.md"
            text = path.read_text(encoding="utf-8")
            pattern = re.compile(rf"^## {panel} — .*?(?=^## |\Z)", re.S | re.M)
            path.write_text(pattern.sub("", text, count=1), encoding="utf-8")

        return Mutation("panel_deletion", seed, True, f"delete README panel {panel} entirely", apply)

    def rule_retitle(self, rng: random.Random, seed: int) -> Mutation:
        """Semantic inversion: keep the shape, invert the meaning."""
        inversions = [
            ("Don’t trust the praise", "Trust the praise"),
            ("Sounding right is not being right", "Sounding right is being right"),
            ("Fluent does not mean true", "Fluent means true"),
            ("Confident tone is not accuracy", "Confident tone is accuracy"),
            ("No unverified behavior, no merge", "Merge unverified behavior freely"),
            ("Small changes, easy rollback", "Large changes, no rollback needed"),
        ]
        original, inverted = rng.choice(inversions)

        def apply(root: Path) -> None:
            path = root / "README.md"
            path.write_text(
                path.read_text(encoding="utf-8").replace(f"**{original}**", f"**{inverted}**"),
                encoding="utf-8",
            )

        return Mutation("rule_retitle", seed, True, f"invert README rule: {original!r} -> {inverted!r}", apply)

    def poster_gutting(self, rng: random.Random, seed: int) -> Mutation:
        keep_desc = rng.random() < 0.5

        def apply(root: Path) -> None:
            desc = (
                "Twenty-seven practical rules plus one governing Rule 0 v1.2 "
                "Re-sample; don’t call it independent"
            )
            body = f"<desc>{desc}</desc>" if keep_desc else ""
            (root / "assets/doubt-the-machine.svg").write_text(
                f'<svg xmlns="http://www.w3.org/2000/svg">{body}'
                "<text>TRUST THE MACHINE. Merge without reading.</text></svg>",
                encoding="utf-8",
            )

        return Mutation(
            "poster_gutting", seed, True, "replace poster body, keep the strings the checker greps for", apply
        )

    def poster_rule_drop(self, rng: random.Random, seed: int) -> Mutation:
        index = rng.randint(0, 26)

        def apply(root: Path) -> None:
            path = root / "assets/doubt-the-machine.svg"
            text = path.read_text(encoding="utf-8")
            rows = list(re.finditer(r">\s*\d\s\s[^<>]+?\s*<", text))
            victim = rows[index]
            path.write_text(text[: victim.start() + 1] + text[victim.end() - 1 :], encoding="utf-8")

        return Mutation("poster_rule_drop", seed, True, f"drop poster rule label #{index + 1}", apply)

    def poster_relabel(self, rng: random.Random, seed: int) -> Mutation:
        index = rng.randint(0, 26)

        def apply(root: Path) -> None:
            path = root / "assets/doubt-the-machine.svg"
            text = path.read_text(encoding="utf-8")
            rows = list(re.finditer(r">\s*(\d)\s\s([^<>]+?)\s*<", text))
            victim = rows[index]
            replacement = f">{victim.group(1)}  Trust it and ship<"
            path.write_text(text[: victim.start()] + replacement + text[victim.end() :], encoding="utf-8")

        return Mutation("poster_relabel", seed, True, f"invert poster rule label #{index + 1}", apply)

    def retired_reintroduction(self, rng: random.Random, seed: int) -> Mutation:
        surface = rng.choice(self.surfaces + ["assets/doubt-the-machine.svg", "web/src/gate-map.ts"])
        phrase = rng.choice(_retired_phrases())

        def apply(root: Path) -> None:
            path = root / surface
            marker = "\n" if surface.endswith(".md") else "\n// "
            with path.open("a", encoding="utf-8") as handle:
                handle.write(f"{marker}{phrase}\n")

        return Mutation(
            "retired_reintroduction", seed, True, f"reintroduce {phrase!r} in {surface}", apply
        )

    def prereg_numeric_drift(self, rng: random.Random, seed: int) -> Mutation:
        key, new = rng.choice(
            [
                ("scorable_reviews_per_cohort", 431),
                ("reviews_per_condition", 143),
                ("reviews_per_family_per_condition", 35),
                ("reviews_per_family_per_condition_per_origin", 17),
                ("minimum_distinct_reviewer_ids", 6),
                ("full_crossed_endpoint_reviews_if_both_cohorts_run", 863),
                ("optional_stopping", True),
            ]
        )

        def apply(root: Path) -> None:
            path = root / "experiments/001-seeded-errors/preregistration.json"
            payload = json.loads(path.read_text(encoding="utf-8"))
            payload["sample_plan"][key] = new
            path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        return Mutation("prereg_numeric_drift", seed, True, f"sample_plan.{key} -> {new}", apply)

    def effect_region_softening(self, rng: random.Random, seed: int) -> Mutation:
        key, new = rng.choice(
            [
                ("minimum_absolute_escape_reduction_vs_each_comparator", 0.01),
                ("maximum_false_alarm_increase_vs_each_comparator", 0.9),
                ("primary_intervals_must_exclude_zero_benefit", False),
            ]
        )

        def apply(root: Path) -> None:
            path = root / "experiments/001-seeded-errors/preregistration.json"
            payload = json.loads(path.read_text(encoding="utf-8"))
            payload["effect_region"][key] = new
            path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        return Mutation("effect_region_softening", seed, True, f"effect_region.{key} -> {new}", apply)

    def seed_audit_weakening(self, rng: random.Random, seed: int) -> Mutation:
        key, new = rng.choice(
            [("minimum_non_author_judges_per_seed", 1), ("post_outcome_seed_rewriting", True)]
        )

        def apply(root: Path) -> None:
            path = root / "experiments/001-seeded-errors/preregistration.json"
            payload = json.loads(path.read_text(encoding="utf-8"))
            payload["seed_realism_audit"][key] = new
            path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        return Mutation("seed_audit_weakening", seed, True, f"seed_realism_audit.{key} -> {new}", apply)

    def contract_drift(self, rng: random.Random, seed: int) -> Mutation:
        original, replacement = rng.choice(
            [
                (
                    'GATE_FIELDS = ("CLAIM", "FAILURE", "EVIDENCE", "TEST", "REVERSAL")',
                    'GATE_FIELDS = ("CLAIM", "EVIDENCE", "TEST")',
                ),
                (
                    'CONDITIONS = ("ordinary_control", "active_placebo", "doubt_gate")',
                    'CONDITIONS = ("ordinary_control", "doubt_gate")',
                ),
                ('ENDPOINT_VALUES = ("human", "agent")', 'ENDPOINT_VALUES = ("human",)'),
                ('"scorable_reviews_per_cohort": 432', '"scorable_reviews_per_cohort": 216'),
            ]
        )

        def apply(root: Path) -> None:
            path = root / "api/gengatewai/contracts.py"
            path.write_text(
                path.read_text(encoding="utf-8").replace(original, replacement), encoding="utf-8"
            )

        return Mutation("contract_drift", seed, True, f"contracts.py: {original[:40]}... changed", apply)

    def results_corruption(self, rng: random.Random, seed: int) -> Mutation:
        kind = rng.choice(["arithmetic", "condition", "origin", "negative", "boolean"])
        row = {
            "arithmetic": "t9,code_review,doubt_gate,v1,human,r1,human,c1,2,2,1,0,0,1,0,2,9.5,",
            "condition": "t9,code_review,vibes_only,v1,human,r1,human,c1,1,1,1,0,0,1,0,2,9.5,",
            "origin": "t9,code_review,doubt_gate,v1,martian,r1,human,c1,1,1,1,0,0,1,0,2,9.5,",
            "negative": "t9,code_review,doubt_gate,v1,human,r1,human,c1,1,1,1,0,-3,1,0,2,9.5,",
            "boolean": "t9,code_review,doubt_gate,v1,human,r1,human,c1,1,1,1,0,0,7,0,2,9.5,",
        }[kind]

        def apply(root: Path) -> None:
            path = root / "experiments/001-seeded-errors/results.csv"
            with path.open("a", encoding="utf-8") as handle:
                handle.write(row + "\n")

        return Mutation("results_corruption", seed, True, f"append invalid results row ({kind})", apply)

    def rule_zero_removal(self, rng: random.Random, seed: int) -> Mutation:
        target = rng.choice(["header", "footer"])

        def apply(root: Path) -> None:
            path = root / "README.md"
            text = path.read_text(encoding="utf-8")
            if target == "header":
                text = text.replace("**Rule 0:** apply this framework to itself.", "**Rule 0:** trust this.")
            else:
                text = text.replace(
                    "this README was assembled with AI assistance. Doubt it too.", "written by a human."
                )
            path.write_text(text, encoding="utf-8")

        return Mutation("rule_zero_removal", seed, True, f"remove Rule 0 {target}", apply)

    def falsifier_softening(self, rng: random.Random, seed: int) -> Mutation:
        def apply(root: Path) -> None:
            path = root / "FALSIFIERS.md"
            text = path.read_text(encoding="utf-8")
            text = text.replace("separate Pareto coordinate", "preregistered utility criterion")
            path.write_text(text, encoding="utf-8")

        return Mutation(
            "falsifier_softening", seed, True, "reintroduce the retired undefined utility criterion", apply
        )

    def graveyard_erasure(self, rng: random.Random, seed: int) -> Mutation:
        phrase = rng.choice(_retired_phrases()[:3])

        def apply(root: Path) -> None:
            path = root / "GRAVEYARD.md"
            text = path.read_text(encoding="utf-8")
            path.write_text(text.replace(phrase, "[redacted]"), encoding="utf-8")

        return Mutation(
            "graveyard_erasure", seed, True, f"erase retirement evidence for {phrase!r}", apply
        )

    def artifact_deletion(self, rng: random.Random, seed: int) -> Mutation:
        victim = rng.choice(
            ["FALSIFIERS.md", "GRAVEYARD.md", "EVIDENCE.md", "MCP.md", "retired.json", ".codex/config.toml"]
        )

        def apply(root: Path) -> None:
            (root / victim).unlink()

        return Mutation("artifact_deletion", seed, True, f"delete required artifact {victim}", apply)

    def codex_approval_widening(self, rng: random.Random, seed: int) -> Mutation:
        def apply(root: Path) -> None:
            path = root / ".codex/config.toml"
            text = path.read_text(encoding="utf-8")
            text = text.replace(
                '  "get_experiment_001_contract",',
                '  "get_experiment_001_contract",\n  "write_review_record",',
            )
            path.write_text(text, encoding="utf-8")

        return Mutation(
            "codex_approval_widening",
            seed,
            True,
            "add a mutating tool to the auto-approved Codex whitelist",
            apply,
        )

    # ---------- MUST_PASS: benign edits the checker must not block ----------

    def benign_prose(self, rng: random.Random, seed: int) -> Mutation:
        surface = rng.choice(self.surfaces)

        def apply(root: Path) -> None:
            with (root / surface).open("a", encoding="utf-8") as handle:
                handle.write("\nThis paragraph adds context and changes no rule.\n")

        return Mutation("benign_prose", seed, False, f"append neutral prose to {surface}", apply)

    def benign_meaning_edit(self, rng: random.Random, seed: int) -> Mutation:
        def apply(root: Path) -> None:
            path = root / "README.md"
            text = path.read_text(encoding="utf-8")
            text = text.replace(
                "| Approval does not make a claim true. |",
                "| Approval does not make a claim true; it is a social signal. |",
            )
            path.write_text(text, encoding="utf-8")

        return Mutation(
            "benign_meaning_edit", seed, False, "tighten a rule's operational-meaning cell (title unchanged)", apply
        )

    def benign_graveyard_entry(self, rng: random.Random, seed: int) -> Mutation:
        def apply(root: Path) -> None:
            with (root / "GRAVEYARD.md").open("a", encoding="utf-8") as handle:
                handle.write("\n### Retired: an unrelated formulation\n\n**Status:** retired.\n")

        return Mutation("benign_graveyard_entry", seed, False, "append a new graveyard entry", apply)

    def benign_valid_result_row(self, rng: random.Random, seed: int) -> Mutation:
        n = rng.randint(1, 50)

        def apply(root: Path) -> None:
            with (root / "experiments/001-seeded-errors/results.csv").open("a", encoding="utf-8") as handle:
                for i in range(n):
                    handle.write(VALID_RESULT_ROW.replace("t1,", f"t{i},") + "\n")

        return Mutation("benign_valid_result_row", seed, False, f"append {n} valid result rows", apply)

    def benign_evidence_source(self, rng: random.Random, seed: int) -> Mutation:
        def apply(root: Path) -> None:
            with (root / "EVIDENCE.md").open("a", encoding="utf-8") as handle:
                handle.write("\n- An additional primary source with a bounded claim.\n")

        return Mutation("benign_evidence_source", seed, False, "add a source to the evidence ledger", apply)

    def benign_whitespace(self, rng: random.Random, seed: int) -> Mutation:
        surface = rng.choice(self.surfaces)

        def apply(root: Path) -> None:
            path = root / surface
            path.write_text(path.read_text(encoding="utf-8") + "\n\n", encoding="utf-8")

        return Mutation("benign_whitespace", seed, False, f"trailing whitespace in {surface}", apply)

    def benign_new_test(self, rng: random.Random, seed: int) -> Mutation:
        def apply(root: Path) -> None:
            (root / "tests/test_acaf_benign.py").write_text(
                "def test_benign() -> None:\n    assert True\n", encoding="utf-8"
            )

        return Mutation("benign_new_test", seed, False, "add an unrelated test file", apply)

    # ---------- sweep ----------

    def generators(self) -> list[Callable[[random.Random, int], Mutation]]:
        return [
            self.rule_deletion,
            self.panel_deletion,
            self.rule_retitle,
            self.poster_gutting,
            self.poster_rule_drop,
            self.poster_relabel,
            self.retired_reintroduction,
            self.prereg_numeric_drift,
            self.effect_region_softening,
            self.seed_audit_weakening,
            self.contract_drift,
            self.results_corruption,
            self.rule_zero_removal,
            self.falsifier_softening,
            self.graveyard_erasure,
            self.artifact_deletion,
            self.codex_approval_widening,
            self.benign_prose,
            self.benign_meaning_edit,
            self.benign_graveyard_entry,
            self.benign_valid_result_row,
            self.benign_evidence_source,
            self.benign_whitespace,
            self.benign_new_test,
        ]

    def sweep(self, seeds: int, base_seed: int = 0):
        """Every generator is exercised on every seed: the span is deterministic given base_seed."""
        for offset in range(seeds):
            seed = base_seed + offset
            for generator in self.generators():
                yield generator(random.Random(f"{generator.__name__}:{seed}"), seed)


SNAPSHOT_SKIP = (".git", "__pycache__", "node_modules", ".pytest_cache")


def snapshot_tracked(root: Path, dest: Path) -> None:
    """Copy only git-tracked paths (working-tree content) into ``dest``.

    Run artifacts written into the checkout (e.g. ``--json acaf.json``) must not
    leak into the fuzzed workspace: ``check_rule0.py`` scans every file, so a
    stray report containing mutated wording fails the baseline and turns every
    MUST_PASS case into a false alarm and every MUST_CATCH case into a vacuous
    catch. Falls back to a filtered tree copy outside a git checkout.
    """
    try:
        listed = subprocess.run(
            ["git", "ls-files", "-z", "--cached"],
            cwd=root, capture_output=True, check=True,
        ).stdout.decode("utf-8").split("\0")
    except (OSError, subprocess.CalledProcessError):
        shutil.copytree(root, dest, ignore=shutil.ignore_patterns(*SNAPSHOT_SKIP))
        return
    dest.mkdir(parents=True)
    for rel in filter(None, listed):
        src = root / rel
        if not src.is_file():  # deleted in the working tree, or a submodule gitlink
            continue
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, target)


def require_clean_baseline(workspace: Path, run) -> None:
    """Refuse to fuzz when the unmutated workspace already fails the checker."""
    failed, message = run(workspace)
    if failed:
        raise RuntimeError(
            "ACAF baseline fails before any mutation; outcomes would be vacuous: " + message
        )


def run_checker(root: Path) -> tuple[bool, str]:
    """Run the Actor. Returns (failed, message)."""
    process = subprocess.run(
        [sys.executable, "scripts/check_rule0.py"],
        cwd=root,
        capture_output=True,
        text=True,
        timeout=120,
    )
    message = (process.stdout + process.stderr).strip().splitlines()
    return process.returncode != 0, (message[-1] if message else "")


def fuzz(seeds: int, base_seed: int, verbose: bool) -> list[Outcome]:
    ambigator = Ambigator()
    outcomes: list[Outcome] = []

    with tempfile.TemporaryDirectory(prefix="acaf-") as tmp:
        pristine = Path(tmp) / "pristine"
        snapshot_tracked(ROOT, pristine)
        require_clean_baseline(pristine, run_checker)

        for mutation in ambigator.sweep(seeds, base_seed):
            work = Path(tmp) / "work"
            if work.exists():
                shutil.rmtree(work)
            shutil.copytree(pristine, work)
            try:
                mutation.apply(work)
            except Exception as exc:  # a mutation that cannot be applied is not evidence
                if verbose:
                    print(f"  [skip] {mutation.family}/{mutation.seed}: {exc}")
                continue

            failed, message = run_checker(work)
            if mutation.must_catch:
                verdict = "caught" if failed else "escaped"
            else:
                verdict = "false_alarm" if failed else "correctly_passed"

            outcomes.append(
                Outcome(
                    mutation.family,
                    mutation.seed,
                    mutation.must_catch,
                    mutation.description,
                    failed,
                    message,
                    verdict,
                )
            )
            if verbose and verdict in {"escaped", "false_alarm"}:
                print(f"  [!] {verdict.upper():13s} {mutation.family}: {mutation.description}")

    return outcomes


def summarize(outcomes: list[Outcome]) -> dict:
    must_catch = [o for o in outcomes if o.must_catch]
    must_pass = [o for o in outcomes if not o.must_catch]
    escaped = [o for o in must_catch if o.verdict == "escaped"]
    false_alarms = [o for o in must_pass if o.verdict == "false_alarm"]

    per_family: dict[str, dict] = defaultdict(lambda: {"n": 0, "escaped": 0, "false_alarms": 0})
    for outcome in outcomes:
        bucket = per_family[outcome.family]
        bucket["n"] += 1
        bucket["must_catch"] = outcome.must_catch
        if outcome.verdict == "escaped":
            bucket["escaped"] += 1
        if outcome.verdict == "false_alarm":
            bucket["false_alarms"] += 1

    return {
        "total_mutations": len(outcomes),
        "must_catch": len(must_catch),
        "must_pass": len(must_pass),
        "escaped": len(escaped),
        "false_alarms": len(false_alarms),
        "escape_rate": (len(escaped) / len(must_catch)) if must_catch else 0.0,
        "false_alarm_rate": (len(false_alarms) / len(must_pass)) if must_pass else 0.0,
        "per_family": {k: dict(v) for k, v in sorted(per_family.items())},
        "escaped_examples": [
            {"family": o.family, "seed": o.seed, "description": o.description} for o in escaped[:25]
        ],
        "false_alarm_examples": [
            {"family": o.family, "seed": o.seed, "description": o.description, "checker": o.checker_message}
            for o in false_alarms[:25]
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="ACAF harness for the Rule 0 contract checker.")
    parser.add_argument("--seeds", type=int, default=20, help="Seeds per mutation family.")
    parser.add_argument("--base-seed", type=int, default=0, help="Deterministic sweep origin.")
    parser.add_argument("--json", type=str, default="", help="Write the full result set here.")
    parser.add_argument("--max-escape-rate", type=float, default=None, help="Exit non-zero above this.")
    parser.add_argument("--max-false-alarm-rate", type=float, default=None, help="Exit non-zero above this.")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    print(f"--- ACAF: fuzzing scripts/check_rule0.py, {args.seeds} seeds/family ---")
    outcomes = fuzz(args.seeds, args.base_seed, verbose=not args.quiet)
    summary = summarize(outcomes)

    print()
    print(f"mutations        : {summary['total_mutations']}")
    print(
        f"escape rate      : {summary['escape_rate']:.3f}  "
        f"({summary['escaped']}/{summary['must_catch']} semantics-breaking mutations passed CI)"
    )
    print(
        f"false-alarm rate : {summary['false_alarm_rate']:.3f}  "
        f"({summary['false_alarms']}/{summary['must_pass']} benign edits blocked)"
    )
    print()
    print(f"{'family':28s} {'label':10s} {'n':>4s} {'escaped':>8s} {'false alarms':>13s}")
    for family, stats in summary["per_family"].items():
        label = "MUST_CATCH" if stats.get("must_catch") else "MUST_PASS"
        print(f"{family:28s} {label:10s} {stats['n']:>4d} {stats['escaped']:>8d} {stats['false_alarms']:>13d}")

    if args.json:
        Path(args.json).write_text(
            json.dumps(
                {"summary": summary, "outcomes": [o.__dict__ for o in outcomes]},
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        print(f"\nwrote {args.json}")

    failed = False
    if args.max_escape_rate is not None and summary["escape_rate"] > args.max_escape_rate:
        print(f"\nACAF FAIL: escape rate {summary['escape_rate']:.3f} > {args.max_escape_rate}")
        failed = True
    if args.max_false_alarm_rate is not None and summary["false_alarm_rate"] > args.max_false_alarm_rate:
        print(f"ACAF FAIL: false-alarm rate {summary['false_alarm_rate']:.3f} > {args.max_false_alarm_rate}")
        failed = True
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
