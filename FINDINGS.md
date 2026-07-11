# QUASAR v0.2 — Findings Log (private)

Every entry: claim, method, number, status. Newest first.

## F2 — Bures attention broadcast ratio ≈ 0.001 (2026-07-11)
Method: single-position pre-attention state transplant between inputs from
distinct Hamiltonians (broadcast_probe.py, n=30). Output shift at patched
position 0.0947; at other positions 0.0001.
Finding: the v0.1-trained QGT's attention carries essentially NO
cross-position information — each position computes near-independently.
Diagnosis: next-step prediction on these dynamics is positionally local;
attention was never forced to earn its keep.
Consequence: v0.2 needs tasks requiring cross-position integration (e.g.
infer global Hamiltonian properties from a trajectory). Broadcast ratio is
now a standing diagnostic. Falsifiable claim: on integration-demanding
tasks, a working Bures attention must raise this ratio by orders of
magnitude, or the mechanism is not pulling its weight.

## F1 — METHODOLOGY TRAP: full-state patching is vacuous (2026-07-11)
First mediation probe transplanted ENTIRE intermediate states and measured
mediation = +1.000 at every stage. This is mathematically forced: in a
strictly sequential network with no bypass pathway, the output is a
deterministic function of any full intermediate state. The probe could not
fail. (Same failure class as the v0.1 C3 rounding bug: a comparison that
agrees by construction.) Rule adopted: every intervention probe must have
a configuration in which it CAN return a null result, demonstrated before
its numbers are trusted. mediation_probe.py is kept as the documented
example of the trap; broadcast_probe.py is the corrected instrument.

# Milestones
1. M1 Analytical backprop through Bures attention (distance gradient
   already verified to ~1e-11; extend through attention softmax + FFN).
2. M2 Capacity scale-up (d_ff 48–96) -> retest C3. Public prediction:
   adaptive beats uniform once per-bin errors separate. Report either way.
3. M3 Cross-position task suite; broadcast ratio as the metric (from F2).
4. M4 Multi-qubit extension (d_model = 4^n - 1).

Release rule: nothing leaves this repo until its claims pass the v0.1
verification standard (floor, ceiling where provable, matched-budget
control, held-out data).

## F3 — M1 COMPLETE: analytical backprop, 633x speedup (2026-07-11)
Micro reverse-mode AD engine (backprop.py), fused geometric primitives,
shares model parameter arrays. V1 forward equivalence 5.6e-17; V2 gradient
vs central finite differences across all 135 params, worst abs 8.4e-11;
V3 633x per-step speedup (428ms -> 0.7ms), grows with param count;
V4 training decreases loss. Bug caught by V1: loss is mean SQUARED Bures
distance — initial reimplementation omitted the square (0.245 discrepancy,
flagged instantly). M2 (capacity scale-up + C3 retest) is unblocked.

## F4 — Articulation refuted at single-qubit scale; bottleneck localized (2026-07-11)
External proposal (adapted): auxiliary head predicting generating physics
(axis, w, g). Geometry says the task needs >=3 integrated positions.
Matched-budget experiment (m3_articulation.py, 400 steps/arm, 0.8s total):
P-A broadcast unchanged (0.0007); P-B no state-prediction gain (0.1464 vs
0.1471); physics head AT predict-mean floor (0.2224 vs 0.2191) — learned
nothing. Diagnosis test (m3b): 12-dim readout ALSO at floor -> readout-
bottleneck hypothesis refuted. Localized cause: all cross-position info
transits ONE 3-dim linear attention mix; cannot carry >=6 numbers of
relational structure. Converges with C3 + F2: the binding constraint is
residual width (d_model=3) and attention depth, NOT d_ff. M2 redefined:
depth sweep (stacked blocks) + multi-qubit d_model, both cheap post-M1.
External doc scorecard: strategies 1,2,4,5 broken/obsolete/premature;
strategy 3 tested and refuted at this scale.

## F5 — LUCID v0: channel layers, emergent CPTP, purity-preserving learning (2026-07-12)
A 9-param Bloch-map layer (lucid_v0.py/v0b.py), same data/budget as F4.
(1) EMERGENT PHYSICALITY: learned map is genuinely CPTP (Choi min eig
+0.031) with nothing enforcing it; random-matrix control -0.458.
(2) BEATS THE TRANSFORMER: holdout Bures^2 0.0566 vs 0.1464 for the
135-param QGT on identical data — explains F2 (the QGT only ever needed
the per-position map, and learned it worse).
(3) LOSS GEOMETRY DETERMINES THE LEARNED AGGREGATE: closed-form mean
channel is depolarizing with s=0.7960 (MC-confirmed 0.7956). MSE training
converges there (diag 0.808; scan eta*_MSE=0.795). Bures training instead
converges to the purity-preserving contraction (diag 0.925-0.93; scan
eta*_Bures=0.925). New quantitative result: Bures learning preserves
purity statistics; Euclidean learning averages directions.
Next: LUCID v1 — mixture-of-channels with Bures-attention gating for
per-trajectory channel INFERENCE (must beat the single-channel 0.0566 to
earn its parameters); interpretability = tomograph the dictionary atoms +
read the mixture weights. Plus Q-SEED: camera shot-noise entropy
(quantum-optical, Sanguinetti et al. PRX 2014 precedent) via termux-api
to physically seed the generator, with min-entropy estimation.
