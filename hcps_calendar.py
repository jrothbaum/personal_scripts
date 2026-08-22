#!/usr/bin/env python3
"""Generate a single-month-at-a-time HTML calendar for the 2026-2027 school year (ES/MS)."""

import calendar
import json
from datetime import date

CLOSED = "closed"
EARLY = "early"
FIRST_DAY = "first_day"
STAFF_ONLY = "staff_only"

EVENTS = {
    date(2026, 8, 13): (STAFF_ONLY, "First day for staff"),
    date(2026, 8, 24): (FIRST_DAY, "First day for K-12 students"),
    date(2026, 8, 27): (FIRST_DAY, "First day for Pre-K/RECC students"),
    date(2026, 9,  7): (CLOSED,    "Labor Day"),
    date(2026, 9, 21): (CLOSED,    "Yom Kippur"),
    date(2026, 9, 30): (EARLY,     "Early dismissal – Staff Professional Day"),
    date(2026, 10, 16): (STAFF_ONLY, "No school for students – Staff Professional Day"),
    date(2026, 10, 28): (STAFF_ONLY, "No school for students – Staff Professional Day"),
    date(2026, 11,  3): (CLOSED,   "Election Day"),
    date(2026, 11, 23): (EARLY,    "Early dismissal – ES/MS Parent/Teacher Conferences"),
    date(2026, 11, 24): (EARLY,    "Early dismissal – ES/MS Parent/Teacher Conferences"),
    date(2026, 11, 25): (STAFF_ONLY, "No school for students – Parent/Teacher Conferences"),
    date(2026, 11, 26): (CLOSED,   "Thanksgiving Holiday"),
    date(2026, 11, 27): (CLOSED,   "Thanksgiving Holiday"),
    date(2026, 12,  9): (EARLY,    "Early dismissal – Staff Professional Day"),
    date(2026, 12, 24): (CLOSED,   "Winter Break"),
    date(2026, 12, 25): (CLOSED,   "Winter Break"),
    date(2026, 12, 28): (CLOSED,   "Winter Break"),
    date(2026, 12, 29): (CLOSED,   "Winter Break"),
    date(2026, 12, 30): (CLOSED,   "Winter Break"),
    date(2026, 12, 31): (CLOSED,   "Winter Break"),
    date(2027,  1,  1): (CLOSED,   "Winter Break"),
    date(2027,  1, 14): (EARLY,    "Early dismissal – ES P/T Conferences; MS Midterm Exams"),
    date(2027,  1, 15): (EARLY,    "Early dismissal – ES P/T Conferences; MS Midterm Exams"),
    date(2027,  1, 18): (CLOSED,   "Martin Luther King Jr. Day"),
    date(2027,  1, 19): (STAFF_ONLY, "No school for students – Staff Professional Day"),
    date(2027,  2,  3): (STAFF_ONLY, "No school for students – Staff Professional Day"),
    date(2027,  2, 11): (EARLY,    "Early dismissal – ES Parent/Teacher Conferences"),
    date(2027,  2, 12): (EARLY,    "Early dismissal – ES Parent/Teacher Conferences"),
    date(2027,  2, 15): (CLOSED,   "Presidents Day"),
    date(2027,  3,  9): (STAFF_ONLY, "No school for students – Eid al-Fitr; Staff Professional Day"),
    date(2027,  3, 22): (CLOSED,   "Spring Break"),
    date(2027,  3, 23): (CLOSED,   "Spring Break"),
    date(2027,  3, 24): (CLOSED,   "Spring Break"),
    date(2027,  3, 25): (CLOSED,   "Spring Break"),
    date(2027,  3, 26): (CLOSED,   "Spring Break"),
    date(2027,  3, 29): (CLOSED,   "Spring Break"),
    date(2027,  4,  8): (EARLY,    "Early dismissal – Staff Professional Day"),
    date(2027,  5, 17): (EARLY,    "Early dismissal – Staff Professional Day"),
    date(2027,  5, 31): (CLOSED,   "Memorial Day"),
    date(2027,  6,  2): (EARLY,    "Early dismissal – Staff Professional Day"),
    date(2027,  6,  7): (EARLY,    "Early dismissal – Staff Professional Day"),
    date(2027,  6,  8): (EARLY,    "Early dismissal – Last Day of School"),
    date(2027,  6,  9): (CLOSED,   "Possible inclement weather day"),
    date(2027,  6, 10): (CLOSED,   "Possible inclement weather day"),
    date(2027,  6, 11): (CLOSED,   "Possible inclement weather day"),
}

