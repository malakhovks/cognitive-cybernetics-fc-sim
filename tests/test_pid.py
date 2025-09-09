from src.controllers.pid import PIDPolicy, PIDConfig
def test_pid_updates_increases_when_below_target():
    pid = PIDPolicy(PIDConfig(kp=0.5, ki=0.0, kd=0.0, target_novelty=0.2))
    pi = 0.2
    pi2 = pid.update(pi, N_meas=0.1, D_meas=0.5, t=1, state={})
    assert pi2 > pi
