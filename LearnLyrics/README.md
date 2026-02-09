# LearnLyrics

A Python script to generate 4K educational images of church song lyrics with progressive word blanks. Designed to help children learn song lyrics by gradually removing words.

## Features

- **4K Resolution**: Generates high-quality 3840x2160 images for modern displays.
- **Progressive Blanks**: Creates images with 0% to 100% of non-stop words removed in 10% increments.
- **Dynamic Font Sizing**: Automatically maximizes font size to fit text without overflow.
- **Cross-Platform**: Works on Windows, macOS, and Linux with appropriate system fonts.
- **Verse Support**: Handles multi-verse songs, generating separate images for each verse.
- **Visual Blanks**: Uses spaced dots (.) to represent removed characters, maintaining word length.
- **Quality Assurance**: Includes unit tests to ensure text fills at least 70% of image width.
- **Readable Layout**: Blue text on white background with proper spacing and centered titles.

## Requirements

- Python 3.6+
- PIL (Pillow)
- NLTK

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/username/LearnLyrics.git
   cd LearnLyrics
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install pillow nltk
   ```

## Usage

1. **Prepare Input Files**: Place your song lyrics in `.txt` files in the `input/` folder. Verses should be marked with numbers followed by a period (e.g., `1.`, `2.`). Blank lines in the input files are automatically removed during processing.

2. **Navigate to the Project Directory**:
   ```bash
   cd LearnLyrics
   ```

3. **Activate the Virtual Environment** (if using one):
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Run the Script**:
   ```bash
   python main.py
   ```

5. **View Results**: Generated images will be saved in the `output/` folder, organized in subfolders by song title. Filenames follow the format: `{percentage}%_verse{verse_number}_{song_title}.png` (e.g., `50%_verse1_I Will Follow God's Plan (164).png`).

### Input File Format

Each `.txt` file should contain song lyrics with verses separated by numbered lines:

```
1. I will follow God's plan for me
Holding to his loving hand
...

2. He has a work for me to do
To bring his children home to him
...
```

### Output Structure

- Images are generated for each verse and each percentage level (25%, 50%, 75%, 100%).
- Each song gets its own subfolder in `output/`.
- Periods in the lyrics are replaced with slashes '/'
- Blanks are represented by spaced dots (e.g., `...` for a 3-letter word).

## Example

Input file: `I Will Follow God's Plan (164).txt`
```
1. I will follow God's plan for me
Holding to his loving hand
...

2. He has a work for me to do
To bring his children home to him
...
```

Output: Multiple images like:
- `0%_verse1_I Will Follow God's Plan (164).png` (full lyrics)
- `50%_verse1_I Will Follow God's Plan (164).png` (50% words removed)
- `0%_verse2_I Will Follow God's Plan (164).png` (second verse full lyrics)

## How It Works

- Parses lyrics into verses, removing blank lines and replacing periods (.) with slashes (/) for better readability.
- For each percentage (0%, 25%, 50%, 75%, 100%):
  - Randomly selects non-stop words to remove (stop words like "the", "a", "and" are preserved).
  - Replaces each removed word with spaced dots equal to its length (e.g., `...` for a 3-letter word).
  - Generates a 4K image with maximized font size to fit the text without overflow.
  - Ensures text fills at least 70% of the image width for quality.
  - Uses blue text on white background with proper spacing.

## Development

This script was iteratively developed to meet specific requirements:
- Initial: Basic image generation with blanks
- Enhanced: 4K resolution, dynamic sizing, cross-platform support
- Refined: Dots for blanks, vertical spacing, overflow prevention

## License

MIT License - see LICENSE file for details.

## Contributing

Pull requests welcome! Please ensure code follows PEP 8 and includes appropriate tests.</content>
<parameter name="filePath">/Users/robchristiansen/Documents/Code/LearnLyrics/README.md