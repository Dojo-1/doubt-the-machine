# Experiment 002 — Auditory transport and candidate holonomy

**Status:** preregistered hypothesis scaffold; no result has been run or promoted.

**Purpose:** apply `Doubt the Machine` to a mathematically attractive claim before allowing the language of holonomy, hypercomplex cognition, or non-duality to harden into belief.

```text
DOUBT -> MEASURE -> TEST -> REVERT -> REPEAT
```

This experiment begins from a deliberately narrowed claim:

> Auditory processing may contain reproducible path-dependent transport structure between heterogeneous representational states. A holonomy interpretation is admissible only if a loop-sensitive invariant predicts held-out observations beyond matched conventional dynamical controls and survives representation attacks.

It does **not** preregister or imply any of the following:

- sound and mind are the same physical vibration;
- neural dynamics are a lossless continuation of acoustic pressure waves;
- perceptual path dependence is automatically geometric holonomy;
- noncommutativity implies quaternionic, octonionic, Clifford, or other hypercomplex necessity;
- a useful mathematical model of auditory processing establishes a theory of consciousness;
- richer geometry may be introduced after failure merely to rescue the interpretation.

## Tick High — frozen claim ledger

| ID | Claim | Initial status | Promotion requirement | Kill / retirement condition |
|---|---|---:|---|---|
| A0 | `sound vibration == neural vibration` | R | none | already rejected as a category error between heterogeneous physical carriers |
| A1 | auditory processing can show order/history dependence | H | reproducible held-out effect with defined task and uncertainty | no effect beyond noise / preprocessing artifact |
| A2 | a learned transport model can expose loop-dependent residual structure | H | preregistered loop statistic stable across seeds and held-out sequences | residual disappears under identity/no-op or representation controls |
| A3 | the residual is usefully modeled as candidate holonomy | H | outperforms matched real-valued dynamical baselines on held-out prediction **and** survives gauge/reparameterization attacks | matched ordinary state-space/RNN model explains the effect equally well, or the score is representation-sensitive |
| A4 | hypercomplex local algebra adds discriminating value | H | capacity/compute-matched held-out gain or invariant unavailable to simpler controls | no reproducible gain after parity matching |
| A5 | `mind is a polyholonomic ecology` | S | outside the scope of this experiment | may remain semantic even if A1-A4 survive |

`A0` is intentionally preserved as a retired formulation. The point is to prevent a poetic sentence from silently returning later as a physical claim.

## Objects

Do not begin with one global latent vector and then rename it a manifold. The experiment distinguishes at least these typed surfaces:

- `X_stimulus`: stimulus / sequence description;
- `X_local`: locally decoded or short-timescale response state;
- `X_context`: longer-timescale contextual state;
- `X_observation`: measured neural or behavioral response;
- `[R]_transport`: residual after a declared forward/return transport pair.

The implementation may use ordinary arrays internally. Type distinction is semantic and operational: transformations, units, clocks, and admissible comparisons must be declared rather than silently assumed equivalent.

## Candidate transport object

For context/action labels `a, b, ...`, learn or estimate transports

```text
T_a : X_context -> X_context
```

or, when source and destination types differ,

```text
T_ab : X_a -> X_b
```

A closed context path `gamma = (a1, ..., ak)` induces

```text
PT_gamma = T_ak o ... o T_a1
```

and a loop defect relative to the declared starting state:

```text
D_gamma(x) = d(x, PT_gamma(x)).
```

A non-zero `D_gamma` is **not** sufficient evidence for holonomy. Memory, hysteresis, nonlinear recurrence, adaptation, model misspecification, hidden state, or preprocessing can all generate path dependence.

## Primary comparison

The holonomy interpretation is eligible for promotion only if its preregistered statistic contributes held-out predictive information beyond all of the following matched controls:

1. linear real-valued state-space model;
2. nonlinear real-valued recurrent model;
3. higher-order real model with comparable interaction order;
4. dynamic/context-dependent real model with comparable topology or gating freedom;
5. shuffled transition labels;
6. shuffled temporal order subject to task-valid constraints;
7. identity/no-op loops;
8. alternate latent bases / invertible reparameterizations.

Hypercomplex variants are evaluated **after** the real-valued controls, not before them.

## Representation attack

A useful loop observable must not be an artifact of one latent basis.

For admissible invertible transforms `G`, compare the conclusion under

```text
z' = G(z)
```

and the corresponding transported operators. Exact numeric equality is not required unless the statistic is designed to be invariant, but the experiment's success/failure conclusion must be stable under the preregistered family of representation changes.

If a semantically equivalent identity insertion or invertible reparameterization flips the conclusion, retire the stronger geometric interpretation.

## Resource parity

For model comparisons report separately:

- trainable parameter count;
- training examples / sequence exposure;
- optimizer and tuning budget;
- wall-clock training and inference time;
- peak memory where available;
- random seeds;
- preprocessing shared or unique to each model.

A richer model does not win merely by receiving more capacity, tuning, or oracle information.

## Required raw outputs

Before aggregation, preserve:

- per-seed held-out predictive score;
- per-loop raw defect values;
- identity/no-op loop defects;
- shuffled-control defects;
- representation-attack results;
- parameter, time, and memory budgets;
- failed runs and exclusions with reasons.

Do not clip loop defects into an accepted range before evaluating a kill condition.

## Decision logic

### Promote A1 only if

Order/history dependence is reproducible on held-out data with uncertainty that excludes the preregistered negligible-effect region.

### Promote A2 only if

Loop-sensitive residual structure survives identity/no-op, shuffle, seed, and held-out controls.

### Promote A3 only if

A loop/transport formulation adds held-out predictive value beyond matched conventional dynamical controls **and** the conclusion survives representation attacks.

### Promote A4 only if

A hypercomplex model yields a reproducible, parity-matched held-out advantage or exposes a preregistered invariant that the matched real-valued models cannot reproduce.

### Never promote A5 from this experiment

Even a successful auditory transport model does not establish that mind or consciousness is literally a polyholonomic ecology.

## Stop rule

If A3 is killed, stop geometric escalation. Do **not** introduce a higher algebra, gerbe, sheaf, higher category, extra dimension, or new hidden variable solely to rescue the holonomy interpretation.

If A4 is killed, retain any useful transport result and retire the hypercomplex necessity claim.

A failed experiment may still leave a useful ordinary dynamical model. Preserve the measurement; retire only the interpretation that failed.

## Independent-witness boundary

The authoring model may propose code, metrics, and analyses, but it cannot promote its own claim from those artifacts alone. At least one promotion witness must differ materially in data, code path, assumptions, or authorship.

Candidate witnesses include:

- a held-out dataset not used to design the metric;
- an independently written baseline implementation;
- independent reproduction of the analysis;
- a reviewer who can inspect raw data and preregistered gates.

Repeated self-critique by the same model is useful debugging, not independent replication.

## Files

- `preregistration.json` — machine-readable frozen hypotheses, metrics, controls, kill conditions, and promotion rules.
- future `results.csv` — raw bounded measurements only after execution.
- future `RESULTS.md` — interpretation written only after raw results exist.

## Current evidence map

| Object | Status |
|---|---:|
| typed auditory transport ontology | S |
| path/order dependence in the selected dataset | H until measured here |
| loop-defect statistic | P as a definition once implementation is frozen |
| loop defect is geometric holonomy | H |
| hypercomplex necessity | H |
| mind as polyholonomic ecology | S |

No empirical promotion has occurred by adding this experiment scaffold.