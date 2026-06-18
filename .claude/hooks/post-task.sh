#!/bin/bash
# Claude Code hook: runs after task completion
# Logs structured data about what happened

HOOK_NAME="post-task"
LOG_DIR=".claude/logs"

mkdir -p "$LOG_DIR"

if [ -n "$CLAUDE_TASK_RESULT" ]; then
    LOG_FILE="$LOG_DIR/task_$(date +%Y%m%d_%H%M%S).json"
    echo "$CLAUDE_TASK_RESULT" > "$LOG_FILE"
    echo "[$HOOK_NAME] ✅ Task log saved: $LOG_FILE"
else
    echo "[$HOOK_NAME] No task result to log"
fi

exit 0
