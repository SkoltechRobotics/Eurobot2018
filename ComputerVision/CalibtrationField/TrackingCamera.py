import cv2
import numpy as np
import pulp
import itertools


def find_true_calibration(img, matrix_k, ds, matrix_m, matrix_l, kp2_h):
    # Find rough transformation
    matrix_k_new = np.linalg.inv(matrix_m.dot(matrix_l)) * 10 ** 3
    field_img = cv2.fisheye.undistortImage(img, matrix_k, ds, Knew=matrix_k_new)

    # Find key points
    gray = cv2.cvtColor(field_img, cv2.COLOR_RGB2GRAY)
    hist = cv2.equalizeHist(gray)

    orb = cv2.ORB_create(100, WTA_K=3)

    kp = orb.detect(hist, None)

    kp_h = np.array([x_.pt for x_ in kp])
    diff_matrix = np.sum((kp_h[:, np.newaxis] - kp_h[np.newaxis, :]) ** 2, axis=2) ** 0.5
    indx = [0]
    summ = [kp_h[0]]
    cont = [1]
    for i in range(1, len(kp)):

        v = np.min(diff_matrix[i, indx])
        if v < 11:
            j = int(np.argmin(diff_matrix[i, indx]))
            summ[j] += kp_h[i]
            cont[j] += 1
        else:
            indx.append(i)
            summ.append(kp_h[i])
            cont.append(1)
    kp1_h = np.array([summ[i] / cont[i] for i in range(len(indx))])

    # Key points matching

    n1 = kp1_h.shape[0]
    n2 = kp2_h.shape[0]
    costs = np.sum((kp1_h[:, np.newaxis] - kp2_h[np.newaxis, :]) ** 2, axis=2) ** 0.5

    prob = pulp.LpProblem("eurobot")
    x = pulp.LpVariable.dicts("x", [(i, j) for (i, j) in itertools.product(
        range(n1), range(n2))], 0, 1, pulp.LpBinary)
    y = pulp.LpVariable.dicts("y", [i for i in range(n1)], 0, 1, pulp.LpBinary)
    z = pulp.LpVariable.dicts("z", [j for j in range(n2)], 0, 1, pulp.LpBinary)

    prob += pulp.lpSum((costs[s1, s2] * x[(s1, s2)]) for s1, s2 in itertools.product(range(n1), range(n2))
                       ) - pulp.lpSum([70 * y[i] for i in range(n1)]) - pulp.lpSum([70 * z[j] for j in range(n2)])

    for s in range(n1):
        prob += pulp.lpSum([x[(s, i)] for i in range(n2)]) == y[s]
    for s in range(n2):
        prob += pulp.lpSum([x[(i, s)] for i in range(n1)]) == z[s]

    prob.solve()

    ind1, ind2 = [], []
    for i, j in itertools.product(range(n1), range(n2)):
        if x[(i, j)].varValue >= 1:
            ind1.append(i)
            ind2.append(j)

    res = cv2.findHomography(kp1_h[ind1], kp2_h[ind2], method=cv2.RHO)
    return res[0]
