"""
Browser Tool using browser-use and Playwright
Control browsers, navigate, click, fill forms, and extract data.
"""

import logging
import base64
from typing import Dict, Any, Optional, List
import asyncio

logger = logging.getLogger(__name__)


class BrowserTool:
    """Browser automation with Playwright and vision AI."""
    
    def __init__(self):
        """Initialize browser tool."""
        self.browser = None
        self.context = None
        self.page = None
    
    async def navigate(self, url: str) -> Dict[str, Any]:
        """
        Navigate to URL.
        
        Args:
            url: URL to navigate to
            
        Returns:
            dict: {success, result, error}
        """
        try:
            from playwright.async_api import async_playwright
            
            if not self.page:
                p = await async_playwright().start()
                self.browser = await p.chromium.launch(headless=True)
                self.context = await self.browser.new_context()
                self.page = await self.context.new_page()
            
            await self.page.goto(url, wait_until="networkidle")
            logger.info(f"Navigated to: {url}")
            
            return {
                "success": True,
                "result": f"Navigated to {url}",
                "error": None,
            }
        except Exception as e:
            logger.error(f"Navigation failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    async def screenshot(self, url: str) -> Dict[str, Any]:
        """
        Take screenshot of URL.
        
        Args:
            url: URL to screenshot
            
        Returns:
            dict: {success, result (base64), error}
        """
        try:
            await self.navigate(url)
            screenshot_bytes = await self.page.screenshot()
            b64_str = base64.b64encode(screenshot_bytes).decode()
            
            return {
                "success": True,
                "result": f"data:image/png;base64,{b64_str}",
                "error": None,
            }
        except Exception as e:
            logger.error(f"Screenshot failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    async def click(self, selector: str) -> Dict[str, Any]:
        """
        Click element by CSS selector.
        
        Args:
            selector: CSS selector
            
        Returns:
            dict: {success, result, error}
        """
        try:
            await self.page.click(selector)
            await asyncio.sleep(1)
            logger.info(f"Clicked: {selector}")
            
            return {
                "success": True,
                "result": f"Clicked {selector}",
                "error": None,
            }
        except Exception as e:
            logger.error(f"Click failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    async def fill_form(self, fields: Dict[str, str]) -> Dict[str, Any]:
        """
        Fill form fields.
        
        Args:
            fields: Dict of selector -> value
            
        Returns:
            dict: {success, result, error}
        """
        try:
            for selector, value in fields.items():
                await self.page.fill(selector, value)
                await asyncio.sleep(0.5)
            
            logger.info(f"Filled {len(fields)} fields")
            return {
                "success": True,
                "result": f"Filled {len(fields)} fields",
                "error": None,
            }
        except Exception as e:
            logger.error(f"Fill form failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    async def extract_text(self, url: str, selector: Optional[str] = None) -> Dict[str, Any]:
        """
        Extract text from page or specific element.
        
        Args:
            url: URL to extract from
            selector: Optional CSS selector
            
        Returns:
            dict: {success, result, error}
        """
        try:
            await self.navigate(url)
            
            if selector:
                text = await self.page.text_content(selector)
            else:
                text = await self.page.content()
            
            logger.info(f"Extracted text from {url}")
            return {
                "success": True,
                "result": text,
                "error": None,
            }
        except Exception as e:
            logger.error(f"Extract text failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    async def scrape(
        self,
        url: str,
        selector: str,
        extract_attr: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Scrape elements from page.
        
        Args:
            url: URL to scrape
            selector: CSS selector for elements
            extract_attr: Optional attribute to extract
            
        Returns:
            dict: {success, result (list), error}
        """
        try:
            await self.navigate(url)
            elements = await self.page.query_selector_all(selector)
            results = []
            
            for elem in elements:
                if extract_attr:
                    value = await elem.get_attribute(extract_attr)
                else:
                    value = await elem.text_content()
                results.append(value)
            
            logger.info(f"Scraped {len(results)} elements from {url}")
            return {
                "success": True,
                "result": results,
                "error": None,
            }
        except Exception as e:
            logger.error(f"Scrape failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    async def close(self) -> None:
        """Close browser."""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()


# Global instance
browser_tool = BrowserTool()


async def navigate(url: str) -> Dict[str, Any]:
    """Navigate wrapper."""
    return await browser_tool.navigate(url)


async def screenshot(url: str) -> Dict[str, Any]:
    """Screenshot wrapper."""
    return await browser_tool.screenshot(url)
