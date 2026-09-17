# Graveyard

A framework that says “revert when it fails” should preserve the evidence that caused reversals.

This file records formulations that were removed, weakened, or replaced. A graveyard entry is not an embarrassment; it is evidence that Rule 0 has been exercised.

## 2026-08-30 — first explicit self-audit

### Retired: “Count how often it disagrees with you”

**Why it failed:** raw disagreement is not evidence. Optimizing for disagreement can create reverse sycophancy or performative contrarianism.

**Replacement:** **Test framing invariance** — ask materially equivalent questions under supportive, opposing, and neutral framing and check whether conclusions track evidence rather than the user stance.

**Status:** retired as a general-purpose diagnostic.

---

### Retired: “No test, no merge”

**Why it failed:** the repository itself says evidence is claim-relative. Runtime tests are appropriate for behavioral claims, but documentation, proofs, metadata, provenance changes, and some configuration changes require different evidence.

**Replacement:** **No unverified behavior, no merge** — match the evidence to the claim made by the change.

**Status:** retired as an absolute formulation.

---

### Retired: “Own every changed line”

**Why it failed:** it expresses responsibility but scales poorly as an operational rule for high-throughput agentic changes. Exhaustive line inspection can become ceremonial while important behavioral invariants remain underspecified.

**Replacement:** **Own every changed behavior** — specify invariants, inspect risk-bearing paths directly, test changed behavior and failure paths, preserve provenance, and sample lower-risk generated surfaces when exhaustive human inspection is not credible.

**Status:** narrowed and replaced; direct line review remains appropriate when risk or scale warrants it.

---

### Retired: `uncertainty × consequence × irreversibility`

**Why it failed:** written as a multiplication, the expression implied a quantitative model without defined units, calibration, or a justified multiplicative relationship.

**Replacement:** verification effort should **increase with uncertainty, consequence, and irreversibility**. Quantitative policies must define domain-specific axes and thresholds explicitly.

**Status:** pseudo-equation retired; qualitative ordering retained.

---

### Retired: three local “Rule 0” rows

The exact retired poster labels were:

- `0  Doubt this list too`
- `0  Doubt the compression`
- `0  Test this list too`

**Why it failed:** the README had one global Rule 0 plus a separate `0` row in each panel, making “Rule 0” ambiguous and visually padding a framework that emphasizes compression.

**Replacement:** one global Rule 0, with short unnumbered reflexive checks under each panel.

**Status:** retired as numbering, preserved as behavior.

## 2026-08-30 — external peer-review hardening

### Retired: poster drift as an acceptable compression difference

**Failure mode:** the v1.1 SVG still distributed three formulations that the canonical README and this graveyard had already retired. The CI contract inspected README and correction history but not the most shareable artifact.

**Evidence / counterexample:** direct inspection of `assets/doubt-the-machine.svg` found “Count disagreement”, “No test, no merge”, “Own every changed line”, and the retired local Rule-0 numbering after those formulations had been removed from the README.

**Replacement:** poster v1.2 uses the canonical replacements, preserves the re-sampling/non-independence caveat, and CI now evaluates poster surfaces through `retired.json`.

**Status:** corrected implementation drift.

---

### Retired: two-arm Experiment 001 as sufficient evidence for the specific gate

**Failure mode:** ordinary review versus the Doubt gate cannot distinguish the gate’s epistemic content from generic slowing-down, attention, or Hawthorne effects.

**Replacement:** add an equal-effort five-field active placebo (`TASK / SUMMARY / DETAILS / ALTERNATIVE / DECISION`) and require the Doubt gate to outperform both comparators.

**Status:** original causal interpretation retired; three-arm interpretation preregistered before data collection.

---

### Retired: undefined “utility analysis” as a kill condition

**Failure mode:** no preregistered exchange rate existed between escaped defects and review minutes, leaving the decision boundary open to post-hoc choice.

**Replacement:** keep important-defect escape, false alarms, and review time as separate coordinates. Pin a minimum 10-point escape-rate improvement and maximum 10-point false-alarm penalty; report review-time cost without inventing a scalar utility after seeing results.

**Status:** retired as an undefined decision rule.

---

### Retired: open-ended Experiment 001 sample size

**Failure mode:** no fixed N, reviewer count, or optional-stopping rule made a negative or positive result difficult to interpret.

**Replacement:** exactly 216 scorable task reviews per cohort, 72 per condition, 18 per task family per condition, at least 12 reviewer IDs, no outcome-driven extension. If uncertainty remains too wide, report inconclusive under a new preregistration rather than extending the same run.

