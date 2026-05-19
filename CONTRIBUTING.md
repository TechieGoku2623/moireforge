# Contributing to MoireQuantum Edge Processor

Thank you for your interest in contributing!

## Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd CHIP
   ```

2. **Set up environment**
   ```bash
   python scripts/setup_dev_environment.py
   pip install -r requirements.txt
   ```

3. **Run tests**
   ```bash
   make test
   ```

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to all functions/classes
- Comment complex logic

## Testing

- Write tests for new features
- Ensure all tests pass: `make test`
- Aim for >80% code coverage

## Documentation

- Update relevant docs when adding features
- Add examples for new APIs
- Keep architecture docs current

## Pull Request Process

1. Create a feature branch
2. Make your changes
3. Add tests
4. Update documentation
5. Run `make test`
6. Submit pull request

## Areas for Contribution

- Device physics models
- RTL design improvements
- Firmware features
- SDK enhancements
- Documentation
- Test coverage

---

Thank you for contributing! 🚀
