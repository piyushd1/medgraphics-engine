```markdown
# medgraphics-engine Development Patterns

> Auto-generated skill from repository analysis

## Overview

The medgraphics-engine is a Python-based medical graphics processing library focused on healthcare visualization and image analysis. This repository follows Python best practices with snake_case naming conventions and a modular architecture suitable for medical imaging applications.

## Coding Conventions

### File Naming
- Use `snake_case` for all Python files
- Module names should be descriptive and lowercase
```python
# Good
image_processor.py
dicom_parser.py
visualization_utils.py

# Avoid
ImageProcessor.py
DicomParser.py
```

### Import Organization
The codebase uses mixed import styles. Follow this order:
```python
# Standard library imports
import os
import sys
from pathlib import Path

# Third-party imports
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Local application imports
from .core import MedicalImage
from .utils import validation_helpers
```

### Export Patterns
- Use `__all__` for explicit module exports
- Mix of function and class exports based on module purpose
```python
__all__ = ['ImageProcessor', 'process_dicom', 'validate_image']

class ImageProcessor:
    pass

def process_dicom(file_path):
    pass
```

## Workflows

### Image Processing Pipeline
**Trigger:** When adding new medical image processing functionality  
**Command:** `/process-image`

1. Create a new module in snake_case format (e.g., `mri_processor.py`)
2. Import required medical imaging libraries (numpy, PIL, pydicom)
3. Implement core processing class with validation
4. Add utility functions for common operations
5. Export main classes and functions via `__all__`
6. Create corresponding test file following `*.test.*` pattern

### Medical Visualization Component
**Trigger:** When creating new visualization features  
**Command:** `/add-visualization`

1. Create visualization module (e.g., `brain_renderer.py`)
2. Import matplotlib, plotly, or other graphics libraries
3. Implement visualization class with medical data validation
4. Add configuration options for medical standards (DICOM compliance)
5. Include export functions for common medical formats
6. Document medical imaging parameters and units

### Data Validation Module
**Trigger:** When adding medical data validation  
**Command:** `/add-validation`

1. Create validation module (e.g., `dicom_validator.py`)
2. Implement medical data type checking
3. Add HIPAA/medical privacy considerations
4. Create error handling for corrupted medical files
5. Include unit conversion utilities
6. Export validation functions

## Testing Patterns

### Test Structure
- Test files follow `*.test.*` naming pattern
- Unknown framework suggests custom testing approach
```python
# Example test structure
def test_image_processing():
    # Setup medical test data
    test_image = create_test_dicom()
    
    # Process
    result = process_medical_image(test_image)
    
    # Validate medical standards
    assert validate_dicom_compliance(result)
    assert check_image_dimensions(result)
```

### Medical Data Testing
- Use synthetic medical data for testing
- Validate DICOM compliance and medical imaging standards
- Test edge cases with corrupted or incomplete medical files
- Ensure patient data privacy in test cases

## Commands

| Command | Purpose |
|---------|---------|
| /process-image | Create new medical image processing module |
| /add-visualization | Add medical data visualization component |
| /add-validation | Implement medical data validation |
| /test-medical | Create tests for medical imaging functionality |
| /dicom-handler | Add DICOM file processing capabilities |
| /medical-export | Create medical format export functionality |
```