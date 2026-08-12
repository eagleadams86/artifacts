#!/usr/bin/env python3
"""Draw favicon.ico — the same mark as the inline SVG icon in claude.html.

The page's icon is an inline SVG data URI, which every current browser prefers.
favicon.ico is the fallback: it's what a browser fetches from the site root on
its own, what older ones use, and what a bookmark or a search result shows. The
two have to be the same picture, so this draws the SVG's geometry with Pillow
rather than hand-editing a binary nobody can review in a diff.

    python3 make_favicon.py

The mark is what the page is: a stack of task cards, the front one carrying two
lines of its content. It sits on the tile the rest of the app family wears —
the midnight page as a rounded square, the soft disc in the bottom-left corner.

The two cards are FLAT fills rather than a gradient, and which one gets which
tone is the whole point: the front card is the lighter accent and the one
behind it the darker, so the stack reads as depth. Drawing them off the
family's diagonal gradient put the lighter tone on the card BEHIND, because
that one sits higher up the axis — correct by the formula and backwards to the
eye. A hairline of the page colour is drawn behind the front card for the same
reason: two indigo rectangles overlapping with no gap between them read as one
odd polygon.

**This file is one of the named public files in .gitignore's whitelist.** That
list is deliberately short — everything else in this folder (task SKILL.md
files, sync machinery, logs) is local-only and must never reach the public
repo. If you add a file here, adding it to the whitelist is a decision, not a
formality.

Everything is drawn at 8x and reduced with Lanczos, which is what gives the
16px version clean edges. Keep the shapes here in step with the SVG in
claude.html if that ever changes.
"""

from PIL import Image, ImageDraw

# The mark, in the SVG's own 64x64 coordinates.
BG = (10, 14, 26, 255)          # #0a0e1a — midnight, the default theme's page
GLOW = (20, 28, 51, 255)        # #141c33 — the darker disc in the corner
BACK = (129, 140, 248, 255)     # #818cf8 — midnight's accent, the card behind
FRONT = (165, 180, 252, 255)    # #a5b4fc — the lighter tone, the card in front

CARD_BACK = (13, 10, 43, 36)    # x0, y0, x1, y1
CARD_FRONT = (19, 26, 49, 52)
CARD_R = 6
GAP = 2.5                       # the page-coloured hairline around the front card
# The card's content. Two lines, not one — a single line centred on a card
# reads as a minus sign. The spacing and weight are set for the 16px frame,
# where anything tighter closes into a single grey band.
LINES = [((25, 34), (43, 34)), ((25, 44), (37, 44))]
LINE_W = 4

SCALE = 8                       # supersample, then reduce
SIZES = [16, 32, 48, 64, 128, 256]


def rect(d, box, r, fill, grow=0):
    x0, y0, x1, y1 = box
    d.rounded_rectangle([(x0 - grow) * SCALE, (y0 - grow) * SCALE,
                         (x1 + grow) * SCALE, (y1 + grow) * SCALE],
                        radius=(r + grow) * SCALE, fill=fill)


def build():
    n = 64 * SCALE
    img = Image.new('RGBA', (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, n, n], fill=BG)
    # the soft disc bottom-left, the way the SVG has it
    d.ellipse([(14 - 20) * SCALE, (52 - 20) * SCALE,
               (14 + 20) * SCALE, (52 + 20) * SCALE], fill=GLOW)

    rect(d, CARD_BACK, CARD_R, BACK)
    rect(d, CARD_FRONT, CARD_R, BG, grow=GAP)     # the separating hairline
    rect(d, CARD_FRONT, CARD_R, FRONT)

    r = LINE_W / 2
    for (x0, y0), (x1, y1) in LINES:
        d.rounded_rectangle([(x0 - r) * SCALE, (y0 - r) * SCALE,
                             (x1 + r) * SCALE, (y1 + r) * SCALE],
                            radius=r * SCALE, fill=BG)

    # Round the corners with an alpha mask. The SVG leaves the disc square at
    # the edges; an icon reads better rounded, and this is the file that ends
    # up on a bookmarks bar.
    mask = Image.new('L', (n, n), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, n - 1, n - 1],
                                           radius=14 * SCALE, fill=255)
    img.putalpha(mask)
    return img


def main():
    art = build()
    frames = [art.resize((s, s), Image.LANCZOS) for s in SIZES]
    frames[-1].save('favicon.ico', format='ICO',
                    sizes=[(s, s) for s in SIZES])
    print('favicon.ico written at ' + ', '.join(f'{s}px' for s in SIZES))
    print('Now bump the ?v= on both favicon.ico references in claude.html — '
          'browsers cache an icon for a long time and will keep showing the old '
          'one otherwise. favicon.ico and claude.html are pushed BY HAND; the '
          'LaunchAgent only ever syncs data/data-*.js.')


if __name__ == '__main__':
    main()
