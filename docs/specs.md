# Magneto  
### A Minimalist Terminal Torrent Cinema Client

---

# 1. Introduction

## 1.1 Overview

**Magneto** is a terminal-based torrent cinema client built in Python using the Textual framework. It allows users to browse, search, stream, and download movies from the YTS torrent API directly from a modern TUI (Text User Interface).

Magneto combines:

- A Yazi-inspired minimal file-manager layout
- Integrated torrent downloading (no external torrent client required)
- Streaming support via local media players (mpv or VLC)
- Real-time progress tracking
- Poster image previews inside supported terminals

The goal is to create a clean, performant, keyboard-driven application that feels native to power users who live in the terminal.

---

## 1.2 Objective

The primary objectives of Magneto are:

1. Provide a fast, minimal, keyboard-driven interface for browsing YTS movies.
2. Enable streaming directly to mpv or VLC using magnet links.
3. Enable torrent downloading inside the application using libtorrent.
4. Display real-time download progress with seeders, ETA, and speeds.
5. Maintain a modern TUI aesthetic inspired by tools like Yazi.
6. Store downloaded movies in `~/Movies` by default.
7. Provide a seamless search experience via a floating modal ("/").

---

# 2. Technology Stack

## 2.1 Programming Language

- **Python 3.11+**
  - Async-first architecture
  - Strong support for TUI and torrent libraries
  - Cross-platform

---

## 2.2 Core Libraries

### UI Framework
- **Textual**
  - Async-native TUI framework
  - Supports layouts, modals, key bindings
  - Image rendering support
  - Reactive state management

---

### HTTP Client
- **httpx**
  - Async HTTP client
  - Used for YTS API calls
  - Clean JSON parsing

---

### Torrent Engine
- **libtorrent (python-libtorrent)**
  - Internal torrent downloading
  - Progress tracking
  - Seeder/peer count
  - ETA estimation
  - Sequential download mode for streaming
  - Full control (no external torrent client required)

---

### Streaming
Two possible approaches:

#### Primary Option (MVP)
- Launch `mpv` or `vlc` as subprocess
- Pass magnet link or local file

#### Advanced Option
- Use libtorrent sequential download
- Start playback once sufficient buffer is available

---

### Optional Utilities
- Pillow (if needed for image handling)
- Rich (Textual dependency)
- platformdirs (for config management)

---

# 3. Project Management & Packaging

## 3.1 Dependency Management

Magneto will use:

> ✅ **Poetry**

Reason:
- Clean dependency locking
- Virtual environment management
- Reproducible builds
- Proper packaging for PyPI

---

## 3.2 Project Structure

```
magneto/
├── src/
│   ├── __init__.py
│   ├── app.py
│   ├── config.py
│   ├── api/
│   │   └── yts.py
│   ├── torrent/
│   │   └── manager.py
│   ├── ui/
│   │   ├── layout.py
│   │   ├── movie_list.py
│   │   ├── movie_details.py
│   │   ├── torrent_panel.py
│   │   ├── search_modal.py
│   │   └── progress.py
│   └── utils/
│       └── paths.py
│
├── pyproject.toml
├── README.md
└── LICENSE
```

---

# 4. Core Features

---

# 4.1 Movie Browsing

Magneto will use the YTS API:

```
https://yts.mx/api/v2/list_movies.json
```

Capabilities:
- List movies
- Paginated results
- Filter by query term
- Display rating, year, runtime, genres

Movie data includes:
- Title
- Year
- Rating
- Description
- Poster image URL
- Available torrents (720p, 1080p, 4K)
- Magnet links
- Seeds & peers

---

# 4.2 Search Functionality

Trigger:
```
/
```

Behavior:
- Open centered floating modal
- Input field auto-focused
- Enter executes search
- Escape closes modal

Results:
- Left column refreshes with search results
- Clear search returns to popular listing

---

# 4.3 Torrent Downloading (Internal)

Magneto must:

- Add magnet links via libtorrent
- Store downloads in `~/Movies`
- Create folder if it does not exist
- Display:
  - Percentage progress
  - Download speed
  - Upload speed
  - Seeders/peers
  - ETA
  - Torrent state (downloading, seeding, finished)

