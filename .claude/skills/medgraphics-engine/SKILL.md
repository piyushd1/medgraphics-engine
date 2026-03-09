```markdown
# medgraphics-engine Development Patterns

> Auto-generated skill from repository analysis

## Overview

This skill teaches development patterns for a Python-based medical graphics engine. The codebase follows mixed coding conventions with a focus on refactoring and iterative improvement. The engine appears to be designed for processing and visualizing medical data and graphics, with an emphasis on clean, maintainable code structure.

## Coding Conventions

### File Naming
- Use `snake_case` for all Python files
- Example: `image_processor.py`, `dicom_renderer.py`, `volume_calculator.py`

### Import Organization
```python
# Standard library imports first
import os
import sys
from pathlib import Path

# Third-party imports
import numpy as np
import matplotlib.pyplot as plt

# Local imports
from .core import MedicalImage
from .utils import validation_helpers
```

### Code Structure
- Mixed export styles accepted but maintain consistency within modules
- Prefer explicit imports over wildcard imports
- Group related functionality into logical modules

### Commit Messages
- Use descriptive commit messages (average 36 characters)
- Prefix with action type when appropriate: `refactor: improve image processing pipeline`
- Focus on what changed and why

## Workflows

### Code Refactoring
**Trigger:** When improving existing code structure or performance
**Command:** `/refactor`

1. Identify the module or function to refactor
2. Write or update tests to cover existing functionality
3. Create a new branch for the refactoring work
4. Make incremental changes while maintaining functionality
5. Run tests after each significant change
6. Update documentation if interfaces change
7. Commit with descriptive message: `refactor: optimize volume rendering algorithm`

### Adding Medical Graphics Features
**Trigger:** When implementing new visualization or processing capabilities
**Command:** `/add-feature`

1. Create feature specification and identify requirements
2. Design API interface following existing patterns
3. Implement core functionality in appropriate module
4. Add comprehensive tests covering edge cases
5. Update documentation and examples
6. Integrate with existing graphics pipeline
7. Commit with clear feature description

### Module Organization
**Trigger:** When adding new functionality or reorganizing code
**Command:** `/organize-module`

1. Group related functions and classes together
2. Follow `snake_case` naming for new files
3. Update `__init__.py` files for proper exports
4. Ensure imports follow the established mixed style consistently
5. Move shared utilities to common modules
6. Update cross-module dependencies

## Testing Patterns

### Test File Structure
- Use `*.test.*` pattern for test files
- Example: `image_processor.test.py`, `dicom_renderer.test.py`
- Place tests adjacent to source files or in dedicated test directories

### Test Organization
```python
# test_medical_imaging.py
class TestMedicalImaging:
    def test_image_loading(self):
        # Test image loading functionality
        pass
    
    def test_volume_rendering(self):
        # Test 3D volume rendering
        pass
```

### Test Coverage
- Write tests for all public APIs
- Include edge cases specific to medical data
- Test error handling for invalid medical file formats
- Validate graphics output and mathematical calculations

## Commands

| Command | Purpose |
|---------|---------|
| `/refactor` | Improve existing code structure and maintainability |
| `/add-feature` | Implement new medical graphics functionality |
| `/organize-module` | Restructure code organization and imports |
| `/test-coverage` | Add or improve test coverage for medical algorithms |
| `/optimize-graphics` | Performance improvements for rendering pipelines |
| `/update-docs` | Update documentation and usage examples |
```