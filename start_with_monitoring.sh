#!/bin/bash
# OpenClaw Enhanced Startup Script
# Starts OpenClaw with enhanced logging and monitoring

LOG_DIR="/home/admin/.openclaw/logs"
BACKUP_DIR="/home/admin/.openclaw/logs/archive"
MAX_LOG_AGE=7  # days

echo "🚀 OpenClaw Enhanced Startup"
echo "=========================="
echo ""

# Create log directories
mkdir -p "$LOG_DIR"
mkdir -p "$BACKUP_DIR"

# Rotate old logs if too large
if [ $(ls "$LOG_DIR"/*.log 2>/dev/null | wc -l) -gt 10 ]; then
    echo "📦 Rotating old logs..."
    for logfile in $(ls -t "$LOG_DIR"/*.log 2>/dev/null | tail -n +5); do
        mv "$logfile" "$BACKUP_DIR/" 2>/dev/null
        gzip "$BACKUP_DIR/$(basename $logfile)" 2>/dev/null
    done
fi

# Clean old logs
find "$LOG_DIR" -name "*.gz" -mtime +$MAX_LOG_AGE -delete 2>/dev/null
find "$LOG_DIR" -name "*.log" -mtime +$MAX_LOG_AGE -delete 2>/dev/null

echo "📁 Log directory: $LOG_DIR"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down..."
    if [ ! -z "$LOG_PID" ]; then
        kill $LOG_PID 2>/dev/null
    fi
    if [ ! -z "$MONITOR_PID" ]; then
        kill $MONITOR_PID 2>/dev/null
    fi
    echo "✅ Cleanup complete"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start enhanced logging system
echo "📝 Starting enhanced logging system..."
node /home/admin/.openclaw/workspace/enhanced_logging.js "$LOG_DIR" &
LOG_PID=$!
echo "   Logging PID: $LOG_PID"

# Start system monitor
echo ""
echo "🛡️  Starting system monitor..."
node /home/admin/.openclaw/workspace/system_monitor.js "/home/admin/.openclaw" "$LOG_DIR" &
MONITOR_PID=$!
echo "   Monitor PID: $MONITOR_PID"

# Wait a moment for services to initialize
sleep 2

# Start OpenClaw gateway
echo ""
echo "🔌 Starting OpenClaw gateway..."
cd /home/admin/.openclaw
openclaw gateway start

# Keep script running
echo ""
echo "✅ All services started"
echo "   - Enhanced Logging: PID $LOG_PID"
echo "   - System Monitor: PID $MONITOR_PID"
echo ""
echo "📊 Health Check: http://localhost:3008"
echo "📁 Logs: $LOG_DIR"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait indefinitely
wait
