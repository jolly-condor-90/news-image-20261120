# -*- coding: utf-8 -*-
"""Build the Friday 20 November 2026 world-news front page (1024x1024, <=1 MiB).

Every story on this page happened, or was first reported, on 20 November 2026.
Drawings are original vector art made with PIL; the map comes from world110.geojson.
"""
import json, math, os, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
S = 2                                  # supersample
W = H = 1024
FD = r'C:\Windows\Fonts'
OUT_DIR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'build20')

# ---------------------------------------------------------------- palette
PAPER  = '#FBF7EC'
INK    = '#191817'
MUTED  = '#574F46'
RED    = '#A62626'
REDLT  = '#C04141'
RULE   = '#8E2222'
OCEAN  = '#D8E8F1'
LAND   = '#EADCB9'
LANDLN = '#B8A175'
PANEL  = '#F2EADA'
WHITE  = '#FFFFFF'
NIGHT  = '#16243F'

REG = {
    'EUROPE':      {'c': '#2C6FB0', 'l': 'EUROPE'},
    'MIDDLE EAST': {'c': '#B43A2E', 'l': 'MIDDLE EAST'},
    'AFRICA':      {'c': '#2F8B5B', 'l': 'AFRICA'},
    'ASIA':        {'c': '#D2861B', 'l': 'ASIA'},
    'AMERICAS':    {'c': '#7748A8', 'l': 'AMERICAS'},
    'OCEANIA':     {'c': '#118A8E', 'l': 'OCEANIA'},
    'WORLD':       {'c': '#5A6472', 'l': 'WORLD'},
}
ORDER = ['EUROPE', 'MIDDLE EAST', 'AFRICA', 'ASIA', 'AMERICAS', 'OCEANIA', 'WORLD']

# ---------------------------------------------------------------- fonts
_fc = {}
def F(size, bold=False, serif=False, narrow=False):
    key = (size, bold, serif, narrow)
    if key in _fc:
        return _fc[key]
    if serif:   name = 'georgiab.ttf' if bold else 'georgia.ttf'
    elif narrow:name = 'ARIALNB.TTF' if bold else 'ARIALN.TTF'
    else:       name = 'arialbd.ttf' if bold else 'arial.ttf'
    f = ImageFont.truetype(os.path.join(FD, name), max(1, int(size * S)))
    _fc[key] = f
    return f

# ---------------------------------------------------------------- helpers
def R(b):  return tuple(int(v * S) for v in b)
def P(p):  return (int(p[0] * S), int(p[1] * S))
def rr(d, b, rad, fill=None, outline=None, width=1):
    d.rounded_rectangle(R(b), radius=int(rad * S), fill=fill, outline=outline,
                        width=max(1, int(width * S)))
def rc(d, b, fill=None, outline=None, width=1):
    d.rectangle(R(b), fill=fill, outline=outline, width=max(1, int(width * S)))
def ci(d, cx, cy, r, fill=None, outline=None, width=1):
    d.ellipse(R((cx-r, cy-r, cx+r, cy+r)), fill=fill, outline=outline,
              width=max(1, int(width * S)))
def ln(d, pts, fill, width=1):
    d.line([P(p) for p in pts], fill=fill, width=max(1, int(width * S)), joint='curve')
def pg(d, pts, fill=None, outline=None, width=1):
    d.polygon([P(p) for p in pts], fill=fill)
    if outline:
        d.line([P(p) for p in pts] + [P(pts[0])], fill=outline,
               width=max(1, int(width * S)))
def tx(d, x, y, s, f, fill=INK, anchor='la'):
    d.text(P((x, y)), s, font=f, fill=fill, anchor=anchor)
def tc(d, x, y, s, f, fill=INK):
    d.text(P((x, y)), s, font=f, fill=fill, anchor='ma')
def tw(d, s, f, maxw):
    out, cur = [], ''
    for word in s.split():
        t = (cur + ' ' + word).strip()
        if d.textlength(t, font=f) <= maxw * S:
            cur = t
        else:
            if cur: out.append(cur); cur = word
            else:   out.append(word); cur = ''
    if cur: out.append(cur)
    return out
def tlines(d, x, y, lines, f, fill=INK, lineh=None):
    lh = lineh or (f.size / S * 1.16)
    for i, L in enumerate(lines):
        tx(d, x, y + i * lh, L, f, fill)
    return y + len(lines) * lh

BOUNDS = []
def mark(name, b):
    BOUNDS.append((name, tuple(b)))

