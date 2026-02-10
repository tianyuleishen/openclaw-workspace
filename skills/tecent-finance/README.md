# Tencent Finance (腾讯财经)

Get stock prices, quotes, and compare stocks using Tencent Finance API.

## Features

- ✅ No API key required
- ✅ Works in mainland China (optimized network)
- ✅ Fast & stable (no rate limits)
- ✅ Multi-market support:
  - US stocks
  - China A-Shares (A股)
  - Hong Kong stocks (港股)

## Installation

```bash
# Make executable
chmod +x skills/tecent-finance/tfin

# Run
./skills/tecent-finance/tfin sh600519    # 贵州茅台
./skills/tecent-finance/tfin sz000001    # 深证成指
./skills/tecent-finance/tfin AAPL        # Apple
```

## Usage

```bash
# Get stock quote
tfin sh600519

# Get index
tfin sh000001    # Shanghai Index
tfin sz399001    # Shenzhen Index

# Compare stocks
tfin compare sh600519 sz300364
```

## Data Sources

- Primary: Tencent Finance API (finance.qq.com)
- Backup: Sina Finance (for mainland China)

## Use Cases

- Real-time stock quotes
- Market index monitoring
- Stock comparison
- A-share analysis (optimized for China)

## References

- Tencent Finance: finance.qq.com
- API: https://qt.gtimg.cn

## License

MIT
