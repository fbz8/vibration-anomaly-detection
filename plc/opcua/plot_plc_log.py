"""
plot_plc_log.py - draw a timeline of one PLC log recorded by read_plc.py.

Run:  python plot_plc_log.py                 (uses the newest log in ./logs)
      python plot_plc_log.py logs/xxx.csv    (a specific log)
Saves plc_cycle.png next to this script.
"""
import csv
import sys
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt

HERE = Path(__file__).parent


def load(path):
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    t0 = datetime.fromisoformat(rows[0]["timestamp"])
    t = [(datetime.fromisoformat(r["timestamp"]) - t0).total_seconds() for r in rows]
    cols = {k: [int(r[k]) for r in rows] for k in rows[0] if k != "timestamp"}
    return t, cols


def main():
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
    else:
        logs = sorted((HERE / "logs").glob("plc_log_*.csv"))
        if not logs:
            sys.exit("No logs found. Run read_plc.py first.")
        path = logs[-1]
    t, c = load(path)

    signals = [("RUN", "tab:blue"), ("LAMP", "gold"), ("MOTOR", "tab:green"), ("JAM", "tab:red")]
    fig, axes = plt.subplots(len(signals) + 1, 1, figsize=(11, 7), sharex=True)
    for ax, (name, color) in zip(axes, signals):
        ax.step(t, c[name], where="post", color=color, linewidth=2)
        ax.fill_between(t, c[name], step="post", color=color, alpha=0.25)
        ax.set_ylim(-0.2, 1.2)
        ax.set_yticks([0, 1])
        ax.set_ylabel(name, rotation=0, ha="right", va="center")
        ax.grid(alpha=0.3)
    ax = axes[-1]
    ax.step(t, c["C1.CV"], where="post", color="black", linewidth=2)
    ax.axhline(10, color="gray", linestyle="--", linewidth=1)
    ax.text(t[0], 10.3, "crate full (10)", color="gray", fontsize=8)
    ax.set_ylabel("Boxes", rotation=0, ha="right", va="center")
    ax.set_xlabel("time (s)")
    ax.grid(alpha=0.3)
    fig.suptitle(f"Conveyor station, live PLC data over OPC UA ({path.name})")
    fig.tight_layout()
    out = HERE / "plc_cycle.png"
    fig.savefig(out, dpi=130)
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
