"""Generate assets/header.svg and assets/footer.svg for the GitHub profile README."""
import math
import random
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

FONT = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"


def wave(y, amp, period, width, height):
    """Seamless wave path covering width + one extra period (for looping translate)."""
    half = period / 2
    d = f"M0,{y} Q{half / 2},{y - amp} {half},{y}"
    x = half
    while x < width + period:
        x += half
        d += f" T{x:g},{y}"
    d += f" V{height} H0 Z"
    return d


# ---------------------------------------------------------------- the cat
# Modelled on the real one: cream-white coat with greige patches on the forehead,
# ears, flanks and tail, pale blue eyes under heavy, slightly grumpy lids, pink nose.
BODY = "M-52,137 C-66,96 -42,48 0,48 C42,48 66,96 52,137 Q0,147 -52,137 Z"
TAIL = "M38,128 C86,134 104,96 88,66 C82,54 92,44 100,52"
CAT = f"""
  <g id="cat" transform="translate(1060 168) scale(.9)">
    <defs>
      <clipPath id="bodyClip"><path d="{BODY}"/></clipPath>
      <clipPath id="headClip"><ellipse cx="0" cy="26" rx="41" ry="33"/></clipPath>
      <clipPath id="lidL"><path d="M-27,19.6 L-5,22.6 V36 H-27 Z"/></clipPath>
      <clipPath id="lidR"><path d="M27,19.6 L5,22.6 V36 H27 Z"/></clipPath>
    </defs>
    <!-- tail (behind body): greige with faint rings -->
    <g class="tail">
      <path d="{TAIL}" fill="none" stroke="url(#patch)" stroke-width="13" stroke-linecap="round"/>
      <path d="{TAIL}" fill="none" stroke="#a89886" stroke-width="13" stroke-dasharray="3 12"
            stroke-dashoffset="-34" opacity=".4"/>
    </g>
    <!-- body -->
    <path d="{BODY}" fill="url(#fur)"/>
    <g clip-path="url(#bodyClip)">
      <!-- greige patches wrapping round from the back -->
      <g fill="url(#patch)" filter="url(#soft)">
        <ellipse cx="-53" cy="104" rx="19" ry="25"/>
        <ellipse cx="49" cy="76" rx="16" ry="19"/>
        <ellipse cx="56" cy="122" rx="12" ry="14"/>
      </g>
      <!-- shadow under the chin -->
      <ellipse cx="0" cy="56" rx="29" ry="8" fill="#ccd8ef" opacity=".6"/>
    </g>
    <path d="M-16,72 C-22,96 -18,120 -8,134 L8,134 C18,120 22,96 16,72 Z" fill="#ffffff" opacity=".85"/>
    <!-- front paws -->
    <ellipse cx="-15" cy="136" rx="13" ry="7.5" fill="#ffffff"/>
    <ellipse cx="15" cy="136" rx="13" ry="7.5" fill="#ffffff"/>
    <path d="M-19,134 v4 M-12,134 v4 M11,134 v4 M18,134 v4" stroke="#b9cff0" stroke-width="1.2" stroke-linecap="round"/>
    <!-- head -->
    <g class="head">
      <!-- ears: greige outside, pink inside -->
      <path d="M-38,12 Q-41,-14 -34,-31 Q-17,-19 -4,0 Z" fill="url(#patch)"/>
      <path d="M38,12 Q41,-14 34,-31 Q17,-19 4,0 Z" fill="url(#patch)"/>
      <path d="M-32,6 Q-33,-10 -30,-20 Q-20,-11 -13,0 Z" fill="#f6bcc4"/>
      <path d="M32,6 Q33,-10 30,-20 Q20,-11 13,0 Z" fill="#f6bcc4"/>
      <ellipse cx="0" cy="26" rx="41" ry="33" fill="url(#fur)"/>
      <!-- forehead patches, split by a white blaze -->
      <g clip-path="url(#headClip)">
        <g fill="url(#patch)" filter="url(#soft)">
          <path d="M-4,-14 H-50 V19 Q-38,19 -31,12 Q-19,5 -9,11 Q-4.5,4 -4,-14 Z"/>
          <path d="M4,-14 H50 V19 Q38,19 31,12 Q19,5 9,11 Q4.5,4 4,-14 Z"/>
        </g>
        <path d="M-23,-1 L-21,7 M-14.5,-4 L-13.5,5 M23,-1 L21,7 M14.5,-4 L13.5,5"
              stroke="#a89886" stroke-width="1.5" stroke-linecap="round" opacity=".45"/>
      </g>
      <!-- eyes: pale blue, heavy lids -->
      <g class="eyes">
        <g clip-path="url(#lidL)">
          <circle cx="-15.5" cy="25" r="7.8" fill="#b4d5f4" stroke="#6f9dd0" stroke-width="1.1"/>
          <circle cx="-15.5" cy="26" r="4.3" fill="#131d38"/>
          <circle cx="-13.4" cy="24.6" r="1.6" fill="#fff"/>
        </g>
        <g clip-path="url(#lidR)">
          <circle cx="15.5" cy="25" r="7.8" fill="#b4d5f4" stroke="#6f9dd0" stroke-width="1.1"/>
          <circle cx="15.5" cy="26" r="4.3" fill="#131d38"/>
          <circle cx="17.6" cy="24.6" r="1.6" fill="#fff"/>
        </g>
        <path d="M-24.4,20 L-7.6,22.3 M24.4,20 L7.6,22.3" stroke="#66728c" stroke-width="1.4" stroke-linecap="round"/>
      </g>
      <!-- nose (pink, one freckle) + mouth -->
      <ellipse cx="0" cy="30.5" rx="3.2" ry="4.5" fill="#f9cdd2" opacity=".55"/>
      <path d="M-4.6,34 Q0,32.6 4.6,34 Q3.2,38.6 0,39.6 Q-3.2,38.6 -4.6,34 Z" fill="#f29aa6"/>
      <circle cx="2.8" cy="37.4" r=".7" fill="#6a5656"/>
      <path d="M-6.5,44.5 Q-3,45.5 0,40 Q3,45.5 6.5,44.5" fill="none" stroke="#8aa3c7" stroke-width="1.4" stroke-linecap="round"/>
      <!-- whiskers -->
      <g stroke="#dfe8f8" stroke-width="1.1" stroke-linecap="round">
        <path d="M-20,38 L-52,33 M-20,41 L-52,44"/>
        <path d="M20,38 L52,33 M20,41 L52,44"/>
      </g>
    </g>
  </g>
"""

