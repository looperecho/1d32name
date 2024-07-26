import sys
import os
import json
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError
from pathlib import Path

from utils import style

# Set the directory for config file
def get_app_support_directory(app_name):
    home = Path.home()
    app_support_directory = home / "Library" / "Application Support" / app_name
    app_support_directory.mkdir(parents=True, exist_ok=True)
    return app_support_directory

# Load the config file
def load_config(config_path):
    # Prompt for config path if none exists
    if not config_path.exists():
        user_path = input("Input your path: ")
        default_config = {
            "directory": user_path
        }
        with open(config_path, 'w') as config_file:
            json.dump(default_config, config_file)
    # Attempt to read config file
    try:
        with open(config_path, 'r') as config_file:
            print(f"Config file    ▶  {style.blue(config_path)}")
            return json.load(config_file)
    except FileNotFoundError:
        file_error = f"Configuration file not found: {config_path}"
        print(style.yellow(file_error))
        return None
    except json.JSONDecodeError:
        json_error = f"Error reading the configuration file: {config_path}"
        print(style.yellow(json_error))
        return None

# Read Artist and Title tags from mp3
def get_tags(file):
    try:
        audio = EasyID3(file)
        artist_tag = audio.get("artist", [""])[0]        
        title_tag = audio.get("title", [""])[0]
        return artist_tag, title_tag
    
    except ID3NoHeaderError:
        filename = file.name
        print(f"{style.yellow('Warning: ')}No ID3 tags found for {style.bold(filename)}")

# Rename files to [Artist - Title] ID3 tags
def rename_file(file, directory):
    try:
        artist_tag, title_tag = get_tags(file)
        new_name = directory / f"{artist_tag} - {title_tag}.mp3"
        os.rename(file, new_name)
        print(f"└──── {style.blue(new_name.name)}")
    except TypeError:
        pass

# Loop dir for mp3 files, and rename
def process_files(directory):
    directory = Path(directory)
    for file in directory.glob("*.mp3"):
        print(f"\nFile: {style.dark_grey(file.name)}")
        rename_file(file, directory)


def main():
    app_name = "ID32Name"
    print(f"\n{style.bold(style.blue(app_name))}")
    
    # Set config dirs
    app_support_directory = get_app_support_directory(app_name)
    config_path = app_support_directory / "config.json"
    
    # Do config read
    config = load_config(config_path)
    directory = config["directory"]
    print(f"Source folder  ▶  {style.magenta(directory)}")
    
    # Prompt before processing
    input(f"\nHit {style.bold('Enter')} to continue...")
    process_files(directory)
    
    # Confirmation
    print(f"\n{style.green('Complete!')}")
    input("\nHit any key to exit...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting App...")
        sys.exit()
