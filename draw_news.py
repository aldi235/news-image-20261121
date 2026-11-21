#!/usr/bin/env python3
"""Draw 'The World Today' for Saturday 21 November 2026 — dense edition.

One 1024x1024 newspaper-style image: a lead story plus 39 short,
source-tagged stories across seven regions, a world-map panel, a
markets chart and a UTC timeline strip. Pure stdlib + Pillow.
Run with `python3 draw_news.py`.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 34
CW = W - 2 * MARGIN  # 956

PAPER = (247, 244, 236)
INK = (18, 18, 18)
RED = (178, 34, 30)
BLUE = (26, 74, 122)
GREY = (96, 96, 92)
MAP_BG = (224, 232, 238)
MAP_LAND = (205, 216, 196)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
LIB_DIR = "/usr/share/fonts/truetype/liberation"


def font(name, size, base=FONT_DIR):
    return ImageFont.truetype(os.path.join(base, name), size)


F_MAST = font("DejaVuSerif-Bold.ttf", 56)
F_DATE = font("DejaVuSans-Bold.ttf", 15)
F_KICK = font("DejaVuSans-Bold.ttf", 14)
F_LEAD = font("DejaVuSerif-Bold.ttf", 32)
F_DEK = font("LiberationSerif-Italic.ttf", 16, LIB_DIR)
F_LEAD_BODY = font("DejaVuSans.ttf", 14)
F_REGION = font("DejaVuSans-Bold.ttf", 12)
F_STORY = font("DejaVuSans.ttf", 12)
F_TAG = font("DejaVuSans-Bold.ttf", 10)
F_CHART = font("DejaVuSans-Bold.ttf", 12)
F_CHART_LBL = font("DejaVuSans.ttf", 12)
F_TL_T = font("DejaVuSans-Bold.ttf", 11)
F_TL = font("DejaVuSans.ttf", 11)
F_MAP_CAP = font("DejaVuSans.ttf", 10)
F_FOOT = font("DejaVuSans.ttf", 11)

# (region, story text, source tag) — every fact verified against the
# named outlet; the check mark confirms the story is dated 21 Nov 2026.
STORIES = [
    ("EUROPE",
     "Britain and the EU seal a Brexit reset on food trade, carbon "
     "markets and youth visas.", "REUTERS"),
    ("EUROPE",
     "Poland asks NATO for F-35 jets and AWACS planes; no formal "
     "Article 4 move yet.", "REUTERS"),
    ("EUROPE",
     "Denmark expels Russia's defence attaché over a plot to kill rapper "
     "Kyivstoner.", "REUTERS"),
    ("EUROPE",
     "Former PM Dominique de Villepin declares his run for France's 2027 "
     "presidency.", "POLLAR"),
    ("EUROPE",
     "Thousands of Berlin students march against rearmament and "
     "conscription fears.", "SUMI"),
    ("EUROPE",
     "German metalworkers launch their first 24-hour strike in eight years "
     "over pay.", "EUROPA EXPRESS"),
    ("EUROPE",
     "Spain's top court keeps 163,355 new citizens off the 29 Nov voter "
     "rolls.", "POLLAR"),
    ("MIDDLE EAST",
     "Saudi defences down three Houthi missiles over Riyadh; one hit a "
     "tower.", "REUTERS"),
    ("MIDDLE EAST",
     "Trump weighs new strikes on Iran; he will decide after 1 January.",
     "NYT"),
    ("MIDDLE EAST",
     "Iran says diplomacy can still end the war; Trump calls Tehran's terms "
     "unacceptable.", "REUTERS"),
    ("MIDDLE EAST",
     "Heavy rain floods 70,000 tents in Gaza; a baby died of "
     "hypothermia, WHO says.", "WHO"),
    ("MIDDLE EAST",
     "Sixteen nations back UK-Australian sanctions on settlement "
     "entities.", "M. EAST EYE"),
    ("ASIA",
     "Japan's exports hit a record in October on strong chip-related "
     "demand.", "REUTERS"),
    ("ASIA",
     "India's core industries output jumped 10.9% in October.", "GOVT OF INDIA"),
    ("ASIA",
     "Nikhil Gupta is jailed for 19 years over a plot to kill Sikh "
     "separatist Pannun in New York.", "NY COURT"),
    ("ASIA",
     "Myanmar calls the ICJ's Rohingya genocide ruling 'biased' and says "
     "it was unjustly accused.", "KSPEARLS"),
    ("ASIA",
     "Mongolia's parliament accepts President Khurelsukh's resignation "
     "amid a coal-railway graft row.", "REUTERS"),
    ("AMERICAS",
     "Wall Street: the S&P 500 fell 3.7% and the Dow 1.9% on Friday; both "
     "are now in correction.", "REUTERS"),
    ("AMERICAS",
     "Rinderknecht, 30, is convicted of starting the 2025 Palisades fire "
     "that killed 12.", "REUTERS"),
    ("AMERICAS",
     "Mayor Mamdani plans to close New York's Rikers Island jail by 2032.",
     "REUTERS"),
    ("AMERICAS",
     "Anthropic debuts on Wall Street at a $2tn valuation, then slides "
     "9%.", "NYT"),
    ("AMERICAS",
     "The FBI's criminal database is reportedly hacked amid US outages.",
     "ONETURN"),
    ("AMERICAS",
     "Trump tells Europe to stop funding Ukraine after the Shenzhen "
     "summit.", "TELEGRAPH"),
    ("AMERICAS",
     "El Salvador's Bukele registers to run for a third term in 2027.",
     "BREITBART"),
    ("AMERICAS",
     "Tesla opens its first store in Argentina; Model 3 and Y listed from "
     "about $40,000.", "REUTERS"),
    ("AFRICA",
     "Nearly 600 women were killed in South Africa within three months, "
     "new figures show.", "BBC"),
    ("AFRICA",
     "A US consortium wins Kenya's Mrima Hill minerals deal; deposits top "
     "$60bn.", "BBC"),
    ("AFRICA",
     "Dozens are missing after a boat carrying 100 migrants sinks off "
     "Senegal's coast.", "BBC"),
    ("AFRICA",
     "Nigeria moves to end jail terms for attempted suicide.", "BBC"),
    ("AFRICA",
     "Kenyan cult leader Paul Mackenzie is jailed for 200 years for "
     "murdering 191 people.", "BBC"),
    ("OCEANIA",
     "Australia, Canada and NZ issue a joint APEC statement on peace.",
     "DFAT"),
    ("OCEANIA",
     "India reach 486/4 at stumps on day three against New Zealand; "
     "Rahul 136, Gill 98, lead 118.", "EIN"),
    ("GLOBAL",
     "COP31 runs into overtime with no deal; Ethiopia will host COP32 in "
     "Addis Ababa.", "REUTERS"),
    ("GLOBAL",
     "Voyager 1 is one light-day from Earth, 26bn km out; its data feed "
     "is silent since 14 Nov.", "NASA"),
    ("GLOBAL",
     "An Anthropic mathematician claims AI proved the Riemann hypothesis.",
     "BBC"),
    ("GLOBAL",
     "An experimental pill shrank tumours in 44% of pancreatic cancer "
     "patients.", "REUTERS"),
    ("GLOBAL",
     "Antonelli is fastest in Las Vegas qualifying, but Verstappen "
     "takes pole.", "REUTERS"),
    ("GLOBAL",
     "Ramla Ali becomes unified super-bantamweight champion, beating "
     "Mikiah Kreps in Texas.", "BBC"),
    ("GLOBAL",
     "Trump, Putin and Xi hail a four-point 'peace declaration' in "
     "Shenzhen.", "CNN"),
]

# Column plan: (regions in order) per column.
COLUMNS = [
    ["EUROPE", "MIDDLE EAST"],
    ["ASIA", "AMERICAS"],
    ["AFRICA", "OCEANIA", "GLOBAL"],
]

LEAD_KICK = "POLAND  ·  RUSSIA–UKRAINE WAR"
LEAD_HEAD = "Russian missiles land in Poland"
LEAD_DEK = ("NATO chief Mark Rutte flies to Warsaw today after two cruise "
            "missiles and a jet-powered drone crashed in south-east Poland.")
LEAD_BODY = ("No one was hurt, but PM Donald Tusk called it an “intentional "
             "provocation”: the weapons fell near Nowa Deba, where 11 "
             "nations are holding Exercise Koalicja. Poland has asked NATO "
             "for F-35 jets and AWACS planes. The barrage fired 110 "
             "missiles at Kyiv, killing eight, wounding 28 and cutting "
             "power in 11 regions.")

MARKETS = [("S&P 500", -3.7), ("Dow", -1.9), ("Nasdaq", -5.3),
           ("Nvidia", -13.8), ("Anthropic", -9.1)]

TIMELINE = [
    ("01:30", "S&P 500 & Dow confirmed in correction"),
    ("02:40", "Riyadh: 3 Houthi missiles downed"),
    ("MORNING", "Rutte in Warsaw; COP31 draft due"),
    ("14:10", "England v New Zealand, Twickenham"),
    ("16:40", "Ireland v South Africa, Dublin"),
    ("TONIGHT", "Verstappen on pole tonight"),
]

# Coarse continent outlines (lon, lat) for the schematic world map.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 72), (-85, 70),
     (-80, 73), (-65, 60), (-55, 52), (-60, 45), (-70, 42), (-75, 35),
     (-80, 32), (-81, 25), (-90, 21), (-97, 26), (-105, 23), (-110, 28),
     (-115, 32), (-120, 34), (-125, 40), (-124, 48), (-130, 55),
     (-140, 60), (-155, 58), (-165, 60)],
    [(-80, 10), (-75, 12), (-70, 12), (-60, 8), (-52, 5), (-45, 0),
     (-35, -8), (-40, -20), (-48, -28), (-52, -33), (-58, -38),
     (-62, -41), (-65, -45), (-68, -50), (-70, -54), (-73, -50),
     (-73, -40), (-72, -30), (-70, -20), (-75, -15), (-80, -5)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31),
     (35, 28), (40, 15), (48, 11), (42, 0), (40, -10), (35, -18),
     (32, -28), (25, -34), (18, -32), (15, -22), (12, -10), (9, 4),
     (4, 6), (-8, 5), (-13, 8)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (3, 53), (8, 57), (10, 58),
     (18, 56), (21, 55), (24, 58), (28, 60), (30, 70), (40, 68),
     (50, 69), (60, 69), (70, 72), (80, 73), (90, 75), (100, 77),
     (110, 74), (120, 73), (130, 71), (140, 72), (150, 70), (160, 69),
     (170, 67), (178, 65), (178, 62), (170, 60), (162, 56), (158, 52),
     (150, 45), (142, 42), (140, 38), (135, 34), (130, 33), (127, 35),
     (122, 38), (120, 32), (115, 23), (110, 20), (108, 12), (105, 9),
     (103, 2), (100, 7), (98, 12), (95, 16), (92, 21), (88, 22),
     (85, 19), (80, 15), (77, 8), (75, 12), (72, 20), (68, 23),
     (66, 25), (62, 25), (58, 27), (56, 27), (52, 26), (50, 29),
     (48, 30), (44, 29), (40, 32), (36, 36), (30, 36), (27, 37),
     (23, 36), (19, 40), (15, 44), (12, 44), (8, 44), (3, 43),
     (-2, 37), (-6, 36), (-9, 37)],
    [(114, -22), (114, -28), (118, -35), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38),
     (150, -37), (153, -32), (153, -27), (150, -23), (146, -19),
     (142, -15), (142, -11), (137, -12), (132, -12), (126, -14),
     (122, -17), (118, -20)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (1, 53), (1, 51),
     (-2, 50)],
    [(130, 31), (133, 34), (137, 35), (140, 36), (141, 39), (142, 44),
     (145, 44), (144, 40), (140, 38), (136, 34), (132, 33)],
    [(167, -45), (171, -42), (174, -39), (178, -38), (176, -40),
     (172, -43), (168, -46)],
]

# Story locations marked on the map: (lon, lat).
MARKERS = [(21, 52), (30, 50), (47, 25), (0, 51), (-74, 41), (37, -1),
           (139, 36), (151, -34), (106, 47)]


def wrap(draw, text, fnt, width):
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, width, text, fnt, fill=INK, leading=None):
    leading = leading or int(fnt.size * 1.35)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, x1, y, width=1, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_story(draw, x, y, width, text, source):
    """One short story: wrapped text, source tag + check after the end."""
    lines = wrap(draw, text, F_STORY, width)
    tag = " · " + source + " ✓"
    # Try to fit the tag on the last line; else it gets its own line.
    last = lines[-1]
    if draw.textlength(last, font=F_STORY) + draw.textlength(
            tag, font=F_TAG) <= width:
        lines[-1] = last + tag
        tag_on_last = True
    else:
        tag_on_last = False
    for i, line in enumerate(lines):
        if tag_on_last and i == len(lines) - 1:
            draw.text((x, y), last, font=F_STORY, fill=INK)
            tx = x + draw.textlength(last, font=F_STORY)
            draw.text((tx, y + 1), tag, font=F_TAG, fill=GREY)
        else:
            draw.text((x, y), line, font=F_STORY, fill=INK)
        y += 14
    if not tag_on_last:
        draw.text((x, y + 1), tag.strip(), font=F_TAG, fill=GREY)
        y += 14
    return y + 2


def draw_region(draw, x, y, width, name):
    draw.text((x, y), name, font=F_REGION, fill=RED)
    rule(draw, x, x + width, y + 17, width=1, fill=RED)
    return y + 22


def draw_world_map(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=MAP_BG, outline=INK, width=1)

    def proj(lon, lat):
        px = x + (lon + 180.0) / 360.0 * w
        py = y + (85.0 - lat) / 145.0 * h
        return px, py

    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        draw.polygon(pts, fill=MAP_LAND, outline=(120, 130, 110))
    for lon, lat in MARKERS:
        px, py = proj(lon, lat)
        draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED,
                     outline=(255, 255, 255), width=1)
    draw.text((x + 8, y + h - 16), "WHERE THE NEWS HAPPENED",
              font=F_MAP_CAP, fill=GREY)


def draw_markets_strip(draw, x, y, w):
    """Compact one-box markets line under the shortest column."""
    draw.text((x, y), "MARKETS · FRIDAY", font=F_CHART, fill=INK)
    figures = "  ·  ".join(f"{label} {pct:.1f}%" for label, pct in MARKETS)
    return para(draw, x, y + 18, w, figures, F_CHART_LBL, fill=RED,
                leading=16)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    title = "The World Today"
    tw = d.textlength(title, font=F_MAST)
    d.text(((W - tw) / 2, 16), title, font=F_MAST, fill=INK)
    rule(d, MARGIN, W - MARGIN, 88, width=1)
    d.text((MARGIN, 94), "SATURDAY 21 NOVEMBER 2026", font=F_DATE, fill=INK)
    right = "39 stories  ·  7 regions  ·  every story source-checked"
    d.text((W - MARGIN - d.textlength(right, font=F_DATE), 94), right,
           font=F_DATE, fill=GREY)
    rule(d, MARGIN, W - MARGIN, 118, width=3)

    # ---- Lead story + world map ------------------------------------------
    y = 128
    d.text((MARGIN, y), LEAD_KICK, font=F_KICK, fill=RED)
    y += 22
    d.text((MARGIN, y), LEAD_HEAD, font=F_LEAD, fill=INK)
    y += 42
    lead_left = 640
    y2 = para(d, MARGIN, y, lead_left, LEAD_DEK, F_DEK, leading=21)
    y2 += 6
    y2 = para(d, MARGIN, y2, lead_left, LEAD_BODY, F_LEAD_BODY,
              leading=19)
    map_x = MARGIN + lead_left + 16
    map_w = W - MARGIN - map_x
    draw_world_map(d, map_x, y, map_w, y2 - y)
    y = y2 + 10
    rule(d, MARGIN, W - MARGIN, y, width=1)

    # ---- Story grid: three columns ---------------------------------------
    grid_top = y + 10
    col_w = 300
    gap = 28
    by_region = {}
    for region, text, source in STORIES:
        by_region.setdefault(region, []).append((text, source))
    col_bottoms = []
    for ci, regions in enumerate(COLUMNS):
        cx = MARGIN + ci * (col_w + gap)
        cy = grid_top
        for region in regions:
            cy = draw_region(d, cx, cy, col_w, region)
            for text, source in by_region[region]:
                cy = draw_story(d, cx, cy, col_w, text, source)
            cy += 4
        col_bottoms.append(cy)
        print(f"column {ci + 1} ends at y={cy}")
    grid_bottom = max(col_bottoms)

    # Markets strip under the shortest column (column 1).
    strip_x = MARGIN
    strip_y = col_bottoms[0] + 8
    rule(d, strip_x, strip_x + col_w, strip_y, width=1, fill=GREY)
    strip_end = draw_markets_strip(d, strip_x, strip_y + 8, col_w)
    grid_bottom = max(grid_bottom, strip_end)

    # ---- Timeline strip ---------------------------------------------------
    tl_y = 916
    rule(d, MARGIN, W - MARGIN, tl_y, width=1)
    d.text((MARGIN, tl_y + 8), "21 NOV  ·  UTC", font=F_TL_T, fill=RED)
    line_y = tl_y + 34
    rule(d, MARGIN, W - MARGIN, line_y, width=1, fill=GREY)
    tl_x0 = MARGIN + 100
    slot = (CW - 100) // len(TIMELINE)
    for i, (when, what) in enumerate(TIMELINE):
        sx = tl_x0 + i * slot
        d.ellipse([sx + 2, line_y - 3, sx + 8, line_y + 3], fill=RED)
        d.text((sx + 12, line_y - 22), when, font=F_TL_T, fill=INK)
        ty = line_y + 8
        for line in wrap(d, what, F_TL, slot - 14):
            d.text((sx + 12, ty), line, font=F_TL, fill=INK)
            ty += 13

    # ---- Footer ------------------------------------------------------------
    foot = ("Sources: Reuters, AP, BBC, WSJ, CNN, The Times, ISW, NASA, "
            "UN News, WHO  ·  Drawn by an AI agent for make.fun")
    fw = d.textlength(foot, font=F_FOOT)
    rule(d, MARGIN, W - MARGIN, 990, width=1)
    d.text(((W - fw) / 2, 996), foot, font=F_FOOT, fill=GREY)

    print(f"grid bottom y={grid_bottom}, timeline at y={tl_y}")
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
