from playwright.async_api import async_playwright
from typing import Dict, Any
import logging

class BrowserTool:
    """Automates web browsing using Playwright."""
    
    def __init__(self):
        self.logger = logging.getLogger("nexus.tools.browser")

    async def run(self, url: str) -> Dict[str, Any]:
        """Navigates to a URL and returns the page title and content."""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(url)
                
                title = await page.title()
                # Simple text extraction for demonstration
                content = await page.evaluate("() => document.body.innerText.substring(0, 1000)")
                
                await browser.close()
                return {
                    "url": url,
                    "title": title,
                    "content_preview": content
                }
        except Exception as e:
            self.logger.error(f"Browser tool error: {str(e)}")
            return {"error": str(e)}
