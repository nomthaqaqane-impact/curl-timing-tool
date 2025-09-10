#!/usr/bin/env python3
import os
import stat
import sys

# ----------------------------
# Configuration
# ----------------------------
GITHUB_RAW_URL = "https://raw.githubusercontent.com/nomthaqaqane-impact/curl-timing-tool/main/curl-format.txt"

HOME = os.path.expanduser("~")
INSTALL_DIR = os.path.join(HOME, ".local", "share", "curl-tool")
BIN_DIR = os.path.join(HOME, ".local", "bin")
WRAPPER_PATH = os.path.join(BIN_DIR, "curltiming")

SHELL_RC_FILES = ["~/.zshrc", "~/.bashrc", "~/.profile"]  # Try these for PATH export

# ----------------------------
# Create directories
# ----------------------------
os.makedirs(INSTALL_DIR, exist_ok=True)
os.makedirs(BIN_DIR, exist_ok=True)

# ----------------------------
# Download curl-format.txt using curl
# ----------------------------
curl_format_path = os.path.join(INSTALL_DIR, "curl-format.txt")
print(f"Downloading curl-format.txt to {curl_format_path}...")
download_cmd = f'curl -fsSL -o "{curl_format_path}" "{GITHUB_RAW_URL}"'
result = os.system(download_cmd)
if result != 0:
    print("❌ Error downloading curl-format.txt. Make sure curl is installed and internet is working.")
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
# Add ~/.local/bin to PATH automatically
# ----------------------------
added_path = False
export_line = f'\nexport PATH="$HOME/.local/bin:$PATH"\n'

for rc_file in SHELL_RC_FILES:
    rc_file_expanded = os.path.expanduser(rc_file)
    if os.path.exists(rc_file_expanded):
        with open(rc_file_expanded, "r") as f:
            content = f.read()
        if "$HOME/.local/bin" not in content:
            with open(rc_file_expanded, "a") as f:
                f.write(export_line)
            added_path = True

# ----------------------------
# Final message
# ----------------------------
print(f"\n✅ curltiming installed at {WRAPPER_PATH}!")

if added_path:
    print("Added ~/.local/bin to your PATH in your shell configuration.")
    print("Reload your terminal or run `source ~/.zshrc` (or equivalent) to update PATH.")
else:
    print("~/.local/bin is already in your PATH.")

print("\nRun your first command:")
print("    curltiming <url>")