Download behavior:
- Multiple torrents supported
- Background updating every 1 second
- Non-blocking UI

---

# 4.4 Streaming
When user selects a torrent:

Options:
- Press `s` → Stream
- Press `d` → Download

Streaming flow (MVP):
- Launch mpv:
  ```
  mpv <magnet_link>
  ```
- Or VLC
- Run as subprocess
- Do not block UI

---

# 4.5 Image Preview

Poster images:
- Download to temp directory
- Render via Textual Image widget

Requirements:
- Terminal must support image protocol (Kitty, WezTerm, iTerm2)
- Fallback to text placeholder if unsupported

---

# 5. UI Specification

---

# 5.1 Layout

Three-column horizontal layout:

```
┌────────────┬──────────────┬──────────────┐
│ Movie List │ Movie Details│ Downloads    │
└────────────┴──────────────┴──────────────┘
```

---

## 5.2 Left Column – Movie List

Content:
- Scrollable list
- Title
- Year
- Rating

Navigation:
- ↑ / ↓ arrows
- j / k (vim-style)
- Enter → focus details
- s → stream
- d → download

Design:
- Minimal
- Highlight selected item
- No heavy borders

---

## 5.3 Center Column – Movie Details

Content:
- Title
- Year
- Rating
- Runtime
- Genres
- Description
- Torrent options
- Poster preview

Layout:
- Poster on top
- Metadata below
- Torrent list selectable

---

## 5.4 Right Column – Downloads Panel

Shows active torrents:

For each torrent:

```
Inception (1080p)
[██████░░░░░░░░░] 42%
Peers: 34
Speed: 2.3 MB/s
ETA: 12m
```

Must:
- Update every second
- Remove completed torrents optionally
- Show seeding state

---

# 5.5 Key Bindings

| Key | Action |
|------|--------|
| ↑ / ↓ | Navigate list |
| j / k | Navigate list |
| Enter | Select movie |
| s | Stream |
| d | Download |
| / | Search |
| r | Refresh |
| q | Quit |
| Esc | Close modal |

---

# 6. Configuration

Future config file:

```
~/.config/magneto/config.toml
```

Configurable:
- Default download directory
- Preferred player (mpv or vlc)
- Max concurrent downloads
- Auto-start streaming buffer size
- Port range for torrents

---

# 7. Performance Requirements

- UI must never block during downloads
- API requests async
- Torrent polling every 1 second
- Capable of handling at least 5 concurrent torrents
- Smooth navigation without lag

---

# 8. Error Handling

Must handle:
- Network failures
- Invalid magnet links
- Torrent tracker errors
- No seeders available
- API downtime
- Media player not installed

Graceful messaging in UI.

---

# 9. Security Considerations

- No telemetry
- No user tracking
- No remote execution
- Clear warning that torrents depend on user jurisdiction

---

# 10. MVP Scope

The first release should include:

✅ Browse movies  
✅ Search  
✅ View details  
✅ Download torrent internally  
✅ Show progress  
✅ Stream via mpv  
✅ Store to ~/Movies  
✅ Minimal 3-column layout  

Not required for MVP:
- Config file
- Theming
- Advanced filtering
- Sequential streaming buffer logic
- Plugin system

---

# 11. Future Enhancements

- Watch history
- Resume downloads
- Dark/light theme switch
- Sorting (rating, year, seeds)
- Filter by quality
- Download queue management
- Built-in player (very advanced)
- Subtitle auto-fetch
- TMDB integration

---

# 12. Identity

Name:
> Magneto

Tagline:
> A minimalist terminal torrent cinema client.

Design philosophy:
- Fast
- Keyboard-first
- Minimal
- Powerful
- No clutter

---

# 13. Final Summary

Magneto is a Python-based, async-first, Textual-powered terminal application that enables browsing, streaming, and downloading YTS torrents with a clean 3-column layout and integrated torrent engine.

It combines:

- Modern TUI design
- Internal torrent management
- External player streaming
- Async API integration
- Minimalist UX inspired by Yazi

This document defines the architecture, UI structure, technology stack, and scope required to build Magneto successfully.
