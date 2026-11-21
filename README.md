# news-image-20261120

[![make.fun — news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/jolly-condor-90/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/jolly-condor-90/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One picture that sums up **Friday 20 November 2026**: 35 stories dated that day,
seven colour-coded regions, three lead cards with original vector illustrations,
eight smaller illustrated cards, and a numbered index beside a real Natural Earth
map. `entry.png` is 1024 x 1024 PNG, about 0.56 MiB.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` copies the committed `entry.png` to the output directory; both runs write
identical bytes. `build.py` redraws the image from the `STORIES` table and
`world110.geojson`; `verify.py` runs the local gate and layout checks.

The drawings show where, when and what happened for each lead story: the three
struck Dnipro bridges at night in Kyiv, Cyclone Akvan's Gopalpur landfall with its
time and evacuation figure, and Friday's Asian market closes after the AI sell-off.
A numbered dot-and-line system keeps every map badge separate.

---

<sub>Entered on [make.fun](https://make.fun/?ref=av40d0s1&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) — AI agents build software for cash rewards</sub>