W, H = 1200, 340
HORIZON = 256
MOON_X, MOON_Y = 920, 86
rng = random.Random(7)


def night_sky(n):
    """Mostly faint static stars (drawn as dot paths) plus a few bright twinkling ones.

    Stars thin out toward the horizon haze and around the moon, as they do in a real sky.
    """
    faint = {0.5: [], 0.7: [], 0.95: []}
    bright = []
    while n:
        x, y = rng.uniform(4, W - 4), rng.uniform(4, HORIZON - 10)
        d = math.hypot(x - MOON_X, y - MOON_Y)
        if rng.random() < (y / HORIZON) ** 2 * 0.9:
            continue
        if d < 62 or (d < 150 and rng.random() < 0.75):
            continue
        n -= 1
        m = rng.random()
        behind_text = 50 < x < 770 and 90 < y < 240
        if m > 0.93 and not behind_text:
            bright.append((x, y))
        else:
            r = 0.5 if m < 0.6 else 0.7 if m < 0.88 else 0.95
            faint[r].append(f"M{x:.1f},{y:.1f}h.01")
    out = [
        f'<path d="{"".join(d)}" fill="none" stroke="#dbe7ff" stroke-width="{2 * r:g}" '
        f'stroke-linecap="round" opacity="{o}"/>'
        for (r, d), o in zip(faint.items(), (0.5, 0.7, 0.9))
    ]
    for x, y in bright:
        tint = rng.choice(["#ffffff", "#d6e6ff", "#fff3dc"])
        r = rng.choice([1.0, 1.2, 1.5])
        out.append(
            f'<g class="star" style="animation-duration:{rng.uniform(2.4, 5.5):.2f}s;'
            f'animation-delay:-{rng.uniform(0, 4):.2f}s">'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r * 4:.1f}" fill="url(#starGlow)"/>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{tint}"/></g>'
        )
    return "\n    ".join(out)


def depth(u):
    """Perspective for the sea: 0 at the horizon, 1 at the bottom edge. Evenly spaced u bunches up far away."""
    return u ** 1.7


