# Claude Scheduled Task Dashboard

A personal dashboard that displays the live outputs of scheduled Claude tasks.

## Dashboard

**[View claude.html](https://eagleadams86.github.io/artifacts/claude.html)**

Cards are sorted by most recently updated and collapse by default — click a card header to expand it (and collapse any other). Refresh the page to see the latest outputs. Each card header shows when the task is due (🕐 line, left) next to when it actually last ran (right), so a task that has missed its slot is visible at a glance.

The page wears the app family's header: a sticky bar with the mark, the name and its strapline on the left, and the controls on the right. A theme picker switches between the four unified themes shared by all my apps, listed alphabetically — ☾ Dark, ☀ Light, ✦ Midnight (the default) and 📜 Sepia. (Dracula, Nord, Sakura, Synthwave and Terminal were retired in August 2026; a saved choice of one of them falls back to Midnight.) A text size picker next to it offers Small / Normal / Large / XL / XXL, and a ↻ Refresh button reloads the cards. Both picker choices are saved in the browser and persist across visits.

Every option in the theme picker is written into the markup at its final size, and **Midnight carries `selected`** — the header paints long before the script at the foot of the page runs, so without it the row reads "Dark" over a midnight page for a moment on every load. The sun is `☀`, the plain text character, not the emoji-presentation `☀️`: the colour-font variant is a different weight and baseline from the `☾` and `✦` beside it. Every sibling app follows both rules.

### Installing It

`manifest.webmanifest` is what turns Chrome's "Install page as app…" into a real install: its own window with no browser chrome, its own icon in the Dock or on the taskbar, opening straight on `claude.html`. Three things have to stay in step or it silently stops being offered, with nothing but a console line to say so:

- **`manifest-src 'self'` in the CSP.** It falls back to `default-src`, which is `'none'` here, so without the directive the manifest fetch is refused. Suspect this first.
- **`make_favicon.py` writes the install icons** — `icon-192.png`, `icon-512.png` and `icon-512-maskable.png` — from the same drawing as `favicon.ico` and the inline SVG.
- **Each of those four files needs its own line in the whitelist `.gitignore`.** An unnamed file here is silently never committed.

**Unlike the sibling apps this does NOT bring offline with it.** Those have a service worker; this page has none and should not — what it displays is task output rewritten hourly, and a cached copy of that presented as current is a wrong answer rather than an old page. Installed, it still needs the network, and that is the right trade for what it shows.

The icon is a stack of task cards — what the page is — on the midnight tile the whole app family wears; the heading shows the same mark, sized in `em` so it follows the text-size picker. `make_favicon.py` (Pillow) keeps `favicon.ico` and the page's inline SVG the same picture, rather than leaving a binary nobody can review in a diff. Re-run it with `python3 make_favicon.py`, then bump the `?v=` on both `favicon.ico` references in `claude.html` — browsers hold on to an icon for a long time.

The palette is `theme.css` — the generated file from the private `claude-theme-pack` repo, the source of truth for the colours of every app in this family, whose script verifies every colour pair at WCAG AA. It is linked in the `<head>`, copied byte-for-byte from the pack; `claude.html`'s own theme blocks hold only the handful of app-specific tokens, documented in the comment above them.

Adding a theme starts in the theme pack (new themes need its contrast gate to pass): regenerate and re-copy the pack's `theme.css`, then four edits in `claude.html` — a `[data-theme="…"]` block for the app tokens, an `<option>` in the picker (kept alphabetical), the `THEMES` validation array in the `<head>` script — and this list.

### Accessibility

Card headers are real buttons, so the whole dashboard works by keyboard: Tab to a card, Enter or Space to expand it. Each card is a labelled region with `aria-expanded`, and the page uses a proper heading outline (`h1` → `h2` per card). All four themes meet WCAG AA contrast (4.5:1 for text, 3:1 for control borders) on every surface, links inside body text are underlined so colour is never the only cue, and the OS "reduce motion" setting disables the smooth scroll and transitions.

**A skip link is the first thing in the tab order**, added 2026-08-21 — every sibling app had one from 2026-08-20 and this page was the last without. Without it a keyboard or screen-reader user tabbed the whole header — brand, two pickers, Refresh — before reaching the first card. It lands on `<main id="grid" tabindex="-1">`; the `tabindex` is what lets focus actually move there rather than the page merely scrolling, and `main:focus { outline: none }` stops the browser then ringing the entire card grid. `tests.html` pins all three parts, and that the skip link comes first.

Both pages are a `<main>` / `<footer>` pair, in that order. A `<footer>` nested inside `main` is **not** contentinfo — it is a plain footer for that section — so `</main>` closes above it and `.wrap` stays an ordinary `<div>`. The privacy page gained the pair on 2026-08-21, along with the family footer it had never carried.

## Tasks

| Task | Schedule | Description |
|---|---|---|
| 🎉 Buffalo Weekend Events | Every Friday at 12:00 AM | Free & paid events in and around Buffalo |
| 📺 Streaming Digest | Every Friday at 12:15 AM | New on Apple TV+, Crunchyroll, and Prime Video |
| 💻 macOS Beta Check | Every Wednesday at 12:30 AM | Go/no-go recommendation for Apple Silicon MacBook Pro |
| 📱 iOS Beta Check | Every Wednesday at 12:45 AM | Go/no-go recommendation for iPhone 15 Pro Max |
| 📲 iPhone Rumors | Every Monday at 1:00 AM | Next-iPhone rumor roundup, grouped by confidence level |
| 💉 GLP-1 News | Every Saturday at 1:15 AM | GLP-1 drug news from the past week — trials, FDA actions, and industry developments |
| 🤖 Claude and Other AI News | Every day at 1:30 AM | Latest Anthropic, Claude, and AI industry news from the past 24 hours |
| 🗞️ Daily News Briefing | Every day at 1:45 AM | Local Pendleton/Buffalo/WNY, US, and global headlines |

## How It Works

The dashboard's footer links to this README as **How it works**.

Each scheduled Claude task writes its output to a local `data/data-*.js` file, which a file watcher pushes to this repo within moments of the task finishing. The `claude.html` dashboard loads all the data files as scripts and renders them as cards — no server required, works as a plain `file://` page or via GitHub Pages.

`tests.html` pins the dashboard's sanitizer — the function that decides what a task's untrusted output may render as HTML — its timestamp helpers, and since 2026-08-21 the page's landmarks and both footers. Open it via a local server (`python3 -m http.server 8015`, then http://localhost:8015/tests.html): it loads the real `claude.html` in a hidden iframe and either reports "All N tests pass" or lists what broke. Its CSP spells out `connect-src 'self'` for the one file it reads as text (`privacy.html`) — without it that fetch is refused by `default-src 'none'` and three tests fail about a file that is plainly there.

GitHub Actions runs the same page headless on every push to `main` (`.github/workflows/tests.yml`), so the sanitizer can't quietly break. Before 2026-08-20 it only ever ran when somebody opened it by hand.

### Handling Task Content Safely

Task output is written by scheduled tasks that summarise pages from the open web, so the dashboard treats it as untrusted. Content is HTML-escaped before rendering, then a small allowlist is re-enabled: bare `<strong>`, `<em>`, `<b>`, `<i>`, `<br>` (no attributes) and `[label](https://…)` markdown links, which become `rel="noopener noreferrer"` anchors. Anything else — script tags, event-handler attributes, `javascript:` URLs — stays inert as visible text. A Content-Security-Policy meta tag backs this up, and a malformed data file degrades to a single "could not be displayed" card instead of blanking the dashboard.

If a task ever needs a new tag (a list, a heading), add it to the allowlist in `formatContent` rather than removing the escaping.

## Privacy Policy

[`privacy.html`](privacy.html) is linked from the dashboard's footer. The page keeps a theme
and a text size in localStorage and makes no network requests at all (`connect-src 'none'`),
so the policy is short — but every public page in this family carries one. It is a named
public file in the whitelist `.gitignore`, like `claude.html` itself, and is pushed by hand.

It carries the family footer too, since 2026-08-21: the repo under **How it works**, and the
authorship line. **That line is two links, not one** — "independent personal project" points at
[NOTICE](NOTICE) and "MIT licensed" points at [LICENSE](LICENSE). The dashboard's own footer
had them as a single link reading "MIT licensed" that landed on NOTICE; a licence is the terms
and NOTICE is who owns it, so the words and the destination disagreed. Both footers carry the
split pair now, and `tests.html` asserts which link goes where. There is deliberately **no**
privacy link in the privacy page's own footer — you are standing on it.

## Ownership and Licence

The Claude Task Dashboard is an independent personal project by Charles Adams — built on
personally owned hardware, with a personally paid-for Claude subscription, in a personal
GitHub account. No employer equipment, funding or code went into it, and it carries no
employer information: the cards are the output of his own scheduled personal-interest
tasks, summarising public pages from the open web. The whitelist `.gitignore` keeps
everything else in the working folder local-only.

It is [MIT licensed](LICENSE), so anyone may use, modify and redistribute it. Running it
inside an organisation conveys no ownership of it; permission comes from that licence,
granted by the author as copyright holder. [NOTICE](NOTICE) records this in full.
