import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

class TemplateEngine:
    """
    Template engine for MedGraphics that merges unstructured content
    and a client's specific visual theme into a single self-contained HTML document.
    """
    def __init__(self, templates_dir: str = "templates"):
        """
        Initialize the template engine with Jinja2 environment.

        Args:
            templates_dir (str): Path to the directory containing Jinja HTML templates.
        """
        self.templates_dir = Path(templates_dir)

        # Configure Jinja2 environment with block settings for cleaner HTML output
        self.env = Environment(
            loader=FileSystemLoader(self.templates_dir),
            trim_blocks=True,
            lstrip_blocks=True
        )

    def render(self, template_name: str, data: dict, theme: dict, width: int = 1080, height: int = 1920) -> str:
        """
        Renders a given template file with the provided data and client styling.

        Args:
            template_name (str): The filename of the template (e.g. 'base.html').
            data (dict): The dynamic content mapped into the template variables.
            theme (dict): Client configuration (colors, fonts).
            width (int): Target pixel width of the generated image (from output format).
            height (int): Target pixel height of the generated image (from output format).

        Returns:
            str: The fully rendered HTML string, ready for Playwright processing.
        """
        # Ensure we can load the specified template
        template = self.env.get_template(template_name)

        # Build context dictionary to pass into Jinja
        context = {
            "data": data,
            "theme": theme,
            "width": width,
            "height": height
        }

        # Render the template into HTML
        return template.render(**context)
