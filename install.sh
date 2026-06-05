#!/bin/bash

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "Checking for uv..."
if ! command -v uv &> /dev/null; then
    echo "Error: 'uv' is not installed or not in PATH."
    echo "Please install uv (e.g. curl -LsSf https://astral.sh/uv/install.sh | sh) and try again."
    exit 1
fi

echo "Setting up configuration directory..."
mkdir -p ~/.config/sheetspan

if [ -f "$DIR/credentials.json" ]; then
    echo "Found credentials.json in source directory. Moving to ~/.config/sheetspan/..."
    cp "$DIR/credentials.json" ~/.config/sheetspan/credentials.json
else
    echo "Notice: credentials.json not found in $DIR."
fi

echo "Creating .desktop file..."
mkdir -p ~/.local/share/applications/
DESKTOP_FILE="$HOME/.local/share/applications/sheetspan.desktop"

echo "[Desktop Entry]" > "$DESKTOP_FILE"
echo "Version=1.0" >> "$DESKTOP_FILE"
echo "Name=Sheetspan" >> "$DESKTOP_FILE"
echo "Comment=Open spreadsheet in Google Sheets" >> "$DESKTOP_FILE"
echo "Exec=uv run $DIR/sheetspan.py %f" >> "$DESKTOP_FILE"
echo "Icon=x-office-spreadsheet" >> "$DESKTOP_FILE"
echo "Terminal=false" >> "$DESKTOP_FILE"
echo "Type=Application" >> "$DESKTOP_FILE"
echo "Categories=Office;Spreadsheet;" >> "$DESKTOP_FILE"
echo "MimeType=text/csv;application/vnd.ms-excel;application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;application/vnd.oasis.opendocument.spreadsheet;" >> "$DESKTOP_FILE"

echo "Updating desktop database and mime types..."
update-desktop-database ~/.local/share/applications/ || echo "Warning: update-desktop-database failed, but continuing..."

xdg-mime default sheetspan.desktop text/csv application/vnd.ms-excel application/vnd.openxmlformats-officedocument.spreadsheetml.sheet application/vnd.oasis.opendocument.spreadsheet

echo ""
echo "Installation complete!"
if [ ! -f ~/.config/sheetspan/credentials.json ]; then
    echo "IMPORTANT: You must create a Google Drive API OAuth Client ID (Desktop app)"
    echo "and save it as ~/.config/sheetspan/credentials.json before using Sheetspan."
else
    echo "Credentials found and configured!"
fi
