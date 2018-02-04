from cubesequence import *

optimizer = CubePickingOptimizer()
optimizer.set_plan([0, 1, 2])
time = optimizer.get_fun_time(3, 2, 2)
seq = optimizer.find_optimal_sequence(time)
for s in seq:
    print(s)
print(time(seq))
