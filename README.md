# Claude Scheduled Task Dashboard

A personal dashboard that displays the live outputs of scheduled Claude tasks.

## Dashboard

**[View claude.html](https://eagleadams86.github.io/artifacts/claude.html)**

Cards are sorted by most recently updated and collapse by default — click a card header to expand it (and collapse any other). Refresh the page to see the latest outputs. Each card header shows when the task is due (🕐 line, left) next to when it actually last ran (right), so a task that has missed its slot is visible at a glance.

A theme picker in the top-right switches between the four unified themes shared by all my apps, listed alphabetically — ☾ Dark, ☀️ Light, ✦ Midnight (the default) and 📜 Sepia. (Dracula, Nord, Sakura, Synthwave and Terminal were retired in August 2026; a saved choice of one of them falls back to Midnight.) A text size picker next to it offers Small / Normal / Large / XL / XXL. Both choices are saved in the browser and persist across visits.

The palettes are transcribed from the private `claude-theme-pack` repo — the source of truth for the colours of every app in this family — whose script verifies every colour pair at WCAG AA. The token mapping is documented in the comment above the theme blocks in `claude.html`.

Adding a theme starts in the theme pack (new themes need its contrast gate to pass), then four edits in `claude.html`: a `[data-theme="…"]` block, an `<option>` in the picker (kept alphabetical), the `THEMES` validation array in the `<head>` script, and this list.

### Accessibility

Card headers are real buttons, so the whole dashboard works by keyboard: Tab to a card, Enter or Space to expand it. Each card is a labelled region with `aria-expanded`, and the page uses a proper heading outline (`h1` → `h2` per card). All four themes meet WCAG AA contrast (4.5:1 for text, 3:1 for control borders) on every surface, links inside body text are underlined so colour is never the only cue, and the OS "reduce motion" setting disables the smooth scroll and transitions.

## Tasks

| Task | Schedule | Description |
|---|---|---|
| 🎉 Buffalo Weekend Events | Every Friday at 12:00 AM | Free & paid events in and around Buffalo |
| 📺 Streaming Digest | Every Friday at 12:15 AM | New on Apple TV+, Crunchyroll, and Prime Video |
| 💻 macOS Beta Check | Every Wednesday at 12:30 AM | Go/no-go recommendation for Apple Silicon MacBook Pro |
| 📱 iOS Beta Check | Every Wednesday at 12:45 AM | Go/no-go recommendation for iPhone 15 Pro Max |
| 📲 iPhone Rumors | Every Monday at 1:00 AM | Next-iPhone rumor roundup, grouped by confidence level |
| 💉 GLP-1 News | Every day at 1:15 AM | GLP-1 drug news — trials, FDA actions, and industry developments |
| 🤖 Claude and Other AI News | Every day at 1:30 AM | Latest Anthropic, Claude, and AI industry news from the past 24 hours |
| 🗞️ Daily News Briefing | Every day at 1:45 AM | Local Pendleton/Buffalo/WNY, US, and global headlines |

## How it works

Each scheduled Claude task writes its output to a local `data/data-*.js` file, which a file watcher pushes to this repo within moments of the task finishing. The `claude.html` dashboard loads all the data files as scripts and renders them as cards — no server required, works as a plain `file://` page or via GitHub Pages.

### Handling task content safely

Task output is written by scheduled tasks that summarise pages from the open web, so the dashboard treats it as untrusted. Content is HTML-escaped before rendering, then a small allowlist is re-enabled: bare `<strong>`, `<em>`, `<b>`, `<i>`, `<br>` (no attributes) and `[label](https://…)` markdown links, which become `rel="noopener noreferrer"` anchors. Anything else — script tags, event-handler attributes, `javascript:` URLs — stays inert as visible text. A Content-Security-Policy meta tag backs this up, and a malformed data file degrades to a single "could not be displayed" card instead of blanking the dashboard.

If a task ever needs a new tag (a list, a heading), add it to the allowlist in `formatContent` rather than removing the escaping.
