```markdown
# medgraphics-engine Development Patterns

> Auto-generated skill from repository analysis

## Overview

The medgraphics-engine is a Python-based graphics engine focused on medical visualization and image processing. This codebase follows Python best practices with snake_case naming conventions and maintains a modular structure for medical graphics operations, rendering, and data visualization.

## Coding Conventions

### File Naming
- Use **snake_case** for all Python files
- Example: `image_processor.py`, `render_engine.py`, `medical_viewer.py`

### Import Style
- Mixed import patterns detected - standardize on:
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
from .utils import image_helpers
```

### Export Style
- Use `__all__` for explicit exports:
```python
__all__ = ['MedicalRenderer', 'ImageProcessor', 'GraphicsEngine']
```

### Code Structure
- Keep modules focused on single responsibilities
- Use descriptive variable names related to medical terminology
- Document complex algorithms with inline comments

## Workflows

### Adding New Graphics Feature
**Trigger:** When implementing new visualization or rendering capabilities
**Command:** `/add-graphics-feature`

1. Create feature module in appropriate subdirectory using snake_case
2. Import required dependencies (numpy, matplotlib, medical libs)
3. Implement core functionality with medical-specific parameter validation
4. Add comprehensive docstrings with medical context
5. Create corresponding test file with `.test.` pattern
6. Update module exports and documentation

### Medical Image Processing
**Trigger:** When adding new image processing capabilities
**Command:** `/add-image-processor`

1. Create processor module: `{feature_name}_processor.py`
2. Define processing class with medical image format support
3. Implement validation for medical image standards (DICOM, NIfTI)
4. Add error handling for corrupted or invalid medical data
5. Include metadata preservation methods
6. Write unit tests covering edge cases and medical scenarios

### Graphics Engine Enhancement
**Trigger:** When extending core rendering capabilities
**Command:** `/enhance-engine`

1. Identify target rendering component
2. Create backup of existing functionality
3. Implement enhancement with backward compatibility
4. Add configuration options for medical-specific requirements
5. Update performance benchmarks
6. Test with various medical image formats and sizes

## Testing Patterns

### Test File Structure
- Use pattern: `*.test.*` for test files
- Example: `image_processor.test.py`, `renderer.test.py`

### Test Organization
```python
import unittest
from unittest.mock import Mock, patch

class TestMedicalRenderer(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures with sample medical data"""
        pass
    
    def test_dicom_rendering(self):
        """Test DICOM image rendering capabilities"""
        pass
    
    def test_performance_benchmarks(self):
        """Ensure rendering meets medical application requirements"""
        pass
```

### Medical Data Testing
- Use anonymized medical datasets for testing
- Test with various image dimensions and bit depths
- Validate metadata preservation
- Test memory usage with large medical images

## Commands

| Command | Purpose |
|---------|---------|
| `/add-graphics-feature` | Add new visualization or rendering capability |
| `/add-image-processor` | Create new medical image processing module |
| `/enhance-engine` | Extend core graphics engine functionality |
| `/run-medical-tests` | Execute medical-specific test suites |
| `/benchmark-performance` | Run performance tests for medical workflows |
| `/validate-dicom` | Test DICOM compatibility and standards compliance |
| `/check-memory-usage` | Analyze memory consumption with large medical datasets |
| `/update-docs` | Update documentation with medical use cases and examples |
```