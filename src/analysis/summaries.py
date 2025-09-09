import json, os, glob
import pandas as pd
import numpy as np
def summarize(results_dir: str, out_csv: str):
    rows = []
    for scen_dir in sorted(glob.glob(os.path.join(results_dir, "*"))):
        if not os.path.isdir(scen_dir): continue
        scenario = os.path.basename(scen_dir)
        for fp in sorted(glob.glob(os.path.join(scen_dir, "trial_*.json"))):
            with open(fp, "r") as f: obj = json.load(f)
            rows.append({"scenario": scenario,
                         "trial": int(os.path.splitext(os.path.basename(fp))[0].split("_")[1]),
                         "T_insight": obj.get("T_insight", None) if obj.get("T_insight", None) is not None else np.nan,
                         "N_avg": float(np.mean(obj["N"])) if obj["N"] else np.nan,
                         "D_avg": float(np.mean(obj["D"])) if obj["D"] else np.nan})
    df = pd.DataFrame(rows)
    if df.empty: print("No results found in", results_dir); return
    os.makedirs(os.path.dirname(out_csv), exist_ok=True); df.to_csv(out_csv, index=False)
    print("Wrote", out_csv)
