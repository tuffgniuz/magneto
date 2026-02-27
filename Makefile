# Makefile for the Magneto project

# Default destination for the binary
INSTALL_DIR ?= $(HOME)/.local/bin

# Removes build artifacts
clean:
	@echo "Cleaning up build artifacts..."
	@rm -rf dist/ build/ magneto.spec

# Creates the standalone binary using PyInstaller
build:
	@echo "Building the binary..."
	@poetry run pyinstaller src/magneto/app.py \
		--onefile \
		--name magneto \
		--collect-all rich \
		--collect-all textual \
		--add-data "src/magneto/ui/style.tcss:magneto/ui"

# Installs the binary to the local bin directory
# It depends on 'build', so it will build the binary first if needed.
install: build
	@echo "Installing magneto to $(INSTALL_DIR)..."
	@mkdir -p $(INSTALL_DIR)
	@cp dist/magneto $(INSTALL_DIR)/magneto
	@echo "Installation complete. You can now run 'magneto' from your terminal."

.PHONY: clean build install
