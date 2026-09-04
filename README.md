# Claude Scheduled Task Dashboard

A personal dashboard that displays the live outputs of scheduled Claude tasks.

## Dashboard

**[View claude.html](https://eagleadams86.github.io/artifacts/claude.html)**

Cards are sorted by most recently updated and collapse by default — click a card header to expand it (and collapse any other). Refresh the page to see the latest outputs. Each card header shows when the task is due (🕐 line, left) next to when it actually last ran (right), so a task that has missed its slot is visible at a glance.

### Finding Things

**⌕ Find searches every card's output at once**, not just the one that happens to be open — the app family's window, the same one Money Map, Sprint Predictability, Flow Metrics and Golf Handicap open on **⌘K / Ctrl+K**. Type two characters or more and the results list every *line* that mentions them, under the card it came from and how old that card's output is. Picking one — a click, or **Enter** for the top result — opens that card, highlights every match in it and scrolls to the line. Escape or a click outside closes the window; a second ⌘K does too. (Until 2026-09-04 Enter did nothing: only typing was wired up, so you had to Tab out of the box to reach a result. With nothing matching, Enter still does nothing and the window stays open — there is nowhere to go.)

Cards themselves are also searched by title, description and schedule, so "beta" finds both beta-check cards even in a week when neither of them ran. The list stops at 80 results and says how many more there were, so a search that matched half the page never quietly shows you a slice of itself.

This is not a convenience the browser's own Ctrl+F could have covered. Card bodies are `display: none` while collapsed and only one card opens at a time, so until 2026-08-22 a browser find reached exactly one card's text: eight tasks' worth of output with no way to search across it. Until 2026-08-23 the answer was a search *field* in the header bar that filtered the grid to the matching cards; the window replaced it, both because the family puts the same control in the same place in every app and because "which line of which briefing" is the more useful answer than "which four cards".

**⇕ Expand all** opens every card at once and turns into Collapse all once they are. While more than one card is open, clicking a card header closes only that one; the one-card-at-a-time habit applies when one card is open, which is the case it was written for.

### Overdue Tasks

A task that has missed its own slot wears an amber **overdue** badge, in words as well as colour. The threshold is read from the same schedule string the card shows — a day for "Every day", a week for "Every Friday" — plus six hours' grace for a task that starts late and the push that carries its output here. A schedule phrased in some way the page does not recognise falls back to the flat 8-day rule this used to apply to everything, which is why a daily task could previously stop for three days without anything being said.

A card with no readable timestamp at all is a different state and keeps the muted badge it always had: that is a task that has never run, or a data file that is wrong.

### Links, Copying and Printing

Opening a card puts its id in the address bar, so a card can be bookmarked or sent to someone — `claude.html#daily-news-briefing` opens on that card. The hash comes off again when several cards are open, since there is no single card to name. It uses `replaceState`, so Back still means the page you came from rather than the last card you closed.

Each open card carries **Copy** and **Print**. Copy puts the task's raw output on the clipboard — markdown link syntax and all, which survives being pasted into a note better than a stripped-out link would. Print prints that one card; printing the page itself prints every card's output, expanded, with the header and footer left off. The page names no colour for paper: the theme pack's own print rule swaps the dark themes to the Light palette when printing, so a midnight card prints as ink on white without this page inventing a print palette of its own.

### Sharing a Snapshot

**Share** builds a read-only link out of the cards you pick. The output travels *inside* the
link itself — nothing is uploaded, no copy is kept, and opening one touches nothing the reader
has saved. It is a **snapshot**: these tasks rewrite themselves on their own schedules and a
link will not follow them, so send a fresh one when the output moves. There is no way to
withdraw one once sent.

Opening a link shows only the cards it carries, with a banner saying so and a way back to the
live page. Everything else on the page still works on them — Find, Expand all, Copy, Print,
the ticking timestamps. Two things are worth knowing:

- **A shared card's output goes through `formatContent`, the same sanitizer as the live data.**
  A link is untrusted input by definition — whoever holds it can edit it — and that function is
  the only path to a card body anywhere on this page.
- **A link carries the id, the timestamp and the output, and nothing else.** Titles, schedules
  and descriptions are hard-coded in `TASKS` on the page reading the link, so sending them would
  be sending a copy of something the reader already has — and a copy that could disagree with it.
  A card whose id the reading page does not know is simply not shown.

Task output is prose, so these links are long: all eight cards runs to about 27,000 characters.
The window says so and suggests picking fewer, which is the honest fix — this is the one page in
the family where the too-long warning is the normal case rather than the edge.

### Staying Current

The dashboard is a snapshot of the moment it loaded. The relative timestamps tick, so a tab left open overnight no longer insists a card was updated five minutes ago, and once the page has been open longer than the hourly push cycle it says so and offers a reload. It cannot check whether newer output exists — the page's CSP is `connect-src 'none'` — so it says the one thing it does know, which is how long ago this copy arrived. That matters more now that it works offline, not less: it is what makes a copy served from the cache honest about its age.

The page is capped at 2400px wide — Money Map's `--page-w`, deliberately the same number rather than the 1500px Sprint Predictability and Flow Metrics use. That narrower cap is for pages of charts and short tables, which do not grow with the window; a card body here is a whole briefing, and it uses whatever width there is. The cap exists at all so the page still has a shape on an ultrawide screen instead of running to both bezels, and it sits on the row inside the header rather than on the bar itself, so the bar's background still reaches the window edges while its contents line up with the cards.

The page wears the app family's header: a sticky bar with the mark, the name and its strapline on the left, and the controls on the right. A theme picker switches between the four unified themes shared by all my apps, listed alphabetically — ◐ Auto, ☾ Dark, ☀ Light, ✦ Midnight and 📜 Sepia. **Auto is the default** (2026-08-22): with nothing saved the page follows your own system, Light or Midnight, and changes with it while it is open. Midnight is the base palette and what Auto means by "dark". (Dracula, Nord, Sakura, Synthwave and Terminal were retired in August 2026; a saved choice of one of them falls back to Auto.) A text size picker next to it offers Small / Normal / Large / XL / XXL, and a ↻ Refresh button reloads the cards. Both picker choices are saved in the browser and persist across visits.

Every option in the theme picker is written into the markup at its final size, and **Auto carries `selected`** — the header paints long before the script at the foot of the page runs, so without it the row names a theme the page is not showing for a moment on every load. (Midnight carried it until 2026-08-22, when the family default moved.) The sun is `☀`, the plain text character, not the emoji-presentation `☀️`: the colour-font variant is a different weight and baseline from the `☾` and `✦` beside it. Every sibling app follows both rules.

### Installing It

`manifest.webmanifest` is what turns Chrome's "Install page as app…" into a real install: its own window with no browser chrome, its own icon in the Dock or on the taskbar, opening straight on `claude.html`. Three things have to stay in step or it silently stops being offered, with nothing but a console line to say so:

- **`manifest-src 'self'` in the CSP.** It falls back to `default-src`, which is `'none'` here, so without the directive the manifest fetch is refused. Suspect this first.
- **`make_favicon.py` writes the install icons** — `icon-192.png`, `icon-512.png` and `icon-512-maskable.png` — from the same drawing as `favicon.ico` and the inline SVG.
- **Each of those four files needs its own line in the whitelist `.gitignore`.** An unnamed file here is silently never committed.

**It works offline too, since 2026-08-22.** This was the one page in the family without a service worker, on the argument that what it displays is task output rewritten hourly and a cached copy of that presented as current is a wrong answer rather than an old page. That argument was right — and it is not what the worker does. `sw.js` is **network-first**: the cache only ever answers a network that actually failed, so a newer briefing landing while you are online is impossible to miss. Offline, you get the last copy, and every card states its own age from its data file's own timestamp, so a stale briefing says so rather than passing itself off as this morning's.

`sw-kill.js` sits beside it unused, which is deliberate: a service worker is resident and can keep serving itself, so the way out has to already be in the repo. `cp sw-kill.js sw.js`, commit, push, and every installed copy uninstalls itself on the next load.

The icon is a stack of task cards — what the page is — on the midnight tile the whole app family wears; the heading shows the same mark, sized in `em` so it follows the text-size picker. `make_favicon.py` (Pillow) keeps `favicon.ico` and the page's inline SVG the same picture, rather than leaving a binary nobody can review in a diff. Re-run it with `python3 make_favicon.py`, then bump the `?v=` on both `favicon.ico` references in `claude.html` — browsers hold on to an icon for a long time.

The palette is `theme.css` — the generated file from the private `claude-theme-pack` repo, the source of truth for the colours of every app in this family, whose script verifies every colour pair at WCAG AA. It is linked in the `<head>`, copied byte-for-byte from the pack; `claude.html`'s own theme blocks hold only the handful of app-specific tokens, documented in the comment above them.

Adding a theme starts in the theme pack (new themes need its contrast gate to pass): regenerate and re-copy the pack's `theme.css`, then four edits in `claude.html` — a `[data-theme="…"]` block for the app tokens, an `<option>` in the picker (kept alphabetical), the `THEMES` validation array in the `<head>` script — and this list.

### Accessibility

Card headers are real buttons, so the whole dashboard works by keyboard: Tab to a card, Enter or Space to expand it. In the Find window the box is labelled rather than relying on its placeholder, each result is a real button so Tab walks the list and Enter opens one, and the result *count* — not the list — is the live region, so a screen reader hears "12 results" per keystroke instead of the whole list read out again. Expand all carries its state in its own label — it controls eight cards, and an `aria-expanded` on one button cannot honestly describe eight. Each card is a labelled region with `aria-expanded`, and the page uses a proper heading outline (`h1` → `h2` per card). All four themes meet WCAG AA contrast (4.5:1 for text, 3:1 for control borders) on every surface, links inside body text are underlined so colour is never the only cue, and the OS "reduce motion" setting disables the smooth scroll and transitions.

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

`tests.html` pins the dashboard's sanitizer — the function that decides what a task's untrusted output may render as HTML — its timestamp helpers, the page's landmarks and both footers, and since 2026-08-22 the schedule parsing behind the overdue badge (including that an unrecognised wording falls back rather than guessing), the search highlighting (that marks come out leaving the text exactly as it was, and that the needle is matched literally rather than as a pattern) and, since 2026-08-23, the Find window's matcher — what counts as a hit, that a line matched twice is listed once, that the index a result carries points at the mark the highlighter actually makes, and that the cap counts what it dropped. It also pins the offline worker's shape (network-first, the allowlisted shell, the `data/data-*.js` pattern and nothing beside it) and the Pages root — that `index.html` and `.nojekyll` are both served, so Jekyll can never again publish this repo's markdown as CSP-less pages on the shared origin. Open it via a local server (`python3 -m http.server 8015`, then http://localhost:8015/tests.html): it loads the real `claude.html` in a hidden iframe and either reports "All N tests pass" or lists what broke. Its CSP spells out `connect-src 'self'` for the files it reads as text (`privacy.html`, `sw.js`, `sw-kill.js`, `index.html`, `.nojekyll` and `claude.html`'s own source) — without it those fetches are refused by `default-src 'none'` and tests fail about files that are plainly there — and `https://api.github.com` for the CI-scorecard line added 2026-08-22. That line is why the endpoint is named at all: the page is published beside `claude.html` and refuses to *run* there, so without it a reader on the live site is told the suite cannot run and nothing about whether it passes. It is one public, unauthenticated read of this workflow's run list, on the dev page only — `claude.html` and `privacy.html` name no external host, and must not.

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
