#!/usr/bin/env python3
"""Repair broken patches in an image-to-3D normal map (tangent space, OpenGL/glTF convention).

Pixal3D bakes its normal map from the generated high-res surface. On Sid (11.11.2026) about 5 % of the used texels
(11 % in the hair) were garbage. In the render they looked like cracks, splinters and dark seams, although geometry and
base colour were clean there. This sets texels that tilt more than about 17 degrees (plus a grown region around them)
to neutral and softens the edge.

usage: python3 fix_normal_map.py normal.png out.png [--mask coverage.png] [--seed-dev 0.30] [--grow-dev 0.10] [--grow-px 10]
  --mask      optional UV coverage mask (white = texel used by the mesh); only used for the statistics
  --seed-dev  |xy| of the decoded normal that marks a texel as broken (0.30 = about 17 degrees)
  --grow-dev  neighbours above this deviation join a broken patch (0.10 = about 6 degrees) ...
  --grow-px   ... up to this many pixels away
Writes out.png and out_mask.png (the repaired texels). Always compare renders with the old map, the new map and no map at all:
if what is left is only noise, dropping the normal map is often the cleanest fix (colours then look a little flatter).
"""
import argparse
import numpy as np
import cv2

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("normal"); ap.add_argument("out")
ap.add_argument("--mask"); ap.add_argument("--seed-dev", type=float, default=0.30)
ap.add_argument("--grow-dev", type=float, default=0.10); ap.add_argument("--grow-px", type=int, default=10)
a = ap.parse_args()

n = cv2.imread(a.normal, cv2.IMREAD_UNCHANGED)
if n is None:
    raise SystemExit("cannot read " + a.normal)
n = n[..., :3][..., ::-1].astype(np.float32)                 # BGR -> RGB
v = n / 255.0 * 2 - 1
dev = np.sqrt(v[..., 0] ** 2 + v[..., 1] ** 2)
cov = np.ones(dev.shape, bool)
if a.mask:
    m = cv2.imread(a.mask, cv2.IMREAD_GRAYSCALE)
    cov = m > 127

seed = (dev > a.seed_dev).astype(np.uint8)
grow = (dev > a.grow_dev).astype(np.uint8)
k3 = np.ones((3, 3), np.uint8)
m = seed.copy()
for _ in range(a.grow_px):                                     # geodesic growth of the seeds inside 'grow'
    m2 = (cv2.dilate(m, k3) & grow) | seed
    if (m2 == m).all():
        break
    m = m2
mask = cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))   # 3 px safety ring
out = n.copy()
out[mask > 0] = (128, 128, 255)
band = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))) & (1 - cv2.erode(mask, k3))
bl = cv2.GaussianBlur(out, (0, 0), 1.2)
out[band > 0] = bl[band > 0]
out8 = np.clip(np.rint(out), 0, 255).astype(np.uint8)
cv2.imwrite(a.out, out8[..., ::-1])
cv2.imwrite(a.out.rsplit(".", 1)[0] + "_mask.png", mask * 255)

v2 = out8.astype(np.float32) / 255 * 2 - 1
dev2 = np.sqrt(v2[..., 0] ** 2 + v2[..., 1] ** 2)
print("repaired: %.2f %% of used texels (seeds %.2f %%)" % (100 * mask[cov].mean(), 100 * seed[cov].mean()))
print("deviation of used texels before, percentiles 50/90/99/99.9:", [round(float(np.percentile(dev[cov], p)), 3) for p in (50, 90, 99, 99.9)])
print("deviation of used texels after,  percentiles 50/90/99/99.9:", [round(float(np.percentile(dev2[cov], p)), 3) for p in (50, 90, 99, 99.9)])
print("wrote", a.out)
