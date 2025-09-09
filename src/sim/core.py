from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
import itertools
import numpy as np
Pair = Tuple[int, int]
@dataclass
class SimConfig:
    seed: int = 20250827
    horizon: int = 50
    topics: int = 20
    outputs_per_cycle: int = 20
    breakthrough: Pair = (18, 19)
    noise_novelty: float = 0.02
    delay_steps: int = 1
    shock_enabled: bool = True
    shock_at_cycle: int = 25
    shock_outputs_after: int = 10
    target_novelty: float = 0.20
@dataclass
class SimState:
    rng: np.random.Generator
    known_pairs: set
    popularity: Dict[Pair, int]
    time_to_insight: Optional[int] = None
    N_hist: List[float] = field(default_factory=list)
    D_hist: List[float] = field(default_factory=list)
    pi_hist: List[float] = field(default_factory=list)
def _choose_unknown_pair(rng: np.random.Generator, T: int, known: set) -> Pair:
    while True:
        i, j = rng.choice(T, size=2, replace=False)
        p = tuple(sorted((int(i), int(j))))
        if p not in known: return p
def _weighted_known_pair(rng: np.random.Generator, pop: Dict[Pair, int]) -> Pair:
    pairs = list(pop.keys()); w = np.array([pop[p] for p in pairs], dtype=float); w = w / w.sum()
    idx = rng.choice(len(pairs), p=w); return pairs[int(idx)]
def init_state(cfg: SimConfig) -> 'SimState':
    rng = np.random.default_rng(cfg.seed)
    core = set(range(10))
    known = {tuple(sorted(p)) for p in itertools.combinations(core, 2)}
    pop = {p: 1 for p in known}
    return SimState(rng=rng, known_pairs=known, popularity=pop)
class PolicyBase:
    def update(self, pi: float, N_meas: float, D_meas: float, t: int, state: Dict[str, Any]) -> float: raise NotImplementedError
class ConstantPolicy(PolicyBase):
    def __init__(self, value: float): self.value = float(value)
    def update(self, pi, N_meas, D_meas, t, state): return self.value
def run_one_trial(cfg: SimConfig, policy: PolicyBase) -> Dict[str, Any]:
    st = init_state(cfg); T = cfg.topics; H = cfg.horizon; M = cfg.outputs_per_cycle
    total_pairs = T * (T - 1) // 2; pi = getattr(policy, "pi0", cfg.target_novelty)
    for t in range(H):
        M_t = M
        if cfg.shock_enabled and (t + 1) >= cfg.shock_at_cycle: M_t = cfg.shock_outputs_after
        Mexp = int(round(pi * M_t)); new_disc = 0; topics_used = set()
        for _ in range(Mexp):
            if len(st.known_pairs) >= total_pairs: break
            p = _choose_unknown_pair(st.rng, T, st.known_pairs); topics_used.update(p)
            if p not in st.known_pairs:
                st.known_pairs.add(p); st.popularity[p] = 1; new_disc += 1
                if p == tuple(sorted(cfg.breakthrough)) and st.time_to_insight is None: st.time_to_insight = t + 1
        for _ in range(M_t - Mexp):
            p = _weighted_known_pair(st.rng, st.popularity); topics_used.update(p); st.popularity[p] = st.popularity.get(p, 0) + 1
        N = new_disc / max(M_t, 1); D = len(topics_used) / T
        st.N_hist.append(N); st.D_hist.append(D); st.pi_hist.append(pi)
        N_meas = N + st.rng.normal(0.0, cfg.noise_novelty); D_meas = D
        pi = policy.update(pi, N_meas, D_meas, t, state={"N_hist": st.N_hist, "D_hist": st.D_hist, "pi_hist": st.pi_hist})
    return {"N": st.N_hist, "D": st.D_hist, "pi": st.pi_hist, "T_insight": st.time_to_insight}
