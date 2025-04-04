import os
import re
from pathlib import Path
from kivy.logger import Logger

# Define the log directory
LOG_DIR = Path.home() / ".kivy" / "logs"

Logger.info(f"LogCleaner: Removing oldest logs files...")

# Regular expression to extract the date and occurrence from files named kivy_YY-MM-DD_N.txt
log_pattern = re.compile(r"kivy_(\d{2})-(\d{2})-(\d{2})_(\d+)\.txt")

# List and filter files matching the pattern, storing:
# - The path to the file
# - A Tuple (year, month, day)
# - The occurrence number as an integer
log_files = [
    (file, tuple(map(int, match.groups()[0:3])), int(match.group(4)))
    for file in LOG_DIR.glob("kivy_*.txt")
    if (match := log_pattern.match(file.name))
]

for file, _, _ in log_files:
    try:
        os.remove(file)
        Logger.info(f"LogCleaner: Deleted: {file}")
    except Exception as e:
        Logger.error(f"LogCleaner: Error deleting {file}: {e}")