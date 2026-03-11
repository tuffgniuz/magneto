# Magneto

Magneto is a terminal UI for browsing movies from YTS, inspecting details, previewing posters, watching trailers, and sending torrents to your local torrent client.

It is built with Textual and is designed around keyboard-driven browsing.

> [!NOTE]
> This project is still in development.

## Demo

![magneto in action](assets/demo.gif)

## Features

- Browse YTS movies from the terminal.
- Search by title with `/`.
- Filter by genre with `f`.
- Browse paginated result sets with `h` and `l`.
- View rich movie details including:
  - poster preview
  - rating
  - genres
  - language
  - cast
  - description
  - trailer availability
- Watch trailers with `w`.
  - Uses `mpv` first when available.
  - Falls back to opening YouTube in the browser.
- View available torrents for the selected movie.
- Download torrents through your default torrent client.
  - Prefers the YTS `.torrent` file URL.
  - Falls back to a magnet link when needed.
- Use Vim-style navigation with `j` and `k` in:
  - the movie list
  - the genre picker
  - the torrent picker

## Installation

### From source

```bash
git clone https://github.com/tuffgniuz/magneto.git
cd magneto
poetry install
make install
```

This installs the `magneto` binary into `~/.local/bin` by default.

Make sure `~/.local/bin` is on your `PATH`.

For Bash or Zsh:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

For Fish:

```fish
fish_add_path ~/.local/bin
```

## Development

Install dependencies:

```bash
poetry install
```

Run the app directly from the project:

```bash
poetry run magneto
```

Build and reinstall the standalone binary:

```bash
make install
```

## Default Keybindings

### Global

- `q`: quit
- `/`: search movies
- `f`: open genre filter
- `c`: clear search query
- `h`: previous page
- `l`: next page
- `w`: watch trailer
- `t`: open torrent list for the selected movie
- `up` / `down`: move selection in the movie list
- `j` / `k`: move selection in list-based views

### Search modal

- `enter`: submit search
- `escape`: close

### Genre modal

- `enter`: select highlighted genre
- `escape`: close
- `j` / `k`: move down / up

### Torrent modal

- `d`: download highlighted torrent
- `escape`: close
- `j` / `k`: move down / up

## Notes

- Poster previews depend on terminal image support and the installed `textual-image` backend.
- Trailer playback prefers `mpv` if it is installed and available on `PATH`.
- Torrent downloads rely on your desktop’s default handler for `.torrent` files or magnet links.
