from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional, Any
import logging

from browser_manager import browser_manager
from config import settings
from api_extended import router as mitm_router
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import WebSocket, WebSocketDisconnect
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Hammer Automation API", version="5.0.0")
app.include_router(mitm_router)

if not os.path.exists("templates"):
    os.makedirs("templates")
templates = Jinja2Templates(directory="templates")

active_websockets = []

class CreateSessionRequest(BaseModel):
    proxy: Optional[str] = None
    use_scrapling: bool = False

class NavigateRequest(BaseModel):
    url: str
    wait_time: int = 5

class ClickRequest(BaseModel):
    x: int
    y: int

class TypeRequest(BaseModel):
    x: int
    y: int
    text: str

class ExecuteJSRequest(BaseModel):
    script: str

class WaitRequest(BaseModel):
    seconds: int

class ScrollRequest(BaseModel):
    direction: str = "down"
    amount: int = 500

class CSSSelectorRequest(BaseModel):
    selector: str

@app.on_event("startup")
async def startup_event():
    await browser_manager.initialize()
    logger.info("Hammer Automation API started")

@app.on_event("shutdown")
async def shutdown_event():
    await browser_manager.cleanup()
    logger.info("Hammer Automation API shut down")

@app.get("/")
async def root():
    return HTMLResponse(content="""
<!DOCTYPE html>
<html>
<head>
    <title>Hammer Automation</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        .header h1 {
            font-size: 48px;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        .header p {
            font-size: 18px;
            opacity: 0.9;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            padding: 40px;
            background: #f8f9fa;
        }
        .stat-card {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s;
        }
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }
        .stat-value {
            font-size: 48px;
            font-weight: bold;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }
        .stat-label {
            font-size: 16px;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .content {
            padding: 40px;
        }
        .section {
            margin-bottom: 40px;
        }
        .section h2 {
            font-size: 32px;
            margin-bottom: 20px;
            color: #333;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }
        .feature-card {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }
        .feature-card h3 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 20px;
        }
        .feature-card ul {
            list-style: none;
            padding-left: 0;
        }
        .feature-card li {
            padding: 5px 0;
            color: #666;
        }
        .feature-card li:before {
            content: "✓ ";
            color: #667eea;
            font-weight: bold;
            margin-right: 8px;
        }
        .endpoints {
            display: grid;
            gap: 15px;
        }
        .endpoint {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
            transition: all 0.3s;
        }
        .endpoint:hover {
            background: #e9ecef;
            transform: translateX(5px);
        }
        .method {
            display: inline-block;
            padding: 6px 14px;
            border-radius: 6px;
            font-weight: bold;
            margin-right: 15px;
            font-size: 14px;
        }
        .post {background: #28a745; color: white;}
        .get {background: #007bff; color: white;}
        .delete {background: #dc3545; color: white;}
        code {
            background: #e9ecef;
            padding: 4px 8px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
        }
        .footer {
            background: #333;
            color: white;
            text-align: center;
            padding: 30px;
            margin-top: 40px;
        }
        .footer a {
            color: #667eea;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔨 Hammer Automation</h1>
            <p>Universal Browser Automation API with Advanced Cloudflare/CAPTCHA Bypass</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value" id="sessions">0</div>
                <div class="stat-label">Active Sessions</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">✅</div>
                <div class="stat-label">Status: Online</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">∞</div>
                <div class="stat-label">Supported Sites</div>
            </div>
        </div>
        
        <div class="content">
            <div class="section">
                <h2>🚀 Features</h2>
                <div class="features">
                    <div class="feature-card">
                        <h3>Anti-Bot Bypass</h3>
                        <ul>
                            <li>Cloudflare Turnstile</li>
                            <li>hCaptcha & reCAPTCHA</li>
                            <li>Canvas/WebGL fingerprinting</li>
                            <li>TLS fingerprint spoofing</li>
                        </ul>
                    </div>
                    <div class="feature-card">
                        <h3>Browser Automation</h3>
                        <ul>
                            <li>Playwright + Stealth mode</li>
                            <li>Scrapling integration</li>
                            <li>Session management</li>
                            <li>Proxy support</li>
                        </ul>
                    </div>
                    <div class="feature-card">
                        <h3>Advanced Actions</h3>
                        <ul>
                            <li>Click at coordinates</li>
                            <li>Type with human delays</li>
                            <li>Execute JavaScript</li>
                            <li>Scroll & navigation</li>
                        </ul>
                    </div>
                    <div class="feature-card">
                        <h3>Data Extraction</h3>
                        <ul>
                            <li>CSS selectors</li>
                            <li>XPath selectors</li>
                            <li>Screenshot capture</li>
                            <li>HTML content export</li>
                        </ul>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>📡 API Endpoints</h2>
                <div class="endpoints">
                    <div class="endpoint">
                        <span class="method post">POST</span>
                        <code>/session/create</code>
                        <p>Create new browser session (Playwright or Scrapling)</p>
                    </div>
                    <div class="endpoint">
                        <span class="method post">POST</span>
                        <code>/session/{id}/navigate</code>
                        <p>Navigate to URL with automatic Cloudflare bypass</p>
                    </div>
                    <div class="endpoint">
                        <span class="method post">POST</span>
                        <code>/session/{id}/click</code>
                        <p>Click at specific coordinates (x, y)</p>
                    </div>
                    <div class="endpoint">
                        <span class="method post">POST</span>
                        <code>/session/{id}/type</code>
                        <p>Type text with human-like delays</p>
                    </div>
                    <div class="endpoint">
                        <span class="method post">POST</span>
                        <code>/session/{id}/execute</code>
                        <p>Execute JavaScript code</p>
                    </div>
                    <div class="endpoint">
                        <span class="method post">POST</span>
                        <code>/session/{id}/scroll</code>
                        <p>Scroll page (up/down/top/bottom)</p>
                    </div>
                    <div class="endpoint">
                        <span class="method post">POST</span>
                        <code>/session/{id}/css</code>
                        <p>Extract data using CSS selectors</p>
                    </div>
                    <div class="endpoint">
                        <span class="method get">GET</span>
                        <code>/session/{id}/screenshot</code>
                        <p>Capture page screenshot</p>
                    </div>
                    <div class="endpoint">
                        <span class="method get">GET</span>
                        <code>/session/{id}/content</code>
                        <p>Get HTML content</p>
                    </div>
                    <div class="endpoint">
                        <span class="method post">POST</span>
                        <code>/session/{id}/wait</code>
                        <p>Wait for specified seconds</p>
                    </div>
                    <div class="endpoint">
                        <span class="method delete">DELETE</span>
                        <code>/session/{id}</code>
                        <p>Close browser session</p>
                    </div>
                    <div class="endpoint">
                        <span class="method get">GET</span>
                        <code>/docs</code>
                        <p>Interactive API documentation (Swagger UI)</p>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>Hammer Automation v2.0.0 | <a href="/docs">API Documentation</a></p>
            <p>Universal automation for any website, any task</p>
        </div>
    </div>
    
    <script>
        async function updateStats() {
            try {
                const response = await fetch('/stats');
                const data = await response.json();
                document.getElementById('sessions').textContent = data.active_sessions;
            } catch (error) {
                console.error('Failed to update stats:', error);
            }
        }
        
        updateStats();
        setInterval(updateStats, 5000);
    </script>
</body>
</html>
    """)

