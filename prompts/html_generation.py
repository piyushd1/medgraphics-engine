HTML_GENERATION_PROMPT = """
You are an expert frontend developer who creates beautiful medical infographic HTML.

Generate a COMPLETE, SELF-CONTAINED HTML file for a medical infographic with these specs:

**Content data:**
{content_json}

**Template type:** {template_type}
**Dimensions:** {width}x{height}px
**Theme:**
- Primary color: {primary_color}
- Secondary color: {secondary_color}
- Accent color: {accent_color}
- Heading font: {font_heading}
- Body font: {font_body}

**RULES:**
1. Output ONLY valid HTML. No markdown, no explanations, no backticks.
2. All CSS must be in <style> tags (no external files)
3. Include Google Fonts <link> for the specified fonts
4. Use CSS variables for all colors
5. body must be exactly {width}px x {height}px with overflow:hidden
6. Use soft gradients, rounded corners (8-16px), subtle shadows
7. Use emoji for icons (they're specified in the content data)
8. Text must be perfectly readable — proper font sizes and contrast
9. Design must look polished and professional — like a high-end health app
10. NO JavaScript needed — this is a static render

Start your response with <!DOCTYPE html> and end with </html>.
"""
