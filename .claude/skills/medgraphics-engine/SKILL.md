```markdown
# medgraphics-engine Development Patterns

> Auto-generated skill from repository analysis

## Overview

This skill teaches the development patterns for the medgraphics-engine, a Python-based medical graphics processing system. The codebase focuses on medical imaging, visualization, and graphics manipulation with a clean, modular architecture using snake_case conventions and feature-driven development.

## Coding Conventions

### File Naming
- Use snake_case for all Python files: `medical_image_processor.py`, `dicom_renderer.py`
- Keep filenames descriptive and module-specific
- Group related functionality in appropriately named modules

### Import Organization
```python
# Standard library imports first
import os
import sys
from typing import Optional, List

# Third-party imports
import numpy as np
import matplotlib.pyplot as plt

# Local imports last
from .core import ImageProcessor
from .utils import validation_helpers
```

### Code Structure
- Mixed import/export patterns suggest flexibility in module design
- Maintain consistent indentation and spacing
- Use descriptive variable names following snake_case convention

### Commit Messages
- Use `feat:` prefix for new features
- Keep messages concise (around 45 characters)
- Examples:
  - `feat: add DICOM image loading support`
  - `feat: implement 3D mesh rendering`
  - `feat: enhance medical data validation`

## Workflows

### Feature Development
**Trigger:** When adding new medical graphics functionality
**Command:** `/add-feature`

1. Create feature branch with descriptive name: `feat/dicom-processor`
2. Implement core functionality in appropriately named snake_case module
3. Add comprehensive error handling for medical data validation
4. Write unit tests following `*.test.*` pattern
5. Commit with `feat:` prefix and concise description
6. Test integration with existing medical imaging pipeline

### Medical Data Processing
**Trigger:** When implementing new medical data handling
**Command:** `/process-medical-data`

1. Create new processor module: `medical_data_processor.py`
2. Implement data validation for medical standards (DICOM, HL7, etc.)
3. Add appropriate error handling for corrupt or invalid medical data
4. Include logging for audit trail requirements
5. Write comprehensive tests covering edge cases
6. Document any medical imaging standards compliance

### Graphics Rendering Pipeline
**Trigger:** When adding new visualization capabilities
**Command:** `/add-renderer`

1. Create renderer module following snake_case: `volume_renderer.py`
2. Implement core rendering logic with performance considerations
3. Add configuration options for different medical visualization needs
4. Include memory management for large medical datasets
5. Test with various medical image formats and sizes
6. Document rendering parameters and usage examples

## Testing Patterns

### Test File Structure
- Follow `*.test.*` naming pattern: `image_processor.test.py`
- Group tests by functionality and medical use cases
- Include edge cases specific to medical data (corrupted files, invalid formats)

### Test Categories
```python
# Unit tests for core functionality
def test_dicom_loading():
    """Test DICOM file loading with valid medical data"""
    pass

def test_invalid_medical_data_handling():
    """Test graceful handling of corrupted medical files"""
    pass

def test_rendering_performance():
    """Test rendering performance with large medical datasets"""
    pass
```

### Medical Data Testing
- Always test with anonymized medical data samples
- Include tests for various medical imaging modalities (CT, MRI, X-ray)
- Validate compliance with medical data standards
- Test memory usage with large medical image volumes

## Commands

| Command | Purpose |
|---------|---------|
| `/add-feature` | Create new medical graphics feature with proper structure |
| `/process-medical-data` | Implement new medical data processing capability |
| `/add-renderer` | Add new medical visualization/rendering functionality |
| `/setup-tests` | Create comprehensive test suite for medical graphics module |
| `/validate-dicom` | Implement DICOM standard validation and processing |
| `/optimize-rendering` | Optimize graphics rendering for large medical datasets |
```