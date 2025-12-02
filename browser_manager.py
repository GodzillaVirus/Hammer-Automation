import asyncio
import random
import uuid
from typing import Dict, Optional, Any
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from playwright_stealth import stealth_async
import logging

try:
    from scrapling.fetchers import StealthyFetcher, StealthySession
    SCRAPLING_AVAILABLE = True
except ImportError:
    SCRAPLING_AVAILABLE = False

logger = logging.getLogger(__name__)

class BrowserSession:
    def __init__(self, session_id: str, page: Page, context: BrowserContext, session_type: str = "playwright"):
        self.session_id = session_id
        self.page = page
        self.context = context
        self.session_type = session_type
        self.scrapling_session = None
        self.created_at = asyncio.get_event_loop().time()
        self.last_activity = self.created_at

class BrowserManager:
    def __init__(self):
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.sessions: Dict[str, BrowserSession] = {}
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        ]
    
    async def initialize(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process',
            ]
        )
        logger.info("Browser initialized successfully")
    
    async def create_session(self, proxy: Optional[str] = None, use_scrapling: bool = False) -> str:
        if not self.browser and not use_scrapling:
            await self.initialize()
        
        session_id = str(uuid.uuid4())
        
        if use_scrapling and SCRAPLING_AVAILABLE:
            scrapling_session = StealthySession(headless=True, solve_cloudflare=True)
            session = BrowserSession(session_id, None, None, "scrapling")
            session.scrapling_session = scrapling_session
            logger.info(f"Scrapling session created: {session_id}")
        else:
            user_agent = random.choice(self.user_agents)
            
            context = await self.browser.new_context(
                user_agent=user_agent,
                viewport={'width': 1920, 'height': 1080},
                locale='en-US',
                timezone_id='America/New_York',
                proxy={'server': proxy} if proxy else None,
            )
            
            await context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
                window.chrome = {runtime: {}};
            """)
            
            page = await context.new_page()
            await stealth_async(page)
            
            session = BrowserSession(session_id, page, context, "playwright")
            logger.info(f"Playwright session created: {session_id}")
        
        self.sessions[session_id] = session
        return session_id
    
    async def get_session(self, session_id: str) -> Optional[BrowserSession]:
        session = self.sessions.get(session_id)
        if session:
            session.last_activity = asyncio.get_event_loop().time()
        return session
    
    async def close_session(self, session_id: str):
        session = self.sessions.pop(session_id, None)
        if session:
            if session.session_type == "scrapling" and session.scrapling_session:
                session.scrapling_session.__exit__(None, None, None)
            elif session.context:
                await session.context.close()
            logger.info(f"Session closed: {session_id}")
    
    async def navigate(self, session_id: str, url: str, wait_time: int = 5):
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")
        
        if session.session_type == "scrapling":
            page_result = session.scrapling_session.fetch(url, google_search=False)
            await asyncio.sleep(wait_time)
            return {
                "url": url,
                "title": page_result.css('title::text').get() if page_result else "Unknown"
            }
        else:
            await session.page.goto(url, wait_until='domcontentloaded', timeout=30000)
            await asyncio.sleep(wait_time)
            
            return {
                "url": session.page.url,
                "title": await session.page.title()
            }
    
    async def click(self, session_id: str, x: int, y: int):
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")
        
        if session.session_type == "scrapling":
            raise ValueError("Click not supported in Scrapling mode")
        
        await session.page.mouse.click(x, y)
        await asyncio.sleep(1)
        
        return {"success": True}
    
    async def type_text(self, session_id: str, x: int, y: int, text: str):
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")
        
        if session.session_type == "scrapling":
            raise ValueError("Type not supported in Scrapling mode")
        
        await session.page.mouse.click(x, y)
        await asyncio.sleep(0.5)
        await session.page.keyboard.type(text, delay=random.randint(50, 150))
        
        return {"success": True}
    
    async def execute_js(self, session_id: str, script: str):
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")
        
        if session.session_type == "scrapling":
            raise ValueError("Execute JS not supported in Scrapling mode")
        
        result = await session.page.evaluate(script)
        return {"result": result}
    
    async def screenshot(self, session_id: str) -> bytes:
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")
        
        if session.session_type == "scrapling":
            raise ValueError("Screenshot not supported in Scrapling mode")
        
        screenshot = await session.page.screenshot(full_page=False)
        return screenshot
    
    async def get_content(self, session_id: str) -> str:
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")
        
        if session.session_type == "scrapling":
            return "Scrapling content extraction - use CSS/XPath selectors"
        
        content = await session.page.content()
        return content
    
    async def css_selector(self, session_id: str, selector: str) -> Any:
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")
        
        if session.session_type == "scrapling":
            return {"error": "Use Scrapling API directly"}
        
        elements = await session.page.query_selector_all(selector)
        results = []
        for element in elements[:10]:
            text = await element.text_content()
            results.append(text)
        
        return {"results": results}
    
    async def wait(self, session_id: str, seconds: int):
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")
        
        await asyncio.sleep(seconds)
        return {"success": True}
    
    async def scroll(self, session_id: str, direction: str = "down", amount: int = 500):
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")
        
        if session.session_type == "scrapling":
            raise ValueError("Scroll not supported in Scrapling mode")
        
        if direction == "down":
            await session.page.evaluate(f"window.scrollBy(0, {amount})")
        elif direction == "up":
            await session.page.evaluate(f"window.scrollBy(0, -{amount})")
        elif direction == "top":
            await session.page.evaluate("window.scrollTo(0, 0)")
        elif direction == "bottom":
            await session.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        
        await asyncio.sleep(1)
        return {"success": True}
    
    async def cleanup(self):
        for session_id in list(self.sessions.keys()):
            await self.close_session(session_id)
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        logger.info("Browser manager cleaned up")

browser_manager = BrowserManager()
