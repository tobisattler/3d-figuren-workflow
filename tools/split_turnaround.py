"""Split a 3-view turnaround sheet (front | side facing image-left | back) into
three square images at identical scale and vertical position, for Pixal3D/img23d.

usage: python3 split_turnaround.py SHEET.png OUTDIR NAME
writes OUTDIR/NAME_front.png, NAME_side_left.png, NAME_back.png and prints the boxes.
"""
import sys
import numpy as np
from PIL import Image

sheet, outdir, name = sys.argv[1], sys.argv[2], sys.argv[3]
im = Image.open(sheet).convert("RGB")
a = np.asarray(im).astype(np.int16)
H, W, _ = a.shape
# background colour from the four corners
bg = np.median(np.concatenate([a[:20, :20].reshape(-1, 3), a[:20, -20:].reshape(-1, 3),
                               a[-20:, :20].reshape(-1, 3), a[-20:, -20:].reshape(-1, 3)]), axis=0)
fg = np.abs(a - bg).max(axis=2) > 28
col = fg.sum(axis=0) > 3
# runs of foreground columns, merge runs separated by < 2% of width
runs, x = [], 0
while x < W:
    if col[x]:
        s = x
        while x < W and col[x]:
            x += 1
        runs.append([s, x])
    x += 1
merged = []
for r in runs:
    if merged and r[0] - merged[-1][1] < 0.02 * W:
        merged[-1][1] = r[1]
    else:
        merged.append(r)
merged = [r for r in merged if r[1] - r[0] > 0.05 * W]
if len(merged) != 3:
    sys.exit(f"expected 3 figures, found {len(merged)}: {merged}")
rows = np.where(fg.sum(axis=1) > 3)[0]
top, bot = rows.min(), rows.max()
side = H  # square canvas, same height as the sheet keeps scale and vertical position
bounds = [0] + [(merged[i][1] + merged[i + 1][0]) // 2 for i in range(2)] + [W]
for i, ((x0, x1), tag) in enumerate(zip(merged, ["front", "side_left", "back"])):
    sx0, sx1 = bounds[i], bounds[i + 1]          # this figure's strip, up to the midpoints of the gaps
    strip = a[:, sx0:sx1].astype(np.uint8)
    # per-row background from the strip's outer columns, so vertical gradients carry on without seams
    edge = np.concatenate([strip[:, :8], strip[:, -8:]], axis=1)
    rowbg = np.median(edge, axis=1).astype(np.uint8)       # (H, 3)
    canvas = np.repeat(rowbg[:, None, :], side, axis=1)
    cx = (x0 + x1) // 2
    off = side // 2 - (cx - sx0)
    lo, hi = max(0, off), min(side, off + (sx1 - sx0))
    canvas[:, lo:hi] = strip[:, lo - off:hi - off]
    Image.fromarray(canvas).save(f"{outdir}/{name}_{tag}.png")
    print(tag, "x", x0, x1, "w", x1 - x0)
print("rows", top, bot, "height", bot - top, "sheet", W, H)
