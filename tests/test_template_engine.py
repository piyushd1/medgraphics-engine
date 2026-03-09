import json
import os
import sys

# Ensure the root directory is on the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.template_engine import TemplateEngine

def test_base_template():
    # Test Data as provided
    test_theme = {
        "primary_color": "#2B6CB0",
        "secondary_color": "#EBF4FF",
        "accent_color": "#38A169",
        "text_color": "#1A202C",
        "background_color": "#F7FAFC",
        "font_heading": "Poppins",
        "font_body": "Inter"
    }

    test_data = {
        "title": "Why Regular Check-ups Matter",
        "subtitle": "Early detection saves lives",
        "items": [
            {"icon": "🩺", "heading": "Prevention", "description": "Catch issues before symptoms appear"},
            {"icon": "📋", "heading": "Tracking", "description": "Monitor health trends over time"},
        ],
        "footer": "Schedule your annual check-up today"
    }

    # Initialize Engine
    engine = TemplateEngine("templates")

    # Render template
    html = engine.render("base.html", data=test_data, theme=test_theme, width=1080, height=1920)

    # Output assertions verification
    print("--- RENDERED HTML ---\n")
    print(html)
    print("\n--- TEST RESULTS ---")
    
    # Assertions
    assert html.startswith("<!DOCTYPE html>"), "HTML must start with DOCTYPE"
    assert "https://fonts.googleapis.com/css2?family=Poppins" in html, "Google Fonts links missing or incorrect"
    assert "--primary: #2B6CB0" in html, "CSS variables missing or incorrect"
    assert "width: 1080px;" in html, "Body width missing or incorrect"
    assert "height: 1920px;" in html, "Body height missing or incorrect"
    assert "{{" not in html and "}}" not in html, "Unrendered Jinja placeholders found"
    
    print("All assertions passed successfully!")

if __name__ == "__main__":
    test_base_template()
