import cv2
import numpy as np
from colormath.color_diff import delta_e_cmc
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color


def color_distance(c1, c2):
    color1 = sRGBColor(*c1, is_upscaled=True)
    lab_color1 = convert_color(color1, LabColor)
    color2 = sRGBColor(*c2, is_upscaled=True)
    lab_color2 = convert_color(color2, LabColor)
    return delta_e_cmc(lab_color1, lab_color2)


def permutations(array, n=None, perm=None):
    if perm is None:
        perm = []
    if n is None:
        n = len(array)
    if n == 0:
        yield perm
    else:
        for i in range(len(array)):
            yield from permutations(array[:i] + array[i + 1:], n - 1,
                                    perm + [array[i]])


def all_plans():
    yield from permutations(list(range(5)), 3)


PLANS = list(all_plans())
COLORS = np.array([[0, 124, 176], [208, 93, 40], [14, 14, 16], [97, 153, 59],
                   [247, 181, 0]], dtype=np.uint8)
LABELS = ['blue', 'orange', 'black', 'green', 'yellow']


def find_colors(img, matrix, h_border, w_border):
    small_img = cv2.warpPerspective(img, matrix, (w_border, h_border))

    clh_img = cv2.cvtColor(small_img, cv2.COLOR_RGB2HSV)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(30, 30))
    clh_img[:, :, 2] = clahe.apply(clh_img[:, :, 2])
    clh_img = cv2.cvtColor(clh_img, cv2.COLOR_HSV2RGB)

    points1 = np.float32([(0, h_border), (0, 0),
                          (w_border, 0)])
    points2 = np.float32([(0, h_border // 30), (0, 0),
                          (w_border // 30, 0)])

    rough_img = cv2.warpAffine(clh_img, cv2.getAffineTransform(points1, points2),
                               (w_border // 30, h_border // 30))

    height, width = rough_img.shape[0:2]
    dist_array = np.zeros((height, width, COLORS.shape[0]))

    for i in range(COLORS.shape[0]):
        dist_array[:, :, i] = np.apply_along_axis(color_distance, 2, rough_img, COLORS[i])

    plan_dist_array = np.zeros((height, width - 4, len(PLANS)))

    for i, plan in enumerate(PLANS):
        plan_dist_array[:, :, i] = sum(
            [np.roll(dist_array[:, :, plan[x]] ** 2, -2 * x, axis=1)[:, :-4] for x in range(3)])

    best_plan = np.unravel_index(np.argmin(plan_dist_array), (height, width - 4, len(PLANS)))[2]
    ind = np.unravel_index(np.argmin(plan_dist_array), (height, width - 4, len(PLANS)))[0:2]
    return PLANS[best_plan], ind
