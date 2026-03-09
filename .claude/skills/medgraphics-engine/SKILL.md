```markdown
# medgraphics-engine Development Patterns

> Auto-generated skill from repository analysis

## Overview

This skill teaches development patterns for the medgraphics-engine, a Python-based medical graphics processing engine. The codebase follows Python conventions with snake_case file naming and supports mixed import/export styles for flexibility in medical imaging workflows.

## Coding Conventions

### File Naming
- Use `snake_case` for all Python files
- Example: `image_processor.py`, `dicom_handler.py`, `volume_renderer.py`

### Import Style
The codebase supports mixed import styles depending on context:

```python
# Standard library imports
import os
import sys
from pathlib import Path

# Third-party imports
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Local imports
from .core import ImageProcessor
from medgraphics.utils import validate_dicom
```

### Export Style
Mixed export patterns are used:

```python
# Direct exports
def process_medical_image(image_data):
    return processed_data

# Class-based exports
class MedicalImageProcessor:
    def __init__(self):
        pass
    
    def render(self):
        pass

# Module-level exports
__all__ = ['MedicalImageProcessor', 'process_medical_image']
```

## Workflows

### Medical Image Processing
**Trigger:** When processing medical imaging data (DICOM, MRI, CT scans)
**Command:** `/process-medical-image`

1. Import required medical imaging libraries
2. Create image processor class with snake_case naming
3. Implement validation methods for medical data
4. Add processing pipeline methods
5. Include error handling for medical data formats
6. Write corresponding test file following `*.test.*` pattern

### Graphics Engine Component
**Trigger:** When adding new graphics rendering functionality
**Command:** `/add-graphics-component`

1. Create new module file using snake_case convention
2. Define component class with clear medical graphics purpose
3. Implement core rendering methods
4. Add configuration and parameter validation
5. Include performance optimization for medical data sizes
6. Document component usage and medical use cases

### Data Validation Pipeline
**Trigger:** When implementing medical data validation
**Command:** `/add-data-validation`

1. Create validation module following naming conventions
2. Implement medical data format checkers
3. Add DICOM/medical imaging standard compliance checks
4. Include error reporting for invalid medical data
5. Write comprehensive validation tests
6. Document supported medical imaging formats

## Testing Patterns

Tests follow the `*.test.*` pattern and should include:

```python
# Example: image_processor.test.py
import unittest
from medgraphics.core import ImageProcessor

class TestImageProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = ImageProcessor()
        
    def test_medical_image_validation(self):
        # Test medical data validation
        pass
        
    def test_dicom_processing(self):
        # Test DICOM file processing
        pass
        
    def test_rendering_pipeline(self):
        # Test graphics rendering
        pass
```

## Commit Conventions

Use freeform commit messages (average ~44 characters) that clearly describe changes:

```
Fix DICOM metadata parsing issue
Add volume rendering optimization  
Update medical image validation
Refactor graphics pipeline core
```

## Commands

| Command | Purpose |
|---------|---------|
| `/process-medical-image` | Set up medical image processing workflow |
| `/add-graphics-component` | Add new graphics rendering component |
| `/add-data-validation` | Implement medical data validation pipeline |
| `/setup-test` | Create test file following repository patterns |
| `/optimize-rendering` | Add performance optimizations for medical graphics |
```