@app.get("/stats")
async def get_stats():
    return {
        "active_sessions": len(browser_manager.sessions),
        "scrapling_available": True
    }

@app.post("/session/create")
async def create_session(request: CreateSessionRequest):
    try:
        session_id = await browser_manager.create_session(request.proxy, request.use_scrapling)
        return {
            "session_id": session_id,
            "status": "created",
            "type": "scrapling" if request.use_scrapling else "playwright"
        }
    except Exception as e:
        logger.error(f"Failed to create session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/session/{session_id}/navigate")
async def navigate(session_id: str, request: NavigateRequest):
    try:
        result = await browser_manager.navigate(session_id, request.url, request.wait_time)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Navigation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/session/{session_id}/click")
async def click(session_id: str, request: ClickRequest):
    try:
        result = await browser_manager.click(session_id, request.x, request.y)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Click failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/session/{session_id}/type")
async def type_text(session_id: str, request: TypeRequest):
    try:
        result = await browser_manager.type_text(session_id, request.x, request.y, request.text)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Type failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/session/{session_id}/execute")
async def execute_js(session_id: str, request: ExecuteJSRequest):
    try:
        result = await browser_manager.execute_js(session_id, request.script)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Execute JS failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/session/{session_id}/scroll")
async def scroll(session_id: str, request: ScrollRequest):
    try:
        result = await browser_manager.scroll(session_id, request.direction, request.amount)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Scroll failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/session/{session_id}/css")
async def css_selector(session_id: str, request: CSSSelectorRequest):
    try:
        result = await browser_manager.css_selector(session_id, request.selector)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"CSS selector failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/session/{session_id}/screenshot")
async def screenshot(session_id: str):
    try:
        screenshot_bytes = await browser_manager.screenshot(session_id)
        return Response(content=screenshot_bytes, media_type="image/png")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Screenshot failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/session/{session_id}/content")
async def get_content(session_id: str):
    try:
        content = await browser_manager.get_content(session_id)
        return {"content": content}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Get content failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/session/{session_id}/wait")
async def wait(session_id: str, request: WaitRequest):
    try:
        result = await browser_manager.wait(session_id, request.seconds)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Wait failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/session/{session_id}")
async def close_session(session_id: str):
    try:
        await browser_manager.close_session(session_id)
        return {"status": "closed"}
    except Exception as e:
        logger.error(f"Close session failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
