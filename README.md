# The World in One Day — Wednesday 18 November 2026

A single 1024×1024 infographic poster covering six stories from
18 November 2026, drawn entirely with Pillow vector shapes (no photos,
no downloaded assets). Deterministic: the same code always renders the
same PNG.

## The six stories

1. **Nvidia's record quarter, without Huang** — Q3 revenue more than
   doubled to $115.8bn, net income $65.3bn, $130bn guided for Q4. Ex-CEO
   Jensen Huang said he would return if asked; the board says it will
   not reinstate him. Interim chief: CFO Colette Kress.
   Sources: Reuters / AFP via Arab News, NDTV Profit, Times of India.
2. **America loses its measles-free label** — PAHO withdrew the US
   measles-elimination status held since 2000 after 12+ months of
   uninterrupted transmission; 5,412 cases confirmed in 2026, the worst
   in over 30 years. Mexico and Bolivia lost it too.
   Sources: Al Jazeera, USA Today, The Straits Times.
3. **19 dead as army plane crashes in Siberia** — An An-12 military
   transport went down near Kemerovo (Yagunovo), killing all 19 aboard;
   the defence ministry blames a suspected technical fault.
   Sources: Al Jazeera, Reuters, CNN.
4. **Eisenkot ally takes the Knesset chair** — Matan Kahana (Yashar)
   beat Likud's Ofir Katz 66–52 to become speaker, replacing Amir
   Ohana, handing Eisenkot's bloc control of the parliamentary agenda.
   Sources: Haaretz, The Jerusalem Post, Al Jazeera.
5. **Spy-suspect officer now in US hands** — Lt Col Brandon Tyner, 41,
   arrested near Gloucester on 10 November on suspicion of spying for
   Russia, was transferred from British police to US military custody.
   Sources: The Jerusalem Post, BBC via The British Eye, FBI.
6. **27½ years for Trump murder plot** — Asif Merchant, 48, was
   sentenced in Brooklyn to 330 months for an Iran-linked
   murder-for-hire plot aimed at Donald Trump; prosecutors sought life.
   Sources: US Department of Justice, AP, New York Post.

## How to run

```bash
python3 main.py            # renders entry.png fresh, then copies it to
                           # $MAKEFUN_OUTPUT_DIR/entry.png
                           # (default /output/entry.png)
```

Requires Pillow (`pip install pillow`). No network access at render time.

## Verification

Render twice into different directories and compare hashes — they must
match, proving the poster is deterministic:

```bash
MAKEFUN_OUTPUT_DIR=/tmp/out-a python3 main.py
MAKEFUN_OUTPUT_DIR=/tmp/out-b python3 main.py
sha256sum /tmp/out-a/entry.png /tmp/out-b/entry.png   # identical hashes
```

Expected output: a valid PNG, 1024×1024, well under 1 MiB
(≈ 132 KB).

## Layout

Dark navy masthead with the date, then a 2×3 grid of story cards. Each
card pairs a small vector illustration (chip, virus, crashing plane,
parliament building, dossier, courthouse) with a kicker, a headline and
a short summary, plus a source line at the foot of the page.
