# medgraphics-engine Development Patterns

> Auto-generated skill from repository analysis

## Overview

This skill teaches development patterns for the medgraphics-engine, a Python-based medical graphics generation system. The engine follows a modular architecture with core components in the `engine/` directory, HTML template system, and prompt-based generation pipeline. The codebase emphasizes comprehensive testing and follows consistent patterns for feature development across interconnected modules.

## Coding Conventions

### File Naming
- Use `snake_case` for all Python files: `template_engine.py`, `graphics_processor.py`
- Test files use `test_` prefix: `test_engine.py`, `test_template_processor.py`
- Template files in `templates/` directory: `base.html`, `medical_chart.html`

### Import Style
```python
# Mixed import style - adapt to existing patterns in each module
from engine.core import GraphicsEngine
import numpy as np
from .utils import helper_function
```

### Export Style
```python
# Mixed export patterns - follow existing module conventions
__all__ = ['GraphicsEngine', 'TemplateProcessor']

# Or direct class/function definitions without explicit exports
class MedicalGraphicsEngine:
    pass
```

### Commit Messages
- Use `feat:` prefix for new features
- Keep messages concise (~69 characters average)
- Example: `feat: add medical chart template with base inheritance`

## Workflows

### Feature Development with Tests
**Trigger:** When you need to add a new core feature or component to the engine
**Command:** `/new-feature`

1. Create implementation file in `engine/` directory using snake_case naming
2. Write comprehensive test file with `test_` prefix covering all functionality
3. Update related configuration files or integration points in the engine
4. Ensure proper error handling and edge cases are covered
5. Test integration with existing engine components

Example structure:
```python
# engine/medical_processor.py
class MedicalProcessor:
    def __init__(self):
        self.config = {}
    
    def process_data(self, medical_data):
        # Implementation here
        pass

# test_medical_processor.py
import unittest
from engine.medical_processor import MedicalProcessor

class TestMedicalProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = MedicalProcessor()
    
    def test_process_data(self):
        # Test implementation
        pass
```

### Template System Expansion
**Trigger:** When you need to add new visual output formats or template types
**Command:** `/new-template`

1. Create new template file in `templates/` directory
2. Ensure proper inheritance from `base.html` template
3. Add corresponding test coverage for template rendering
4. Update template engine integration to recognize new template
5. Test template with various data inputs

Example template structure:
```html
<!-- templates/medical_report.html -->
{% extends "base.html" %}

{% block title %}Medical Report{% endblock %}

{% block content %}
<div class="medical-report">
    {{ report_data }}
</div>
{% endblock %}
```

### Multi-file Feature Implementation
**Trigger:** When you need to add interconnected functionality across the generation pipeline
**Command:** `/new-pipeline-feature`

1. Create core implementation files in `engine/` directory
2. Add corresponding prompt templates and schemas in `prompts/`
3. Implement pipeline orchestration connecting all components
4. Write comprehensive test suite covering integration points
5. Update documentation and configuration as needed

Example pipeline structure:
```python
# engine/pipeline_component.py
class PipelineComponent:
    def __init__(self, prompt_handler, template_engine):
        self.prompt_handler = prompt_handler
        self.template_engine = template_engine
    
    def execute(self, input_data):
        processed = self.prompt_handler.process(input_data)
        return self.template_engine.render(processed)

# prompts/medical_prompts.py
MEDICAL_ANALYSIS_PROMPT = """
Analyze the following medical data:
{data}
"""
```

## Testing Patterns

### Test File Structure
- All test files use `test_*.py` naming pattern
- Tests should cover both unit functionality and integration scenarios
- Use descriptive test method names: `test_medical_processor_handles_invalid_data`

### Test Coverage Areas
```python
class TestEngineComponent(unittest.TestCase):
    def setUp(self):
        # Initialize test fixtures
        pass
    
    def test_normal_operation(self):
        # Test standard functionality
        pass
    
    def test_edge_cases(self):
        # Test boundary conditions
        pass
    
    def test_error_handling(self):
        # Test exception scenarios
        pass
    
    def test_integration_with_other_components(self):
        # Test component interactions
        pass
```

## Commands

| Command | Purpose |
|---------|---------|
| `/new-feature` | Create a new engine component with comprehensive test coverage |
| `/new-template` | Add HTML template with base inheritance and testing |
| `/new-pipeline-feature` | Implement complex multi-module functionality with prompt integration |
| `/test-coverage` | Generate and review test coverage for existing components |
| `/engine-integration` | Connect new components to the main engine pipeline |