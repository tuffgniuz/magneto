# Magneto

> [!NOTE]
> This project is still in development.

A textual-based application for browsing and searching movies from YTS.

## Installation from Source

For a local installation, you can build a standalone binary from the source code. This requires `make` to be installed on your system.

1.  **Clone and Enter the Repository**:
    ```bash
    git clone https://github.com/tuffgniuz/magneto.git
    cd magneto
    ```

2.  **Build and Install**:
    Run the following command to build the binary and install it to `~/.local/bin`:
    ```bash
    make install
    ```
    This command will automatically handle dependency installation, bundling, and copying the executable to the correct path.

3.  **Run the Application**:
    Once installed, you can run the application from anywhere in your terminal:
    ```bash
    magneto
    ```

> [!IMPORTANT]
> Ensure that `~/.local/bin` is in your system's `PATH` to run `magneto` globally.

#### How to add `~/.local/bin` to your `PATH`:

**For Bash and Zsh:**
Add this line to your `~/.bashrc` or `~/.zshrc`:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

**For Fish:**
Run this command in your terminal:
```fish
fish_add_path ~/.local/bin
```

## Development

To run the application in a development environment:

1.  **Install Dependencies**:
    ```bash
    poetry install
    ```

2.  **Run the App**:
    ```bash
    poetry run magneto
    ```


## Key Bindings

### Global
- `/`: Search for movies
- `c`: Clear search results
- `t`: Show available torrents for the selected movie
- `up`/`down` (or `k`/`j`): Navigate the movie list
- `q`: Quit the application

### Search Modal
- `enter`: Submit search
- `escape`: Cancel and close search modal

### Torrent Modal
- `d`: Download the selected torrent (opens magnet link in default client)
- `escape`: Close the torrent modal
