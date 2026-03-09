# medgraphics-engine Development Patterns

> Auto-generated skill from repository analysis

## Overview

This skill covers development patterns for the medgraphics-engine, a Python-based medical graphics engine. The codebase follows a component-driven architecture with comprehensive test coverage, emphasizing modular engine components, template-based rendering, and consistent testing practices.

## Coding Conventions

### File Naming
- Use `snake_case` for all Python files
- Engine components: `engine/component_name.py`
- Test files: `test_component_name.py`
- Templates: `templates/template_name.html`

### Import Style
```python
# Standard library imports first
import os
import sys

# Third-party imports
import numpy as np
import matplotlib.pyplot as plt

# Local imports
from engine.core import BaseEngine
from engine.renderer import GraphicsRenderer
```

### Commit Messages
- Use conventional commit format: `feat:`, `fix:`
- Keep messages around 72 characters
- Examples:
  - `feat: add new rendering engine component`
  - `fix: resolve template loading issue`

## Workflows

### Add Engine Component
**Trigger:** When someone wants to add a new core engine functionality
**Command:** `/new-engine-component`

1. Create component file in `engine/` directory using snake_case naming
2. Create corresponding test file with `test_` prefix
3. Implement core functionality following engine patterns:
   ```python
   class NewComponent:
       def __init__(self):
           self.initialized = False
       
       def process(self, data):
           """Main processing method"""
           pass
   ```
4. Write comprehensive tests covering all methods and edge cases
5. Update any related documentation or imports

### Feature with Tests
**Trigger:** When someone wants to add any new feature to the system
**Command:** `/new-feature`

1. Create or modify implementation file following snake_case convention
2. Create corresponding test file with `test_` prefix
3. Write feature code with proper error handling
4. Write test cases covering:
   - Happy path scenarios
   - Edge cases
   - Error conditions
   ```python
   def test_feature_happy_path():
       # Test normal operation
       pass
   
   def test_feature_edge_cases():
       # Test boundary conditions
       pass
   
   def test_feature_error_handling():
       # Test error scenarios
       pass
   ```

### Template System Development
**Trigger:** When someone wants to add new visual templates or template functionality
**Command:** `/new-template`

1. Create or modify template engine component in `engine/template_engine.py`
2. Add HTML templates in `templates/` directory with descriptive names
3. Create corresponding tests in `test_template*.py`
4. Update template system with new functionality:
   ```python
   def load_template(self, template_name):
       """Load and parse template file"""
       template_path = f"templates/{template_name}.html"
       # Implementation here
   ```

## Testing Patterns

### Test File Structure
```python
import unittest
from engine.component import ComponentName

class TestComponentName(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.component = ComponentName()
    
    def test_method_name(self):
        """Test specific functionality"""
        # Arrange
        # Act
        # Assert
        pass
    
    def tearDown(self):
        """Clean up after tests"""
        pass

if __name__ == '__main__':
    unittest.main()
```

### Test Naming
- Test files: `test_*.py`
- Test methods: `test_method_description`
- Test classes: `TestComponentName`

## Commands

| Command | Purpose |
|---------|---------|
| `/new-engine-component` | Create a new core engine component with tests |
| `/new-feature` | Add a new feature with comprehensive test coverage |
| `/new-template` | Add HTML templates with template engine support |
| `/run-tests` | Execute test suite for the project |
| `/fix-imports` | Standardize import statements across files |