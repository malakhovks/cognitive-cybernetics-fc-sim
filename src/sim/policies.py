from typing import Dict, Any
from .core import PolicyBase
from ..controllers.pid import PIDPolicy, PIDConfig
from ..controllers.lqr import LQRPolicy, LQRConfig
from ..controllers.cpg import CPGPolicy, CPGConfig
class NoControlPolicy(PolicyBase):
    def __init__(self, value: float = 0.05): self.value = float(value)
    def update(self, pi, N_meas, D_meas, t, state): return self.value
class ImpactOnlyPolicy(PolicyBase):
    def update(self, pi, N_meas, D_meas, t, state): return 0.0
class RandomPolicy(PolicyBase):
    def update(self, pi, N_meas, D_meas, t, state): return 1.0
def make_policy(name: str, cfg: Dict[str, Any]) -> PolicyBase:
    n = name.lower()
    if n in ["no_control", "nocontrol"]: return NoControlPolicy(0.05)
    if n in ["impact_only", "impact"]: return ImpactOnlyPolicy()
    if n in ["random"]: return RandomPolicy()
    if n in ["pid"]:
        return PIDPolicy(PIDConfig(kp=cfg["pid"]["kp"], ki=cfg["pid"]["ki"], kd=cfg["pid"]["kd"], target_novelty=cfg["targets"]["novelty"]))
    if n in ["lqr"]:
        return LQRPolicy(LQRConfig(q1=cfg["lqr"]["q"][0], q2=cfg["lqr"]["q"][1], r=cfg["lqr"]["r"], target_novelty=cfg["targets"]["novelty"], pi_bar=cfg["targets"]["novelty"]))
    if n in ["cpg"]:
        return CPGPolicy(CPGConfig(gamma=cfg["cpg"]["gamma"], lr_theta=cfg["cpg"]["lr_theta"], lr_mu=cfg["cpg"]["lr_mu"],
                                   var_pi=cfg["cpg"]["var_pi"], d_min=cfg["cpg"]["d_min"],
                                   lambda_n=cfg["cpg"]["lambdas"]["novelty"], lambda_i=cfg["cpg"]["lambdas"]["impact"],
                                   lambda_u=cfg["cpg"]["lambdas"]["smooth"], target_novelty=cfg["targets"]["novelty"]))
    raise ValueError(f"Unknown policy: {name}")