# Conservative budget (in) for the week-row grid on a printed landscape page,
# after the nav-header/title + day-of-week row. See build_month() and the
# @media print block for how it's used.
GRID_PRINT_BUDGET_IN = 6.4

RA_COLORS = {
    "RED":    "#fca5a5",
    "ORANGE": "#fdba74",
    "YELLOW": "#fde047",
    "GREEN":  "#86efac",
    "BLUE":   "#93c5fd",
}

COLOR_DAYS = {
    date(2026,  8, 24): "RED",
    date(2026,  8, 25): "ORANGE",
    date(2026,  8, 26): "YELLOW",
    date(2026,  8, 27): "GREEN",
    date(2026,  8, 28): "BLUE",
    date(2026,  8, 31): "RED",
    date(2026,  9,  1): "ORANGE",
    date(2026,  9,  2): "YELLOW",
    date(2026,  9,  3): "GREEN",
    date(2026,  9,  4): "BLUE",
    date(2026,  9,  8): "RED",
    date(2026,  9,  9): "ORANGE",
    date(2026,  9, 10): "YELLOW",
    date(2026,  9, 11): "GREEN",
    date(2026,  9, 14): "BLUE",
    date(2026,  9, 15): "RED",
    date(2026,  9, 16): "ORANGE",
    date(2026,  9, 17): "YELLOW",
    date(2026,  9, 18): "GREEN",
    date(2026,  9, 22): "BLUE",
    date(2026,  9, 23): "RED",
    date(2026,  9, 24): "ORANGE",
    date(2026,  9, 25): "YELLOW",
    date(2026,  9, 28): "GREEN",
    date(2026,  9, 29): "BLUE",
    date(2026,  9, 30): "RED",
    date(2026, 10,  1): "ORANGE",
    date(2026, 10,  2): "YELLOW",
    date(2026, 10,  5): "GREEN",
    date(2026, 10,  6): "BLUE",
    date(2026, 10,  7): "RED",
    date(2026, 10,  8): "ORANGE",
    date(2026, 10,  9): "YELLOW",
    date(2026, 10, 12): "GREEN",
    date(2026, 10, 13): "BLUE",
    date(2026, 10, 14): "RED",
    date(2026, 10, 15): "ORANGE",
    date(2026, 10, 19): "YELLOW",
    date(2026, 10, 20): "GREEN",
    date(2026, 10, 21): "BLUE",
    date(2026, 10, 22): "RED",
    date(2026, 10, 23): "ORANGE",
    date(2026, 10, 26): "YELLOW",
    date(2026, 10, 27): "GREEN",
    date(2026, 10, 29): "BLUE",
    date(2026, 10, 30): "RED",
    date(2026, 11,  2): "ORANGE",
    date(2026, 11,  4): "YELLOW",
    date(2026, 11,  5): "GREEN",
    date(2026, 11,  6): "BLUE",
    date(2026, 11,  9): "RED",
    date(2026, 11, 10): "ORANGE",
    date(2026, 11, 11): "YELLOW",
    date(2026, 11, 12): "GREEN",
    date(2026, 11, 13): "BLUE",
    date(2026, 11, 16): "RED",
    date(2026, 11, 17): "ORANGE",
    date(2026, 11, 18): "YELLOW",
    date(2026, 11, 19): "GREEN",
    date(2026, 11, 20): "BLUE",
    date(2026, 11, 23): "RED",
    date(2026, 11, 24): "ORANGE",
    date(2026, 11, 30): "YELLOW",
    date(2026, 12,  1): "GREEN",
    date(2026, 12,  2): "BLUE",
    date(2026, 12,  3): "RED",
    date(2026, 12,  4): "ORANGE",
    date(2026, 12,  7): "YELLOW",
    date(2026, 12,  8): "GREEN",
    date(2026, 12,  9): "BLUE",
    date(2026, 12, 10): "RED",
    date(2026, 12, 11): "ORANGE",
    date(2026, 12, 14): "YELLOW",
    date(2026, 12, 15): "GREEN",
    date(2026, 12, 16): "BLUE",
    date(2026, 12, 17): "RED",
    date(2026, 12, 18): "ORANGE",
    date(2026, 12, 21): "YELLOW",
    date(2026, 12, 22): "GREEN",
    date(2026, 12, 23): "BLUE",
    date(2027,  1,  4): "RED",
    date(2027,  1,  5): "ORANGE",
    date(2027,  1,  6): "YELLOW",
    date(2027,  1,  7): "GREEN",
    date(2027,  1,  8): "BLUE",
    date(2027,  1, 11): "RED",
    date(2027,  1, 12): "ORANGE",
    date(2027,  1, 13): "YELLOW",
    date(2027,  1, 14): "GREEN",
    date(2027,  1, 15): "BLUE",
    date(2027,  1, 20): "RED",
    date(2027,  1, 21): "ORANGE",
    date(2027,  1, 22): "YELLOW",
    date(2027,  1, 25): "GREEN",
    date(2027,  1, 26): "BLUE",
    date(2027,  1, 27): "RED",
    date(2027,  1, 28): "ORANGE",
    date(2027,  1, 29): "YELLOW",
    date(2027,  2,  1): "GREEN",
    date(2027,  2,  2): "BLUE",
    date(2027,  2,  4): "RED",
    date(2027,  2,  5): "ORANGE",
    date(2027,  2,  8): "YELLOW",
    date(2027,  2,  9): "GREEN",
    date(2027,  2, 10): "BLUE",
    date(2027,  2, 11): "RED",
    date(2027,  2, 12): "ORANGE",
    date(2027,  2, 16): "YELLOW",
    date(2027,  2, 17): "GREEN",
    date(2027,  2, 18): "BLUE",
    date(2027,  2, 19): "RED",
    date(2027,  2, 22): "ORANGE",
    date(2027,  2, 23): "YELLOW",
    date(2027,  2, 24): "GREEN",
    date(2027,  2, 25): "BLUE",
    date(2027,  2, 26): "RED",
    date(2027,  3,  1): "ORANGE",
    date(2027,  3,  2): "YELLOW",
    date(2027,  3,  3): "GREEN",
    date(2027,  3,  4): "BLUE",
    date(2027,  3,  5): "RED",
    date(2027,  3,  8): "ORANGE",
    date(2027,  3, 10): "YELLOW",
    date(2027,  3, 11): "GREEN",
    date(2027,  3, 12): "BLUE",
    date(2027,  3, 15): "RED",
    date(2027,  3, 16): "ORANGE",
    date(2027,  3, 17): "YELLOW",
    date(2027,  3, 18): "GREEN",
    date(2027,  3, 19): "BLUE",
    date(2027,  3, 30): "RED",
    date(2027,  3, 31): "ORANGE",
    date(2027,  4,  1): "YELLOW",
    date(2027,  4,  2): "GREEN",
    date(2027,  4,  5): "BLUE",
    date(2027,  4,  6): "RED",
    date(2027,  4,  7): "ORANGE",
    date(2027,  4,  8): "YELLOW",
    date(2027,  4,  9): "GREEN",
    date(2027,  4, 12): "BLUE",
    date(2027,  4, 13): "RED",
    date(2027,  4, 14): "ORANGE",
    date(2027,  4, 15): "YELLOW",
    date(2027,  4, 16): "GREEN",
    date(2027,  4, 19): "BLUE",
    date(2027,  4, 20): "RED",
    date(2027,  4, 21): "ORANGE",
    date(2027,  4, 22): "YELLOW",
    date(2027,  4, 23): "GREEN",
    date(2027,  4, 26): "BLUE",
    date(2027,  4, 27): "RED",
    date(2027,  4, 28): "ORANGE",
    date(2027,  4, 29): "YELLOW",
    date(2027,  4, 30): "GREEN",
    date(2027,  5,  3): "BLUE",
    date(2027,  5,  4): "RED",
    date(2027,  5,  5): "ORANGE",
    date(2027,  5,  6): "YELLOW",
    date(2027,  5,  7): "GREEN",
    date(2027,  5, 10): "BLUE",
    date(2027,  5, 11): "RED",
    date(2027,  5, 12): "ORANGE",
    date(2027,  5, 13): "YELLOW",
    date(2027,  5, 14): "GREEN",
    date(2027,  5, 17): "BLUE",
    date(2027,  5, 18): "RED",
    date(2027,  5, 19): "ORANGE",
    date(2027,  5, 20): "YELLOW",
    date(2027,  5, 21): "GREEN",
    date(2027,  5, 24): "BLUE",
    date(2027,  5, 25): "RED",
    date(2027,  5, 26): "ORANGE",
    date(2027,  5, 27): "YELLOW",
    date(2027,  5, 28): "GREEN",
    date(2027,  6,  1): "BLUE",
    date(2027,  6,  2): "RED",
    date(2027,  6,  3): "ORANGE",
    date(2027,  6,  4): "YELLOW",
    date(2027,  6,  7): "GREEN",
    date(2027,  6,  8): "BLUE",
    date(2027,  6,  9): "RED",
    date(2027,  6, 10): "ORANGE",
    date(2027,  6, 11): "YELLOW",
    date(2027,  6, 14): "GREEN",
    date(2027,  6, 15): "BLUE",
}

