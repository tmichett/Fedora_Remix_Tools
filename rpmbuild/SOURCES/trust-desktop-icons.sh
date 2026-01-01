#!/bin/bash
# Script to trust Fedora Remix Tools desktop icon on first login
# This runs via autostart in the user's GNOME session

DESKTOP_FILE="$HOME/Desktop/Fedora_Remix_Tools.desktop"
MARKER_FILE="$HOME/.config/fedora-remix-tools-trusted"

# Only run once
if [ -f "$MARKER_FILE" ]; then
    exit 0
fi

# Wait for GNOME Shell to be ready (check for gnome-shell process)
for i in {1..30}; do
    if pgrep -x "gnome-shell" > /dev/null 2>&1; then
        break
    fi
    sleep 1
done

# Additional wait for desktop to fully initialize
sleep 5

# Trust the desktop file if it exists
if [ -f "$DESKTOP_FILE" ]; then
    # Set executable permission
    chmod +x "$DESKTOP_FILE"
    
    # Set GNOME trusted metadata (we're in a user session so gio should work)
    gio set "$DESKTOP_FILE" metadata::trusted true 2>/dev/null
    
    # Restart nautilus to apply changes (forces desktop refresh)
    if command -v nautilus &>/dev/null; then
        nautilus -q 2>/dev/null || true
    fi
    
    # Create marker file to prevent running again
    mkdir -p "$(dirname "$MARKER_FILE")"
    touch "$MARKER_FILE"
fi

exit 0

