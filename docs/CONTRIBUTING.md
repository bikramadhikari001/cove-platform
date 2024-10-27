# Contributing to Covenant Tracking Platform

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How to Contribute

### Getting Started

1. Fork the repository
2. Clone your fork: `git clone [your-fork-url]`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Push to your fork: `git push origin feature/your-feature-name`
6. Submit a Pull Request

### Development Environment Setup

1. Install Python 3.8+
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Coding Standards

#### Python Code Style

- Follow PEP 8 style guide
- Use 4 spaces for indentation
- Maximum line length: 88 characters
- Use meaningful variable and function names
- Include docstrings for all functions, classes, and modules

Example:
```python
def calculate_covenant_ratio(assets: float, liabilities: float) -> float:
    """
    Calculate the covenant ratio based on assets and liabilities.

    Args:
        assets (float): Total assets value
        liabilities (float): Total liabilities value

    Returns:
        float: Calculated covenant ratio
    """
    if liabilities == 0:
        raise ValueError("Liabilities cannot be zero")
    return assets / liabilities
```

#### HTML/CSS Style

- Use 2 spaces for indentation in HTML and CSS
- Use semantic HTML elements
- Follow BEM naming convention for CSS classes
- Keep CSS selectors as simple as possible

#### JavaScript Style

- Use ES6+ features
- Use 2 spaces for indentation
- Use camelCase for variable and function names
- Add comments for complex logic

### Git Commit Messages

Format:
```
[Module] Brief description of changes

- Detailed list of changes
- Any important notes
```

Example:
```
[Auth] Implement Auth0 login flow

- Add Auth0 configuration
- Create login and callback routes
- Add user session management
- Update navigation menu with login status
```

### Testing

- Write unit tests for all new features
- Ensure all tests pass before submitting PR
- Include both positive and negative test cases
- Use pytest for Python tests

### Documentation

- Update README.md if adding new features
- Document all API endpoints
- Include inline comments for complex logic
- Update requirements.txt for new dependencies

### Pull Request Process

1. Update documentation
2. Add/update tests
3. Ensure CI/CD pipeline passes
4. Request review from at least one team member
5. Address review comments
6. Squash commits before merging

### Code Review Guidelines

When reviewing code:
- Check for coding standards compliance
- Verify test coverage
- Review documentation updates
- Test functionality locally
- Provide constructive feedback

## Project Structure

```
covenant-tracking-platform/
├── app/
│   ├── auth/          # Authentication related code
│   ├── main/          # Main application routes
│   ├── static/        # Static assets
│   └── templates/     # HTML templates
├── tests/             # Test files
├── docs/              # Documentation
└── requirements.txt   # Project dependencies
```

## Questions or Problems?

- Open an issue for bugs
- Use discussions for questions
- Tag appropriate team members

Thank you for contributing to the Covenant Tracking Platform!
