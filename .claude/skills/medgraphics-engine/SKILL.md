# medgraphics-engine Development Patterns

> Auto-generated skill from repository analysis

## Overview

The medgraphics-engine is a Python-based medical graphics processing system. This repository follows a straightforward Python development approach with snake_case naming conventions and mixed import styles. The codebase appears to focus on medical imaging and graphics processing functionality without relying on heavy frameworks, providing flexibility for specialized medical applications.

## Coding Conventions

### File Naming
- Use `snake_case` for all Python files and modules
- Example: `image_processor.py`, `medical_data_handler.py`, `graphics_renderer.py`

### Import Style
The codebase uses a mixed import approach:
```python
# Standard library imports
import os
import sys
from typing import Optional, List

# Third-party imports
import numpy as np
import matplotlib.pyplot as plt

# Local imports
from .utils import helper_function
from medical_core import DataProcessor
```

### Export Style
Mixed export patterns are used:
```python
# Direct exports
def process_medical_image(image_data):
    pass

# Class-based exports
class MedicalGraphicsEngine:
    def __init__(self):
        pass
```

## Workflows

### Feature Development
**Trigger:** Adding new medical graphics processing functionality
**Command:** `/feature-dev`

1. Create feature branch with descriptive name
2. Implement core functionality in appropriate module using snake_case naming
3. Add comprehensive docstrings for medical domain context
4. Write unit tests following `*.test.*` pattern
5. Test with sample medical data
6. Create pull request with freeform commit message (avg 36 chars)

### Medical Data Processing
**Trigger:** When implementing new data processing capabilities
**Command:** `/data-processing`

1. Define data structure and validation rules
2. Implement processing logic in separate module
3. Add error handling for medical data edge cases
4. Create test cases with synthetic medical data
5. Document processing pipeline and expected formats
6. Integrate with existing graphics engine components

### Graphics Rendering Pipeline
**Trigger:** Adding or modifying rendering capabilities
**Command:** `/graphics-pipeline`

1. Design rendering interface following existing patterns
2. Implement core rendering logic with medical imaging considerations
3. Add configuration options for medical display standards
4. Test rendering with various medical image formats
5. Optimize for performance with large medical datasets
6. Document rendering parameters and output formats

## Testing Patterns

Tests in this repository follow the `*.test.*` naming pattern:

```python
# example_module.test.py
import unittest
from medical_graphics import ImageProcessor

class TestImageProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = ImageProcessor()
    
    def test_medical_image_processing(self):
        # Test implementation
        pass
    
    def test_error_handling(self):
        # Test error cases
        pass
```

Key testing practices:
- Use descriptive test method names
- Include setup and teardown for medical data
- Test both success and error scenarios
- Mock external medical data sources when needed

## Commands

| Command | Purpose |
|---------|---------|
| `/feature-dev` | Guide through adding new medical graphics features |
| `/data-processing` | Workflow for implementing medical data processing |
| `/graphics-pipeline` | Steps for graphics rendering development |
| `/test-medical` | Create comprehensive tests for medical functionality |
| `/optimize-performance` | Guide for optimizing medical image processing performance |