# ---------------------------------------------------------------- stories
# num, region, place, field, headline, body, source, lon, lat, time-label
STORIES = [
 (1,'EUROPE','KYIV, UKRAINE','WAR · OVERNIGHT',
  'Russian missiles hit three Kyiv bridges',
  'A barrage of about 110 missiles and 400 drones damaged three Dnipro bridges and cut power and water. At least 3 were killed in Kyiv; 9 across Ukraine (Kyiv Independent).',
  'Reuters / Kyiv Independent',30.52,50.45,'NIGHT → 03:00 EET · 20 NOV'),
 (2,'ASIA','GOPALPUR, ODISHA','CYCLONE · 08:00 IST',
  'Cyclone Akvan comes ashore in eastern India',
  'Akvan crossed the coast near Gopalpur between 07:30 and 08:30 IST with 70-80 km/h winds, gusting 90. Over 300,000 were moved to shelters; no deaths reported.',
  'IMD / The Hindu / PTI',84.9,19.3,'07:30–08:30 IST · 20 NOV'),
 (3,'WORLD','TAIPEI · SEOUL · TOKYO','MARKETS · FRIDAY CLOSE',
  "AI sell-off sinks Asia's stock markets",
  'Taiex fell 6.2%, Kospi 5.2% and Nikkei 5.1% as Anthropic\'s debut failed to revive AI trades. The region is heading for its worst week since 2020.',
  'Reuters / Al Jazeera',121.5,25.0,"FRI CLOSE · 20 NOV"),
 (4,'EUROPE','BRUSSELS','DIPLOMACY · 20 NOV',
  "UK and EU seal a 'reset' deal",
  'Food checks, linked carbon markets and 100,000 youth places a side were agreed in Brussels.',
  'Reuters / EUobserver',4.35,50.85,'BRUSSELS · 20 NOV'),
 (5,'WORLD','ANTALYA, TÜRKIYE','CLIMATE · DAY 12',
  'COP31 reaches its last day with no deal',
  'The draft leaves out fossil fuels; a third text is due Saturday as the 1.5C goal slips.',
  'UN News / Anadolu',30.7,36.9,'ANTALYA · 20 NOV'),
 (6,'EUROPE','EASTERN POLAND','SECURITY · 20 NOV',
  'Russian cruise missile lands in Poland',
  'A Kh-101 fell in a field near the border; two airports paused flights and no one was hurt.',
  'Reuters / Polish authorities',23.5,52.2,'E. POLAND · 20 NOV'),
 (7,'MIDDLE EAST','JURF AL-SAKHAR, IRAQ','SECURITY · 20 NOV',
  "Iraqi army enters a militia stronghold",
  'Troops deployed south of Karbala to retake the area from Iran-aligned militias.',
  'Reuters',44.2,32.5,'IRAQ · 20 NOV'),
 (8,'EUROPE','ROME, ITALY','LABOUR · 20 NOV',
  "General strike over Italy's budget",
  'The CGIL held a 24-hour strike across 100 squares as workers and students marched.',
  'Reuters',12.5,41.9,'ROME · 20 NOV'),
 (9,'ASIA','TOKYO, JAPAN','ECONOMY · OCT CPI',
  "Japan's inflation picks up to 2.3%",
  'October CPI rose 2.3%, keeping a December Bank of Japan rate rise firmly in view.',
  'Official data / Reuters',139.7,35.7,'TOKYO · 20 NOV'),
 (10,'AFRICA','TURKANA, KENYA','ENERGY · 20 NOV',
  'Kenya starts drilling its first oil well',
  'A ceremony marked the first Turkana well; first crude is targeted for 1 December.',
  'allAfrica',35.0,3.0,'TURKANA · 20 NOV'),
 (11,'OCEANIA','WELLINGTON','CRICKET · 20 NOV',
  'Phillips hits 118 against India',
  'Phillips made 118 and shared a stand of 175 against India.',
  'ICC',174.8,-41.3,'NZ · INDIA · 20 NOV'),
 (12,'EUROPE','LVIV, UKRAINE','WAR','Russian strike on a rail station kills 2',
  'A missile hit Lviv station; two were killed and railway services were disrupted.', 'BBC',24.0,49.8,'20 NOV'),
 (13,'EUROPE','MOSCOW, RUSSIA','POLITICS','Unity Day rallies as bridges close',
  'Authorities closed bridges in central Moscow for Victory and Unity Day events.', 'Reuters',37.6,55.75,'20 NOV'),
 (14,'EUROPE','BERLIN, GERMANY','EDUCATION','Pupils strike over military service',
  'School pupils walked out in several cities against a return to conscription.', 'Al Jazeera',13.4,52.5,'20 NOV'),
 (15,'EUROPE','LONDON, UK','LABOUR','Google workers strike over arms deals',
  'Staff protested the company\'s military contracts outside its King\'s Cross office.', 'Sky News',-0.13,51.5,'20 NOV'),
 (16,'ASIA','BEIJING, CHINA','ECONOMY','China holds lending rates for 18th month',
  'The PBOC left its loan prime rates unchanged for an eighteenth straight month.', 'Xinhua',116.4,39.9,'20 NOV'),
 (17,'ASIA','TOKYO, JAPAN','MARKETS','SoftBank slides 14%, its worst day in years',
  'The tech investor fell 14.5% in morning trade as the AI sell-off deepened.', 'WSJ / Guardian',139.7,35.7,'20 NOV'),
 (18,'ASIA','ODISHA, INDIA','WEATHER','209 mm of rain as Akvan crosses',
  'Ganjam district recorded 209 mm of rain while trains and flights were hit in Bengal.', 'PTI',84.0,19.5,'20 NOV'),
 (19,'ASIA','SEOUL, S. KOREA','POLITICS','Court to rule on impeached top judge',
  'The Constitutional Court set a date for the case of the suspended chief justice.', 'Korea Herald',127.0,37.6,'20 NOV'),
 (20,'EUROPE','SMOLENSK, RUSSIA','WAR','Drones reported to hit chemical plant',
  'Blast site video showed smoke at a plant; Moscow called the claims disinformation.', 'GLAST',32.0,54.8,'20 NOV'),
 (21,'WORLD','STRAIT OF HORMUZ','ENERGY','46 ships waiting; Brent near $92',
  'Tanker disruptions kept crude near $92 a barrel even as US inventories rose.', 'Reuters',56.5,26.6,'20 NOV'),
 (22,'AFRICA','DAKAR, SENEGAL','MIGRATION','Migrant boat capsizes; at least 4 dead',
  'A boat carrying migrants overturned off the coast; four bodies were recovered.', 'allAfrica',-17.4,14.7,'20 NOV'),
 (23,'AMERICAS','SAN SALVADOR','POLITICS','Bukele files for a third term',
  'The president filed his candidacy for a February 2027 election despite a court limit.', 'AP',-89.2,13.7,'20 NOV'),
 (24,'AMERICAS','BUENOS AIRES','MARKETS','Argentina country risk jumps 1,070',
  'The sovereign risk premium rose 1.5% to 1,070 points in a single month.', 'Reuters',-58.4,-34.6,'20 NOV'),
 (25,'AMERICAS','MEXICO CITY','POLITICS','Sheinbaum marks revolution anniversary',
  'The president addressed crowds on the 116th anniversary of the revolution.', 'Reuters',-99.1,19.4,'20 NOV'),
 (26,'AFRICA','BLANTYRE, MALAWI','ENERGY','Fuel crisis: 20 litres a day',
  'Queues for petrol stretched for blocks as the import squeeze deepened.', 'Al Jazeera',34.9,-13.9,'20 NOV'),
 (27,'AMERICAS','NEW YORK, USA','TECHNOLOGY','JPMorgan reports vendor cyberattack',
  'A third-party breach may have exposed customer data at the bank, it said.', 'Reuters',-74.0,40.7,'20 NOV'),
 (28,'WORLD','UNITED NATIONS','RIGHTS','Rohingya camp marks ICJ ruling',
  'Refugees in Cox\'s Bazar marked the court\'s order on Myanmar with prayers.', 'Al Jazeera',-74.0,40.7,'20 NOV'),
 (29,'AMERICAS','LAS VEGAS','MOTORSPORT','Russell fastest in wet F1 practice',
  'George Russell set the pace in a rain-hit practice ahead of the Las Vegas Grand Prix.', 'Autosport',-115.1,36.2,'20 NOV'),
 (30,'ASIA','SHENZHEN, CHINA','TECHNOLOGY','Gemini can now control a Mac',
  'Google said its assistant can operate a Mac, adding pressure on Apple\'s Siri.', 'Reuters',114.1,22.5,'20 NOV'),
 (31,'OCEANIA','SYDNEY, AUSTRALIA','MARKETS','Australian shares fall 1.8%',
  'The ASX 200 tracked the regional sell-off as miners and tech stocks slid.', 'Reuters',151.2,-33.9,'20 NOV'),
 (32,'WORLD','GLOBAL','CLIMATE','World Children\'s Day marked',
  'UNICEF marked the day as a report warned of worsening child hunger.', 'UN News',-74.0,40.7,'20 NOV'),
 (33,'ASIA','KUALA LUMPUR','MIGRATION','Malaysia to resettle 10,000 Rohingya',
  'Kuala Lumpur said it would take in 10,000 Rohingya refugees from camps in Bangladesh.', 'Reuters / Anadolu',101.7,3.1,'20 NOV'),
 (34,'AMERICAS','WASHINGTON, USA','ECONOMY',"Fed's Cook calls for a rate rise now",
  'A Fed governor argued for a December increase as inflation remained sticky.', 'Reuters',-77.0,38.9,'20 NOV'),
 (35,'ASIA','ANTALYA, TÜRKIYE','CLIMATE','$120bn adaptation gap remains',
  'Negotiators said the climate finance gap was still the main sticking point.', 'UN News',30.7,36.9,'20 NOV'),
]
BY_NUM = {s[0]: s for s in STORIES}
COUNTS = {r: sum(1 for s in STORIES if s[1] == r) for r in ORDER}
assert len(STORIES) == 35 and sum(COUNTS.values()) == 35

