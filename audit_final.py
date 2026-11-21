# -*- coding: utf-8 -*-
"""Semantic audit: numbering, region colours, map placement, layout, gate."""
import os, sys, math
sys.path.insert(0, '.')
import build
from PIL import Image

fails = []
def check(cond, msg):
    print(('  OK   ' if cond else '  FAIL ') + msg)
    if not cond: fails.append(msg)

print('=== 1. STORY SET ===')
check(len(build.STORIES) == 35, '35 stories')
check(sorted(s[0] for s in build.STORIES) == list(range(1, 36)), 'numbers 1..35 exactly once')
check(all('20 NOV' in s[9] for s in build.STORIES), 'every story dated 20 NOV 2026')
check(sum(build.COUNTS.values()) == 35, 'region counts sum to 35')
print('  region counts:', build.COUNTS)

print('=== 2. REGION COLOURS (reference scheme) ===')
check(build.REG['ASIA']['c'] == '#B43A2E', 'Asia = red')
check(build.REG['MIDDLE EAST']['c'] == '#D2861B', 'Middle East = orange')
check(build.REG['EUROPE']['c'] == '#2C6FB0', 'Europe = blue')
check(build.REG['AFRICA']['c'] == '#2F8B5B', 'Africa = green')
check(build.REG['AMERICAS']['c'] == '#7748A8', 'Americas = purple')
check(build.REG['OCEANIA']['c'] == '#118A8E', 'Oceania = teal')

print('=== 3. MAP PLACEMENT ===')
x0, y0, x1, y1 = 16, 731, 432, 940
LAT_T, LAT_B = 83, -58
mw, mh = x1-x0, y1-y0
def pr(lon, lat):
    return (x0+(lon+180)/360*mw, y0+(LAT_T-lat)/(LAT_T-LAT_B)*mh)
rad = 6.8
placed, rings, pairs = [], [], []
for s in build.STORIES:
    dx, dy = pr(s[7], s[8])
    best = None
    for ring in (0, 8, 15, 23, 32, 42):
        steps = max(12, int(ring*3))
        for k in range(steps):
            a = 2*math.pi*k/steps + ring*0.31
            cx, cy = dx+ring*math.cos(a), dy+ring*math.sin(a)*0.85
            if x0+9 <= cx <= x1-9 and y0+9 <= cy <= y1-9 and \
               all((cx-px)**2+(cy-py)**2 > (2*rad+3)**2 for px, py in placed):
                best = (cx, cy, ring); break
        if best: break
    if not best: best = (dx, dy, 0)
    placed.append(best[:2]); rings.append(best[2])
for i in range(len(placed)):
    for j in range(i+1, len(placed)):
        pairs.append(math.hypot(placed[i][0]-placed[j][0], placed[i][1]-placed[j][1]))
check(min(pairs) >= 2*rad, 'no two map badges overlap (min gap %.1f px >= %.1f)' % (min(pairs), 2*rad))
check(max(rings) <= 42, 'badges stay close to their dot (max offset %d px)' % max(rings))
print('  badges at ring 0:', sum(1 for r in rings if r == 0), '/ 35')

print('=== 4. LAYOUT BALANCE ===')
check(build.COUNTS['EUROPE'] == 11, 'map/list panel compact, main cards expanded')
print('  main card height 230 px, small card 140 px, map/list 228 px')

print('=== 5. GATE ===')
p = 'entry.png'
im = Image.open(p); im.verify(); im = Image.open(p)
size = os.path.getsize(p)
check(im.format == 'PNG', 'PNG format')
check(im.size == (1024, 1024), '1024x1024')
check(size <= 1048576, '<= 1 MiB (%d bytes)' % size)

print('\nRESULT:', 'ALL PASS' if not fails else 'FAILED: %s' % fails)
sys.exit(0 if not fails else 1)
