#!/bin/bash
# ORCHESTRAI™ DriveOps Sync Agent v1.0
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
WORKSPACE="$HOME/ORCHESTRAI_v23"
LOG="$WORKSPACE/audit_logs/sync.log"
mkdir -p "$WORKSPACE/audit_logs"

find_gdrive() {
    if ls ~/Library/CloudStorage/ 2>/dev/null | grep -q "GoogleDrive"; then
        NAME=$(ls ~/Library/CloudStorage/ | grep "GoogleDrive" | head -1)
        echo "$HOME/Library/CloudStorage/$NAME/My Drive"
        return
    fi
    echo ""
}

GDRIVE=$(find_gdrive)
if [ -z "$GDRIVE" ]; then
    echo "[$TIMESTAMP] ERROR: Google Drive not found." >> "$LOG"
    exit 1
fi

DEST="$GDRIVE/ORCHESTRAI_v23"
mkdir -p "$DEST"
SYNCED=0

while IFS= read -r -d '' file; do
    rel="${file#$WORKSPACE/}"
    dst="$DEST/$rel"
    mkdir -p "$(dirname "$dst")"
    if [ ! -f "$dst" ] || [ "$file" -nt "$dst" ]; then
        cp "$file" "$dst" 2>/dev/null && SYNCED=$((SYNCED+1))
    fi
done < <(find "$WORKSPACE" -type f \( -name "*.md" -o -name "*.sh" -o -name "*.yaml" -o -name "*.txt" \) -print0)

echo "[$TIMESTAMP] Synced $SYNCED files to Google Drive." >> "$LOG"
if [ -t 1 ]; then echo "✓ Synced $SYNCED files to Google Drive"; fi
