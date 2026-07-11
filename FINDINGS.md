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

## F6 — LUCID v1: in-context channel inference CONFIRMED; aggregate win open (2026-07-12)
Mixture of K=6 channel atoms, causal Bures-evidence gating (lucid_v1.py).
R2 CONFIRMED: gate entropy collapses 1.79 -> 0.43 after ONE observed
transition; mixture beats single channel at every position >=1 (0.028 vs
0.042 at t=5, -33%). The in-context capability the transformer lacked (F4)
exists in a channel dictionary with ~55 params. R1 OPEN: average holdout
(0.0695 / 0.0625 with learnable prior / 0.0691 with seeded aggregate atom)
loses to single-channel 0.0566 purely at position 0 — cold-start credit
assignment: prior gradients flow only through 1/6 of loss terms; even the
seeded aggregate atom drifts. Next attacks: position-weighted prior loss,
or hierarchical confidence gate (aggregate fallback outside the softmax).
Oracle ceiling: 0.0000 (true per-trajectory channel) — large headroom.

## VERA — unification thesis (registered)
Refound, don't merge: VERA = LUCID substrate + QUASAR knowledge loop +
conformal uncertainty (SENTINEL lineage) + Veritas thermal governance +
SIC/VEST provenance. Integration milestones I1-I4 in repo docs; each ships
only behind a finding. Leave-behind: QOLAS LLM backbone (never trained),
SKN prototype, demo theater.

## F7 — VERA I1: conformal certificates VERIFIED; gate power curve (2026-07-12)
Per-position split conformal on LUCID v1.1, nonconformity = Bures distance.
I1-a: first run missed registered band [0.87,0.93] at ONE position by
0.002 (0.932, n_cal=300) — consistent with conditional-coverage variance
(sd~1.7%). High-power rerun (n_cal=1000, n_test=2000): ALL positions in
band, 0.904-0.929, mean 0.914. VERIFIED.
I1-b VERIFIED: certified radius contracts 0.531 -> 0.284 along the
sequence — in-context inference now carries a coverage guarantee.
I1-c VERIFIED: shifted physics (w in [1.3,2.0]) collapses coverage to
0.394 — the certificate can fail, hence is informative.
VERA GATE (SECP Sentinel refounded on certificates): mean-score detector
FAILED registered TPR>=0.80 (0.682); diagnosis — the mixture partially
ADAPTS to OOD physics in-context (shifted coverage rises 0.31->0.48 with
position), camouflaging late positions. Adaptation-detection tension:
noted as a general safety observation for adaptive systems. Max-exceedance
detector (any position breaching its certified radius): FPR 0.091, power
curve monotone in shift magnitude: 0.583/0.730/0.790/0.860/0.892 for
w-bands [1.25-1.4]..[2.0-2.5]. Single-number TPR claim was ill-posed;
the power curve is the correct characterization. SECP components adopted
into VERA: Sentinel gate pattern (certificate-fed), hash-chain audit,
rollback; SECP's formal-verification/Byzantine claims left behind until
run. VERA layer status: Substrate F5 / Knowledge C1-C2 / Uncertainty F7 /
Governance+Provenance pending (I2 needs S25 sysfs; I4 SIC/VEST port).
