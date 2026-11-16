"""Generate assets/header.svg and assets/footer.svg for the GitHub profile README."""
import random
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
random.seed(7)

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


def stars(n, w, h, ymax):
    out = []
    for i in range(n):
        x = random.uniform(10, w - 10)
        y = random.uniform(8, ymax)
        r = random.choice([0.7, 0.9, 1.1, 1.4, 1.8])
        dur = random.uniform(2.2, 5.0)
        delay = random.uniform(0, 4)
        out.append(
            f'<circle class="star" cx="{x:.1f}" cy="{y:.1f}" r="{r}" '
            f'style="animation-duration:{dur:.2f}s;animation-delay:-{delay:.2f}s"/>'
        )
    return "\n    ".join(out)


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
header = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Kusanagi - a white cat watching the moon over a blue sea">
  <title>Hi, I'm Kusanagi</title>
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#030b1f"/>
      <stop offset=".55" stop-color="#0a2259"/>
      <stop offset="1" stop-color="#1450b8"/>
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
      <stop offset="0" stop-color="#cfe6ff" stop-opacity=".55"/>
      <stop offset=".45" stop-color="#7fb8ff" stop-opacity=".18"/>
      <stop offset="1" stop-color="#7fb8ff" stop-opacity="0"/>
    </radialGradient>
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
    <clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
  </defs>
  <style>
    .star {{ fill:#fff; animation: twinkle 3s ease-in-out infinite; }}
    @keyframes twinkle {{ 0%,100% {{ opacity:.15 }} 50% {{ opacity:1 }} }}
    .w1 {{ animation: drift 14s linear infinite; }}
    .w2 {{ animation: drift 9s linear infinite reverse; }}
    .w3 {{ animation: drift 6s linear infinite; }}
    @keyframes drift {{ from {{ transform: translateX(0) }} to {{ transform: translateX(-240px) }} }}
    .tail {{ transform-origin: 38px 128px; animation: swish 3.2s ease-in-out infinite; }}
    @keyframes swish {{ 0%,100% {{ transform: rotate(0deg) }} 50% {{ transform: rotate(-14deg) }} }}
    .eyes {{ transform-box: fill-box; transform-origin: center; animation: blink 5s infinite; }}
    @keyframes blink {{ 0%,92%,100% {{ transform: scaleY(1) }} 95% {{ transform: scaleY(.08) }} }}
    .head {{ transform-origin: 0px 50px; animation: tilt 7s ease-in-out infinite; }}
    @keyframes tilt {{ 0%,40%,100% {{ transform: rotate(0deg) }} 50%,85% {{ transform: rotate(-6deg) }} }}
    .meteor {{ animation: meteor 7s ease-in infinite; opacity:0; }}
    @keyframes meteor {{ 0% {{ transform: translate(0,0); opacity:0 }} 3% {{ opacity:1 }} 12% {{ transform: translate(-260px,130px); opacity:0 }} 100% {{ opacity:0 }} }}
    .moon {{ animation: pulse 6s ease-in-out infinite; transform-origin: 920px 86px; }}
    @keyframes pulse {{ 0%,100% {{ transform: scale(1) }} 50% {{ transform: scale(1.06) }} }}
    .fade {{ opacity:0; animation: up .9s ease-out forwards; }}
    .d1 {{ animation-delay:.2s }} .d2 {{ animation-delay:.6s }} .d3 {{ animation-delay:1s }}
    @keyframes up {{ from {{ opacity:0; transform: translateY(10px) }} to {{ opacity:1; transform: translateY(0) }} }}
    .caret {{ animation: caret 1s steps(1) infinite; }}
    @keyframes caret {{ 50% {{ opacity:0 }} }}
  </style>

  <g clip-path="url(#frame)">
    <rect width="{W}" height="{H}" fill="url(#sky)"/>

    <!-- stars -->
    {stars(90, W, H, 230)}

    <!-- shooting star -->
    <g class="meteor"><rect x="720" y="34" width="110" height="2" rx="1" fill="url(#shoot)" transform="rotate(-27 830 35)"/></g>

    <!-- moon -->
    <circle cx="920" cy="86" r="120" fill="url(#moonGlow)" class="moon"/>
    <circle cx="920" cy="86" r="46" fill="#eaf4ff" filter="url(#glow)"/>
    <circle cx="904" cy="74" r="8" fill="#cfe1fa"/>
    <circle cx="935" cy="98" r="11" fill="#cfe1fa"/>
    <circle cx="932" cy="68" r="4.5" fill="#cfe1fa"/>

    <!-- waves -->
    <g class="w1"><path d="{wave(268, 8, 240, W, H)}" fill="#0f3a8a" opacity=".85"/></g>
    <g class="w2"><path d="{wave(288, 10, 240, W, H)}" fill="#1557c9" opacity=".8"/></g>

    <!-- moonlight on water -->
    <g fill="#bfe0ff" opacity=".35">
      <rect x="890" y="294" width="60" height="2" rx="1"/>
      <rect x="872" y="304" width="96" height="2" rx="1"/>
      <rect x="898" y="314" width="44" height="2" rx="1"/>
    </g>

    <!-- rock the cat sits on -->
    <path d="M985,340 C990,318 1000,300 1018,296 C1040,290 1090,288 1118,294 C1140,300 1150,322 1156,340 Z" fill="#081a3d"/>
    <path d="M1018,296 C1040,290 1090,288 1118,294" fill="none" stroke="#2f6fd6" stroke-width="2" opacity=".6"/>

    {CAT}

    <g class="w3"><path d="{wave(318, 7, 240, W, H)}" fill="#2f81f7" opacity=".9"/></g>

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
