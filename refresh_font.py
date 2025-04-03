'''
Refresh ./app/font.py to apply all fonts found in ./app/fonts/
'''

import os
from kivy.logger import Logger
from pathlib import Path

APP_DIR = Path("app/")  # Dossier `app/`
FONT_DIR = APP_DIR / "fonts"  # Dossier des polices
OUTPUT_FILE = FONT_DIR / "font.py"  # Nom du fichier généré

class FontGenerator:
    """
    Generates a Font class with attributes for each font found in the `fonts/` directory.
    """
    @staticmethod
    def generate_font_class():
        if not FONT_DIR.exists():
            Logger.error(f"FontLoader: Font directory '{FONT_DIR}' does not exist.")
            return

        font_attributes = []
        Logger.info("FontLoader: Scanning for font files...")
        
        for root, _, files in os.walk(FONT_DIR):
            for file in files:
                if file.endswith(".ttf"):
                    full_path = Path(root) / file
                    font_name = os.path.splitext(file)[0].replace("-", "_").replace(" ", "_")
                    font_attributes.append(f"    {font_name} = \"{full_path.as_posix()}\"")
                    Logger.info(f"FontLoader: Found font: {file} -> {full_path.as_posix()}")
        
        class_content = """class Font:
    '''
    Contains all fonts found in the `fonts/` directory.
    Fonts are accessible via `Font.FontName`.
    '''
""" + "\n".join(font_attributes)
        
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(class_content)
        Logger.info(f"FontLoader: Font class successfully generated in {OUTPUT_FILE}")

# Run the generator
if __name__ == "__main__":
    FontGenerator.generate_font_class()