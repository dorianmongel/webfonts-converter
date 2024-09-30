# Webfonts Converter v0.0.3

Webfonts Converter is a user-friendly desktop application that simplifies the process of converting font files between different web-compatible formats.

## Features

- Convert TTF AND OTF to WOFF and WOFF2
- Convert WOFF to TTF and WOFF2
- Automatically generate CSS file for easy web integration
- Create an HTML preview file to test the converted font
- Intuitive drag-and-drop interface
- Bilingual support (English and French)

## Installation

1. Ensure you have Python 3.6 or higher installed on your system.
2. Clone this repository:
   ```
   git clone https://github.com/yourusername/webfonts-converter.git
   ```
3. Navigate to the project directory:
   ```
   cd webfonts-converter
   ```
4. Install the required dependencies:
   ```
   pip install PyQt6 fontTools
   ```

## Usage

1. Run the script:
   ```
   python webfonts_converter.py
   ```
2. Drag and drop your font file (TTF or WOFF) onto the application window.
3. The application will automatically convert the font to other formats.
4. A CSS file and an HTML preview file will be generated in the same directory as the original font.


## System Requirements

- Python 3.6 or higher
- PyQt6
- fontTools

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check the [issues page](https://github.com/dorianmongel/webfonts_converter/issues) if you want to contribute.


## Changelog

## v0.0.4
- Added HTML preview file generation
- Improved error handling
- Updated user interface
- Added support for OTF files
- Added a button to remove files from the list
- Improved interface design
- Processing of multiple fonts in a single export

### v0.0.3
- Added HTML preview file generation
- Improved error handling
- Updated user interface

### v0.0.2
- Added support for WOFF to TTF conversion
- Implemented bilingual support (English and French)

### v0.0.1
- Initial release
- Basic TTF to WOFF conversion
- CSS file generation

## Contact

If you have any questions or feedback, please open an issue on the GitHub repository.