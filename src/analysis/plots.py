import os, glob, json
import matplotlib.pyplot as plt
def plot_examples(results_dir: str, out_dir: str, max_trials_per_scenario: int = 1):
    os.makedirs(out_dir, exist_ok=True)
    for scen_dir in sorted(glob.glob(os.path.join(results_dir, "*"))):
        if not os.path.isdir(scen_dir): continue
        scenario = os.path.basename(scen_dir)
        trials = sorted(glob.glob(os.path.join(scen_dir, "trial_*.json")))[:max_trials_per_scenario]
        for fp in trials:
            with open(fp, "r") as f: obj = json.load(f)
            N, D = obj["N"], obj["D"]
            plt.figure(); plt.plot(range(1, len(N)+1), N, label="Novelty")
            plt.title(f"Novelty over time — {scenario}"); plt.xlabel("cycle"); plt.ylabel("novelty fraction")
            plt.legend(); plt.tight_layout()
            plt.savefig(os.path.join(out_dir, f"{scenario}_{os.path.basename(fp).replace('.json','')}_novelty.png")); plt.close()
            plt.figure(); plt.plot(range(1, len(D)+1), D, label="Diversity")
            plt.title(f"Diversity over time — {scenario}"); plt.xlabel("cycle"); plt.ylabel("diversity (topics/T)")
            plt.legend(); plt.tight_layout()
            plt.savefig(os.path.join(out_dir, f"{scenario}_{os.path.basename(fp).replace('.json','')}_diversity.png")); plt.close()
