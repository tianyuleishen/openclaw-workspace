#!/bin/bash
# OpenClaw Hybrid Security System - Phase 1 & 2
# Based on Shannon AI Hacker Architecture

echo "🛡️  OpenClaw Hybrid Security System v2.0"
echo "=========================================="
echo "   Multi-Agent Architecture with CWE Classification"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

print_status() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_danger() { echo -e "${RED}[DANGER]${NC} $1"; }

# Scan with hybrid scanner
scan() {
    local path="$1"
    if [ -z "$path" ]; then
        echo "Usage: hybrid_scan <path>"
        return 1
    fi
    echo ""
    print_status "Hybrid security scan: $path"
    echo ""
    node /home/admin/.openclaw/workspace/hybrid_security_scanner.js "$path"
}

# View reports
reports() {
    echo ""
    print_status "Hybrid Scan Reports"
    echo "====================="
    echo ""
    ls -lt /home/admin/.openclaw/logs/hybrid_scan_*.json 2>/dev/null | head -10 | while read line; do
        echo "   $line"
    done
    echo ""
    tail -15 /home/admin/.openclaw/logs/hybrid_scans.log 2>/dev/null || echo "   No reports yet"
}

# Show features
features() {
    cat << 'EOF'
🛡️  Hybrid Security System Features
===================================

🤖 Multi-Agent Architecture (Shannon-inspired):
   ✅ Recon Agent - Package structure analysis
   ✅ Analysis Agent - Parallel vulnerability scanning
   ✅ Report Agent - Professional security reports

📊 CWE Classification:
   ✅ 12 vulnerability categories
   ✅ 25+ detection patterns
   ✅ Risk prioritization
   ✅ Professional reporting

🔍 Detection Coverage:
   Injection (CWE-78, CWE-89)
   XSS (CWE-79)
   Code Injection (CWE-94)
   Sensitive Data (CWE-200, CWE-259)
   File Operations (CWE-22, CWE-73)
   Prototype Pollution (CWE-915)
   Malware (CWE-506)
   Path Traversal (CWE-22)

📈 Risk Assessment:
   Critical: Block immediately
   High: Require review
   Medium: Caution advised
   Low: Acceptable

EOF
}

# Help
help() {
    cat << 'EOF'
🛡️  OpenClaw Hybrid Security System

Usage: hybrid_system <command> [options]

Commands:
    scan <path>     Run hybrid security scan
    reports         View recent scan reports
    features        Show system features
    help            Show this help

Examples:
    hybrid_system scan /tmp/suspicious_package
    hybrid_system reports

Notes:
    - Uses Shannon-inspired multi-agent architecture
    - Classifies vulnerabilities using CWE taxonomy
    - Provides risk prioritization
    - Generates professional security reports

EOF
}

case "${1:-help}" in
    scan) scan "$2" ;;
    reports) reports ;;
    features) features ;;
    help|--help|-h) help ;;
    *) help ;;
esac