# ================================================================ MAIN ILLUSTRATIONS
def illu_kyiv(d, x, y, w, h):
    """Night city, Dnipro river and three struck bridges. Location, time and event."""
    rc(d, (x, y, x+w, y+h), NIGHT)
    # moon + stars
    ci(d, x+w*0.92, y+h*0.34, h*0.085, fill='#F3EBCB')
    ci(d, x+w*0.89, y+h*0.31, h*0.082, fill=NIGHT)
    for i in range(11):
        ci(d, x+((i*47) % int(w)), y+((i*29) % int(h*0.55)), 0.9, fill='#DDE6FF')
    # skyline
    for i in range(11):
        bx = x + i*w/11; bh = h*(0.26 + 0.07*((i*3) % 4))
        rc(d, (bx, y+h*0.66-bh, bx+w/11-1, y+h*0.66), '#101B33')
        for r in range(2):
            for c in range(2):
                if (i+r+c) % 2 == 0:
                    rc(d, (bx+4+c*w/28, y+h*0.66-bh+5+r*9,
                           bx+7+c*w/28, y+h*0.66-bh+9+r*9), '#E9C75B')
    # river
    rc(d, (x, y+h*0.66, x+w, y+h*0.86), '#274E72')
    for k in range(4):
        ln(d, [(x+w*0.05, y+h*(0.70+0.04*k)), (x+w*0.95, y+h*(0.70+0.04*k))], '#3E6D96', 0.8)
    # three bridges
    for k in range(3):
        bx = x + w*(0.14 + 0.30*k)
        ln(d, [(bx, y+h*0.60), (bx, y+h*0.84)], '#C9D2DD', 2)
        ln(d, [(bx+w*0.18, y+h*0.60), (bx+w*0.18, y+h*0.84)], '#C9D2DD', 2)
        ln(d, [(bx-4, y+h*0.64), (bx+w*0.18+4, y+h*0.64)], '#D8DEE8', 2.4)
        ln(d, [(bx, y+h*0.60), (bx+w*0.09, y+h*0.64)], '#AEBACD', 1)
        ln(d, [(bx+w*0.18, y+h*0.60), (bx+w*0.09, y+h*0.64)], '#AEBACD', 1)
        # broken centre + blast
        ex, ey = bx+w*0.09, y+h*0.64
        if k != 1:
            ln(d, [(ex-6, ey-8), (ex-2, ey+8)], NIGHT, 2.4)
        for a in range(9):
            an = 2*math.pi*a/9
            ln(d, [(ex, ey), (ex+math.cos(an)*h*0.10, ey+math.sin(an)*h*0.10)], '#F5A623', 1.6)
        ci(d, ex, ey, h*0.055, fill='#F0D26A')
        ci(d, ex, ey, h*0.028, fill='#E8702A')
    # incoming missile trails
    for k in range(3):
        sx = x+w*(0.20+0.28*k)
        pts = [(sx + i*w*0.10/8, y+h*0.05 + (i/8)**2*h*0.42) for i in range(9)]
        for i in range(0, len(pts)-1, 2):
            ln(d, [pts[i], pts[i+1]], '#F1D06A', 1.4)
        ci(d, pts[-1][0], pts[-1][1], 2.4, fill='#FFE9A8')
    # place + time labels
    rr(d, (x+6, y+6, x+w*0.44, y+25), 3, fill='#C0302A')
    tx(d, x+11, y+10, 'KYIV · UKRAINE', F(10.5, True), WHITE)
    tx(d, x+w-6, y+12, 'NIGHT → 03:00 EET · 20 NOV', F(7.6, True), '#DCE6F5', anchor='ra')
    rc(d, (x, y+h-20, x+w, y+h), '#8E2B22')
    tx(d, x+7, y+h-16, '3 DNIPRO BRIDGES HIT', F(11.5, True), WHITE)

