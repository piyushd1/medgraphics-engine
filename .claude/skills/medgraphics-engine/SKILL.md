# medgraphics-engine Development Patterns

> Auto-generated skill from repository analysis

## Overview

The medgraphics-engine is a Python-based medical graphics rendering engine that follows a modular component architecture. The codebase emphasizes clean separation of concerns with dedicated engine components, template systems, and comprehensive testing. Development follows consistent patterns for adding new engine components and template functionality.

## Coding Conventions

### File Naming
- Use `snake_case` for all Python files
- Engine components: `engine/{component_name}.py`
- Test files: `test_{component_name}.py`
- Template files: `templates/{template_name}.html`

### Import Style
```python
# Mixed import style - use standard library first, then local imports
import os
import sys
from typing import Dict, List

from engine.core import BaseComponent
from engine.utils import validate_input
```

### Export Style
```python
# Mixed export patterns - use __all__ for public APIs
__all__ = ['GraphicsEngine', 'TemplateProcessor']

class GraphicsEngine:
    """Main graphics engine component."""
    pass
```

### Commit Messages
- Use `feat:` prefix for new features
- Keep messages around 67 characters
- Example: `feat: add new template rendering component for medical charts`

## Workflows

### Engine Component Development
**Trigger:** When someone wants to add a new engine component or service
**Command:** `/new-component`

1. Create the main component file in `engine/{component}.py`
   ```python
   # engine/chart_renderer.py
   class ChartRenderer:
       """Handles medical chart rendering operations."""
       
       def __init__(self):
           self.config = {}
       
       def render(self, data):
           """Render chart from medical data."""
           pass
   ```

2. Create corresponding test file `test_{component}.py`
   ```python
   # test_chart_renderer.py
   import unittest
   from engine.chart_renderer import ChartRenderer
   
   class TestChartRenderer(unittest.TestCase):
       def setUp(self):
           self.renderer = ChartRenderer()
       
       def test_render_basic_chart(self):
           # Test implementation
           pass
   ```

3. Implement component functionality following the established patterns
4. Write comprehensive unit tests covering main use cases

**Frequency:** ~4x/month

### Template System Development
**Trigger:** When someone wants to add templating capabilities or new HTML templates
**Command:** `/new-template`

1. Create engine component for template processing in `engine/template*.py`
   ```python
   # engine/template_processor.py
   class TemplateProcessor:
       """Processes HTML templates for medical graphics."""
       
       def load_template(self, template_name):
           """Load template from templates directory."""
           pass
       
       def render_template(self, template, context):
           """Render template with given context."""
           pass
   ```

2. Add HTML template files in `templates/` directory
   ```html
   <!-- templates/medical_chart.html -->
   <!DOCTYPE html>
   <html>
   <head>
       <title>Medical Chart: {{chart_title}}</title>
   </head>
   <body>
       <div class="chart-container">
           {{chart_content}}
       </div>
   </body>
   </html>
   ```

3. Create test file for validation `test_template*.py`
   ```python
   # test_template_processor.py
   import unittest
   from engine.template_processor import TemplateProcessor
   
   class TestTemplateProcessor(unittest.TestCase):
       def test_load_medical_chart_template(self):
           processor = TemplateProcessor()
           template = processor.load_template('medical_chart.html')
           self.assertIsNotNone(template)
   ```

4. Update template engine integration if needed

**Frequency:** ~2x/month

## Testing Patterns

### Test File Structure
- Use `test_*.py` naming pattern
- Place test files in the root directory alongside source files
- Follow standard unittest patterns or similar framework
- Each component should have corresponding test coverage

### Test Organization
```python
import unittest
from engine.component import Component

class TestComponent(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.component = Component()
    
    def test_basic_functionality(self):
        """Test basic component functionality."""
        result = self.component.process()
        self.assertIsNotNone(result)
    
    def test_error_handling(self):
        """Test component error handling."""
        with self.assertRaises(ValueError):
            self.component.process(invalid_input=True)
```

## Commands

| Command | Purpose |
|---------|---------|
| `/new-component` | Create a new engine component with corresponding test file |
| `/new-template` | Add new template functionality with HTML templates and processing logic |
| `/test-component` | Run tests for a specific component |
| `/engine-docs` | Generate documentation for engine components |