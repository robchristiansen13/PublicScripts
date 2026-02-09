"""
Script to generate 4K images of church song lyrics with varying percentages of words removed.
Designed for educational purposes to help children learn lyrics.

Requirements: Python 3, PIL (Pillow), NLTK
Install: pip install pillow nltk

Calling Instructions:
1. Place .txt files with song lyrics in the 'input/' folder.
2. Make sure you are in the LearningLyrics folder: cd LearnLyrics
3. Run the script: source venv/bin/activate && python main.py
4. Images will be generated in the 'output/' folder.

Usage: python main.py
- Reads .txt files from 'input/' folder
- Generates images in 'output/' folder
- Each image is IMAGE_WIDTH x IMAGE_HEIGHT with large, readable text
- Includes unit test to ensure text fills >WIDTH_FILL_THRESHOLD of width

Cross-platform: Works on Windows, macOS, and Linux with appropriate fonts.

Development History Summary:
- Initial request: Generate images of church song lyrics with blanks for educational purposes.
- Evolved to: 4K resolution, dynamic font sizing to prevent overflow, cross-platform fonts, unit tests for width fill.
- Changed blanks from underscores to dots for better visibility.
- Added vertical spacing between lines for readability, adjusted to prevent cutoff.
- Final features: Progressive 0-100% word removal, spaced dots for blanks, maximized fonts, verse handling, blue text on white background.

Initial prompt:
I am helping children learn lyrics to church songs. I want to generate 1920x1080 images that contain the lyrics. The lyrics themselves are stored in the input subfolder as text documents. 
Read in the all the files. Some of the songs have multiple verses. I want an image for each verse. If no verses are present then one image is fine. The verses are marked in the text files as 1., 2. etc for each verse. 
I want you to generate multiple image versions of each song. Do not ever remove common english stop words (the, a, or, it, he, she, etc - use a library for those) but I want an image with 0% of the non-stop words replaced with periods (matching the string length of the removed word), 25% of the non-stop words replaced, 50%, 75% all the way to 100%. 
"""
import os
import re
import random
import platform
from PIL import Image, ImageDraw, ImageFont
import nltk
from nltk.corpus import stopwords

# Configuration
IMAGE_WIDTH = 3840  # 4K width
IMAGE_HEIGHT = 2160  # 4K height
LYRICS_FONT_SIZE = 200
TITLE_FONT_SIZE = 120
WIDTH_FILL_THRESHOLD = 0.7  # 70% width fill requirement

# Download stopwords if not present
nltk.download('stopwords', quiet=True)
stop_words = set(stopwords.words('english'))

def get_font_paths():
    """Get font paths based on the operating system."""
    system = platform.system()
    if system == 'Windows':
        base = 'C:\\Windows\\Fonts\\'
        return {
            'regular': base + 'arial.ttf',
            'bold': base + 'arialbd.ttf'
        }
    elif system == 'Darwin':  # macOS
        base = '/System/Library/Fonts/'
        return {
            'regular': base + 'Helvetica.ttc',
            'bold': base + 'Helvetica.ttc'  # Use index for bold
        }
    else:  # Linux or others
        # Try common paths
        possible_regular = [
            '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
            '/usr/share/fonts/TTF/DejaVuSans.ttf',
            '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'
        ]
        possible_bold = [
            '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
            '/usr/share/fonts/TTF/DejaVuSans-Bold.ttf',
            '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
        ]
        regular = next((p for p in possible_regular if os.path.exists(p)), None)
        bold = next((p for p in possible_bold if os.path.exists(p)), None)
        return {
            'regular': regular,
            'bold': bold
        }

def parse_verses(file_path):
    """Parse verses from a text file, splitting on lines starting with digits."""
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    verses = []
    current_verse = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if re.match(r'^\d+\.', line):
            if current_verse:
                verse_text = '\n'.join(current_verse).replace('.', '/') # Replace periods in lyrics with slashes
                verses.append(verse_text)
            current_verse = [line]
        else:
            current_verse.append(line)
    if current_verse:
        verse_text = '\n'.join(current_verse).replace('.', '/') # Replace periods in lyrics with slashes
        verses.append(verse_text)
    return verses

def process_verse(verse_text, percentage):
    """Replace a percentage of non-stop words with underscores."""
    # Find all words with positions
    words = []
    for match in re.finditer(r'\b\w+\b', verse_text):
        word = match.group()
        if word.lower() not in stop_words and not word.isdigit():
            words.append((match.start(), match.end(), word))
    
    # Select percentage to replace
    num_to_replace = int(len(words) * percentage / 100)
    to_replace = random.sample(words, num_to_replace)
    
    # Replace in reverse order to maintain positions
    modified_text = verse_text
    for start, end, word in sorted(to_replace, reverse=True):
        replacement = ('.') * (len(word) - 1) + '.' if len(word) > 0 else ''
        modified_text = modified_text[:start] + replacement + modified_text[end:]
    
    return modified_text