def sea_y(u):
    return HORIZON + 1 + (H - HORIZON) * depth(u)


def ripples(u0, u1, rows, period, color, opacity, trough=False):
    """Rows of short wavelets between two depths; smaller, thinner and denser toward the horizon."""
    paths = []
    for i in range(rows):
        u = u0 + (u1 - u0) * (i + rng.random()) / rows
        t = depth(u)
        mean = 5 + 60 * t
        n = max(2, round(period / (mean * 2.8)))
        d = ""
        for k in range(n):
            x = (k + rng.random()) * period / n
            length = mean * rng.uniform(0.5, 1.4)
            arc = (0.3 + 2.2 * t) * rng.uniform(0.5, 1.2) * (-1 if trough else 1)
            y = sea_y(u) + rng.uniform(-1, 1) * (0.5 + 2 * t)
            d += f"M{x:.1f},{y:.1f}q{length / 2:.1f},{-arc:.1f} {length:.1f},0"
        paths.append(f'<path d="{d}" stroke-width="{0.5 + 1.6 * t:.2f}"/>')
    return f'<g fill="none" stroke="{color}" stroke-linecap="round" opacity="{opacity}">{"".join(paths)}</g>'


def tiled(name, cls, period, body):
    """Repeat a period-wide strip so translating it by one period loops seamlessly."""
    copies = "".join(f'<use href="#{name}" x="{period * k}"/>' for k in range(1, math.ceil(W / period) + 1))
    return f'<g class="{cls}"><g id="{name}">{body}</g>{copies}</g>'


def glitter(groups=3, rows=44):
    """Moonlight broken up on the water: a column of streaks that widens toward the viewer."""
    buckets = [[[] for _ in range(3)] for _ in range(groups)]
    for i in range(rows):
        u = (i + rng.random()) / rows
        t = depth(u)
        half = 6 + 58 * t
        for _ in range(2 + round(3 * t + rng.random())):
            length = (3 + 20 * t) * rng.uniform(0.4, 1.3)
            x = MOON_X + rng.gauss(0, half / 2.6) - length / 2
            buckets[rng.randrange(groups)][min(2, int(t * 3))].append(f"M{x:.1f},{sea_y(u):.1f}h{length:.1f}")
    return "".join(
        f'<g class="g{g + 1}">'
        + "".join(f'<path d="{"".join(b)}" stroke-width="{w}"/>' for b, w in zip(bs, (0.7, 1.1, 1.6)) if b)
        + "</g>"
        for g, bs in enumerate(buckets)
    )


def foam(y, x0):
    """Broken line of foam where the swell meets the rock."""
    groups = [["", ""], ["", ""]]
    x = x0
    while x < W:
        length = rng.uniform(1.5, 8)
        thick = rng.random() < 0.35
        dy = rng.gauss(0, 2.2) + (2.5 if thick else 0)
        groups[rng.randrange(2)][thick] += f"M{x:.1f},{y + dy:.1f}q{length / 2:.1f},{rng.uniform(-1, 1):.1f} {length:.1f},0"
        x += length + rng.uniform(1, 12)
    return "".join(
        f'<g class="f{i + 1}"><path d="{thin}" stroke-width="1"/><path d="{thick}" stroke-width="2.2"/></g>'
        for i, (thin, thick) in enumerate(groups)
    )


def crest(y, amp, period, width):
    """Just the top edge of wave(), for a highlight stroke."""
    return wave(y, amp, period, width, 0).rsplit(" V", 1)[0]


# Rock outline pieces, shared by the fills and the moonlit rim strokes.
ROCK_BACK = "992,294 L1008,288 L1024,286.5 L1046,285 L1076,286 L1104,284.5 L1128,285.5 L1146,282"
ROCK_BOULDER = "L1158,272 L1174,266 L1188,256 L1200,252"
ROCK_LIP = "984,301 L1004,300 L1022,301 L1048,302.5 L1078,301 L1106,302.5 L1130,300 L1146,296"
ROCK_LEFT = "984,301 L977,311 L966,318 L958,330 L948,340"
LIP_REVERSED = " L".join(reversed(ROCK_LIP.split(" L")))

header = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Kusanagi - a white cat watching the moon over a blue sea">
  <title>Hi, I'm Kusanagi</title>
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="{HORIZON}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#020715"/>
      <stop offset=".42" stop-color="#051436"/>
      <stop offset=".78" stop-color="#0a2459"/>
      <stop offset=".94" stop-color="#15418d"/>
      <stop offset="1" stop-color="#2c62b8"/>
    </linearGradient>
    <linearGradient id="sea" x1="0" y1="{HORIZON}" x2="0" y2="{H}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#2a5db2"/>
      <stop offset=".07" stop-color="#16428d"/>
      <stop offset=".45" stop-color="#0b2a69"/>
      <stop offset="1" stop-color="#06173f"/>
    </linearGradient>
    <linearGradient id="swell" x1="0" y1="316" x2="0" y2="{H}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#103680"/>
      <stop offset="1" stop-color="#06173f"/>
    </linearGradient>
    <linearGradient id="title" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#ffffff"/>
      <stop offset=".6" stop-color="#bfe0ff"/>
      <stop offset="1" stop-color="#58a6ff"/>
    </linearGradient>
    <linearGradient id="fur" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#fffefb"/>
      <stop offset="1" stop-color="#e2e9f9"/>
    </linearGradient>
    <linearGradient id="patch" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#e0d5c8"/>
      <stop offset="1" stop-color="#c6b9ab"/>
    </linearGradient>
    <radialGradient id="moonGlow">
      <stop offset="0" stop-color="#cfe6ff" stop-opacity=".5"/>
      <stop offset=".3" stop-color="#8fbfff" stop-opacity=".2"/>
      <stop offset="1" stop-color="#7fb8ff" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="moonDisc" cx=".45" cy=".4" r=".62">
      <stop offset="0" stop-color="#ffffff"/>
      <stop offset=".7" stop-color="#e9f0fb"/>
      <stop offset="1" stop-color="#c2d1ea"/>
    </radialGradient>
    <radialGradient id="starGlow">
      <stop offset="0" stop-color="#dfeaff" stop-opacity=".45"/>
      <stop offset="1" stop-color="#dfeaff" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="cloud">
      <stop offset="0" stop-color="#a9c4f0" stop-opacity=".3"/>
      <stop offset=".6" stop-color="#a9c4f0" stop-opacity=".1"/>
      <stop offset="1" stop-color="#a9c4f0" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="seaGlow">
      <stop offset="0" stop-color="#dcecff" stop-opacity=".7"/>
      <stop offset="1" stop-color="#dcecff" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="moonPath">
      <stop offset="0" stop-color="#bcd8ff" stop-opacity=".2"/>
      <stop offset="1" stop-color="#bcd8ff" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="rockFace" x1="0" y1="290" x2="0" y2="{H}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#22386a"/>
      <stop offset="1" stop-color="#081226"/>
    </linearGradient>
    <linearGradient id="rockTop" x1="984" y1="0" x2="1152" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#6387c8"/>
      <stop offset="1" stop-color="#38548e"/>
    </linearGradient>
    <linearGradient id="shoot" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/>
      <stop offset="1" stop-color="#fff"/>
    </linearGradient>
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="3" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="soft" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="1.6"/>
    </filter>
    <!-- stone grain: noise lit from the moon's side, multiplied onto the rock's own colours -->
    <filter id="stone" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">
      <feTurbulence type="fractalNoise" baseFrequency=".07 .13" numOctaves="4" seed="11" result="n"/>
      <feDiffuseLighting in="n" surfaceScale="2.6" diffuseConstant="1.6" lighting-color="#ffffff" result="l">
        <feDistantLight azimuth="210" elevation="44"/>
      </feDiffuseLighting>
      <feBlend in="SourceGraphic" in2="l" mode="multiply" result="b"/>
      <feComposite in="b" in2="SourceAlpha" operator="in"/>
    </filter>
    <clipPath id="moonClip"><circle r="46"/></clipPath>
    <clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
  </defs>
  <style>
    .star {{ animation: twinkle 3s ease-in-out infinite; }}
    @keyframes twinkle {{ 0%,100% {{ opacity:.35 }} 50% {{ opacity:1 }} }}
    .w1 {{ animation: drift 18s linear infinite; }}
    .w2 {{ animation: drift 12s linear infinite reverse; }}
    .w3 {{ animation: drift 8s linear infinite; }}
    @keyframes drift {{ from {{ transform: translateX(0) }} to {{ transform: translateX(-240px) }} }}
    .far {{ animation: flow 160s linear infinite; }}
    .mid {{ animation: flow 70s linear infinite; }}
    .near {{ animation: flow 30s linear infinite; }}
    @keyframes flow {{ from {{ transform: translateX(0) }} to {{ transform: translateX(-600px) }} }}
    .g1 {{ animation: shimmer 2.6s ease-in-out infinite; }}
    .g2 {{ animation: shimmer 3.4s ease-in-out -1.1s infinite; }}
    .g3 {{ animation: shimmer 4.3s ease-in-out -2s infinite; }}
    @keyframes shimmer {{ 0%,100% {{ opacity:.3 }} 50% {{ opacity:1 }} }}
    .f1 {{ animation: foam 4s ease-in-out infinite; }}
    .f2 {{ animation: foam 4s ease-in-out -2s infinite; }}
    @keyframes foam {{ 0%,100% {{ opacity:.12 }} 50% {{ opacity:.65 }} }}
    .clouds {{ animation: clouds 90s ease-in-out infinite alternate; }}
    @keyframes clouds {{ from {{ transform: translateX(0) }} to {{ transform: translateX(-60px) }} }}
    .tail {{ transform-origin: 38px 128px; animation: swish 3.2s ease-in-out infinite; }}
    @keyframes swish {{ 0%,100% {{ transform: rotate(0deg) }} 50% {{ transform: rotate(-14deg) }} }}
    .eyes {{ transform-box: fill-box; transform-origin: center; animation: blink 5s infinite; }}
    @keyframes blink {{ 0%,92%,100% {{ transform: scaleY(1) }} 95% {{ transform: scaleY(.08) }} }}
    .head {{ transform-origin: 0px 50px; animation: tilt 7s ease-in-out infinite; }}
    @keyframes tilt {{ 0%,40%,100% {{ transform: rotate(0deg) }} 50%,85% {{ transform: rotate(-6deg) }} }}
    .meteor {{ animation: meteor 7s ease-in infinite; opacity:0; }}
    @keyframes meteor {{ 0% {{ transform: translate(0,0); opacity:0 }} 3% {{ opacity:1 }} 12% {{ transform: translate(-260px,130px); opacity:0 }} 100% {{ opacity:0 }} }}
    .moon {{ animation: pulse 6s ease-in-out infinite; transform-origin: {MOON_X}px {MOON_Y}px; }}
    @keyframes pulse {{ 0%,100% {{ transform: scale(1) }} 50% {{ transform: scale(1.06) }} }}
    .caret {{ animation: caret 1s steps(1) infinite; }}
    @keyframes caret {{ 50% {{ opacity:0 }} }}
  </style>

  <g clip-path="url(#frame)">
    <rect width="{W}" height="{HORIZON + 1}" fill="url(#sky)"/>

    <!-- stars -->
    {night_sky(270)}

    <!-- shooting star -->
    <g class="meteor"><rect x="720" y="34" width="110" height="2" rx="1" fill="url(#shoot)" transform="rotate(-27 830 35)"/></g>

    <!-- moon: halo, disc, maria -->
    <circle cx="{MOON_X}" cy="{MOON_Y}" r="250" fill="url(#moonGlow)" opacity=".35"/>
    <circle cx="{MOON_X}" cy="{MOON_Y}" r="120" fill="url(#moonGlow)" class="moon"/>
    <circle cx="{MOON_X}" cy="{MOON_Y}" r="46" fill="url(#moonDisc)" filter="url(#glow)"/>
    <g clip-path="url(#moonClip)" transform="translate({MOON_X} {MOON_Y})">
      <g fill="#7d92ba" opacity=".42" filter="url(#soft)">
        <ellipse cx="-27" cy="-3" rx="10" ry="21" transform="rotate(8 -27 -3)"/>
        <ellipse cx="-12" cy="-20" rx="13" ry="10.5"/>
        <ellipse cx="10" cy="-17" rx="8.5" ry="7.5"/>
        <ellipse cx="19" cy="-5" rx="10" ry="7.5" transform="rotate(25 19 -5)"/>
        <ellipse cx="33" cy="-13" rx="4.5" ry="3.5"/>
        <ellipse cx="28" cy="7" rx="5.5" ry="8"/>
        <ellipse cx="17" cy="11" rx="4" ry="4"/>
        <ellipse cx="-10" cy="17" rx="10" ry="7.5"/>
        <ellipse cx="-24" cy="17" rx="5" ry="5"/>
      </g>
      <circle cx="-4" cy="32" r="3.5" fill="#ffffff" opacity=".7" filter="url(#soft)"/>
    </g>

    <!-- thin clouds catching the moonlight -->
    <g class="clouds" fill="url(#cloud)">
      <ellipse cx="850" cy="121" rx="135" ry="8"/>
      <ellipse cx="985" cy="112" rx="110" ry="6"/>
      <ellipse cx="900" cy="131" rx="70" ry="5"/>
      <ellipse cx="1040" cy="56" rx="95" ry="6"/>
      <ellipse cx="790" cy="52" rx="80" ry="4.5"/>
      <ellipse cx="1120" cy="205" rx="150" ry="8"/>
      <ellipse cx="640" cy="232" rx="210" ry="7" opacity=".8"/>
      <ellipse cx="260" cy="238" rx="240" ry="7" opacity=".7"/>
      <ellipse cx="420" cy="62" rx="150" ry="5" opacity=".45"/>
      <ellipse cx="1010" cy="118" rx="60" ry="11" opacity=".7"/>
      <ellipse cx="800" cy="125" rx="70" ry="10" opacity=".6"/>
      <ellipse cx="1150" cy="200" rx="70" ry="12" opacity=".6"/>
    </g>

    <!-- far shore on the horizon -->
    <path d="M0,{HORIZON + 1} V250 C34,245 62,247 104,248.5 C150,243.5 196,242 236,247 C276,251 312,253.5 356,{HORIZON + 1} Z" fill="#0b2458"/>

    <!-- sea -->
    <rect y="{HORIZON}" width="{W}" height="{H - HORIZON}" fill="url(#sea)"/>
    <ellipse cx="{MOON_X}" cy="{HORIZON + 1}" rx="190" ry="5" fill="url(#seaGlow)" opacity=".8"/>
    {tiled("rf", "far", 600, ripples(0.02, 0.42, 9, 600, "#8db2ec", 0.34) + ripples(0.05, 0.42, 6, 600, "#03102e", 0.3, True))}
    <g class="w1"><path d="{wave(283, 2, 240, W, H)}" fill="#06173f" opacity=".22"/></g>
    {tiled("rm", "mid", 600, ripples(0.42, 0.86, 8, 600, "#7ba6ea", 0.32) + ripples(0.44, 0.86, 6, 600, "#020b22", 0.34, True))}
    <g class="w2"><path d="{wave(303, 3, 240, W, H)}" fill="#051334" opacity=".25"/></g>

    <!-- moonlight on the water -->
    <ellipse cx="{MOON_X}" cy="{H}" rx="120" ry="{H - HORIZON}" fill="url(#moonPath)"/>
    <g fill="none" stroke="#e8f2ff" stroke-linecap="round" opacity=".8">{glitter()}</g>

    <!-- rocky ledge the cat sits on -->
    <g filter="url(#stone)">
      <path d="M{ROCK_BACK} {ROCK_BOULDER} V{H} H948 L958,330 L966,318 L977,311 L984,301 Z" fill="url(#rockFace)"/>
      <path d="M{ROCK_BACK} L1152,292 L{LIP_REVERSED} Z" fill="url(#rockTop)"/>
      <path d="M984,301 L1004,300 L1000,316 L988,330 L978,{H} H948 L958,330 L966,318 L977,311 Z" fill="#2f4c86"/>
      <path d="M1004,300 L1022,301 L1048,302.5 L1042,320 L1000,316 Z" fill="#101f40" opacity=".75"/>
      <path d="M1078,301 L1106,302.5 L1112,322 L1086,318 Z" fill="#203763" opacity=".85"/>
      <path d="M1146,282 L1158,272 L1174,266 L1170,282 L1162,300 L1152,292 Z" fill="#3d5b96"/>
      <path d="M1174,266 L1188,256 L1200,252 V300 L1180,296 L1170,282 Z" fill="#1a2f5a"/>
    </g>
    <path d="M1048,302.5 L1042,320 L1050,{H} M1106,302.5 L1112,322 L1104,{H} M1162,300 L1156,318 L1164,{H} M1004,300 L1000,316 L988,330 M1170,282 L1180,296 L1200,300"
          fill="none" stroke="#020611" stroke-width="1.2" stroke-linejoin="round" opacity=".7"/>
    <g fill="none" stroke-linejoin="round" stroke-linecap="round">
      <path d="M{ROCK_BACK} {ROCK_BOULDER}" stroke="#9dbff2" stroke-width="1.3" opacity=".8"/>
      <path d="M{ROCK_LIP}" stroke="#6b93d6" stroke-width="1" opacity=".5"/>
      <path d="M{ROCK_LEFT}" stroke="#6b93d6" stroke-width="1" opacity=".45"/>
    </g>
    <ellipse cx="1062" cy="294.5" rx="50" ry="4.5" fill="#01050f" opacity=".45" filter="url(#soft)"/>

    {CAT}

    <!-- swell breaking against the rock -->
    <g class="w3">
      <path d="{wave(322, 3, 240, W, H)}" fill="url(#swell)" opacity=".95"/>
      <path d="{crest(322, 3, 240, W)}" fill="none" stroke="#7aa7ec" stroke-width="1" opacity=".35"/>
    </g>
    <ellipse cx="1082" cy="338" rx="150" ry="12" fill="#020816" opacity=".4"/>
    {tiled("rn", "near", 600, ripples(0.9, 1, 3, 600, "#6f9de6", 0.3) + ripples(0.9, 1, 2, 600, "#010716", 0.35, True))}
    <g fill="none" stroke="#dcebff" stroke-linecap="round">{foam(322, 934)}</g>

    <!-- text -->
    <g font-family="{FONT}">
      <text x="72" y="118" font-size="22" fill="#79c0ff" font-family="{MONO}">&gt; hello, world<tspan class="caret">_</tspan></text>
      <text x="70" y="182" font-size="64" font-weight="800" fill="url(#title)" letter-spacing="1">Hi, I'm Kusanagi</text>
      <text x="74" y="226" font-size="22" fill="#a5c8ff">@Fudzuki  ·  Wideplink / Discope / TAO  ·  Japan</text>
    </g>
  </g>
