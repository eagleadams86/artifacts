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

# The INSTALL icons, named by manifest.webmanifest AND by the whitelist in
# .gitignore — a new file here needs a line there too or it silently will not be
# committed. 192 and 512 are the two sizes Chrome asks for when it offers
# "Install app"; they are the same drawing as favicon.ico, ROUNDED, because
# nothing masks a `purpose: any` icon so the corners have to be in the file.
PWA_ICONS = [(192, 'icon-192.png'), (512, 'icon-512.png')]

# The maskable one is a DIFFERENT drawing, and this mark is the one in the family
# that genuinely needs it. A launcher crops to whatever outline it likes — a
# circle on many Android ones — so only the middle 80% survives: a disc of radius
# 25.6 in this 64 viewport. The card stack's far corner sits at 29.07 from the
# centre, outside it, where the lottery ball (21.1) and the golf flag (21.1) both
# fit as drawn. So here the foreground is scaled about the centre while the
# background stays full bleed. 0.85 brings 29.07 to 24.7, inside with a little to
# spare. Move the cards and re-check that number.
MASKABLE = (512, 'icon-512-maskable.png')
MASKABLE_SCALE = 0.85


def rect(d, box, r, fill, grow=0, k=1.0):
    x0, y0, x1, y1 = box
    d.rounded_rectangle([p(x0 - grow, k) * SCALE, p(y0 - grow, k) * SCALE,
                         p(x1 + grow, k) * SCALE, p(y1 + grow, k) * SCALE],
                        radius=(r + grow) * k * SCALE, fill=fill)


def p(v, k):
    """A coordinate, scaled about the tile's own centre. `k` is 1 everywhere but
    the maskable icon, where the foreground is pulled in to clear the crop."""
    return 32 + (v - 32) * k


def build(rounded=True, k=1.0):
    n = 64 * SCALE
    img = Image.new('RGBA', (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # The background is NOT scaled: it has to reach the edges whatever `k` is, or
    # the maskable icon would be a shrunken tile floating on nothing.
    d.rectangle([0, 0, n, n], fill=BG)
    # the soft disc bottom-left, the way the SVG has it
    d.ellipse([p(14 - 20, k) * SCALE, p(52 - 20, k) * SCALE,
               p(14 + 20, k) * SCALE, p(52 + 20, k) * SCALE], fill=GLOW)

    rect(d, CARD_BACK, CARD_R, BACK, k=k)
    rect(d, CARD_FRONT, CARD_R, BG, grow=GAP, k=k)     # the separating hairline
    rect(d, CARD_FRONT, CARD_R, FRONT, k=k)

    r = LINE_W / 2
    for (x0, y0), (x1, y1) in LINES:
        d.rounded_rectangle([p(x0 - r, k) * SCALE, p(y0 - r, k) * SCALE,
                             p(x1 + r, k) * SCALE, p(y1 + r, k) * SCALE],
                            radius=r * k * SCALE, fill=BG)

    if not rounded:
        # Full bleed, for the maskable icon — the launcher supplies the shape.
        return img.convert('RGB')
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

    for size, name in PWA_ICONS:
        art.resize((size, size), Image.LANCZOS).save(name, format='PNG',
                                                     optimize=True)
        print(f'{name} written (rounded — nothing masks a `purpose: any` icon)')

    size, name = MASKABLE
    build(rounded=False, k=MASKABLE_SCALE).resize(
        (size, size), Image.LANCZOS).save(name, format='PNG', optimize=True)
    print(f'{name} written (full bleed, cards at {MASKABLE_SCALE:.0%})')

    print('Now bump the ?v= on both favicon.ico references in claude.html — '
          'browsers cache an icon for a long time and will keep showing the old '
          'one otherwise. favicon.ico and claude.html are pushed BY HAND; the '
          'LaunchAgent only ever syncs data/data-*.js.')


if __name__ == '__main__':
    main()
