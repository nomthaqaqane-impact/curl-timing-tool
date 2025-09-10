#!/usr/bin/env python3
import os
import sys
import stat
import urllib.request

# ----------------------------
# Configuration
# ----------------------------
GITHUB_RAW_URL = "https://raw.githubusercontent.com/nomthaqaqane-impact/curl-timing-tool/main/curl-format.txt"

HOME = os.path.expanduser("~")
INSTALL_DIR = os.path.join(HOME, ".local", "share", "curl-tool")
BIN_DIR = os.path.join(HOME, ".local", "bin")
WRAPPER_PATH = os.path.join(BIN_DIR, "curltiming")

# ----------------------------
# Create directories
# ----------------------------
os.makedirs(INSTALL_DIR, exist_ok=True)
os.makedirs(BIN_DIR, exist_ok=True)

# ----------------------------
# Download curl-format.txt
# ----------------------------
curl_format_path = os.path.join(INSTALL_DIR, "curl-format.txt")
try:
    print(f"Downloading curl-format.txt to {curl_format_path}...")
    urllib.request.urlretrieve(GITHUB_RAW_URL, curl_format_path)
except Exception as e:
    print(f"Error downloading curl-format.txt: {e}")
    sys.exit(1)

# ----------------------------
# Create wrapper script
# ----------------------------
wrapper_script = f"""#!/usr/bin/env bash
curl -s -L -o /dev/null -w "@{curl_format_path}" "$@"
"""

with open(WRAPPER_PATH, "w") as f:
    f.write(wrapper_script)

# Make it executable
st = os.stat(WRAPPER_PATH)
os.chmod(WRAPPER_PATH, st.st_mode | stat.S_IEXEC)

# ----------------------------
# Final message
# ----------------------------
print(f"✅ curltiming installed at {WRAPPER_PATH}!")
print("Make sure ~/.local/bin is in your PATH, then run:")
print("    curltiming <url>")