def illu_cyclone(d, x, y, w, h):
    """Bay of Bengal, Odisha coast, Gopalpur landfall with time."""
    rc(d, (x, y, x+w, y+h), '#2E6E96')
    # land mass (left) with coastline curve
    coast = [(x, y), (x+w*0.34, y), (x+w*0.40, y+h*0.20),
             (x+w*0.37, y+h*0.40), (x+w*0.43, y+h*0.58),
             (x+w*0.39, y+h*0.78), (x+w*0.45, y+h), (x, y+h)]
    pg(d, coast, '#D8C79B')
    # coastline graticule fields
    for i in range(3):
        ln(d, [(x, y+h*(0.25+0.22*i)), (x+w*0.39, y+h*(0.27+0.22*i))], '#C0AD7E', 0.7)
    # rain streaks over land
    for k in range(9):
        rx = x+w*(0.05+0.033*k); ry = y+h*(0.30+0.02*(k % 3))
        ln(d, [(rx, ry), (rx-2, ry+7)], '#8FA8BD', 0.9)
    # Gopalpur dot
    gx, gy = x+w*0.40, y+h*0.50
    ci(d, gx, gy, 3.4, fill='#C0392B', outline=WHITE, width=1)
    tx(d, gx-6, gy-9, 'GOPALPUR', F(8, True), INK, anchor='ra')
    # landfall rings
    for r in (10, 17, 24):
        ci(d, gx, gy, r, outline='#F2C14E', width=1.4)
    # cyclone spiral approaching from sea
    cx, cy = x+w*0.72, y+h*0.42
    for r in range(10, 30, 5):
        pts = [(cx + (r - i*0.35)*math.cos(i*0.42),
                cy + (r - i*0.35)*math.sin(i*0.42)*0.8) for i in range(28)]
        ln(d, pts, WHITE, 1.4)
    ci(d, cx, cy, 4, fill=WHITE)
    ln(d, [(cx-14, cy+18), (gx+16, gy-6)], '#F2C14E', 1.6)
    pg(d, [(gx+22, gy-10), (gx+12, gy-6), (gx+22, gy-2)], '#F2C14E')
    # labels
    rr(d, (x+6, y+6, x+w*0.50, y+25), 3, fill='#1F5E6B')
    tx(d, x+11, y+10, 'ODISHA · INDIA', F(10.5, True), WHITE)
    tx(d, x+w-6, y+12, '07:30–08:30 IST · 20 NOV', F(7.6, True), '#EAF3F7', anchor='ra')
    tx(d, x+w*0.55, y+h*0.82, 'BAY OF BENGAL', F(7.8, True), '#EAF3F7')
    rc(d, (x, y+h-20, x+w, y+h), '#1F5E6B')
    tx(d, x+7, y+h-16, 'LANDFALL · 70–80 km/h · 300,000+ EVACUATED', F(10.5, True), WHITE)

def illu_selloff(d, x, y, w, h):
    """Falling markets with four index tickers and the day's close."""
    rc(d, (x, y, x+w, y+h), '#152036')
    for i in range(4):
        ln(d, [(x, y+h*(0.26+0.13*i)), (x+w*0.62, y+h*(0.26+0.13*i))], '#31405B', 0.7)
    # candlesticks + falling line
    vals = [0.34, 0.31, 0.36, 0.30, 0.40, 0.37, 0.48, 0.44, 0.56, 0.52, 0.64, 0.72]
    pts = []
    for i, v in enumerate(vals):
        px = x+w*(0.05 + i*0.55/11)
        pts.append((px, y+h*v))
        ln(d, [(px, y+h*(v-0.05)), (px, y+h*(v+0.04))], '#D8664F', 1)
        rc(d, (px-2, y+h*v, px+2, y+h*(v+0.05)), '#E0563C')
    ln(d, pts, '#F0704E', 2.2)
    # falling AI chip
    ccx, ccy = x+w*0.28, y+h*0.32
    rr(d, (ccx-12, ccy-8, ccx+12, ccy+8), 2, fill='#C9A227', outline='#F0D26A', width=1.2)
    tx(d, ccx, ccy, 'AI', F(9.5, True), '#2B2410', anchor='mm')
    for p in range(3):
        rc(d, (ccx-15, ccy-5+p*5, ccx-12, ccy-2+p*5), '#F0D26A')
        rc(d, (ccx+12, ccy-5+p*5, ccx+15, ccy-2+p*5), '#F0D26A')
    # tickers
    rows = [('TAIPEI', '-6.2%'), ('SEOUL', '-5.2%'),
            ('TOKYO', '-5.1%'), ('HONG KONG', '-1.9%')]
    for i, (nm, pct) in enumerate(rows):
        ry = y+h*(0.16+i*0.16)
        tx(d, x+w*0.65, ry, nm, F(8.6, True), '#C8D2E2')
        tx(d, x+w*0.97, ry, pct, F(9.2, True), '#FF8A6B', anchor='ra')
    # labels
    tx(d, x+7, y+5, 'ASIA · FRIDAY\'S CLOSE', F(9.5, True), WHITE)
    tx(d, x+w-6, y+5, '20 NOV 2026', F(7.8, True), '#B9C7DE', anchor='ra')
    rc(d, (x, y+h-20, x+w, y+h), '#7E2A22')
    tx(d, x+7, y+h-16, 'WORST WEEK SINCE 2020', F(11.5, True), WHITE)

