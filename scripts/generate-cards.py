"""Generate assets/streak.svg and assets/activity.svg from the GitHub contribution calendar.

Replaces the hosted streak-stats and activity-graph services. Run with a token for the
profile owner so private contributions are counted:

    GITHUB_TOKEN=... python3 scripts/generate-cards.py [OUT_DIR]   (OUT_DIR defaults to assets/)

PROFILE_USER defaults to the token's own account.
"""
import json
import os
import sys
import urllib.request
from datetime import date, datetime, timedelta, timezone
from html import escape
from pathlib import Path

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(parents=True, exist_ok=True)

TOKEN = os.environ.get("GITHUB_TOKEN")
if not TOKEN:
    sys.exit("GITHUB_TOKEN is required")

FONT = "'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif"
ACTIVITY_DAYS = 31

# Palette shared with the stats cards in the README.
BG = "#0a2259"
STROKE = "#1f6feb"
RING = "#58a6ff"
FIRE = "#79c0ff"
LABEL = "#dbe9ff"
NUM = "#ffffff"
DATES = "#a5c8ff"


def graphql(query, **variables):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as res:
        body = json.load(res)
    if body.get("errors"):
        sys.exit(f"GraphQL error: {body['errors']}")
    return body["data"]


def fetch_calendar(username):
    """Every day from account creation until today, as {date: count}."""
    if username:
        created = graphql("query($login: String!) { user(login: $login) { createdAt } }", login=username)["user"]["createdAt"]
    else:
        viewer = graphql("{ viewer { login createdAt } }")["viewer"]
        username, created = viewer["login"], viewer["createdAt"]
    now = datetime.now(timezone.utc)
    start = datetime.fromisoformat(created.replace("Z", "+00:00"))
    days = {}
    for year in range(start.year, now.year + 1):
        frm = max(start, datetime(year, 1, 1, tzinfo=timezone.utc))
        to = min(now, datetime(year, 12, 31, 23, 59, 59, tzinfo=timezone.utc))
        data = graphql(
            """query($login: String!, $from: DateTime!, $to: DateTime!) {
                 user(login: $login) { contributionsCollection(from: $from, to: $to) {
                   contributionCalendar { weeks { contributionDays { date contributionCount } } } } } }""",
            login=username, **{"from": frm.isoformat(), "to": to.isoformat()},
        )
        for week in data["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]:
            for day in week["contributionDays"]:
                days[date.fromisoformat(day["date"])] = day["contributionCount"]
    return username, dict(sorted(days.items()))


def streaks(days):
    """Total, current streak and longest streak, each as (count, first day, last day)."""
    dates = list(days)
    total = (sum(days.values()), dates[0], dates[-1])

    longest = (0, dates[0], dates[0])
    run_start, run = None, 0
    for d in dates:
        if days[d]:
            run_start = run_start or d
            run += 1
            if run > longest[0]:
                longest = (run, run_start, d)
        else:
            run_start, run = None, 0

    # Today doesn't break the streak until it's over.
    end = dates[-1] if days[dates[-1]] else dates[-1] - timedelta(days=1)
    d = end
    while days.get(d):
        d -= timedelta(days=1)
    current = ((end - d).days, d + timedelta(days=1), end)
    return total, current, longest


def fmt_date(d, with_year):
    return f"{d:%b} {d.day}, {d.year}" if with_year else f"{d:%b} {d.day}"


def fmt_range(start, end, today):
    if start == end:
        return fmt_date(start, start.year != today.year)
    with_year = start.year != end.year or end.year != today.year
    right = "Present" if end == today else fmt_date(end, with_year)
    return f"{fmt_date(start, with_year)} - {right}"


def streak_svg(total, current, longest, today):
    w, h = 495, 195
    cols = (w / 6, w / 2, w * 5 / 6)
    cur_range = fmt_range(current[1], current[2], today) if current[0] else "No current streak"
    long_range = fmt_range(longest[1], longest[2], today) if longest[0] else "No streak yet"
    desc = (f"Total contributions: {total[0]:,}. Current streak: {current[0]:,} days. "
            f"Longest streak: {longest[0]:,} days.")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="streakTitle streakDesc">
  <title id="streakTitle">GitHub streak</title>
  <desc id="streakDesc">{desc}</desc>
  <rect width="{w}" height="{h}" rx="4.5" fill="{BG}"/>
  <g stroke="{STROKE}" stroke-width="1">
    <line x1="{w / 3:.1f}" y1="28" x2="{w / 3:.1f}" y2="170"/>
    <line x1="{w * 2 / 3:.1f}" y1="28" x2="{w * 2 / 3:.1f}" y2="170"/>
  </g>
  <g font-family="{FONT}" text-anchor="middle">
    <text x="{cols[0]:.1f}" y="79" font-size="28" font-weight="700" fill="{NUM}">{total[0]:,}</text>
    <text x="{cols[0]:.1f}" y="115" font-size="14" fill="{LABEL}">Total Contributions</text>
    <text x="{cols[0]:.1f}" y="141" font-size="12" fill="{DATES}">{escape(fmt_range(total[1], total[2], today))}</text>

    <circle cx="{cols[1]:.1f}" cy="71" r="40" fill="none" stroke="{RING}" stroke-width="5"/>
    <rect x="{cols[1] - 15:.1f}" y="19" width="30" height="24" fill="{BG}"/>
    <path transform="translate({cols[1] - 6.5:.1f} 19.5) scale(.55)" fill="{FIRE}"
          d="M12 0C12 0 14 6 14 10C14 12 13 14 11 14C9 14 8 12.5 8 11C8 8 9 5 9 5C9 5 4 10 4 15C4 20 7.6 24 12 24C16.4 24 20 20 20 15C20 7.5 12 0 12 0Z"/>
    <text x="{cols[1]:.1f}" y="81" font-size="28" font-weight="700" fill="{NUM}">{current[0]:,}</text>
    <text x="{cols[1]:.1f}" y="140" font-size="14" font-weight="700" fill="{FIRE}">Current Streak</text>
    <text x="{cols[1]:.1f}" y="166" font-size="12" fill="{DATES}">{escape(cur_range)}</text>

    <text x="{cols[2]:.1f}" y="79" font-size="28" font-weight="700" fill="{NUM}">{longest[0]:,}</text>
    <text x="{cols[2]:.1f}" y="115" font-size="14" fill="{LABEL}">Longest Streak</text>
    <text x="{cols[2]:.1f}" y="141" font-size="12" fill="{DATES}">{escape(long_range)}</text>
  </g>
</svg>
"""


def nice_max(v):
    """Top of the y-axis: four gridline steps of 1/2/5 x 10^n that cover v."""
    step, mags = 1, (1, 2, 5)
    i = 0
    while 4 * step < v:
        i += 1
        step = mags[i % 3] * 10 ** (i // 3)
    return 4 * step


def activity_svg(days):
    recent = list(days.items())[-ACTIVITY_DAYS:]
    w, h = 1200, 360
    left, right, top, bottom = 70, 30, 70, 50
    pw, ph = w - left - right, h - top - bottom
    ymax = nice_max(max(c for _, c in recent))

    def px(i):
        return left + pw * i / (len(recent) - 1)

    def py(c):
        return top + ph * (1 - c / ymax)

    pts = [(px(i), py(c)) for i, (_, c) in enumerate(recent)]
    line = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    area = f"M{pts[0][0]:.1f},{top + ph} L" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f" L{pts[-1][0]:.1f},{top + ph} Z"

    grid, ylabels = [], []
    for k in range(5):
        v = ymax * k / 4
        y = py(v)
        grid.append(f'<line x1="{left}" y1="{y:.1f}" x2="{w - right}" y2="{y:.1f}"/>')
        ylabels.append(f'<text x="{left - 12}" y="{y + 4:.1f}" text-anchor="end">{v:g}</text>')
    xlabels = "".join(
        f'<text x="{px(i):.1f}" y="{h - bottom + 24}" text-anchor="middle">{d.day}</text>' for i, (d, _) in enumerate(recent)
    )
    points = "".join(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4"><title>{d:%b} {d.day}: {c} contributions</title></circle>'
        for (x, y), (d, c) in zip(pts, recent)
    )
    first, last = recent[0][0], recent[-1][0]
    desc = f"Daily contributions from {first:%b} {first.day} to {last:%b} {last.day}: " + ", ".join(str(c) for _, c in recent)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="actTitle actDesc">
  <title id="actTitle">Contribution Graph</title>
  <desc id="actDesc">{desc}</desc>
  <defs>
    <linearGradient id="actArea" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{STROKE}" stop-opacity=".6"/>
      <stop offset="1" stop-color="{STROKE}" stop-opacity=".05"/>
    </linearGradient>
  </defs>
  <rect width="{w}" height="{h}" rx="6" fill="{BG}"/>
  <g font-family="{FONT}">
    <text x="{w / 2}" y="40" text-anchor="middle" font-size="22" font-weight="600" fill="{FIRE}">Contribution Graph</text>
    <g stroke="{DATES}" stroke-opacity=".15">{"".join(grid)}</g>
    <g font-size="13" fill="{DATES}">{"".join(ylabels)}{xlabels}</g>
    <text transform="translate(22 {top + ph / 2}) rotate(-90)" text-anchor="middle" font-size="13" fill="{DATES}">Contributions</text>
  </g>
  <path d="{area}" fill="url(#actArea)"/>
  <polyline points="{line}" fill="none" stroke="{RING}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>
  <g fill="{NUM}">{points}</g>
</svg>
"""


username, days = fetch_calendar(os.environ.get("PROFILE_USER"))
today = list(days)[-1]
total, current, longest = streaks(days)
(OUT / "streak.svg").write_text(streak_svg(total, current, longest, today))
(OUT / "activity.svg").write_text(activity_svg(days))
print(f"{username}: total={total[0]} current={current[0]} longest={longest[0]}")
