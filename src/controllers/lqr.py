from dataclasses import dataclass
import numpy as np
@dataclass
class LQRConfig:
    q1: float = 1.0
    q2: float = 0.1
    r: float = 0.05
    target_novelty: float = 0.20
    pi_bar: float = 0.20
class LQRPolicy:
    def __init__(self, cfg: LQRConfig, pi0: float = None):
        self.cfg = cfg; self.pi0 = cfg.pi_bar if pi0 is None else float(pi0)
        self.K = np.array([0.5, 0.0])
    def _identify_AB(self, N_hist, pi_hist):
        if len(N_hist) < 4: return None, None
        rN = self.cfg.target_novelty; X, Xn, U = [], [], []
        for t in range(2, len(N_hist)-1):
            x_t = np.array([N_hist[t] - rN, N_hist[t] - N_hist[t-1]])
            x_tp1 = np.array([N_hist[t+1] - rN, N_hist[t+1] - N_hist[t]])
            u_t = np.array([pi_hist[t] - self.cfg.pi_bar])
            X.append(x_t); Xn.append(x_tp1); U.append(u_t)
        X = np.stack(X); Xn = np.stack(Xn); U = np.stack(U)
        Z = np.concatenate([X, U], axis=1)
        try:
            AB, *_ = np.linalg.lstsq(Z, Xn, rcond=None)
            A = AB[:2, :]; B = AB[2:, :].T; return A, B
        except Exception: return None, None
    def _dlqr(self, A, B, Q, R):
        X = np.matrix(np.copy(Q))
        for _ in range(100):
            Xn = A.T @ X @ A - A.T @ X @ B @ np.linalg.inv(R + B.T @ X @ B) @ B.T @ X @ A + Q
            if np.allclose(X, Xn, atol=1e-6): break
            X = Xn
        K = np.linalg.inv(R + B.T @ X @ B) @ (B.T @ X @ A); return np.asarray(K)
    def update(self, pi, N_meas, D_meas, t, state):
        N_hist = state.get("N_hist", []); pi_hist = state.get("pi_hist", [pi]*len(N_hist))
        if t > 5:
            A, B = self._identify_AB(N_hist, pi_hist + [pi])
            if A is not None and B is not None:
                Q = np.diag([self.cfg.q1, self.cfg.q2]); R = np.array([[self.cfg.r]])
                try: self.K = np.squeeze(self._dlqr(A, B, Q, R))
                except Exception: pass
        rN = self.cfg.target_novelty
        if len(N_hist) >= 2: x = np.array([N_hist[-1] - rN, N_hist[-1] - N_hist[-2]])
        else: x = np.array([N_meas - rN, 0.0])
        u = - float(self.K @ x); return float(np.clip(self.cfg.pi_bar + u, 0.0, 1.0))
