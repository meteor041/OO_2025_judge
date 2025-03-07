#!/bin/bash

# 定义变量
SCRIPT_PATH="run2.py"
DEST_DIR="/root/OO_2025_judge/src/dest"
LOG_DIR="/root/OO_2025_judge/src/log"
TIMEOUT=30  # 5分钟
INTERVAL=60  # 10分钟
COUNTER_FILE="/root/OO_2025_judge/src/log/counter.txt"

# 初始化计数器
if [ -f "$COUNTER_FILE" ]; then
    COUNTER=$(cat "$COUNTER_FILE")
else
    COUNTER=0
fi

# 执行Python脚本，并设置超时
timeout $TIMEOUT python3 "$SCRIPT_PATH"
EXIT_STATUS=$?

# 检查执行状态
if [ $EXIT_STATUS -eq 0 ]; then
    COUNTER=$((COUNTER + 1))
    echo "$(date): Script executed successfully." > "$LOG_DIR/log $COUNTER_$(date)"
    mv "/root/OO_2025_judge/src/output/output.txt" "$DEST_DIR/output $COUNTER_$(date).txt"
    mv "/root/OO_2025_judge/src/output/input.txt" "$DEST_DIR/input $COUNTER_$(date).txt"
    echo "$COUNTER" > "$COUNTER_FILE"
elif [ $EXIT_STATUS -eq 124 ]; then
    echo "$(date): Script execution timed out." > "$LOG_DIR/log $COUNTER_$(date)"
else
    echo "$(date): Script execution failed with exit status $EXIT_STATUS." > "$LOG_DIR/log $COUNTER_$(date)"
fi
