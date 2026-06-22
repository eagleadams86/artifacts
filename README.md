# artifacts

A personal dashboard that displays the live outputs of scheduled Claude tasks.

## Dashboard

**[View claude.html](https://eagleadams86.github.io/artifacts/claude.html)**

Cards are sorted by most recently updated and expand to show full content. Refresh the page to see the latest outputs.

## Tasks

| Task | Schedule | Description |
|---|---|---|
| 🗞️ Daily News Briefing | 6:00 AM & 6:00 PM daily | Local Pendleton/Buffalo/WNY, US, and global headlines |
| 🔊 Soundbar Price Alert | Every day at 12:00 AM | Samsung HW-Q600F — alert when ≤$300 incl. shipping |
| 📱 iOS Beta Check | Every day at 4:00 AM | Go/no-go recommendation for iPhone 15 Pro Max |
| 🎉 Buffalo Weekend Events | Every day at 5:00 AM | Free & paid events in and around Buffalo |
| 📺 Streaming Digest | Every day at 2:00 AM | New on Apple TV+, Crunchyroll, and Prime Video |

## Notes & Guides

| File | Description |
|---|---|
| 📓 [Nice_Guy_to_Integrated_Man_Notes.html](https://eagleadams86.github.io/artifacts/Nice_Guy_to_Integrated_Man_Notes.html) | Personal development notes — Nice Guy to Kind Man |

## How it works

Each scheduled Claude task writes its output to a corresponding `data/data-*.js` file in this repo. The `claude.html` dashboard loads all five files as scripts and renders them as cards — no server required, works as a plain `file://` page or via GitHub Pages.
