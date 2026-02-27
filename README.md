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

-   `/`: Show search
-   `c`: Clear search
-   `q`: Quit
