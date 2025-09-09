from dataclasses import dataclass
@dataclass
class PIDConfig:
    kp: float = 0.5
    ki: float = 0.0
    kd: float = 0.0
    target_novelty: float = 0.20
    d_limit: float = 1.0
class PIDPolicy:
    def __init__(self, cfg: PIDConfig, pi0: float = None):
        self.cfg = cfg; self.pi0 = cfg.target_novelty if pi0 is None else float(pi0)
        self._i = 0.0; self._prev_e = 0.0
    def update(self, pi, N_meas, D_meas, t, state):
        e = self.cfg.target_novelty - N_meas
        self._i += e; d = e - self._prev_e if t > 0 else 0.0
        delta = self.cfg.kp * e + self.cfg.ki * self._i + self.cfg.kd * d
        delta = max(-self.cfg.d_limit, min(self.cfg.d_limit, delta))
        pi_new = max(0.0, min(1.0, pi + delta)); self._prev_e = e; return pi_new