# ================================================================ SMALL ILLUSTRATIONS
def _strip(d, x, y, w, h, text, col):
    rc(d, (x, y+h-14, x+w, y+h), col)
    tx(d, x+4, y+h-11, text, F(7.6, True), WHITE)

def illu_euuk(d, x, y, w, h):
    rc(d, (x, y, x+w, y+h), '#E8EFF3')
    ux, uy, uw, uh = x+w*0.06, y+h*0.15, w*0.24, h*0.44
    rc(d, (ux, uy, ux+uw, uy+uh), '#1B3E86')
    ln(d, [(ux, uy), (ux+uw, uy+uh)], WHITE, 2)
    ln(d, [(ux+uw, uy), (ux, uy+uh)], WHITE, 2)
    ln(d, [(ux+uw/2, uy), (ux+uw/2, uy+uh)], WHITE, 3)
    ln(d, [(ux, uy+uh/2), (ux+uw, uy+uh/2)], WHITE, 3)
    ex, ey = x+w*0.34, uy
    rc(d, (ex, ey, ex+uw, ey+uh), '#1F4EA0')
    for a in range(12):
        an = 2*math.pi*a/12
        ci(d, ex+uw/2+math.cos(an)*uh*0.27, ey+uh/2+math.sin(an)*uh*0.27, 1.5, fill='#F2C14E')
    # handshake
    hx, hy = x+w*0.72, y+h*0.36
    ln(d, [(hx-14, hy-8), (hx, hy+2), (hx+14, hy-8)], '#C98E63', 4)
    ci(d, hx, hy+2, 3, fill='#E0AA80')
    tx(d, x+w*0.63, y+h*0.53, '100,000', F(12.5, True, serif=True), RED)
    _strip(d, x, y, w, h, 'FOOD · CARBON · VISAS', '#2B5E86')

def illu_cop(d, x, y, w, h):
    rc(d, (x, y, x+w, y+h), '#CDE7EA')
    gx, gy, gr = x+w*0.26, y+h*0.40, h*0.30
    ci(d, gx, gy, gr, fill='#2E8FB8', outline=WHITE, width=1.2)
    ci(d, gx-gr*0.33, gy-gr*0.22, gr*0.28, fill='#5AA469')
    ci(d, gx+gr*0.30, gy+gr*0.16, gr*0.24, fill='#5AA469')
    rr(d, (x+w*0.52, y+h*0.16, x+w*0.58, y+h*0.60), 2, fill=WHITE, outline='#444', width=1.1)
    rc(d, (x+w*0.535, y+h*0.36, x+w*0.565, y+h*0.60), fill=RED)
    ci(d, x+w*0.55, y+h*0.64, h*0.075, fill=RED, outline='#444', width=1.1)
    rr(d, (x+w*0.66, y+h*0.20, x+w*0.96, y+h*0.56), 3, fill='#F6E7D2', outline=RED, width=1.6)
    tx(d, x+w*0.81, y+h*0.30, 'COP31', F(10.5, True), INK, anchor='mm')
    tx(d, x+w*0.81, y+h*0.46, 'NO DEAL', F(10, True), RED, anchor='mm')
    tx(d, x+6, y+h*0.53, '38°', F(11, True, serif=True), RED)
    _strip(d, x, y, w, h, 'ANTALYA · DAY 12 · NO DEAL', '#1F5E6B')

def illu_poland(d, x, y, w, h):
    rc(d, (x, y, x+w, y+h), '#DDE8C8')
    pg(d, [(x, y+h*0.66), (x+w*0.5, y+h*0.50), (x+w, y+h*0.62), (x+w, y+h), (x, y+h)], '#C9D6A6')
    # field furrows
    for i in range(4):
        ln(d, [(x, y+h*(0.72+0.06*i)), (x+w, y+h*(0.66+0.06*i))], '#AFC08C', 0.8)
    # missile falling
    ln(d, [(x+w*0.30, y+h*0.08), (x+w*0.52, y+h*0.50)], '#6E7A55', 1.6)
    pg(d, [(x+w*0.52, y+h*0.50), (x+w*0.46, y+h*0.44), (x+w*0.56, y+h*0.42)], '#4E5A3E')
    ci(d, x+w*0.55, y+h*0.56, h*0.09, fill='#E9A23B')
    for a in range(8):
        an = 2*math.pi*a/8
        ln(d, [(x+w*0.55, y+h*0.56),
                (x+w*0.55+math.cos(an)*h*0.15, y+h*0.56+math.sin(an)*h*0.15)], '#D8663A', 1.2)
    tx(d, x+6, y+6, 'KH-101', F(9.5, True), '#4E5A3E')
    _strip(d, x, y, w, h, 'MISSILE IN A FIELD · 2 AIRPORTS PAUSED', '#6B6E3C')

def illu_iraq(d, x, y, w, h):
    rc(d, (x, y, x+w, y+h), '#E7D8B4')
    ci(d, x+w*0.86, y+h*0.20, h*0.11, fill='#F0C85A')
    pg(d, [(x, y+h*0.72), (x+w*0.5, y+h*0.58), (x+w, y+h*0.70), (x+w, y+h), (x, y+h)], '#CDB58A')
    for k in range(2):
        vx = x+w*(0.18+0.38*k); vy = y+h*0.50
        rc(d, (vx-16, vy-6, vx+16, vy+6), '#4B6142', outline='#2F4029', width=1)
        rc(d, (vx-8, vy-12, vx+8, vy-5), '#5F7A52', outline='#2F4029', width=1)
        ln(d, [(vx+10, vy-8), (vx+16, vy-16)], '#2F4029', 1.4)
        for ww in (-12, -4, 4, 12):
            ci(d, vx+ww, vy+7, 2.6, fill='#222A1E')
    tx(d, x+6, y+6, 'JURF AL-SAKHAR', F(9, True), '#3D4A32')
    _strip(d, x, y, w, h, 'ARMY ENTERS MILITIA STRONGHOLD', '#6E4A2C')

