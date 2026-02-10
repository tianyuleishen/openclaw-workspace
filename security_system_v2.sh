#!/bin/bash
# OpenClaw Enhanced Security System - v2.0
# With improved typosquatting detection and advanced features

echo "🛡️  OpenClaw Security System v2.0"
echo "=================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

print_status() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_danger() { echo -e "${RED}[DANGER]${NC} $1"; }

# Enhanced package scanner
scan_package() {
    local path="$1"
    if [ -z "$path" ]; then
        echo "Usage: scan <path>"
        return 1
    fi
    echo ""
    print_status "Enhanced package scan: $path"
    echo ""
    node /home/admin/.openclaw/workspace/package_security_scanner_v2.js "$path"
}

# Enhanced skill scanner
scan_skill() {
    local slug="$1"
    if [ -z "$slug" ]; then
        echo "Usage: scan_skill <slug>"
        return 1
    fi
    echo ""
    print_status "ClawHub skill scan: $slug"
    echo ""
    node /home/admin/.openclaw/workspace/skill_security_scanner.js "scan" "$slug"
}

# Legacy package scanner
scan_legacy() {
    local path="$1"
    echo ""
    print_status "Legacy package scan: $path"
    echo ""
    node /home/admin/.openclaw/workspace/package_security_scanner.js "$path"
}

# View logs
view_logs() {
    local log_dir="/home/admin/.openclaw/logs"
    echo ""
    print_status "Security Logs v2.0"
    echo "==================="
    echo ""
    if [ -d "$log_dir" ]; then
        echo "Enhanced scans:"
        ls -lt "$log_dir"/enhanced_scan_*.json 2>/dev/null | head -5 | while read line; do echo "   $line"; done
        echo ""
        echo "Skill scans:"
        ls -lt "$log_dir"/skill_scan_*.json 2>/dev/null | head -5 | while read line; do echo "   $line"; done
        echo ""
        echo "Legacy scans:"
        ls -lt "$log_dir"/scan_*.json 2>/dev/null | head -5 | while read line; do echo "   $line"; done
    fi
}

# Show version
version() {
    echo ""
    echo "🛡️  OpenClaw Security System"
    echo "   Version: 2.0.0 (Enhanced)"
    echo ""
    echo "   Components:"
    echo "   - Enhanced Package Scanner v2.0"
    echo "     ✅ Typosquatting detection (Levenshtein, Jaccard, Soundex)"
    echo "     ✅ Homoglyph detection"
    echo "     ✅ 50+ signature patterns"
    echo "     ✅ Heuristic analysis"
    echo ""
    echo "   - Skill Security Scanner"
    echo "     ✅ ClawHub integration"
    echo "     ✅ File analysis"
    echo "     ✅ Owner reputation"
    echo ""
    echo "   - Legacy Package Scanner"
    echo "     ✅ Basic detection"
}

# Help
help() {
    cat << EOF
🛡️  OpenClaw Security System v2.0

Usage: security <command> [options]

Commands:
    scan <path>           Enhanced package scan (v2.0 - recommended)
    scan_legacy <path>    Legacy package scan (v1.0)
    scan_skill <slug>     Scan ClawHub skill
    logs                  View security logs
    version               Show version info
    help                  Show this help

Enhanced Features (v2.0):
    ✅ Typosquatting detection
       - Levenshtein distance
       - Jaccard similarity (n-gram)
       - Soundex phonetic matching
       - Homoglyph detection
    
    ✅ Advanced heuristics
       - Crypto mining detection
       - Ransomware patterns
       - Obfuscation analysis
       - Shell injection detection
    
    ✅ 50+ signature patterns
       - Process operations
       - File system operations
       - Network operations
       - Environment access

Examples:
    security scan ./suspicious_package
    security scan /tmp/exprss
    security scan_skill openai-whisper
    security logs

EOF
}

case "${1:-help}" in
    scan) scan_package "$2" ;;
    scan_legacy) scan_legacy "$2" ;;
    scan_skill) scan_skill "$2" ;;
    logs) view_logs ;;
    version) version ;;
    help|--help|-h) help ;;
    *) help ;;
esac

