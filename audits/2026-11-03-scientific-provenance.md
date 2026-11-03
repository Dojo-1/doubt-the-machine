# Scientific provenance: a bounded Rule 0 audit

**Tock / verification record — 2026-11-03.** No new active rules, effectiveness claims, or experimental results. This is a worked audit, not an AI-authorship detector or an accusation about any researcher.

## Verdict

The repository already states the correct boundary: model agreement, human/agent labels, and completed review forms do not establish independent evidence. Its running gate deliberately does **not** assess evidence substance. The remaining vulnerability is *lineage opacity*: a model may generate the question, literature comparison, proposed method, tests, ablation plan, and explanation, after which a human can rewrite the manuscript. Their different final presentations do not constitute independent origins. Equally, model-assisted design does not invalidate an independently replicated finding. **Scientific validity and intellectual provenance are different claims requiring different witnesses.**

## Freeze the claim before improving it

Claim under challenge: **“A polished paper containing prior-work comparisons, theory, ablations, and human-presented prose is evidence that the underlying research ideas were independently human-originated.”**

- Status before: **H**, unsupported by the artifact types named in the claim.
- Scope: scientific and engineering research narratives; no inference about a particular author's conduct.
- Strongest correction: publication artifacts can support statements about methods, reported measurements, and, with independent replication, scientific results. They cannot ordinarily identify the origin of ideas.
- Forbidden promotion: AI-generated or AI-paraphrased authorship must not be inferred from style, method recombination, reviewer identity, or the mere existence of ablations.

## Claim-to-artifact ledger

| Claim | Status | Artifact / observation | Audit result |
|---|---|---|---|
| The five-question gate exists | P | README and api/gengatewai/service.py | Specified and instantiated; not proof of effectiveness |
| The API verifies substantive independence | R (strong interpretation) | gate_substance.py and service.py | It explicitly sets gate_substance_assessed=False; warnings are heuristics |
| Human/agent labels alone certify independence | R | tests/test_independence_boundary.py | The existing tests correctly reject this shortcut |
| A model-generated prior-work comparison is necessarily false | R | Logical counterexample: it may accurately cite independent measurements | Origin of narrative and correctness of the cited data are distinct |
| A model-generated prior-work comparison is an independent witness by itself | R | Same evidence-production path may be reused | Requiring actual source/instrument lineage is essential |
| Doubt the Machine improves net research-review outcomes | H | Experiment 001 is a design pilot with no executed confirmatory replication | Cannot promote |
| A particular paper's ideas originated with AI and were human-paraphrased | H | Requires process provenance; none collected in this audit | Remains unknown |
| A method's reported runtime is an independent speedup over matched sampling | H until controlled | Baseline, data budget, tuning, preprocessing, wall time, seeds | Headline full-data comparison alone does not establish incremental benefit |

Here P is inspectable structural fact, H an unresolved hypothesis, R a retired overstrong inference. S (design) and M (bounded measurement) apply elsewhere in the repository; no new M claim is created here. Retiring an *inference* above does not accuse the repository of having asserted it.

## Concrete self-audit of this repository

The precise live path is api/gengatewai/service.py -> ceremony_warnings in api/gengatewai/gate_substance.py. The EVIDENCE_ANCHOR expression notices URLs, command-like words, paths, and numerals. Thus a fabricated “pytest -q: 21 passed” can avoid the missing-anchor warning. **This is not a failed truth classifier**, because the documented API claims only cheap ceremonial warnings and always says the substance has not been assessed. The failure would be downstream if a caller treated “no warning” as verified evidence.

The test suite deliberately checks this distinction in tests/test_gate_substance.py. The human/agent pairing tests in tests/test_independence_boundary.py correctly preserve the provenance warning for every origin/reviewer combination. However, neither endpoint records a causal chain for the generation of the hypothesis, design, benchmark, measurements, and interpretation. That is a scope gap, not a silently proven feature.

ACAF.md transparently labels its original mutation tests as same-development-loop evidence. Experiment 001 openly remains a design pilot. The repository therefore does **not** warrant promotion to “independently validated effective scientific reviewer.” This audit adds no numerical effectiveness claim. The open governance issue #19 also describes branch-rule enforcement that needs direct verification; branch-rule prose is not enforcement.

## Worked paper example: CluSTER (bounded, not a full re-review)

Primary bibliographic records:
- arXiv version: https://arxiv.org/abs/2609.12584
- EMNLP 2026 proceedings: https://aclanthology.org/2026.emnlp-main.342/
- Published code: https://github.com/kaist-dmlab/CluSTER

The accessible arXiv abstract reports an **up-to 69.6%** training-time reduction, whereas the proceedings abstract reports **64.6%**. This is a demonstrable **version-dependent claim**, not evidence of impropriety. A rigorous comparison must name the version, denominator, baseline, and experimental setting. Both abstracts originate from the same research work; they are not independent replications of one another.

The technique is presented as a combination of gradient-based clustering, balanced selection/allocation, and weighted aggregation. Combining prior ideas may be useful engineering. It is not, without a further theorem or experiment, evidence either of strong conceptual originality **or** of machine-originated authorship.

### Exact toy counterexample: cluster-size weighting cannot generally undo within-cluster selection