def illu_italy(d, x, y, w, h):
    rc(d, (x, y, x+w, y+h), '#F0E6DA')
    for i in range(4):
        bx = x+w*(0.12+0.24*i)
        ci(d, bx, y+h*0.36, h*0.10, fill='#465266')
        pg(d, [(bx-9, y+h*0.48), (bx+9, y+h*0.48), (bx+7, y+h*0.78), (bx-7, y+h*0.78)], '#7C8AA0')
        ln(d, [(bx-8, y+h*0.56), (bx-16, y+h*0.68)], '#465266', 2)
    rr(d, (x+w*0.56, y+h*0.18, x+w*0.94, y+h*0.52), 2, fill=WHITE, outline=RED, width=1.6)
    tx(d, x+w*0.75, y+h*0.31, 'SCIOPERO', F(9.5, True), RED, anchor='mm')
    tx(d, x+w*0.75, y+h*0.44, '24h', F(8.5, True), INK, anchor='mm')
    _strip(d, x, y, w, h, '100 SQUARES · ROME', '#8E2B22')

def illu_japan(d, x, y, w, h):
    rc(d, (x, y, x+w, y+h), '#EAF1F4')
    for i in range(4):
        ln(d, [(x+w*0.05, y+h*(0.30+0.12*i)), (x+w*0.62, y+h*(0.30+0.12*i))], '#CCD9DE', 0.7)
    bars = [0.50, 0.46, 0.52, 0.44, 0.38, 0.32]
    for i, v in enumerate(bars):
        rc(d, (x+w*(0.06+i*0.085), y+h*v, x+w*(0.11+i*0.085), y+h*0.78), '#7FA6BB')
    pts = [(x+w*(0.085+i*0.085), y+h*(v-0.04)) for i, v in enumerate(bars)]
    ln(d, pts, RED, 1.8)
    rr(d, (x+w*0.60, y+h*0.16, x+w*0.96, y+h*0.54), 3, fill=WHITE, outline=RED, width=1.4)
    tx(d, x+w*0.78, y+h*0.36, '+2.3%', F(16, True, serif=True), RED, anchor='mm')
    tx(d, x+6, y+h*0.53, 'OCT CPI', F(8.5, True), '#4A5C66')
    _strip(d, x, y, w, h, 'BOJ DECEMBER RISE IN VIEW', '#2C6FB0')

def illu_kenya(d, x, y, w, h):
    rc(d, (x, y, x+w, y+h), '#EADFBE')
    pg(d, [(x, y+h*0.72), (x+w*0.5, y+h*0.58), (x+w, y+h*0.70), (x+w, y+h), (x, y+h)], '#CDBE8C')
    # derrick
    px, py = x+w*0.42, y+h*0.18
    ln(d, [(px-14, y+h*0.72), (px, py), (px+14, y+h*0.72)], '#5B4A33', 2)
    for i in range(4):
        yy = py + i*h*0.12
        ln(d, [(px-14+i*3.5, yy), (px+14-i*3.5, yy)], '#7A6447', 1.2)
    rc(d, (px-9, py-8, px+9, py-2), '#3F4A52')
    ln(d, [(px, py-2), (px, y+h*0.70)], '#6B5A40', 1.2)
    rr(d, (x+w*0.66, y+h*0.16, x+w*0.96, y+h*0.40), 2, fill=WHITE, outline='#5B4A33', width=1)
    tx(d, x+w*0.81, y+h*0.28, '1st WELL', F(9, True), '#5B4A33', anchor='mm')
    tx(d, x+5, y+h*0.52, 'TURKANA', F(9, True), '#5B4A33')
    _strip(d, x, y, w, h, 'FIRST CRUDE DUE 1 DECEMBER', '#2F8B5B')

def illu_cricket(d, x, y, w, h):
    rc(d, (x, y, x+w, y+h), '#1E4E3A')
    # scoreboard
    rr(d, (x+w*0.06, y+h*0.14, x+w*0.56, y+h*0.76), 3, fill='#132C21', outline='#8FC0A0', width=1.2)
    tx(d, x+w*0.31, y+h*0.30, 'NZ', F(9, True), '#9FD6B4', anchor='mm')
    tx(d, x+w*0.31, y+h*0.56, '118', F(19, True, serif=True), '#F2C14E', anchor='mm')
    # stumps + ball
    sx = x+w*0.76
    for k in range(3):
        rc(d, (sx-12+k*9, y+h*0.34, sx-9+k*9, y+h*0.78), '#EDE6D2')
    rc(d, (sx-15, y+h*0.34, sx+15, y+h*0.38), '#EDE6D2')
    ci(d, sx+18, y+h*0.62, h*0.09, fill='#C0392B', outline='#8E2B22', width=1)
    ln(d, [(sx+14, y+h*0.62), (sx+22, y+h*0.62)], WHITE, 0.9)
    tx(d, x+6, y+5, 'WELLINGTON', F(9, True), '#CFE9D9')
    _strip(d, x, y, w, h, '118 · STAND OF 175 · v INDIA', '#118A8E')

MAIN_ILLU = {1: illu_kyiv, 2: illu_cyclone, 3: illu_selloff}
SMALL_ILLU = {4: illu_euuk, 5: illu_cop, 6: illu_poland, 7: illu_iraq,
              8: illu_italy, 9: illu_japan, 10: illu_kenya, 11: illu_cricket}

