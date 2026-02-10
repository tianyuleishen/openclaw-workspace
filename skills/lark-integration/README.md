# Lark (Feishu) Integration

Connect Lark (Feishu) messaging to OpenClaw via webhook bridge.

## Features

- ✅ Bidirectional messaging (Lark ↔ OpenClaw)
- ✅ Text, rich text (post), and image support
- ✅ Document/wiki reading
- ✅ Bitable (database) operations
- ✅ Support for Lark International & China Feishu

## Quick Start

```bash
# Set credentials
export FEISHU_APP_ID=cli_xxx
export FEISHU_APP_SECRET=your_secret

# Start the bridge
cd skills/lark-integration/scripts
node bridge-webhook.mjs
```

## Usage

- **Send messages**: Configure in OpenClaw config
- **Receive messages**: Webhook bridge handles automatically
- **Read documents**: Use `feishu_doc` tool
- **Manage files**: Use `feishu_drive` tool

## Supported Operations

| Tool | Purpose |
|------|---------|
| `feishu_doc` | Read/write documents |
| `feishu_drive` | Cloud file management |
| `feishu_wiki` | Knowledge base operations |
| `feishu_bitable_*` | Database operations |

## References

- Lark International: larksuite.com
- China Feishu: feishu.cn
- OpenClaw docs: docs.openclaw.ai

## License

MIT
