#!/bin/sh
set -e

echo "📦 Installing system dependencies..."
apt-get update && apt-get install -y unzip

echo "🐍 Installing Python dependencies..."
pip install requests

echo "📂 Unzipping logs..."
if [ -f "logs.zip" ]; then
    unzip -o logs.zip -d build_logs
else
    echo "❌ logs.zip not found!"
    exit 1
fi

echo "🔍 Searching for error logs..."
# Find files containing "error" (case-insensitive), take the first one
LOG_FILE=$(find build_logs -name '*.txt' -exec grep -li 'error' {} + | head -n 1)

if [ -z "$LOG_FILE" ]; then
    echo "⚠️ No log file with 'error' found. Falling back to the largest text file."
    LOG_FILE=$(find build_logs -name "*.txt" -type f -printf "%s %p\n" | sort -rn | head -n1 | cut -d" " -f2)
fi

if [ -z "$LOG_FILE" ]; then
    echo "❌ No log files found in build_logs!"
    exit 1
fi

echo "🚀 Analyzing Log File: $LOG_FILE"
python scripts/ai_rca.py \
  --logs "$LOG_FILE" \
  --output rca.md \
  --model "qwen2.5-coder:7b" \
  --endpoint "http://host.docker.internal:11434/api/generate"