# ================================================================ MAP
def load_map():
    path = os.path.join(HERE, 'world110.geojson')
    if not os.path.exists(path):
        path = os.path.join(ROOT, 'world110.geojson')
    data = json.load(open(path, encoding='utf-8'))
    rings = []
    for ft in data['features']:
        if ft['properties'].get('NAME') == 'Antarctica':
            continue
        g = ft['geometry']
        polys = [g['coordinates']] if g['type'] == 'Polygon' else g['coordinates']
        for p in polys:
            if p and len(p[0]) > 2:
                rings.append(p[0])
    return rings
RINGS = load_map()

def draw_map(d, box):
    x0, y0, x1, y1 = box
    mw, mh = x1-x0, y1-y0
    LAT_T, LAT_B = 83, -58
    def pr(lon, lat):
        return (x0 + (lon+180)/360*mw, y0 + (LAT_T-lat)/(LAT_T-LAT_B)*mh)
    rc(d, box, OCEAN, outline='#97B4C6', width=1)
    for lon in range(-180, 181, 30):
        ln(d, [pr(lon, LAT_T), pr(lon, LAT_B)], '#C6DEEA', 0.6)
    for lat in range(-60, 84, 30):
        ln(d, [pr(-180, lat), pr(180, lat)], '#C6DEEA', 0.6)
    for ring in RINGS:
        pg(d, [pr(c[0], c[1]) for c in ring], LAND, outline=LANDLN, width=0.7)
    # numbered pins: dot at the real place, label pushed to a free ring, joined by a line
    entries = []
    for s in STORIES:
        dx, dy = pr(s[7], s[8])
        entries.append([s[0], REG[s[1]]['c'], dx, dy])
    rad = 6.6
    placed, out = [], []
    for num, col, dx, dy in entries:
        best = None
        for ring in (0, 9, 17, 26, 36, 48, 62, 78):
            steps = max(8, int(ring*2.1))
            for k in range(steps):
                a = 2*math.pi*k/steps + ring*0.37
                cx = dx + ring*math.cos(a)
                cy = dy + ring*math.sin(a)*0.85
                if x0+9 <= cx <= x1-9 and y0+9 <= cy <= y1-9:
                    if all((cx-px)**2+(cy-py)**2 > (2*rad+3.5)**2 for px, py in placed):
                        best = (cx, cy, ring); break
            if best: break
        if not best: best = (dx, dy, 0)
        cx, cy, ring = best
        placed.append((cx, cy))
        out.append((num, col, dx, dy, cx, cy, ring))
    for num, col, dx, dy, cx, cy, ring in out:
        if ring > 2:
            ln(d, [(dx, dy), (cx, cy)], '#5B6874', 0.8)
            ci(d, dx, dy, 1.8, fill=col)
        ci(d, cx, cy, rad, fill=col, outline=WHITE, width=1.2)
        tc(d, cx, cy+2.8, str(num), F(8.8, True), WHITE)
    mark('map', box)

