#!/bin/bash
# OpenClaw Enhanced Security System
# Integrates malware scanning, threat detection, and package security

echo "🛡️  OpenClaw Enhanced Security System"
echo "=================================="
echo ""

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_danger() {
    echo -e "${RED}[DANGER]${NC} $1"
}

# Start security services
start_security() {
    print_status "Starting security services..."
    
    if curl -s http://localhost:3009/health > /dev/null 2>&1; then
        print_success "Security system already running on port 3009"
    else
        print_status "Starting security defense system..."
        node /home/admin/.openclaw/workspace/start_security_system.js 2>/dev/null &
        sleep 2
        
        if curl -s http://localhost:3009/health > /dev/null 2>&1; then
            print_success "Security system started on port 3009"
        else
            print_warning "Security system startup failed"
        fi
    fi
}

# Scan a local package
scan_package() {
    local package_path="$1"
    
    if [ -z "$package_path" ]; then
        echo "Usage: scan <path_or_package_name>"
        return 1
    fi
    
    echo ""
    print_status "Scanning package: $package_path"
    echo ""
    
    if [[ "$package_path" =~ ^npm: ]]; then
        node /home/admin/.openclaw/workspace/package_security_scanner.js "$package_path"
    elif [ -d "$package_path" ]; then
        node /home/admin/.openclaw/workspace/package_security_scanner.js "$package_path"
    else
        print_danger "Path not found: $package_path"
        return 1
    fi
}

# Scan clawhub skill
scan_skill() {
    local slug="$1"
    
    if [ -z "$slug" ]; then
        echo "Usage: scan_skill <skill-slug>"
        echo ""
        echo "Examples:"
        echo "  scan_skill openai-whisper"
        echo "  scan_skill blogwatcher"
        echo "  scan_skill github"
        return 1
    fi
    
    echo ""
    print_status "Scanning ClawHub skill: $slug"
    echo ""
    
    node /home/admin/.openclaw/workspace/skill_security_scanner.js "scan" "$slug"
}

# Secure install clawhub skill
install_skill() {
    local slug="$1"
    
    if [ -z "$slug" ]; then
        echo "Usage: install_skill <skill-slug>"
        echo ""
        echo "This will:"
        echo "  1. Scan the skill for malware"
        echo "  2. Download and inspect files"
        echo "  3. Ask for confirmation if risks found"
        echo "  4. Install if safe"
        return 1
    fi
    
    echo ""
    print_status "Secure install: $slug"
    echo ""
    
    node /home/admin/.openclaw/workspace/skill_security_scanner.js "install" "$slug"
}

# Pre-install security check for npm packages
pre_install_scan() {
    local package_name="$1"
    
    if [ -z "$package_name" ]; then
        echo "Usage: preinstall <package_name>"
        return 1
    fi
    
    echo ""
    print_status "Pre-installation scan for: $package_name"
    echo ""
    
    node /home/admin/.openclaw/workspace/package_security_scanner.js "npm:$package_name"
}

# Secure npm package installation
secure_install() {
    local package="$1"
    shift
    local args="$@"
    
    echo ""
    print_status "Secure installation of: $package"
    echo ""
    
    # Pre-scan
    echo "1. Pre-installation scan..."
    node /home/admin/.openclaw/workspace/package_security_scanner.js "npm:$package"
    
    local result=$?
    if [ $result -ne 0 ]; then
        print_warning "Potential security issues detected"
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_status "Installation cancelled"
            return 1
        fi
    fi
    
    # Install
    echo "2. Installing package..."
    source /home/admin/.openclaw/venv/bin/activate
    pip install $package $args
    
    print_success "Package installed: $package"
}

# View security logs
view_logs() {
    local log_dir="/home/admin/.openclaw/logs"
    
    echo ""
    print_status "Security Logs"
    echo "==============="
    echo ""
    
    if [ -d "$log_dir" ]; then
        echo "Recent package scans:"
        ls -lt "$log_dir"/scan_*.json 2>/dev/null | head -5
        
        echo ""
        echo "Recent skill scans:"
        ls -lt "$log_dir"/skill_scan_*.json 2>/dev/null | head -5
        
        echo ""
        echo "Quarantine log:"
        tail -10 "$log_dir"/quarantine.log 2>/dev/null || echo "No quarantined packages"
        
        echo ""
        echo "Skill scans log:"
        tail -10 "$log_dir"/skill_scans.log 2>/dev/null || echo "No skill scans recorded"
    else
        print_warning "Log directory not found: $log_dir"
    fi
}

# Run security audit
audit() {
    echo ""
    print_status "Running security audit..."
    echo ""
    
    echo "1. Security System Status:"
    curl -s http://localhost:3009/health 2>/dev/null | jq '.' || echo "   Security system: Not running"
    
    echo ""
    echo "2. Recent package scans:"
    ls -lt /home/admin/.openclaw/logs/scan_*.json 2>/dev/null | head -3 | while read line; do
        echo "   $line"
    done
    
    echo ""
    echo "3. Recent skill scans:"
    ls -lt /home/admin/.openclaw/logs/skill_scan_*.json 2>/dev/null | head -3 | while read line; do
        echo "   $line"
    done
    
    echo ""
    echo "4. Quarantined packages:"
    ls -lt /home/admin/.openclaw/quarantine/ 2>/dev/null | head -5 || echo "   None"
    
    echo ""
    echo "5. Vulnerabilities detected:"
    grep -r "CRITICAL\|HIGH" /home/admin/.openclaw/logs/scan_*.json 2>/dev/null | wc -l || echo "   0"
}

# Show help
help() {
    cat << 'EOF'
🛡️  OpenClaw Security Commands

Package Security:
    scan <path>              Scan local package directory
    preinstall <name>        Pre-installation npm package scan
    install <pkg>           Secure package installation

ClawHub Skill Security (NEW!):
    scan_skill <slug>       Scan skill from clawhub.com
    install_skill <slug>    Secure install skill from clawhub.com

    Examples:
        scan_skill openai-whisper     # Scan Whisper skill
        install_skill blogwatcher     # Scan then install blogwatcher
        scan_skill github             # Scan GitHub skill

System:
    start                   Start security services
    audit                   Run full security audit
    logs                    View security logs
    help                    Show this help

Integration Points:
    1. Pre-installation scanning for npm packages
    2. Pre-installation scanning for ClawHub skills
    3. Local package directory scanning
    4. Automatic quarantine of threats
    5. Complete audit trail

EOF
}

# Main
case "${1:-help}" in
    start)
        start_security
        ;;
    scan)
        scan_package "$2"
        ;;
    scan_skill)
        scan_skill "$2"
        ;;
    install_skill)
        install_skill "$2"
        ;;
    preinstall)
        pre_install_scan "$2"
        ;;
    install)
        secure_install "$2" "${@:3}"
        ;;
    audit)
        audit
        ;;
    logs)
        view_logs
        ;;
    help|--help|-h)
        help
        ;;
    *)
        help
        ;;
esac
