# Cognitive Architecture Skill - Migration System

This directory contains the migration and upgrade utilities for the Cognitive Architecture Skill, ensuring memory documents and data are preserved during upgrades.

## Overview

The migration system provides:

- **Automatic backups** before performing upgrades
- **Memory preservation** during version updates
- **Safe rollback** capabilities
- **Version compatibility** management
- **Data format migration** tools

## Components

### 1. Migration System (`migrate.js`)

Handles the migration of data from one version to another, preserving memory structures and converting formats as needed.

### 2. Backup Utility (`backup_util.js`)

Provides comprehensive backup and restore functionality for cognitive data.

### 3. Upgrade Script (`upgrade.js`)

Manages the complete upgrade process with safety checks and verification.

## Usage

### Checking for Updates

```bash
node migration/upgrade.js check
```

### Performing a Dry Run

```bash
node migration/upgrade.js dry-run
```

### Creating a Backup

```bash
node migration/backup_util.js create "Backup before upgrade"
```

### Listing Available Backups

```bash
node migration/backup_util.js list
```

### Performing an Upgrade

```bash
node migration/upgrade.js upgrade [version]
```

### Rolling Back

```bash
node migration/upgrade.js rollback <backup-name>
```

## Safety Features

- **Automatic backups** before any upgrade
- **Memory preservation** - all memory documents are retained
- **Verification checks** after upgrade completion
- **Rollback capability** if upgrade fails
- **Version tracking** for audit purposes

## Data Preservation

The system specifically preserves:

- **Memory data** - All short-term, long-term, episodic, semantic, and procedural memories
- **Configuration settings** - Custom configurations and preferences
- **Version history** - Complete upgrade history for troubleshooting

## Integration with OpenClaw

The migration system is designed to work seamlessly with OpenClaw's skill management system and follows OpenClaw's safety and security guidelines.