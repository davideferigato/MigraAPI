#!/bin/bash
# Claude Code hook: runs before Claude edits any file
# Creates a backup of the file in .claude/backups/

HOOK_NAME="pre-edit"
BACKUP_DIR=".claude/backups"

if [ -z "$CLAUDE_FILE_PATH" ]; then
    echo "[$HOOK_NAME] No file path provided, skipping backup"
    exit 0
fi

mkdir -p "$BACKUP_DIR"

# Create backup with timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/$(basename "$CLAUDE_FILE_PATH").$TIMESTAMP.bak"

if [ -f "$CLAUDE_FILE_PATH" ]; then
    cp "$CLAUDE_FILE_PATH" "$BACKUP_FILE"
    echo "[$HOOK_NAME] ✅ Backup created: $BACKUP_FILE"
else
    echo "[$HOOK_NAME] ⚠️ File does not exist, no backup created"
fi

exit 0
