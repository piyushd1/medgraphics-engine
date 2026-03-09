# 🏥 MedGraphics Engine

 MedGraphics Engine is an intelligent, multi-step pipeline built to generate professional, pixel-perfect medical infographics.

 It leverages Large Language Models (LLMs) via LiteLLM for intelligent topic ideation and structural content parsing, seamlessly injecting the results into beautifully crafted HTML/CSS templates. Finally, Playwright renders the DOM into high-resolution PNG assets autonomously.

## Features

- **LLM Router**: Cost-aware dynamic routing using `LiteLLM`, backing off gracefully from `gemini` → `openai` → `anthropic` if rate limits or authentication errors strike.
- **Template Engine**: Robust Jinja2 rendering pipeline supporting customizable Client Profiles (brand colors and typography injections). Included templates:
  - Timeline
  - Comparison (Side-by-side)
  - Checklist
  - Flowchart
  - Info Card
  - Icon Grid
- **Playwright Renderer**: Headless Chromium-based snapshot tool configured without JavaScript execution to prevent XSS vulnerabilities, optimized for Google Font loading and retina-scale exports.
- **Streamlit Web Dashboard**: Built-in 4-page UI interface allowing brand managers to govern `.env` keys, build CSS profiles, deploy generation runs, and download historical assets.

## Quickstart

### Prerequisites:
- Python 3.12+
- `pip install -r requirements.txt`
- Playwright installation: `python -m playwright install chromium`

### Running the App:
```bash
streamlit run app.py
```
This spawns the interactive User Interface. Please navigate to the **⚙️ Model Settings** tab first to instantiate your API Keys.

### Generating the Sample Portfolio
To run the automated matrix script testing all 36 combinations of Specialties, Templates, and Formats natively, execute:
```bash
python generate_portfolio.py
```
Output assets will be dumped into the `portfolio/` directory.

## E2E Testing Pipeline
The suite utilizes PyTest to govern system stability. Tests are isolated within the `tests/` directory to interface naturally with CI providers (e.g., GitHub Actions).

```bash
python -m pytest tests/
```