**Status:** retired before result collection.

## 2026-08-30 — tock-003 endpoint-factor hardening

### Retired: single-origin Experiment 001 sample plan

**Failure mode:** the 216-review cohort plan fixed the reviewer side but did not record whether the artifact under review came from the human side or the AI/agent side. A positive result could therefore hide whether the gate helped on human artifacts, agent artifacts, or only one endpoint pairing.

**Replacement:** keep the three review conditions unchanged, add `artifact_origin` as a crossed `human | agent` factor, and collect exactly 432 scorable task reviews per reviewer cohort: 144 per condition, 36 per task family per condition, and 18 per task family per condition per artifact-origin cell. If both reviewer cohorts run, the full crossed-endpoint plan contains 864 scorable reviews.

**Status:** superseded before result collection; measurement design changed, rule content unchanged.

## 2026-08-31 — tock-005 decidability correction

### Retired: confirmatory interpretation of Experiment 001's fixed-N sample

**Failure mode:** the primary estimand is per important seeded defect, but the preregistration fixed task-review counts rather than the number of important defects contributed by each task. Before any result existed, it also did not supply an empirically grounded baseline escape probability or reviewer/matched-task dependence estimate. The fixed 432-review cohort therefore had **unknown confirmatory decidability**; the repository could not honestly claim that the design was powered to promote or kill the effectiveness hypothesis.

**Evidence / counterexample:** the adversarial audit identified that the denominator for the primary contrast was not fixed and that power depended materially on unstated baseline/ICC/defects-per-task assumptions. The audit's illustrative power numbers were assumption-dependent; the closed finding is the missing planning quantities, not a specific numerical power verdict. At amendment time `results.csv` still contained only its header, so no outcome had been inspected.

**Replacement:** preserve `preregistration.json` byte-for-byte and add the prospective `amendment-2026-08-31-pilot.json`. Experiment 001 remains a fixed-N randomized three-arm, two-origin **design pilot** used to estimate the realized important-defect denominator, baseline arm/family/origin rates, reviewer/matched-task dependence, false alarms, review cost, and realism retention. It cannot promote or kill the H-level effectiveness claim. A separate powered replication must be preregistered from frozen pilot planning estimates before replication outcomes exist.

**Reversal of the replacement:** if a future independent design audit shows that the original fixed-N protocol had a valid confirmatory power argument using only quantities frozen before the 2026-08-31 amendment, record that evidence and supersede this pilot-only interpretation explicitly; do not silently rewrite the amendment or original preregistration.

**Status:** confirmatory interpretation superseded prospectively before result collection; original preregistration preserved as correction history.

## 2026-09-01 — tick: single-comparator kill condition #1

### Retired: “catches no more seeded important defects than ordinary review” as the whole no-detection-benefit test

**Failure mode:** Falsifier #1 (“No detection benefit”) named only ordinary review, but Experiment 001 is a three-arm design whose promotion policy and `preregistration.json` effect region require the Doubt gate to outperform **both** ordinary review and the equal-effort active placebo. As worded, a gate that beat ordinary review but merely matched the active placebo — a benefit attributable to generic forced deliberation rather than the gate’s epistemic content — would not trip the kill condition, yet also could not be promoted. That asymmetry is a place where a failed result could be rescued.

**Evidence / counterexample:** the promotion policy in `FALSIFIERS.md` requires a preregistered baseline comparison; the 2026-08-30 three-arm hardening entry above requires the gate to “outperform both comparators”; and `preregistration.json` fixes the effect region with `minimum_absolute_escape_reduction_vs_each_comparator` and `maximum_false_alarm_increase_vs_each_comparator`. Direct inspection.

**Replacement:** falsifier #1 now trips when the gate catches no more important defects than ordinary review **or** the active placebo within uncertainty, making non-detection symmetric with the both-comparators promotion rule.

**Status:** replaced; kill-condition scope tightened, no active rule reworded.

**Reversal of the replacement:** if a future independent audit shows the active-placebo requirement was already fully carried by falsifiers #2/#5 or the promotion policy, restore the single-comparator wording and record the reason here.

## Machine-readable retirement source

`retired.json` is the machine-readable ledger used by CI to prevent retired wording from reappearing on declared public surfaces. This human-readable graveyard preserves the reasons, evidence, and replacements.

## Entry template

```text
Date:
Rule / claim retired:
Failure mode:
Evidence / counterexample:
Replacement, if any:
Status: weakened | replaced | retired
Reversal of the replacement:
```