def check_image_fill(output_path, verse_text):
    """Unit test: Check if blue text reaches over WIDTH_FILL_THRESHOLD of the image width."""
    # Calculate max line width
    dummy_img = Image.new('RGB', (1, 1), 'white')
    draw_dummy = ImageDraw.Draw(dummy_img)
    
    # Get font
    fonts = get_font_paths()
    try:
        if fonts['regular']:
            lyrics_font = ImageFont.truetype(fonts['regular'], LYRICS_FONT_SIZE)
        else:
            lyrics_font = ImageFont.load_default()
    except:
        lyrics_font = ImageFont.load_default()
    
    lines = verse_text.split('\n')
    max_line_width = 0
    for line in lines:
        bbox = draw_dummy.textbbox((0, 0), line, font=lyrics_font)
        line_width = bbox[2] - bbox[0]
        max_line_width = max(max_line_width, line_width)
    
    max_x = 50 + max_line_width
    width = IMAGE_WIDTH
    if max_x / width <= WIDTH_FILL_THRESHOLD:
        print(f"FAIL: Image {output_path} does not fill {WIDTH_FILL_THRESHOLD*100}% width (max_x={max_x}, width={width})")
        return False
    else:
        print(f"PASS: Image {output_path} fills >{WIDTH_FILL_THRESHOLD*100}% width")
        return True

def check_bottom_overflow(output_path, verse_text):
    """Unit test: Check if blue text overflows into the bottom 5% of the image."""
    img = Image.open(output_path)
    width, height = img.size
    bottom_start = int(height * 0.95)  # Bottom 5% starts at 95% height
    
    # Scan pixels in the bottom 5%
    for y in range(bottom_start, height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            if (r, g, b) == (0, 0, 255):  # Blue text
                print(f"FAIL: Image {output_path} has blue text in bottom 5% (overflow at y={y})")
                return False
    
    print(f"PASS: Image {output_path} has no blue text in bottom 5%")
    return True

def get_max_font_size(draw, text_lines, font_path, max_width, max_height, extra_space):
    """Find the maximum font size that fits all text lines within max_width and max_height."""
    for size in range(200, 10, -1):
        try:
            font = ImageFont.truetype(font_path, size)
        except:
            font = ImageFont.load_default()
        max_line_width = max(draw.textbbox((0, 0), line, font=font)[2] for line in text_lines)
        if max_line_width > max_width:
            continue
        # Calculate total height
        total_height = 0
        for line in text_lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            line_height = bbox[3] - bbox[1]
            total_height += line_height
        total_height += (len(text_lines) - 1) * extra_space
        if total_height <= max_height:
            return size
    return 10  # Minimum fallback

def generate_image(song_title, verse_text, percentage, output_path, has_multiple, verse_number):
    img = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), 'white')
    draw = ImageDraw.Draw(img)
    
    # Get font paths
    fonts = get_font_paths()
    
    # Determine max font size for lyrics based on actual text
    text_lines = verse_text.split('\n')
    extra_space = 30  # Additional vertical space between lines
    max_bottom = int(IMAGE_HEIGHT * 0.94)  # Leave buffer to avoid bottom 5%
    available_height = max_bottom - 250  # From y=250 to max_bottom
    lyrics_font_size = get_max_font_size(draw, text_lines, fonts['regular'], IMAGE_WIDTH - 100, available_height, extra_space)
    title_font_size = TITLE_FONT_SIZE
    
    # Fonts
    try:
        if fonts['bold']:
            title_font = ImageFont.truetype(fonts['bold'], title_font_size)
        elif fonts['regular']:
            title_font = ImageFont.truetype(fonts['regular'], title_font_size)  # Fallback to regular
        else:
            title_font = ImageFont.load_default()
        
        if fonts['regular']:
            lyrics_font = ImageFont.truetype(fonts['regular'], lyrics_font_size)
        else:
            lyrics_font = ImageFont.load_default()
    except:
        title_font = ImageFont.load_default()
        lyrics_font = ImageFont.load_default()
    
    # For macOS, use index for bold if available
    if platform.system() == 'Darwin' and fonts['bold'] and 'Helvetica' in fonts['bold']:
        try:
            title_font = ImageFont.truetype(fonts['bold'], title_font_size, index=1)  # Bold index
        except:
            pass  # Keep as is
    
    # Title with percentage and verse if multiple
    full_title = song_title
    if has_multiple:
        full_title += f" - Verse {verse_number}"
    full_title += f" - {percentage}% removed"
    title_bbox = draw.textbbox((0, 0), full_title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (IMAGE_WIDTH - title_width) // 2
    draw.text((title_x, 50), full_title, fill=(0, 0, 255), font=title_font)
    
    # Lyrics
    y = 250
    for line in verse_text.split('\n'):
        draw.text((50, y), line, fill=(0, 0, 255), font=lyrics_font)
        bbox = draw.textbbox((0, 0), line, font=lyrics_font)
        line_height = bbox[3] - bbox[1]
        y += line_height + extra_space
    
    img.save(output_path)
    
    # Unit tests
    check_image_fill(output_path, verse_text)
    check_bottom_overflow(output_path, verse_text)

def main():
    input_dir = 'input'
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.txt'):
            song_title = file_name[:-4]  # Remove .txt
            song_folder = os.path.join(output_dir, song_title)
            os.makedirs(song_folder, exist_ok=True)
            file_path = os.path.join(input_dir, file_name)
            verses = parse_verses(file_path)
            
            has_multiple = len(verses) > 1
            for verse_idx, verse in enumerate(verses):
                verse_number = verse_idx + 1
                for percentage in range(0, 101, 25):
                    modified_verse = process_verse(verse, percentage)
                    output_file = f"{percentage}%_verse{verse_number}_{song_title}.png"
                    output_path = os.path.join(song_folder, output_file)
                    generate_image(song_title, modified_verse, percentage, output_path, has_multiple, verse_number)
                    print(f"Generated {output_file}")

if __name__ == "__main__":
    main()