# ================================================================ BUILD
def build():
    im = Image.new('RGB', (W*S, H*S), PAPER)
    d = ImageDraw.Draw(im)
    M = 16

    # ---- masthead
    ln(d, [(M, 11), (W-M, 11)], RED, 1.4)
    tx(d, M, 13, 'THE WORLD IN ONE DAY', F(10.5, True), RED)
    s = '35 STORIES  ·  7 REGIONS  ·  EVERY ONE DATED FRIDAY 20 NOVEMBER 2026'
    tx(d, W-M, 13, s, F(9.4), MUTED, anchor='ra')
    tc(d, W/2, 26, 'Friday 20 November 2026', F(45, True, serif=True), INK)
    tc(d, W/2, 74, "Missiles hit Kyiv's bridges  ·  Cyclone Akvan strikes India  ·  An AI sell-off sinks Asia's markets  ·  UK and EU seal a deal",
       F(12.4), MUTED)
    ln(d, [(M, 90), (W-M, 90)], RED, 1.6)
    mark('headline', (M, 18, W-M, 89))

    # ---- six key numbers
    stats = [('3', 'KYIV BRIDGES HIT BY MISSILES'),
             ('300,000+', 'MOVED TO SHELTERS BEFORE AKVAN'),
             ('−6.2%', "TAIWAN'S TAIEX, FRIDAY'S CLOSE"),
             ('100,000', 'YOUTH PLACES IN THE UK–EU DEAL'),
             ('2.3%', "JAPAN'S OCTOBER INFLATION"),
             ('118', 'PHILLIPS AGAINST INDIA')]
    bw = (W-2*M)/6
    for i, (big, lab) in enumerate(stats):
        x0 = M+i*bw
        if i: ln(d, [(x0, 96), (x0, 128)], '#C9BFA9', 0.8)
        tx(d, x0+5, 97, big, F(16.5, True, serif=True), RED)
        tlines(d, x0+5, 117, tw(d, lab, F(7.6), bw-10)[:2], F(7.6), INK, lineh=8.8)
        mark('stat%d' % i, (x0, 94, x0+bw, 130))
    ln(d, [(M, 131), (W-M, 131)], '#C9BFA9', 0.8)

    # ---- seven-region key
    total = sum(COUNTS.values()); bx = M
    for r in ORDER:
        seg = (W-2*M)*COUNTS[r]/total
        rc(d, (bx, 135, bx+seg, 153), REG[r]['c'])
        lab = '%s %d' % (REG[r]['l'], COUNTS[r])
        tc(d, bx+seg/2, 140, lab, F(8.3 if seg > 78 else 7.4, True), WHITE)
        bx += seg
    mark('regionbar', (M, 135, W-M, 153))

    # ---- three main cards
    gap = 8; cw = (W-2*M-2*gap)/3
    for i, num in enumerate([1, 2, 3]):
        s = BY_NUM[num]; x0 = M+i*(cw+gap); y0 = 157; ch = 204; ih = 96
        col = REG[s[1]]['c']
        rc(d, (x0, y0, x0+cw, y0+ch), WHITE, outline='#BEB5A2', width=1)
        MAIN_ILLU[num](d, x0+1, y0+1, cw-2, ih)
        yy = y0+ih+3
        rc(d, (x0+3, yy, x0+cw-3, yy+15), col)
        tx(d, x0+7, yy+2, '%d · %s · %s' % (num, s[2], s[3]), F(8.8, True), WHITE)
        yy += 18
        hl = tw(d, s[4], F(17.4, True, serif=True), cw-12)[:3]
        yy = tlines(d, x0+7, yy, hl, F(17.4, True, serif=True), INK, lineh=18.0)
        yy += 2
        bl = tw(d, s[5], F(10.6), cw-13)[:4]
        tlines(d, x0+7, yy, bl, F(10.6), MUTED, lineh=11.8)
        tx(d, x0+7, y0+ch-10, s[6], F(8.0, True), col)
        mark('main%d' % num, (x0, y0, x0+cw, y0+ch))

    # ---- eight small cards, enlarged so each holds a real illustration
    g2 = 6; sw = (W-2*M-3*g2)/4; sh = 132; ih2 = 57
    for i, num in enumerate(range(4, 12)):
        s = BY_NUM[num]; row, cc = i//4, i%4
        x0 = M+cc*(sw+g2); y0 = 366+row*(sh+8)
        col = REG[s[1]]['c']
        rc(d, (x0, y0, x0+sw, y0+sh), WHITE, outline='#BEB5A2', width=1)
        SMALL_ILLU[num](d, x0+1, y0+1, sw-2, ih2)
        yy = y0+ih2+4
        rc(d, (x0+3, yy, x0+sw-3, yy+15), col)
        tx(d, x0+6, yy+2, '%d · %s' % (num, s[2]), F(8.4, True), WHITE)
        yy += 18
        hl = tw(d, s[4], F(13.2, True, serif=True), sw-11)[:3]
        yy = tlines(d, x0+6, yy, hl, F(13.2, True, serif=True), INK, lineh=14.2)
        yy += 2
        bl = tw(d, s[5], F(9.2), sw-11)[:2]
        tlines(d, x0+6, yy, bl, F(9.2), MUTED, lineh=10.6)
        mark('small%d' % num, (x0, y0, x0+sw, y0+sh))

    # ---- map + remaining stories
    y0 = 660; mbox = (M, y0, 432, 930)
    rc(d, (M, y0-17, 432, y0-1), INK)
    tx(d, M+6, y0-15, 'WHERE IT HAPPENED', F(10.5, True), WHITE)
    tx(d, 426, y0-15, '1–35 number the stories; dots and lines mark 7 regions.', F(7.6), WHITE, anchor='ra')
    draw_map(d, mbox)
    tx(d, M+4, 920, 'Numbers are placed around a dot so they never overlap.', F(7.8), MUTED)

    lx0, lx1 = 440, W-M
    rc(d, (lx0, y0-17, lx1, y0-1), INK)
    tx(d, lx0+6, y0-15, 'ALSO ON FRIDAY 20 NOVEMBER 2026  —  24 MORE STORIES', F(10.2, True), WHITE)
    rc(d, (lx0, y0, lx1, 930), PANEL, outline='#BEB5A2', width=1)
    items = [s for s in STORIES if s[0] >= 12]
    half = (len(items)+1)//2; colw = (lx1-lx0-14)/2
    for j, s in enumerate(items):
        cc, rw = j//half, j % half
        cx = lx0+7+cc*colw; cy = y0+5+rw*21.0
        col = REG[s[1]]['c']
        ci(d, cx+5, cy+4, 5.8, fill=col)
        tc(d, cx+5, cy+6, str(s[0]), F(7.2, True), WHITE)
        tlines(d, cx+14, cy, tw(d, s[4], F(8.6), colw-19)[:1], F(8.6), INK, lineh=10.0)
    mark('list', (lx0, y0, lx1, 930))

    # ---- compact date check, pulled down close to the foot
    rc(d, (M, 940, W-M, 984), '#FBF3E4', outline=RED, width=1.3)
    rc(d, (M, 940, M+124, 955), RED)
    tx(d, M+5, 942, 'DATE CHECK  ✓', F(9.6, True), WHITE)
    tx(d, M+8, 959, 'Every story happened, or was first reported, on Friday 20 November 2026 in at least one time zone — the day this image sums up.',
       F(9.2), INK)
    dc = ("Left out as earlier news: the Trump–Xi Shenzhen summit and Anthropic's IPO pricing (19 Nov); the ICJ Myanmar ruling, "
          "BepiColombo's launch (2018) and Bhumibol's death (2016). Claims are attributed; no forecast is shown as fact.")
    tlines(d, M+8, 972, tw(d, dc, F(8.6), W-2*M-16)[:2], F(8.6), MUTED, lineh=10.2)
    mark('datecheck', (M, 940, W-M, 984))

    # ---- sources hugging the bottom edge with a tight, even margin
    ln(d, [(M, 994), (W-M, 994)], '#C9BFA9', 0.8)
    tc(d, W/2, 1000, 'Sources named beside each story · Original drawings, not photographs · 20 November 2026',
       F(8.8), MUTED)
    mark('footer', (M, 994, W-M, 1020))

    im = im.resize((W, H), Image.LANCZOS)
    os.makedirs(OUT_DIR, exist_ok=True)
    p = os.path.join(OUT_DIR, 'entry.png')
    im.save(p, optimize=True)
    # 300 px legibility proof
    im.resize((300, 300), Image.LANCZOS).save(os.path.join(OUT_DIR, 'preview300.png'))
    print('WROTE', p, os.path.getsize(p), 'bytes')
    bad = [(n, b) for n, b in BOUNDS if b[0] < 0 or b[1] < 0 or b[2] > W or b[3] > H]
    print('OUT OF FRAME:', bad if bad else 'none')
    return p

if __name__ == '__main__':
    build()
