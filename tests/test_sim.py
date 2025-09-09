from src.sim.core import SimConfig, run_one_trial
from src.controllers.pid import PIDPolicy, PIDConfig
def test_basic_run():
    cfg = SimConfig(seed=123, horizon=10, topics=12, outputs_per_cycle=10)
    pol = PIDPolicy(PIDConfig(kp=0.5, ki=0.0, kd=0.0, target_novelty=0.2))
    out = run_one_trial(cfg, pol)
    assert "N" in out and "D" in out and "pi" in out
    assert len(out["N"]) == cfg.horizon
