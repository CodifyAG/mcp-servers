# Contributing to MCP Server for Harvest Time Tracking

Thank you for your interest in contributing to the MCP Server for Harvest Time Tracking! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## Getting Started

1. **Fork the repository** on GitHub.
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/mcp-server-harvest-time-tracking.git
   cd mcp-server-harvest-time-tracking
   ```
3. **Set up your development environment**:
   ```bash
   make setup
   ```
4. **Create a new branch** for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

### Environment Setup

Make sure to set up your environment variables as described in the README:
```
HARVEST_ACCOUNT_ID=<your-harvest-account-id>
HARVEST_ACCESS_TOKEN=<your-harvest-access-token>
```

### Running Tests

Before submitting your changes, run the tests to ensure everything works correctly:
```bash
make test
```

### Coding Standards

- Follow PEP 8 style guidelines for Python code
- Write docstrings for all functions, classes, and modules
- Include type hints where appropriate
- Keep functions focused on a single responsibility
- Maintain test coverage for new code

## Pull Request Process

1. **Update your fork** with the latest changes from the main repository:
   ```bash
   git remote add upstream https://github.com/original-owner/mcp-server-harvest-time-tracking.git
   git fetch upstream
   git merge upstream/main
   ```

2. **Commit your changes** with clear, descriptive commit messages:
   ```bash
   git commit -m "Add feature: detailed description of the changes"
   ```

3. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Submit a pull request** to the main repository's `main` branch.
   - Provide a clear description of the changes
   - Reference any related issues
   - Include screenshots or examples if applicable

5. **Address review comments** if requested by maintainers.

## Feature Requests and Bug Reports

- Use the GitHub issue tracker to submit feature requests or bug reports
- Clearly describe the issue or feature
- For bugs, include steps to reproduce, expected behavior, and actual behavior
- If possible, include a minimal code example that demonstrates the issue

## Adding New Features

When implementing new Harvest API endpoints:

1. Add the corresponding function in the appropriate module under `src/api/`
2. Update the feature implementation status in the README.md
3. Add tests for the new functionality
4. Document the new feature with examples in the README.md

## Documentation

- Update the README.md with details of changes to the interface
- Include examples for new features
- Keep the feature implementation status table up to date

## License

By contributing to this project, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).

## Questions?

If you have any questions or need help, please open an issue on GitHub or reach out to the maintainers.

Thank you for contributing to the MCP Server for Harvest Time Tracking!