This is a mathematical test of a *possible reasoning bridge*, not a statement that the CluSTER code necessarily commits the error. At one fixed parameter state, let a cluster contain scalar per-example gradients:

~~~text
g = (0, 0, 10)
full cluster mean = 10 / 3
select the one farthest from the cluster mean -> 10
selected cluster mean = 10
difference = 10 - 10/3 = 20/3
~~~

Multiplying either mean by the same cluster-proportion weight does not cancel the difference. Consequently, a proof of unbiasedness for **uniform random within-cluster sampling** does not automatically prove unbiasedness for a **deterministic peripheral subset**. If the paper's actual estimator applies a valid inclusion-probability correction, samples uniformly, or proves a different target quantity, this objection must be revised or retired. The precise theorem and source code must be checked before attributing this mismatch to the authors.

The small arithmetic is independently inspectable; the paper-specific mapping and empirical consequences are **not** independently established in this audit.

### Separate what an artifact can and cannot witness

| Artifact | Could support | Cannot by itself establish |
|---|---|---|
| Literature comparison | References and method contrasts after source checking | Whether the model or human first identified the connection |
| Formal proposition | A theorem under its actual assumptions, if correctly checked | Whether implementation satisfies those assumptions |
| A numerical ablation | Reported effect on its tested setup, if logs and code agree | Generality, causality absent controls, or intellectual provenance |
| Human-authored final prose | Human communication and interpretation | Human origination of every underlying idea |
| Conference acceptance | External editorial/peer-review process | Independent replication of the reported experiments |
| Independent reimplementation and held-out data | Reproduced bounded performance effects | The identity of whoever originated the initial idea |

**Independence is claim-relative, not a global badge.** A measured hardware run can supply evidence about performance even if its experimental design was suggested by a model. It does not thereby testify to human authorship. Conversely, an independently written paper description cannot validate fabricated raw measurements.

## Round-trip / where the meaning can drift

1. Requirement: decide whether the engineering result is useful, novel, valid, and who conceived it (four separate questions).
2. Formalization: define separate observables and witnesses for method novelty, measured benefit, theoretical adequacy, and authorship provenance.
3. Implementation: inspect the actual selection and gradient-update paths, not only their prose description.
4. Tests: distinguish self-authored demonstrations from independent oracles; include exact counterexamples and benign controls.
5. Measurements: preserve random-selection comparators, same data/compute budget, preprocessing cost, seeds, raw scores, confidence intervals, and exclusions.
6. Interpretation: promote at most the measured bounded effect; do not infer author origin from benchmark performance.
7. Return: ask whether the original four questions were answered individually. If not, preserve their unresolved remainder.

## One bounded next test (NOT executed here)

- **Object:** the published source version, implementation commit, and one explicitly chosen gradient/selection claim.
- **Prediction to scrutinize:** the practical selected-gradient estimator matches the expectation asserted by its theoretical justification under its actual selection policy.
- **Primary observation:** selected gradient minus full-cluster gradient on a tiny known-answer dataset at a fixed model state, before normalization or clipping.
- **Controls:** uniform within-cluster draw; deterministic peripheral draw; equal size-weighting; any implemented probability correction; same samples and state.
- **Representation attack:** reorder samples and permute cluster labels; an exact substantive conclusion should not depend on these.
- **Kill condition:** an explicit valid correction or different theorem target eliminates the alleged theory-to-implementation gap. Record this as a negative finding, not a defeat to conceal.
- **Stop condition:** do not infer real-world model accuracy, overall speedup, intent, or AI authorship from the toy result.
- **Promotion rule:** only after checking paper and code may the finding be called a verified implementation mismatch; only a separate reproduction can establish performance effects.

For a real performance test, preregister a matched-data-budget random baseline, selection-overhead-inclusive wall clock, held-out quality, and uncertainty across independent runs. The existing Experiment 001 stop rule still applies: do not initiate a new broad effectiveness experiment to chase this example.

## Independent witness and correction history

**None collected here.** The text, worked example, and structural tests of this audit are AI-assisted and form a correlated construction. They are not an external reproduction, source-code execution, or independent peer review. This is an inspectable hypothesis and correction record, not validation of the broader framework.

Corrections worth retaining:
- **Retired:** treating polished ablations and comparisons as evidence against substantial AI participation.
- **Retired:** treating model-written comparisons as automatically invalid.
- **Preserved:** originality of ideas, correctness of claims, and independence of validation are separate dimensions.
- **Unresolved:** the actual provenance of any particular paper's ideas, and whether a particular benchmark survives independent reproduction.

**Rule 0 applies to this document too.** Its falsifier is straightforward: show an authentic independent provenance record, an error in the cited source version, a valid theorem-to-code bridge we overlooked, or an experiment where this audit procedure causes more false accusations or wasted work than it prevents. Narrow or retire the relevant conclusion, keeping the correction visible.

## Snapshot and reproducibility boundary

Repository inspected on 2026-11-03. At inspection, main was 1ca72f63a3da7fe63eee9f1927b94e66a07eba8e and dev was cbdd17f727e4ba629a673d65283373ff7315cdf6. No paper experiment, third-party implementation replay, or independent reproduction was executed for this audit. The accompanying manifest enumerates the exact evidential gaps rather than filling them with generated certainty.
