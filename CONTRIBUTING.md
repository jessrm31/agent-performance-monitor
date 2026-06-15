# 🤝 Contributing to Agent Performance Monitor

Thanks for your interest in contributing to Agent Performance Monitor! We welcome contributions from everyone.

## Code of Conduct

Please be respectful and constructive in all interactions.

## Getting Started

### Prerequisites

- Python 3.9+
- Git
- pip or Poetry
- Docker (optional)

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/jessrm31/agent-performance-monitor.git
cd agent-performance-monitor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Run migrations
alembic upgrade head
```

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation
- `test/` - Test improvements
- `refactor/` - Code refactoring
- `perf/` - Performance improvements

### 2. Make Changes

**Code Style:**

```bash
# Format code
black backend/ sdk/ cli/
isort backend/ sdk/ cli/

# Check for issues
flake8 backend/ sdk/ cli/
mypy backend/ sdk/ cli/
pylint backend/ sdk/ cli/
```

**Security Checklist:**

- [ ] No secrets or credentials in code
- [ ] All user input validated
- [ ] No hardcoded API keys
- [ ] Error messages don't leak sensitive info
- [ ] Logging excludes secrets
- [ ] Dependencies checked with `safety check`

### 3. Write Tests

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=backend --cov-report=html

# Run specific test
pytest tests/test_api.py::test_something

# Run integration tests only
pytest -m integration
```

**Test Coverage:**
- Aim for minimum 80% code coverage
- Add tests for new features
- Include edge cases and error scenarios

### 4. Commit Changes

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "feature: Add performance metrics dashboard"
```

Commit message format:
```
<type>: <subject>

<body>

<footer>
```

Types:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Code style (formatting, missing semicolons, etc.)
- `refactor:` Code refactoring
- `perf:` Performance improvements
- `test:` Test improvements
- `chore:` Build, dependencies, etc.

Example:
```
feat: Add token consumption metrics

Implement new metrics endpoint to track token consumption per agent
and per tool. Includes:
- New AgentMetrics model
- GET /api/v1/metrics/tokens endpoint
- Unit and integration tests

Closes #42
```

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear title describing the change
- Description of what changed and why
- Related issues (use `Closes #issue-number`)
- Screenshots or demo videos if applicable

## Pull Request Guidelines

### Before Submitting

- [ ] Code follows style guidelines
- [ ] All tests pass locally
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] No secrets in code
- [ ] Commit messages are clear
- [ ] No unnecessary dependencies added

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issues
Closes #issue-number

## Testing
Describe testing performed

## Screenshots (if applicable)
Add screenshots or demos

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No security issues
- [ ] No new warnings
```

## Code Review Process

1. **Automated Checks**: GitHub Actions will run tests, linting, and security scans
2. **Code Review**: Maintainers will review code
3. **Feedback**: Address any requested changes
4. **Merge**: Once approved, maintainers will merge

## Documentation

### Types of Documentation

1. **README**: High-level overview and quick start
2. **API Docs**: Endpoint documentation
3. **User Guides**: How to use features
4. **Architecture Docs**: System design and decisions
5. **Code Comments**: Explain complex logic

### Writing Documentation

```markdown
# Feature Name

## Overview
Brief description of the feature

## Configuration
How to configure

## Usage
How to use it

## Examples
Code examples

## Troubleshooting
Common issues and solutions
```

## Security Considerations

See [SECURITY.md](SECURITY.md) for detailed security guidelines.

**Key Points:**
- Never commit secrets
- Validate all user input
- Use parameterized queries
- Hash passwords appropriately
- Log without exposing secrets
- Keep dependencies updated

## Performance Considerations

- Profile code for bottlenecks
- Optimize database queries
- Use pagination for large datasets
- Implement caching where appropriate
- Monitor memory usage

## Common Issues

### Tests Failing

```bash
# Clear cache and reinstall
rm -rf __pycache__ .pytest_cache
pip install -r requirements.txt
pytest
```

### Import Errors

```bash
# Reinstall in development mode
pip install -e .
```

### Database Issues

```bash
# Reset database
rm apm.db
alembic downgrade base
alembic upgrade head
```

## Getting Help

- **Documentation**: Check [docs/](docs/)
- **Discussions**: [GitHub Discussions](https://github.com/jessrm31/agent-performance-monitor/discussions)
- **Issues**: [GitHub Issues](https://github.com/jessrm31/agent-performance-monitor/issues)
- **Email**: support@apm.dev

## Recognition

Contributors will be recognized in:
- README.md
- Release notes
- GitHub contributors page

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Happy contributing! 🎉
