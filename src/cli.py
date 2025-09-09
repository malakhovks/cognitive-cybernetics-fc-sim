import argparse, os
from .utils.io import load_yaml, ensure_dir, write_json
from .sim.core import SimConfig, run_one_trial
from .sim.policies import make_policy
from .analysis.summaries import summarize as summarize_fn
from .analysis.plots import plot_examples as plot_fn
SCENARIOS = ["impact_only", "no_control", "random", "pid", "lqr", "cpg"]
def cmd_run(args):
    cfg = load_yaml(args.config)
    sim_cfg = SimConfig(seed=cfg["seed"], horizon=cfg["horizon"], topics=cfg["topics"],
                        outputs_per_cycle=cfg["outputs_per_cycle"], breakthrough=tuple(cfg["breakthrough"]),
                        noise_novelty=cfg["noise_novelty"], delay_steps=cfg["delay_steps"],
                        shock_enabled=cfg["shock"]["enabled"], shock_at_cycle=cfg["shock"]["at_cycle"],
                        shock_outputs_after=cfg["shock"]["outputs_after"], target_novelty=cfg["targets"]["novelty"])
    scenarios = SCENARIOS if args.scenario == "all" else [s.strip() for s in args.scenario.split(",")]
    for scen in scenarios:
        out_dir = os.path.join(args.results, scen); ensure_dir(out_dir)
        for i in range(args.trials):
            policy = make_policy(scen, cfg)
            sim_cfg.seed = cfg["seed"] + i
            obj = run_one_trial(sim_cfg, policy)
            write_json(os.path.join(out_dir, f"trial_{i}.json"), obj)
    print("Done. Results in", args.results)
def cmd_summarize(args): ensure_dir(os.path.dirname(args.out)); summarize_fn(args.results, args.out)
def cmd_plot(args): ensure_dir(args.out); plot_fn(args.results, args.out, max_trials_per_scenario=args.max_examples)
def main():
    ap = argparse.ArgumentParser(description="Feedback-Controlled Knowledge-Production Simulator")
    sub = ap.add_subparsers(dest="cmd", required=True)
    ap_run = sub.add_parser("run", help="Run simulations")
    ap_run.add_argument("--config", required=True)
    ap_run.add_argument("--scenario", default="all", help="comma list or 'all'")
    ap_run.add_argument("--trials", type=int, default=50)
    ap_run.add_argument("--results", default="results")
    ap_run.set_defaults(func=cmd_run)
    ap_sum = sub.add_parser("summarize", help="Summarize results to CSV")
    ap_sum.add_argument("--results", required=True)
    ap_sum.add_argument("--out", required=True)
    ap_sum.set_defaults(func=cmd_summarize)
    ap_plot = sub.add_parser("plot", help="Make basic plots")
    ap_plot.add_argument("--results", required=True)
    ap_plot.add_argument("--out", required=True)
    ap_plot.add_argument("--max-examples", type=int, default=1)
    ap_plot.set_defaults(func=cmd_plot)
    args = ap.parse_args(); args.func(args)
if __name__ == "__main__": main()
