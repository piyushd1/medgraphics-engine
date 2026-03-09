from playwright.sync_api import sync_playwright
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class Renderer:
    def __init__(self):
        """Initialize Playwright with headless Chromium"""
        self.playwright = None
        self.browser = None
        
    def start(self):
        """Launch browser (call once, reuse for batch)"""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        
    def stop(self):
        """Clean up browser resources"""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def _wait_for_fonts(self, page, timeout_ms: int = 5000) -> bool:
        """Wait for fonts with timeout. Returns True if fonts loaded."""
        try:
            page.evaluate(
                """() => Promise.race([
                    document.fonts.ready,
                    new Promise((_, reject) => setTimeout(() => reject('timeout'), %d))
                ])""" % timeout_ms
            )
            return True
        except Exception as e:
            # Fonts didn't load — proceed anyway with system fonts
            logger.warning(f"Fonts failed to load within timeout: {e}")
            return False
    
    def render_html_to_png(
        self, 
        html_content: str, 
        output_path: str,
        width: int = 1080, 
        height: int = 1920,
        device_scale_factor: int = 2  # 2x for retina quality
    ) -> str:
        """
        Render HTML string to PNG file.
        
        Args:
            html_content: Complete HTML string
            output_path: Where to save the PNG
            width: Viewport width in px
            height: Viewport height in px
            device_scale_factor: 2 = retina (2160x3840 actual pixels)
        
        Returns:
            Path to saved PNG file
        """
        if not self.browser:
            self.start()

        page = self.browser.new_page(
            viewport={"width": width, "height": height},
            device_scale_factor=device_scale_factor,
            java_script_enabled=False  # Mitigate XSS from LLM HTML
        )
        
        try:
            # Step 1: Set content and wait for network requests to finish
            page.set_content(html_content, wait_until="networkidle")
            
            # Step 2: Explicitly wait for all fonts to be loaded (with timeout)
            self._wait_for_fonts(page)
            
            # Step 3: Small safety delay for rendering to settle
            page.wait_for_timeout(500)  # 500ms buffer
            
            # Step 4: Take the screenshot
            page.screenshot(path=output_path, full_page=False)
            
        except Exception as e:
            logger.error(f"Error rendering HTML: {e}")
            raise
            
        finally:
            page.close()
            
        return output_path
    
    def render_batch(
        self,
        html_list: list[dict],  # [{"html": str, "filename": str}]
        output_dir: str,
        width: int = 1080,
        height: int = 1920
    ) -> list[str]:
        """Render multiple HTMLs to PNGs. Returns list of output paths."""
        import os
        output_paths = []
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        for item in html_list:
            # Prevent path traversal by extracting just the basename
            safe_filename = os.path.basename(item["filename"])
            path = str(Path(output_dir) / safe_filename)
            self.render_html_to_png(item["html"], path, width, height)
            output_paths.append(path)
        return output_paths
    
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
