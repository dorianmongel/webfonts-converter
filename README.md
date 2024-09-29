# Webfonts Converter

## Description

Webfonts Converter is a Python-based tool designed to simplify the process of converting font files to various webfont formats. This application allows users to easily transform font files into formats suitable for web use, including TTF, WOFF, WOFF2.

## Features

- Convert font files to multiple webfont formats
- Support for various input font formats (TTF, WOFF, WOFF2)
- User-friendly graphical interface
- Batch conversion capability
- Cross-platform compatibility (Windows, macOS, Linux)

## Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

### Steps

1. Clone this repository or download the source code.
2. Navigate to the project directory in your terminal.
3. Install the required dependencies:


## Building the Application

To create a standalone executable:

1. Ensure you have PyInstaller installed:
2. Run the following command in the project directory:

pyinstaller --name="Convertisseur de Webfonts" --windowed --onefile --icon=icon.icns webfonts_converter.py