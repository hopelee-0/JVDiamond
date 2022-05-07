import numpy as np

T_objective = 0.75
T_setup = 38.2/88.4
P_in = 83
P_out = 0.248

P_in_gc = P_in*T_objective*T_setup
P_out_gc = P_out/T_objective/T_setup

T = 100*np.sqrt(P_out_gc/P_in_gc)

print(T)