</svg>
"""

FW, FH = 1200, 150
paws = []
for i in range(7):
    x = 160 + i * 130
    y = 66 + (14 if i % 2 else -6)
    paws.append(
        f'<g class="paw" style="animation-delay:{i * 0.45:.2f}s" transform="translate({x} {y}) rotate(90)">'
        '<ellipse cx="0" cy="6" rx="9" ry="7.5"/>'
        '<circle cx="-9" cy="-5" r="3.6"/><circle cx="-3" cy="-10" r="3.6"/>'
        '<circle cx="3" cy="-10" r="3.6"/><circle cx="9" cy="-5" r="3.6"/></g>'
    )
footer = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{FW}" height="{FH}" viewBox="0 0 {FW} {FH}" role="img" aria-label="Paw prints over blue waves">
  <title>Thanks for visiting</title>
  <defs>
    <clipPath id="f"><rect width="{FW}" height="{FH}" rx="18"/></clipPath>
  </defs>
  <style>
    .paw {{ fill:#ffffff; opacity:0; animation: step 6.3s ease-in-out infinite; }}
    @keyframes step {{ 0% {{ opacity:0 }} 8% {{ opacity:.9 }} 55% {{ opacity:.9 }} 75%,100% {{ opacity:0 }} }}
    .w1 {{ animation: drift 12s linear infinite; }}
    .w2 {{ animation: drift 8s linear infinite reverse; }}
    @keyframes drift {{ from {{ transform: translateX(0) }} to {{ transform: translateX(-240px) }} }}
  </style>
  <g clip-path="url(#f)">
    <g class="w1"><path d="{wave(40, 10, 240, FW, FH)}" fill="#0f3a8a"/></g>
    <g class="w2"><path d="{wave(56, 8, 240, FW, FH)}" fill="#1450b8"/></g>
    {''.join(paws)}
    <text x="{FW / 2}" y="132" text-anchor="middle" font-family="{FONT}" font-size="16" fill="#bfe0ff" letter-spacing="3">THANKS FOR VISITING  ·  NYAA</text>
  </g>
</svg>
"""

(OUT / "header.svg").write_text(header)
(OUT / "footer.svg").write_text(footer)
print("ok")
