from engine.renderer import Renderer
import os

test_html = '''
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;700&family=Inter:wght@400;500&display=swap" rel="stylesheet">
    <style>
        body { width: 1080px; height: 1920px; background: linear-gradient(135deg, #EBF4FF 0%, #F0FFF4 100%); 
               font-family: 'Poppins', sans-serif; display: flex; align-items: center; justify-content: center; }
        h1 { font-size: 48px; color: #2B6CB0; text-align: center; }
    </style>
</head>
<body>
    <h1>MedGraphics Engine<br>Renderer Test</h1>
</body>
</html>
'''

def test_renderer():
    os.makedirs("output", exist_ok=True)
    with Renderer() as renderer:
        path = renderer.render_html_to_png(test_html, "output/test_render.png", 1080, 1920)
        print(f"Rendered to: {path}")

if __name__ == "__main__":
    test_renderer()