MONTH_NAMES = [
    "", "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]

DAY_NAMES = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #eef2f7;
    color: #333;
    padding: 2rem 1.5rem;
    min-height: 100vh;
}

h1 {
    text-align: center;
    font-size: 1.9rem;
    font-weight: 700;
    color: #1a1a2e;
    margin-bottom: 1.25rem;
    letter-spacing: -0.01em;
}

.toolbar {
    display: flex;
    justify-content: center;
    margin-bottom: 0.75rem;
}
.toggle-btn {
    background: #fff;
    border: 1px solid #ccc;
    color: #555;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 0.35rem 0.9rem;
    border-radius: 999px;
    cursor: pointer;
}
.toggle-btn:hover { background: #f4f6fa; }

/* Legend */
.legend {
    display: flex;
    flex-wrap: wrap;
    gap: 0.6rem 1.2rem;
    justify-content: center;
    margin-bottom: 1.75rem;
}
.legend-item {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    font-size: 0.82rem;
    color: #555;
}
.legend-swatch {
    width: 14px;
    height: 14px;
    border-radius: 4px;
    flex-shrink: 0;
}
.legend-group-label {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #999;
    align-self: center;
    margin-right: -0.4rem;
}
.extra-info.hidden { display: none; }

/* Outer wrapper — single column, centered */
.calendar-wrapper {
    max-width: 740px;
    margin: 0 auto;
}

/* Navigation header */
.nav-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #fff;
    color: #1a1a2e;
    border: 1px solid #e0e3eb;
    border-bottom: none;
    border-radius: 14px 14px 0 0;
    padding: 0.85rem 1.25rem;
}
.nav-title {
    font-size: 1.3rem;
    font-weight: 700;
    letter-spacing: 0.03em;
}
.nav-btn {
    background: none;
    border: 1px solid #ccc;
    color: #1a1a2e;
    font-size: 1.35rem;
    font-weight: bold;
    cursor: pointer;
    width: 2.4rem;
    height: 2.4rem;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background 0.15s;
    line-height: 1;
    flex-shrink: 0;
}
.nav-btn:hover:not(:disabled) { background: #f0f2f6; }
.nav-btn:disabled { opacity: 0.25; cursor: default; }

/* Month card */
.month-card {
    background: #fff;
    border: 1px solid #e0e3eb;
    border-radius: 0 0 14px 14px;
    overflow: hidden;
}
.month-print-title { display: none; }

/* Day-of-week header row */
.dow-row {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    background: #f4f6fa;
    border-bottom: 1px solid #e8eaf0;
}
.dow-cell {
    text-align: center;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    padding: 0.55rem 0;
    color: #888;
    text-transform: uppercase;
}
.dow-cell.weekend { color: #bbb; }

/* Calendar grid */
.cal-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
}

.day-cell {
    min-height: 90px;
    padding: 8px 9px 6px;
    border: 1px solid #f0f2f6;
    position: relative;
}
.day-cell.empty { background: #f9fafb; }
.day-cell.weekend { background: #f7f8fb; }

.color-bar {
    position: relative;
    margin: -8px -9px 5px;
    padding: 0 6px;
    height: 18px;
    color: #000;
}
.bar-label {
    display: block;
    height: 18px;
    line-height: 18px;
    text-align: center;
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.05em;
}
.bar-daynum {
    position: absolute;
    right: 6px;
    top: 0;
    height: 18px;
    line-height: 18px;
    font-size: 0.68rem;
    font-weight: 700;
}

.event-label {
    font-size: 0.68rem;
    line-height: 1.35;
    margin-top: 4px;
    color: inherit;
    opacity: 0.85;
}

/* CSS tooltip */
.day-cell[data-tip] { cursor: help; }
.day-cell[data-tip]:hover::after {
    content: attr(data-tip);
    position: absolute;
    bottom: calc(100% + 5px);
    left: 50%;
    transform: translateX(-50%);
    background: #1a1a2e;
    color: #fff;
    padding: 5px 10px;
    border-radius: 6px;
    font-size: 0.74rem;
    white-space: nowrap;
    z-index: 20;
    pointer-events: none;
    box-shadow: 0 2px 8px rgba(0,0,0,0.25);
}

/* Print — one month filling a full landscape page */
/*
   Print sizing uses fixed physical units (in), not vh/flex-fill — vh resolves
   inconsistently across browsers' print engines and can silently overflow to
   a second page. These numbers are budgeted to fit inside the smallest common
   landscape page (A4: 8.27in tall, 0.3in margins => 7.67in usable) with room
   to spare, rather than exactly filling whatever page the browser reports.
*/
@media print {
    @page { size: landscape; margin: 0.3in; }

    * {
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
        color-adjust: exact !important;
    }

    body { background: #fff; padding: 0; }
    .extra-info { display: none; }
    .toolbar { display: none; }
    .nav-btn { display: none; }
    .nav-header { justify-content: center; padding: 0.12in 0.2in; }

    .dow-cell.weekend, .day-cell.weekend { display: none; }
    .dow-row, .cal-grid { grid-template-columns: repeat(5, 1fr); }

    .calendar-wrapper { max-width: none; }
    .month-card { page-break-inside: avoid; break-inside: avoid; }

    /*
       Row height is a literal value baked in per month at generation time
       (see --row-h on .cal-grid), not a flexible unit (fr / flex:1). CSS
       Grid's fr-track sizing during print pagination has shown real
       differences between Chrome's own print-preview/print pipeline and
       its --print-to-pdf CLI path, and reportedly across browsers too — a
       plain absolute length sidesteps that entirely and is deterministic
       everywhere.
    */
    .cal-grid { grid-auto-rows: var(--row-h); }
    .day-cell { min-height: 0; overflow: hidden; }
    .event-label { font-size: 0.62rem; line-height: 1.25; }

    /* Print-all-months mode: one month per page, each with its own heading */
    body.print-all .nav-header { display: none; }
    body.print-all .month-print-title {
        display: block;
        text-align: center;
        font-size: 1.1rem;
        font-weight: 700;
        color: #1a1a2e;
        margin-bottom: 0.08in;
    }
    body.print-all .month-card:not(:last-child) {
        page-break-after: always;
        break-after: page;
    }
}
"""

SWATCH_COLORS = {
    FIRST_DAY:  "#86efac",
    CLOSED:     "#fca5a5",
    EARLY:      "#fde047",
    STAFF_ONLY: "#fca5a5",
}

LEGEND_LABELS = [
    (FIRST_DAY,  "First Day of School"),
    (CLOSED,     "No School for Students"),
    (EARLY,      "Early Dismissal (3 hrs)"),
]


def short_label(description: str) -> str:
    text = description
    if "–" in text:
        text = text.split("–", 1)[1].strip()
    if len(text) > 26:
        text = text[:25] + "…"
    return text


def build_month(year: int, month: int, index: int) -> str:
    cal = calendar.Calendar(firstweekday=6)  # weeks start on Sunday
    weeks = cal.monthdatescalendar(year, month)

    dow_cells = "".join(
        f'<div class="dow-cell{" weekend" if i in (0, 6) else ""}">{DAY_NAMES[i]}</div>'
        for i in range(7)
    )

    day_cells = []
    effective_weeks = 0
    for week in weeks:
        # A week with no in-month weekday collapses to nothing once weekends
        # are hidden for print — its whole row must vanish, not just its
        # Sat/Sun cell, or it leaves a blank row and throws off row heights.
        week_has_weekday = any(
            d.month == month and d.weekday() not in (5, 6) for d in week
        )
        if week_has_weekday:
            effective_weeks += 1

        for d in week:
            if d.month != month:
                hide_weekend = not week_has_weekday or d.weekday() in (5, 6)
                empty_weekend = " weekend" if hide_weekend else ""
                day_cells.append(f'<div class="day-cell empty{empty_weekend}"></div>')
                continue

            is_weekend = not week_has_weekday or d.weekday() in (5, 6)  # Sat, Sun
            event = EVENTS.get(d)

            classes = ["day-cell"]
            if is_weekend:
                classes.append("weekend")

            tip_attr = ""
            label_html = ""
            if event:
                etype, desc = event
                classes.append(etype)
                tip_attr = f' data-tip="{desc}"'
                if etype == EARLY:
                    display = "Early Dismissal"
                elif etype in (CLOSED, STAFF_ONLY):
                    display = "No School: " + short_label(desc)
                else:
                    display = short_label(desc)
                label_html = f'<div class="event-label">{display}</div>'

            color_name = COLOR_DAYS.get(d)
            bg_style = f' style="background:{RA_COLORS[color_name]}"' if color_name else ""
            bar_html = (
                f'<div class="color-bar"{bg_style}>'
                f'<span class="bar-label">{color_name or ""}</span>'
                f'<span class="bar-daynum">{d.day}</span>'
                f'</div>'
            )

            day_cells.append(
                f'<div class="{" ".join(classes)}"{tip_attr}>'
                f'{bar_html}'
                f'{label_html}'
                f'</div>'
            )

    grid = "\n    ".join(day_cells)
    hidden = " hidden" if index > 0 else ""
    month_label = f"{MONTH_NAMES[month]} {year}"
    # Conservative print budget (in) for the week-row grid alone, after the
    # nav-header/title + day-of-week row — see the @media print note. Divided
    # by the actual week count so 5- and 6-week months both fill it exactly.
    row_h_in = GRID_PRINT_BUDGET_IN / effective_weeks
    return (
        f'<div class="month-card" id="month-{index}"{hidden}>'
        f'<div class="month-print-title">{month_label}</div>'
        f'<div class="dow-row">{dow_cells}</div>'
        f'<div class="cal-grid" style="--row-h:{row_h_in:.3f}in">\n    {grid}\n  </div>'
        f'</div>'
    )


def main():
    school_months = [
        (2026, 8), (2026, 9), (2026, 10), (2026, 11), (2026, 12),
        (2027, 1), (2027, 2), (2027, 3), (2027, 4), (2027, 5), (2027, 6),
    ]

    month_labels = [f"{MONTH_NAMES[m]} {y}" for y, m in school_months]
    months_html = "\n".join(build_month(y, m, i) for i, (y, m) in enumerate(school_months))

    legend_items = [
        f'<div class="legend-item">'
        f'<div class="legend-swatch" style="background:{SWATCH_COLORS[t]}"></div>'
        f'{label}</div>'
        for t, label in LEGEND_LABELS
    ]
    legend_items.append('<div class="legend-group-label">RA Color Day</div>')
    legend_items.extend(
        f'<div class="legend-item">'
        f'<div class="legend-swatch" style="background:{hexval}"></div>'
        f'{name.title()}</div>'
        for name, hexval in RA_COLORS.items()
    )
    legend_html = "\n    ".join(legend_items)

    js = f"""
const MONTHS = {json.dumps(month_labels)};
let current = 0;

const prevBtn = document.getElementById('btn-prev');
const nextBtn = document.getElementById('btn-next');
const navTitle = document.getElementById('nav-title');

const printAllBtn = document.getElementById('print-all-btn');
let showingAll = false;

function exitShowAll() {{
    showingAll = false;
    document.body.classList.remove('print-all');
    printAllBtn.textContent = 'Show all months for printing';
}}

function showMonth(idx) {{
    if (showingAll) {{
        exitShowAll();
        for (let i = 0; i < MONTHS.length; i++) {{
            document.getElementById('month-' + i).hidden = true;
        }}
    }} else {{
        document.getElementById('month-' + current).hidden = true;
    }}
    current = idx;
    document.getElementById('month-' + current).hidden = false;
    navTitle.textContent = MONTHS[current];
    prevBtn.disabled = current === 0;
    nextBtn.disabled = current === MONTHS.length - 1;
}}

prevBtn.addEventListener('click', () => showMonth(current - 1));
nextBtn.addEventListener('click', () => showMonth(current + 1));
prevBtn.disabled = true;

const extraInfo = document.getElementById('extra-info');
const extraToggle = document.getElementById('extra-toggle');
extraToggle.addEventListener('click', () => {{
    const nowHidden = extraInfo.classList.toggle('hidden');
    extraToggle.textContent = nowHidden ? 'Show extra' : 'Hide extra';
}});

printAllBtn.addEventListener('click', () => {{
    showingAll = !showingAll;
    if (showingAll) {{
        for (let i = 0; i < MONTHS.length; i++) {{
            document.getElementById('month-' + i).hidden = false;
        }}
        document.body.classList.add('print-all');
        printAllBtn.textContent = 'Back to one month';
    }} else {{
        exitShowAll();
        for (let i = 0; i < MONTHS.length; i++) {{
            document.getElementById('month-' + i).hidden = (i !== current);
        }}
    }}
}});

window.addEventListener('afterprint', () => {{
    if (showingAll) {{
        exitShowAll();
        for (let i = 0; i < MONTHS.length; i++) {{
            document.getElementById('month-' + i).hidden = (i !== current);
        }}
    }}
}});
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>2026–2027 School Year Calendar (ES/MS)</title>
  <style>
{CSS}
  </style>
</head>
<body>
  <div class="toolbar">
    <button class="toggle-btn" id="extra-toggle">Hide extra</button>
    <button class="toggle-btn" id="print-all-btn">Show all months for printing</button>
  </div>
  <div class="extra-info" id="extra-info">
    <h1>2026–2027 School Year Calendar</h1>
    <div class="legend">
      {legend_html}
    </div>
  </div>
  <div class="calendar-wrapper">
    <div class="nav-header">
      <button class="nav-btn" id="btn-prev">&#8249;</button>
      <span id="nav-title">{month_labels[0]}</span>
      <button class="nav-btn" id="btn-next">&#8250;</button>
    </div>
    {months_html}
  </div>
  <script>{js}</script>
</body>
</html>
"""

    out = "hcps_calendar_2026_2027.html"
    with open(out, "w") as f:
        f.write(html)
    print(f"Written to {out}")


if __name__ == "__main__":
    main()
