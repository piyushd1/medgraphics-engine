import json
from engine.template_engine import TemplateEngine

def generate_preview_html():
    engine = TemplateEngine("templates")
    
    test_theme = {
        "primary_color": "#2B6CB0",
        "secondary_color": "#EBF4FF",
        "accent_color": "#38A169",
        "text_color": "#1A202C",
        "background_color": "#F7FAFC",
        "font_heading": "Poppins",
        "font_body": "Inter"
    }

    templates_data = {
        "timeline": {
            "title": "What is Anomaly Scan?",
            "subtitle": "Anomaly Scan (Level-II)",
            "timeline_items": [
                {"week": 10, "icon": "❤️", "label": "Heart"},
                {"week": 12, "icon": "🦴", "label": "Limbs"},
                {"week": 20, "icon": "🧠", "label": "Brain"}
            ],
            "highlight_range": {"start": 20, "end": 24, "label": "Anomaly Scan Window"},
            "bullets": ["Detailed ultrasound at 20-24 weeks", "Checks baby's physical development"],
            "footer": "A routine and important check for peace of mind"
        },
        "comparison": {
            "title": "Anomaly Scan: Understanding the Timelines",
            "subtitle": "Informative Pathways, Not Alarming Outcomes",
            "left": {
                "heading": "WITH ANOMALY SCAN",
                "subheading": "Reassurance & Monitoring",
                "steps": [
                    {"icon": "🔍", "label": "Scan Performed"},
                    {"icon": "✅", "label": "Early Reassurance"},
                    {"icon": "📅", "label": "Planned Care"}
                ]
            },
            "right": {
                "heading": "WITHOUT ANOMALY SCAN",
                "subheading": "Delayed Awareness",
                "steps": [
                    {"icon": "❓", "label": "Uncertainty"},
                    {"icon": "⚠️", "label": "Late Detection"},
                    {"icon": "🏥", "label": "Urgent Action"}
                ]
            },
            "bottom_note": "Skipping DOES NOT cause harm. But physical issues may be detected LATE.",
            "footer_left": "Outcome: Clarity, proactive management",
            "footer_right": "Outcome: Potential for unexpected findings"
        },
        "checklist": {
            "title": "What Anomaly Scan Helps With",
            "items": [
                {"icon": "💝", "heading": "Early reassurance", "description": "Gives peace of mind about baby's development early on."},
                {"icon": "📅", "heading": "Planned monitoring", "description": "Allows scheduling appropriate follow-up appointments."},
                {"icon": "⚕️", "heading": "Medical planning", "description": "Provides info for delivery setting decisions."}
            ],
            "footer": "Timely scans provide clarity and peace of mind"
        },
        "flowchart": {
            "title": "Skipping check-ups delays detection",
            "paths": [
                {
                    "heading": "Regular Check-ups",
                    "color": "positive",
                    "steps": ["Scheduled check", "Early detection", "Easier treatment", "Protected health"]
                },
                {
                    "heading": "No Check-ups",
                    "color": "negative",
                    "steps": ["Check skipped", "Late diagnosis", "Complications", "Uncertainty"]
                }
            ]
        },
        "info_card": {  
            "title": "NT Scan",
            "bullets": ["Measures fluid at the back of the baby's neck", "Typically done at 12-14 weeks", "Non-invasive ultrasound"],
            "illustration_placeholder": True,
            "background_style": "soft_gradient"
        },
        "icon_grid": {
            "title": "Found early through regular check-ups",
            "center": {"icon": "🩺", "label": "REGULAR CHECK-UPS"},
            "cards": [
                {"icon": "💉", "heading": "Diabetes", "description": "Glucose screening & management"},
                {"icon": "💓", "heading": "Heart issues", "description": "Cardiovascular assessment"},
                {"icon": "🩸", "heading": "High Blood Pressure", "description": "Blood pressure monitoring"},
                {"icon": "🔬", "heading": "Some cancers", "description": "Early detection screenings"}
            ]
        }
    }

    import os
    os.makedirs("preview", exist_ok=True)
    
    # Generate Story Output (1080x1920)
    for name, data in templates_data.items():
        html = engine.render(f"{name}.html", data=data, theme=test_theme, width=1080, height=1920)
        with open(f"preview/{name}_story.html", "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Generated preview/{name}_story.html")
        
    print("Test script execution completed.")

if __name__ == "__main__":
    generate_preview_html()
