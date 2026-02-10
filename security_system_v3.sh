#!/bin/bash
# OpenClaw Security System v3.0 - Vulnerability Scanner Edition

echo "🛡️  OpenClaw Security System v3.0"
echo "=================================="
echo ""
echo "   Vulnerability Scanner with CWE Classification"
echo ""

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

# v3.0 Vulnerability Scanner
scan_vuln() {
    local path="$1"
    if [ -z "$path" ]; then
        echo "Usage: scan_vuln <path>"
        return 1
    fi
    echo ""
    print_status "Vulnerability scan (v3.0): $path"
    echo ""
    node /home/admin/.openclaw/workspace/package_security_scanner_v3.js "$path"
}

# v2.0 Enhanced Scanner
scan_enhanced() {
    local path="$1"
    echo ""
    print_status "Enhanced scan (v2.0): $path"
    node /home/admin/.openclaw/workspace/package_security_scanner_v2.js "$path"
}

# ClawHub skill scanner
scan_skill() {
    local slug="$1"
    if [ -z "$slug" ]; then
        echo "Usage: scan_skill <slug>"
        return 1
    fi
    echo ""
    print_status "ClawHub skill scan: $slug"
    node /home/admin/.openclaw/workspace/skill_security_scanner.js "scan" "$slug"
}

# View vulnerability logs
view_logs() {
    echo ""
    print_status "Vulnerability Scan Logs"
    echo "========================="
    echo ""
    ls -lt /home/admin/.openclaw/logs/vuln_scan_*.json 2>/dev/null | head -10 | while read line; do
        echo "   $line"
    done
    echo ""
    tail -10 /home/admin/.openclaw/logs/vulnerability_scans.log 2>/dev/null || echo "   No vulnerability scans yet"
}

# Show version and features
version() {
    cat << 'EOF'
🛡️  OpenClaw Security System v3.0
==================================

📦 Vulnerability Scanner Features:
   ✅ CWE-79 (XSS) - Cross-Site Scripting
   ✅ CWE-89 (SQLi) - SQL Injection
   ✅ CWE-200 (Secrets) - Sensitive Data Exposure
   ✅ CWE-94 (Code Injection) - Code Injection
   ✅ CWE-915 (ProtoPollution) - Prototype Pollution
   ✅ CWE-78 (CmdInjection) - Command Injection
   ✅ CWE-506 (CryptoMining) - Cryptocurrency Mining
   
🔍 Detection Methods:
   - Pattern matching
   - CWE classification
   - Risk scoring
   - Typosquatting detection
   
📊 Vulnerability Database:
   - XSS patterns: 4
   - SQLi patterns: 4
   - Code injection: 3
   - Secrets detection: 5
   - Crypto mining: 4
   
🛡️  Protection Levels:
   CRITICAL: Block immediately
   HIGH: Require review
   MEDIUM: Caution advised
   LOW/INFO: Acceptable

EOF
}

# Help
help() {
    cat << 'EOF'
🛡️  OpenClaw Security System v3.0

Usage: security_v3 <command> [options]

Commands:
    scan_vuln <path>     Vulnerability scan v3.0 (recommended)
    scan_enhanced <path> Enhanced scan v2.0
    scan_skill <slug>    Scan ClawHub skill
    logs                 View vulnerability logs
    version              Show version and features
    help                 Show this help

Vulnerability Categories (CWE):
    CWE-79   XSS              CWE-89   SQL Injection
    CWE-200  Secrets          CWE-94   Code Injection
    CWE-915  Proto Pollution  CWE-78   Command Injection
    CWE-506  Crypto Mining

Examples:
    security_v3 scan_vuln /tmp/suspicious_package
    security_v3 scan_enhanced /tmp/exprss
    security_v3 scan_skill openai-whisper
    security_v3 logs

EOF
}

case "${1:-help}" in
    scan_vuln) scan_vuln "$2" ;;
    scan_enhanced) scan_enhanced "$2" ;;
    scan_skill) scan_skill "$2" ;;
    logs) view_logs ;;
    version) version ;;
    help|--help|-h) help ;;
    *) help ;;
esac
