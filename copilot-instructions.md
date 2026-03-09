# MedGraphics Engine — Coding Guidelines

## What This Project Does
Medical infographic generator. LLMs generate HTML/CSS code, Playwright renders to PNG.

## Stack
Python 3.11+, Streamlit, LiteLLM, Jinja2, Playwright

## Code Rules
- Type hints on all function signatures
- Docstrings on all classes and public methods
- Max line length: 120 characters
- Use pathlib.Path, not os.path
- Use f-strings for string formatting
- All HTML templates must be self-contained (inline CSS only)
- Google Fonts loaded via link tags in HTML head
- No external CSS files — Playwright needs everything in one HTML file

## Key Modules
- engine/llm_router.py — LiteLLM-based model routing with cost tracking
- engine/template_engine.py — Jinja2 HTML template rendering with theming
- engine/renderer.py — Playwright headless browser HTML-to-PNG conversion
- engine/pipeline.py — Orchestrates: topic gen → content brief → HTML gen → render
- prompts/ — LLM prompt templates (must output JSON, no markdown)
- templates/ — Jinja2 HTML/CSS infographic templates
- config/ — YAML configs for models and medical specialties

## Testing
- pytest for all tests
- Test files go in tests/ directory
- Every new module needs a test file
