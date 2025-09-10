#!/usr/bin/env bash
set -e

# default install location
INSTALL_DIR="$HOME/.local/share/curl-tool"
BIN_DIR="$HOME/.local/bin"

mkdir -p "$INSTALL_DIR" "$BIN_DIR"

# download curl-format.txt from GitHub
curl -s -o "$INSTALL_DIR/curl-format.txt" https://raw.githubusercontent.com/nomthaqaqane-impact/curl-timing-tool/main/curl-format.txt

# create a wrapper command
cat <<'EOF' > "$BIN_DIR/curltiming"
#!/usr/bin/env bash
curl -s -L -o /dev/null -w "@$HOME/.local/share/curl-tool/curl-format.txt" "$@"
EOF

chmod +x "$BIN_DIR/curltiming"

echo "Installed! Make sure $BIN_DIR is in your PATH, then run: curltiming <url>"
