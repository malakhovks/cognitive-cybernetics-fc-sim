from dataclasses import dataclass
import numpy as np
@dataclass
class CPGConfig:
    gamma: float = 0.95
    lr_theta: float = 0.01
    lr_mu: float = 0.01
    var_pi: float = 0.02
    d_min: float = 0.6
    lambda_n: float = 1.0
    lambda_i: float = 0.0
    lambda_u: float = 0.1
    target_novelty: float = 0.20
class CPGPolicy:
    def __init__(self, cfg: CPGConfig, pi0: float = None):
        self.cfg = cfg; self.pi0 = cfg.target_novelty if pi0 is None else float(pi0)
        self.theta = np.array([0.0, 2.0, 0.5, -0.1, 0.0])
        self.mu = 0.0; self.prev_pi = self.pi0
    @staticmethod
    def _sigmoid(x): return 1.0 / (1.0 + np.exp(-x))
    def _features(self, N_hist, D_hist):
        dN = N_hist[-1] - N_hist[-2] if len(N_hist) >= 2 else 0.0
        N = N_hist[-1] if N_hist else self.cfg.target_novelty
        D = D_hist[-1] if D_hist else 0.5
        return np.array([1.0, N, D, dN, 0.0])
    def update(self, pi, N_meas, D_meas, t, state):
        N_hist, D_hist = state.get("N_hist", []), state.get("D_hist", [])
        phi = self._features(N_hist, D_hist); m = float(self._sigmoid(self.theta @ phi))
        pi_new = float(np.clip(m, 0.0, 1.0))
        rN = self.cfg.target_novelty
        N_last = N_hist[-1] if N_hist else N_meas
        D_last = D_hist[-1] if D_hist else D_meas
        reward = self.cfg.lambda_n * (1.0 - abs(N_last - rN)) - self.cfg.lambda_u * (pi_new - self.prev_pi) ** 2
        penalty = self.mu * max(0.0, self.cfg.d_min - D_last); adv = reward - penalty
        grad = (m * (1.0 - m)) * phi * adv; self.theta += self.cfg.lr_theta * grad
        self.mu = max(0.0, self.mu + self.cfg.lr_mu * (self.cfg.d_min - D_last)); self.prev_pi = pi_new
        return pi_new
