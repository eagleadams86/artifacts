# Claude Scheduled Task Dashboard

A personal dashboard that displays the live outputs of scheduled Claude tasks.

## Dashboard

**[View claude.html](https://eagleadams86.github.io/artifacts/claude.html)**

Cards are sorted by most recently updated and collapse by default — click a card header to expand it (and collapse any other). Refresh the page to see the latest outputs.

A theme picker in the top-right switches between eight themes — 🌙 Dark, 🧛 Dracula, ☀️ Light, 🌌 Midnight (default), ❄️ Nord, 🌸 Sakura, 🌆 Synthwave, and 🖥️ Terminal (green monospace). A text size picker next to it offers Small / Normal / Large / XL / XXL. Both choices are saved in the browser and persist across visits.

## Tasks

| Task | Schedule | Description |
|---|---|---|
| 🤖 Claude News | Every day at 1:00 AM | Latest Anthropic & Claude news from the past 24 hours |
| 📲 iPhone Rumors | Every day at 1:30 AM | Next-iPhone rumor roundup, grouped by confidence level |
| 📺 Streaming Digest | Every day at 2:00 AM | New on Apple TV+, Crunchyroll, and Prime Video |
| 🗞️ Daily News Briefing | Every day at 2:30 AM | Local Pendleton/Buffalo/WNY, US, and global headlines |
| 🎉 Buffalo Weekend Events | Every day at 3:00 AM | Free & paid events in and around Buffalo |
| 📱 iOS Beta Check | Every day at 3:30 AM | Go/no-go recommendation for iPhone 15 Pro Max |
| 💻 macOS Beta Check | Every day at 4:00 AM | Go/no-go recommendation for Apple Silicon MacBook Pro |

## How it works

Each scheduled Claude task writes its output to a local `data/data-*.js` file, which a file watcher pushes to this repo within moments of the task finishing. The `claude.html` dashboard loads all the data files as scripts and renders them as cards — no server required, works as a plain `file://` page or via GitHub Pages.
