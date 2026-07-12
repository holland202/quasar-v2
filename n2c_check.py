"""N2'' — is the progress curriculum REAL, or a degenerate uniform?
Two checks that must both pass before any claim:
  (i)  weight trajectory: did progress-weights actually deviate from
       uniform DURING training? (final weights ~uniform at convergence is
       expected — progress -> 0 everywhere.)
  (ii) multi-seed: uniform vs error vs progress, 5 seeds each, so the
       +5% is not a data-draw artifact.
"""
import numpy as np
import lucid2q as L2
from backprop import T, matmul, bures_mean_loss
from n2_capacity import STEPS, BS, LR, NBINS, BINS, make, bin_err

def run(mode, seed):
    rr = np.random.default_rng(seed)
    M = T(rr.normal(0, 0.05, (15, 15)))
    w = np.ones(NBINS) / NBINS
    prev = bin_err(M.data.T); traj = []
    for s in range(STEPS):
        if s % 200 == 0 and s > 0:
            cur = bin_err(M.data.T)
            if mode == "error":
                w = cur / cur.sum()
            elif mode == "progress":
                p = np.clip(prev - cur, 0, None)
                w = (p + 1e-4) / (p + 1e-4).sum()
            prev = cur
            traj.append(w.copy())
        k = int(np.random.default_rng(seed * 9973 + s).choice(NBINS, p=w))
        x, y = make(BS, *BINS[k])
        M.grad = None
        bures_mean_loss(matmul(T(x, requires_grad=False), M), y).backward()
        M.data -= LR * M.grad
    return float(bin_err(M.data.T).mean()), np.array(traj)

_, tr = run("progress", 7)
dev = np.abs(tr - 1/NBINS).sum(1)
print("(i) progress-weight L1 deviation from uniform, over training:")
print("   " + " ".join(f"{v:.2f}" for v in dev))
print(f"   max {dev.max():.3f}, mean {dev.mean():.3f}, final {dev[-1]:.3f}")
print(f"   -> curriculum was {'REAL (weights deviated substantially)' if dev.max() > 0.25 else 'DEGENERATE (never left uniform) -- any win is a data-draw artifact'}")
print("   early weights:", np.round(tr[0], 3))
print("   mid   weights:", np.round(tr[len(tr)//2], 3))
print("   final weights:", np.round(tr[-1], 3))

print("\n(ii) 5 seeds per arm, matched budget:")
res = {}
for mode in ("uniform", "error", "progress"):
    v = [run(mode, 7 + s)[0] for s in range(5)]
    res[mode] = np.array(v)
    print(f"   {mode:>9}: {res[mode].mean():.5f} +- {res[mode].std():.5f}   "
          f"{np.round(res[mode], 4)}")
u, e, p = res["uniform"], res["error"], res["progress"]
print(f"\n   error-proportional vs uniform : {100*(u.mean()-e.mean())/u.mean():+.2f}%"
      f"   (wins {int((e<u).sum())}/5)")
print(f"   progress-proportional vs uniform: {100*(u.mean()-p.mean())/u.mean():+.2f}%"
      f"   (wins {int((p<u).sum())}/5)")
