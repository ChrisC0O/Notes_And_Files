### Create .exe with PyInstaller:
```ps1
pyinstaller -F .\SCRIPT.py --onefile
```
If using [Alive-Progress](https://pypi.org/project/alive-progress/):
```ps1
pyinstaller -F --collect-data grapheme .\SCRIPT.py --onefile
```
Use --windowed to hide the terminal
```ps1
pyinstaller --onefile --windowed your_script.py
```



### URL encode with urllib:
```py
import urllib.parse

print(urllib.parse.quote("http://www.sample.com/", safe=""))
```


### Get Unix time stamp:
```py
import time

time.time()
```

### F-String formatting:
```py
part_type = "Engine"
print(f"{part_type:<30}")  # Left-align, spaces: 'Engine                         '
print(f"{part_type:>30}")  # Right-align, spaces: '                         Engine'
print(f"{part_type:^30}")  # Center-align, spaces: '            Engine             '
print(f"{part_type:.<30}") # Left-align, dots: 'Engine.........................'
print(f"{part_type:*^30}") # Center-align, asterisks: '************Engine************'
```

### Basic Config File Example using configparser

```py
"""
Basic Config File Example using configparser
--------------------------------------------

This script demonstrates how to:
1. Load an INI config file.
2. Read values from it.
3. Update values.
4. Save changes back to disk.

INI files are simple text files with sections and key-value pairs.
They are human-readable and easy to edit manually.

Example config.ini content:

[settings]
last_portfolio_id = 123456
username = Chris
"""

import configparser

# 1️⃣ Specify the config file path
CONFIG_FILE = "config.ini"

# 2️⃣ Create a ConfigParser object
config = configparser.ConfigParser()

# 3️⃣ Load the config file (does nothing if file doesn't exist yet)
config.read(CONFIG_FILE)

# 4️⃣ Ensure the section exists
if "settings" not in config:
    config["settings"] = {}  # create an empty section if missing

# 5️⃣ Read values safely with defaults
# getint returns an integer; default=0 if the key doesn't exist
last_id = config["settings"].getint("last_portfolio_id", 0)
print(f"Last portfolio ID: {last_id}")

# You can also get strings (default empty string)
username = config["settings"].get("username", "")
print(f"Username: {username}")

# 6️⃣ Update or add values
config["settings"]["last_portfolio_id"] = str(last_id + 1)
config["settings"]["username"] = "ChrisUpdated"

# 7️⃣ Save changes back to the INI file
with open(CONFIG_FILE, "w") as f:
    config.write(f)

print("Config file updated successfully!")
```

Helper class
```py
import configparser
import os

class ConfigManager:
    def __init__(self, file_path="config.ini", default_section="settings"):
        self.file_path = file_path
        self.section = default_section
        self.config = configparser.ConfigParser()
        
        # Load existing file if present
        if os.path.exists(self.file_path):
            self.config.read(self.file_path)
        
        # Ensure section exists
        if self.section not in self.config:
            self.config[self.section] = {}

    def get(self, key, default=None, value_type=str):
        """Get a value from the config, with optional type conversion."""
        if key not in self.config[self.section]:
            return default
        value = self.config[self.section][key]
        try:
            if value_type == int:
                return int(value)
            elif value_type == float:
                return float(value)
            elif value_type == bool:
                return self.config[self.section].getboolean(key)
            return value  # default str
        except ValueError:
            return default

    def set(self, key, value):
        """Set a value and save immediately."""
        self.config[self.section][key] = str(value)
        self._save()

    def _save(self):
        """Write the config back to the file."""
        with open(self.file_path, "w") as f:
            self.config.write(f)

# -----------------------------
# Example usage
# -----------------------------
if __name__ == "__main__":
    cfg = ConfigManager()

    # Get existing value or default
    last_id = cfg.get("last_portfolio_id", 0, int)
    print(f"Last portfolio ID: {last_id}")

    # Update value
    cfg.set("last_portfolio_id", last_id + 1)
    cfg.set("username", "ChrisUpdated")

    # Get updated value
    print(f"Updated last ID: {cfg.get('last_portfolio_id', 0, int)}")

```
