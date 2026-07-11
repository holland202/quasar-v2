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
