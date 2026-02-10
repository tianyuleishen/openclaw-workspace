# Installation Guide for Cognitive Architecture Skill

## Prerequisites

- OpenClaw v2.0 or higher
- Node.js 18 or higher
- npm or yarn package manager

## Installation Methods

### Method 1: Via ClawHub (Recommended)

The easiest way to install the Cognitive Architecture Skill is through ClawHub:

```bash
# Make sure you're in your OpenClaw workspace
cd ~/.openclaw/workspace

# Install the skill via ClawHub
clawhub install cognitive-architecture
```

### Method 2: Manual Installation

If you prefer manual installation:

1. Navigate to your OpenClaw skills directory:
   ```bash
   cd ~/.openclaw/workspace/skills
   ```

2. Clone the repository:
   ```bash
   git clone https://github.com/tianyuleishen/cognitive-architecture-skill.git cognitive-architecture
   ```

3. Verify the installation:
   ```bash
   ls -la cognitive-architecture/
   ```
   
   You should see the following files:
   - `SKILL.md`
   - `memory_system.js`
   - `reasoning_engine.js`
   - `coordination_system.js`
   - `examples/` directory

### Method 3: Direct Download

If you don't have git available, you can download and extract the files:

1. Download the latest release from GitHub
2. Extract the archive
3. Rename the extracted folder to `cognitive-architecture`
4. Move it to `~/.openclaw/workspace/skills/`

## Verification

After installation, verify that the skill is properly recognized:

1. Restart your OpenClaw gateway:
   ```bash
   openclaw gateway restart
   ```

2. Test the installation by running the demo:
   ```bash
   cd ~/.openclaw/workspace/skills/cognitive-architecture
   node examples/demo.js
   ```

3. You should see output confirming all cognitive architecture components are working.

## Configuration

The skill works out-of-the-box with no special configuration required. However, you can customize behavior by modifying the JavaScript instantiation parameters in your agent code:

```javascript
// Example customization
const memorySystem = new MemorySystem({
  shortTermTTL: 300000,      // 5 minutes for short-term memory items
  maxEpisodicSize: 1000,     // Maximum number of episodic memories to retain
});

const coordinationSystem = new CoordinationSystem({
  taskTimeout: 300000,       // 5 minutes before considering a task timed out
  maxMessageHistory: 1000,   // Maximum number of messages to keep in history
});
```

## Updating

To update to the latest version:

### Via ClawHub:
```bash
clawhub update cognitive-architecture
```

### Manual Update:
```bash
cd ~/.openclaw/workspace/skills/cognitive-architecture
git pull origin main
```

## Migration and Upgrade Safety

The cognitive architecture skill includes a comprehensive migration system that ensures your memory documents and data are preserved during upgrades. The system automatically creates backups before any upgrade and provides rollback capabilities if needed.

### Migration Features:
- Automatic backup before upgrades
- Memory preservation during version updates
- Safe rollback to previous versions
- Version compatibility management

For detailed upgrade instructions, see the [Migration System Documentation](migration/README.md).

## Troubleshooting

### Common Issues:

1. **Skill not recognized**: Make sure the skill folder is in the correct location (`~/.openclaw/workspace/skills/cognitive-architecture/`)

2. **Module not found**: Verify all required files are present in the skill directory

3. **Permission errors**: Ensure you have read/write permissions to the skills directory

4. **Demo not running**: Check that you're running Node.js 18 or higher

### Getting Help:

- Check the OpenClaw documentation: https://docs.openclaw.ai
- Visit our GitHub issues: https://github.com/tianyuleishen/cognitive-architecture-skill/issues
- Join the OpenClaw Discord: https://discord.gg/clawd

## Next Steps

Once installed, you can:
- Explore the examples in the `examples/` directory
- Integrate cognitive components into your agents
- Refer to the main README for usage instructions
- Join the community to share your experiences