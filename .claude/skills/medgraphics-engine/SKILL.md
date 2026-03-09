```markdown
# medgraphics-engine Development Patterns

> Auto-generated skill from repository analysis

## Overview

The medgraphics-engine is a Python-based medical graphics rendering and processing system. This codebase follows a straightforward Python project structure with snake_case naming conventions and flexible import patterns. The project appears to focus on medical visualization and graphics processing capabilities.

## Coding Conventions

### File Naming
- **Pattern:** snake_case for all files
- **Examples:**
  ```
  image_processor.py
  medical_renderer.py
  dicom_handler.py
  visualization_utils.py
  ```

### Import Style
- **Pattern:** Mixed import styles allowed
- **Examples:**
  ```python
  # Standard imports
  import os
  import sys
  from pathlib import Path
  
  # Third-party imports
  import numpy as np
  from PIL import Image
  import matplotlib.pyplot as plt
  
  # Local imports
  from .utils import helper_function
  from medgraphics.core import Renderer
  ```

### Export Style
- **Pattern:** Mixed export patterns
- **Examples:**
  ```python
  # Direct exports
  def process_medical_image():
      pass
  
  # Class exports
  class MedicalRenderer:
      pass
  
  # Module-level exports
  __all__ = ['process_medical_image', 'MedicalRenderer']
  ```

## Workflows

### Core Development
**Trigger:** When implementing new medical graphics features
**Command:** `/dev-workflow`

1. Create new module with snake_case naming
2. Import required dependencies using mixed style
3. Implement core functionality with clear function/class names
4. Add appropriate exports for public API
5. Write freeform commit message (~40 chars) describing changes

### Testing Implementation
**Trigger:** When adding tests for new functionality
**Command:** `/add-tests`

1. Create test file following `*.test.*` pattern
2. Import testing framework and module under test
3. Write test cases covering core functionality
4. Run tests to verify implementation
5. Commit with descriptive message about test coverage

### Medical Image Processing
**Trigger:** When working with medical imaging data
**Command:** `/process-medical-image`

1. Create processing module (e.g., `dicom_processor.py`)
2. Import medical imaging libraries (SimpleITK, pydicom, etc.)
3. Implement image loading and preprocessing functions
4. Add visualization utilities for medical data
5. Export processing functions for external use

### Graphics Rendering Setup
**Trigger:** When implementing new rendering capabilities
**Command:** `/setup-renderer`

1. Create renderer module with snake_case naming
2. Import graphics libraries (OpenGL, VTK, matplotlib)
3. Define renderer class with initialization methods
4. Implement core rendering functions
5. Add configuration and parameter handling

## Testing Patterns

### Test File Structure
- **Pattern:** `*.test.*` naming convention
- **Location:** Tests can be co-located with source files or in separate directories
- **Example structure:**
  ```python
  # image_processor.test.py
  def test_load_dicom_image():
      # Test DICOM image loading
      pass
  
  def test_image_preprocessing():
      # Test preprocessing pipeline
      pass
  
  def test_medical_visualization():
      # Test visualization output
      pass
  ```

### Test Implementation
```python
# Example test structure
import unittest
from medgraphics.processor import MedicalImageProcessor

class TestMedicalProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = MedicalImageProcessor()
    
    def test_image_loading(self):
        # Test implementation
        pass
```

## Commands

| Command | Purpose |
|---------|---------|
| `/dev-workflow` | Set up new feature development workflow |
| `/add-tests` | Create and implement test files |
| `/process-medical-image` | Implement medical image processing functionality |
| `/setup-renderer` | Create new graphics rendering components |
| `/snake-case-file` | Generate properly named Python module |
| `/commit-freeform` | Create freeform commit message (~40 chars) |
```