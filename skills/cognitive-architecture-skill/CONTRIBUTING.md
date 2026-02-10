# Contributing to Cognitive Architecture Skill

Thank you for your interest in contributing to the Cognitive Architecture Skill for OpenClaw! We appreciate your help in making this project better.

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md) to ensure a welcoming environment for everyone.

## How Can I Contribute?

### Reporting Bugs

- Check the [Issues](https://github.com/tianyuleishen/cognitive-architecture-skill/issues) to see if the bug has already been reported
- Use a clear and descriptive title
- Include as much information as possible:
  - OpenClaw version
  - Node.js version
  - Steps to reproduce
  - Expected behavior
  - Actual behavior
  - Console logs if applicable

### Suggesting Features

- Check the [Issues](https://github.com/tianyuleishen/cognitive-architecture-skill/issues) to see if the feature has already been suggested
- Explain why this feature would be useful
- Describe the desired behavior
- Provide examples if possible

### Improving Documentation

- Fix typos or unclear descriptions
- Add examples or tutorials
- Improve existing documentation
- Translate documentation to other languages

### Submitting Changes

#### Prerequisites

- Node.js 18+
- OpenClaw 2.0+
- Git

#### Setting Up Your Environment

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/cognitive-architecture-skill.git
   cd cognitive-architecture-skill
   ```
3. Create a branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

#### Making Changes

1. Make sure your code follows the project's style guidelines
2. Add tests if applicable
3. Ensure all tests pass
4. Update documentation if needed

#### Testing Your Changes

```bash
# Run the demo to test functionality
node examples/demo.js

# Test individual components
node -e "
const MemorySystem = require('./memory_system');
const ms = new MemorySystem();
ms.storeLongTerm('test', 'value');
console.log(ms.retrieve('test'));
"
```

#### Submitting a Pull Request

1. Commit your changes with a clear message:
   ```bash
   git add .
   git commit -m "Add feature: description of your feature"
   ```
2. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
3. Open a Pull Request on GitHub
4. Fill out the PR template completely
5. Wait for review and address feedback

## Development Guidelines

### Code Style

- Use clear, descriptive variable and function names
- Write JSDoc comments for all public functions
- Follow existing code patterns in the project
- Use consistent indentation (2 spaces)

### File Structure

```
cognitive-architecture-skill/
├── SKILL.md              # Skill definition
├── memory_system.js      # Memory management
├── reasoning_engine.js   # Reasoning engine
├── coordination_system.js # Coordination system
├── examples/
│   └── demo.js          # Example usage
├── README.md            # Main documentation
├── LICENSE              # License information
├── CONTRIBUTING.md      # Contribution guide
├── CODE_OF_CONDUCT.md   # Code of conduct
└── package.json         # Package information (optional)
```

### Testing

All new features and bug fixes should include appropriate tests. Run the demo to verify functionality:

```bash
node examples/demo.js
```

### Documentation

- Update the README if you change functionality
- Add JSDoc comments to new functions
- Include examples where appropriate

## Questions?

If you have any questions, feel free to open an issue or reach out to the maintainers.

Thank you for contributing!