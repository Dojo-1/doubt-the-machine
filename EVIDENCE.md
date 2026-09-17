# Evidence and provenance

This repository is an operating discipline, not a claim of novelty over all prior work. These sources provide lineage, constraints, and counterevidence for important rules.

## Evidence map

| Repository claim | External evidence / lineage | What it supports | What it does **not** establish |
|---|---|---|---|
| Model agreement can follow user beliefs rather than truth | Sharma et al., *Towards Understanding Sycophancy in Language Models*, ICLR 2024 / arXiv:2310.13548 | Sycophancy is a real failure mode across evaluated assistants; user-aligned responses can be preferred over correct ones | That every model or every disagreement is sycophantic |
| Self-critique is not independent verification | Huang et al., *Large Language Models Cannot Self-Correct Reasoning Yet*, ICLR 2024 / arXiv:2310.01798 | Intrinsic self-correction without external feedback can fail or degrade reasoning on studied settings | That self-reflection is always useless |
| Iterative self-feedback can still improve some tasks | Madaan et al., *Self-Refine*, NeurIPS 2023 / arXiv:2303.17651 | Self-feedback can improve outputs on several evaluated tasks | That self-feedback constitutes independent evidence or guarantees correctness |
| Software assurance should use multiple verification mechanisms and risk-sensitive practice | NIST SP 800-218, *Secure Software Development Framework (SSDF)* | Provenance, review, testing, vulnerability response, and risk management belong in software assurance | That one fixed checklist is sufficient for all software changes |
| Claims should expose ways they could fail rather than only seek confirmation | Falsification and preregistration traditions in science; operationalized here as explicit kill conditions | The repository’s design choice to ask for falsifiers and preserve negative results | That the specific Doubt the Machine gate is empirically effective |
| Faithful copies of live claims can become stale after their source changes | Evolving Agents Labs public site and `lora-kernel` repository, inspected 2026-09-10 | A concrete mirror-drift counterexample: the site still said `specified · nothing built` / no `[ran]` while the project repository had later `[ran]` results from 2026-09-08 and 2026-09-09 | That duplicated text is generally unsafe, that the underlying experiments are invalid, or that this failure mode is common enough to justify a measured effectiveness claim |

## Primary links

- Sharma et al. (2024), **Towards Understanding Sycophancy in Language Models**  
  https://arxiv.org/abs/2310.13548  
  ICLR proceedings: https://proceedings.iclr.cc/paper_files/paper/2024/hash/0105f7972202c1d4fb817da9f21a9663-Abstract-Conference.html

- Huang et al. (2024), **Large Language Models Cannot Self-Correct Reasoning Yet**  
  https://arxiv.org/abs/2310.01798  
  OpenReview: https://openreview.net/forum?id=IkmD3fKBPQ

- Madaan et al. (2023), **Self-Refine: Iterative Refinement with Self-Feedback**  
  https://arxiv.org/abs/2303.17651

- NIST SP 800-218, **Secure Software Development Framework (SSDF) Version 1.1**  
  https://csrc.nist.gov/publications/detail/sp/800-218/final

- Evolving Agents Labs, **public site** (status surface inspected 2026-09-10)  
  https://evolvingagentslabs.github.io/

- Evolving Agents Labs, **lora-kernel** (later execution surface; commits/results from 2026-09-08 and 2026-09-09)  
  https://github.com/EvolvingAgentsLabs/lora-kernel

## Internal evidence levels

This repository uses a deliberately simple evidence vocabulary for its own claims:

- **P — proved/definitionally closed:** an exact logical or structural claim supported by an inspectable artifact.
- **M — measured:** a bounded empirical result with data, controls, and uncertainty.
- **H — hypothesis:** a testable claim not yet adequately measured here.
- **S — semantic/design:** a useful framing, architecture, slogan, or operational proposal.
- **R — retired:** a claim or formulation killed or narrowed by evidence or contradiction.

Current map:

| Object | Status | Reason |
|---|---|---|
| Five-question gate exists and is specified | P | Inspectable repository artifact |
| Evidence should be matched to claim type | S | Design principle with strong methodological lineage, not a theorem |
| Same-model critique is independent evidence | R | Explicitly rejected; common failure modes remain correlated |
| Framing invariance is a better diagnostic than disagreement count | H | Motivated by sycophancy evidence; not yet measured in this framework |
| Transformations can lose decision-relevant information, and live mirrors can drift from their source | S | Operational rule sharpened by a concrete public counterexample; prevalence and review benefit remain unmeasured |
| Doubt the Machine improves net review quality | H | Experiment 001 is preregistered but not yet executed |
| The framework is generally safer/better than ordinary review | H | Forbidden promotion until replicated measurements support a bounded claim |

## Citation policy

External references are **constraints and lineage**, not decorations. A cited paper supports only the bounded observation it actually studied. If later work contradicts a rule, update this file and `GRAVEYARD.md` rather than defending the wording.