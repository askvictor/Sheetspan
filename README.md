# Sheetspan

Sheetspan is a lightweight Linux utility that seamlessly integrates local spreadsheet files with Google Sheets. Simply double-click any local `.csv`, `.xlsx`, `.xls`, or `.ods` file in your file manager, and Sheetspan will automatically upload it to a `sheetspan` folder in your Google Drive, convert it to a native Google Sheets document, and open it directly in your default web browser.

> ✨ **Note:** This project was entirely vibecoded.

## Features

- **Seamless Desktop Integration**: Automatically registers as the default application for spreadsheet files on Linux via `xdg-mime` and `.desktop` files.
- **Auto-Conversion**: Converts Excel and CSV files to native Google Sheets format upon upload.
- **Organized Drive**: Keeps your Google Drive organized by isolating all uploaded files into a dedicated `sheetspan` directory.
- **Zero-Clutter Dependencies**: Uses [`uv`](https://github.com/astral-sh/uv) to manage Python dependencies in isolated, ephemeral environments using PEP 723 inline script metadata.

## Prerequisites

- A Linux Desktop Environment
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/) installed on your system
- Python 3.10+
- A Google Cloud Project with the Google Drive API enabled

## Installation

1. **Get Google Drive API Credentials**:
   - Navigate to the [Google Cloud Console](https://console.cloud.google.com/).
   - Enable the **Google Drive API** for your project.
   - Go to **Credentials** -> **Create Credentials** -> **OAuth client ID**.
   - Choose **Desktop app** as the application type.
   - Download the generated JSON file and rename it to `credentials.json` in the root of this project.

2. **Run the Installer**:
   Execute the installation script:
   ```bash
   ./install.sh
   ```
   This script will:
   - Move your `credentials.json` to the correct location (`~/.config/sheetspan/`).
   - Generate a `sheetspan.desktop` entry.
   - Update your system's MIME type database to associate spreadsheet files with Sheetspan.

## Usage

Simply double-click any supported spreadsheet file in your file manager, or run it via the command line:

```bash
uv run sheetspan.py /path/to/your/spreadsheet.csv
```

*On the very first run*, your default web browser will open requesting OAuth consent to access your Google Drive. After granting permission, the app will cache a `token.json` file securely and will not prompt you again.

## License

This project is licensed under the **GNU General Public License (GPL)**.
