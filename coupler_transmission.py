import numpy as np

T_objective = 0.75
T_beamsplitter = 303e-6/12.7e-3
P_in_m = 12.7e-3
P_out_m = 110e-9

P_in_B = T_objective*P_in_m
P_out_A = P_out_m/T_beamsplitter
P_out_B = P_out_A/T_objective

T = 100*np.sqrt(P_out_B/P_in_B)

print(T)
