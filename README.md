> ## Start here
>
> **QUASAR v0.2** — Bures-metric geometry applied to single-qubit AI learning. Every claim carries a numbered prediction, registered before the code runs. Failed predictions are kept and marked, not deleted — [FINDINGS.md](FINDINGS.md) is the lab notebook: 16 entries (F1–F16), two of them headline refutations kept in full.
>
> Self-tests pass on a cold clone: QGT 6/6 suites, backprop.py V1–V4. Pure NumPy — no cloud, built and verified on a Galaxy S25 Ultra.
>
> v0.1 is [archived](https://github.com/holland202/quasar) as the public timestamped baseline; this repo is where the work is active.

# QUASAR v0.2

Development repo, now public. Public timestamped baseline: github.com/holland202/quasar (v0.1).
Start with FINDINGS.md — it is the lab notebook and the roadmap.

Core modules are copied from v0.1 (quantum_geometric_transformer.py,
quantum_geometric_rl.py, quasar.py). Probes: mediation_probe.py (kept as a
documented methodology trap — read FINDINGS.md F1 before trusting any
intervention probe), broadcast_probe.py (the corrected instrument; current
baseline broadcast ratio 0.001).

Run: pip install numpy, then any script directly. Pure NumPy.
