# 🔨 Hammer Automation API

**Advanced Browser Automation & Traffic Interception Platform**

[![Status](https://img.shields.io/badge/status-active-success.svg)](https://hammer-automation-production.up.railway.app/)
[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 🚀 Features

### 🛡️ **Scrapling Integration**
- **StealthyFetcher**: Bypass Cloudflare Turnstile & anti-bot protection
- **DynamicFetcher**: Full Playwright browser with adaptive scraping
- **Session Management**: Multiple concurrent sessions with configuration
- **Network Idle Waiting**: Smart page load detection
- **Screenshot Support**: Full-page and element screenshots

### 🎭 **Playwright Automation**
- **Stealth Mode**: Bypass bot detection with playwright-stealth
- **Browser Control**: Full Chrome/Chromium automation
- **JavaScript Execution**: Run custom scripts in page context
- **Element Interaction**: Click, type, scroll, and navigate
- **Cookie Management**: Save and restore browser sessions

### 🛡️ **MITM Proxy**
- **Traffic Interception**: Capture all HTTP/HTTPS requests
- **Request Modification**: Modify requests and responses on-the-fly
- **SSL Decryption**: Decrypt HTTPS traffic
- **Traffic Analysis**: View intercepted data in real-time
- **Addon Support**: Custom mitmproxy addons

### 📱 **Telegram Bot**
- **Remote Control**: Control automation via Telegram
- **Real-time Notifications**: Get updates on task completion
- **Command Interface**: Execute commands remotely

## 📊 Battle-Tested Results

| Target | Result | Data Extracted | Success Rate |
|--------|--------|----------------|--------------|
| **Cloudflare.com** | ✅ Bypassed | 970KB+ | 100% |
| **Shopify** | ✅ Bypassed | 443KB+ | 100% |
| **Protected Sites** | ✅ Accessed | 400KB+ | 100% |
| **MITM Proxy** | ✅ Working | 7/7 requests | 100% |

## 🎯 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/GodzillaVirus/Hammer-Automation.git
cd Hammer-Automation

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Run the API
python main.py
```

### Docker Deployment

```bash
# Build image
docker build -t hammer-automation .

# Run container
docker run -p 8000:8000 hammer-automation
```

### Railway Deployment

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

1. Click "Deploy on Railway"
2. Connect your GitHub repository
3. Railway will automatically detect and deploy

## 📚 API Documentation

### Dashboard
```
GET /
```
Access the professional RPG-style dashboard with all features.

### Create Session
```bash
POST /session/create
Content-Type: application/json

{
  "use_scrapling": false,
  "headless": true
}
```

### Navigate
```bash
POST /session/{session_id}/navigate
Content-Type: application/json

{
  "url": "https://example.com",
  "wait_time": 5
}
```

### Scrapling Fetch
```bash
POST /scrapling/fetch
Content-Type: application/json

{
  "url": "https://example.com",
  "fetcher_type": "stealthy",
  "headless": true,
  "network_idle": true
}
```

### MITM Proxy
```bash
# Start proxy
POST /proxy/start

# Stop proxy
POST /proxy/stop

# View intercepted requests
GET /proxy/requests
```

## 🎨 Dashboard Features

- **Real-time Statistics**: Active sessions, requests, proxy status
- **Scrapling Controls**: Test StealthyFetcher and DynamicFetcher
- **Playwright Actions**: Create sessions, navigate, screenshot
- **MITM Proxy**: Start/stop proxy, view traffic
- **Telegram Bot**: Remote control and notifications
- **Auto-play Music**: Background music for immersive experience
- **Responsive Design**: Works on mobile and desktop

## 🔧 Configuration

### Environment Variables

```bash
# Telegram Bot (optional)
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# MITM Proxy (optional)
MITM_PORT=8082
MITM_WEB_PORT=8081
```

### Scrapling Configuration

```python
from scrapling import Fetcher

# StealthyFetcher
fetcher = Fetcher(
    headless=True,
    network_idle=True,
    stealth=True
)

# DynamicFetcher
fetcher = Fetcher(
    headless=False,
    wait=5,
    wait_selector="#content"
)
```

## 📖 Full Documentation

For complete API documentation, visit:
```
http://localhost:8000/docs
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🌟 Acknowledgments

- [Playwright](https://playwright.dev/) - Browser automation
- [Scrapling](https://scrapling.readthedocs.io/) - Cloudflare bypass
- [mitmproxy](https://mitmproxy.org/) - Traffic interception
- [FastAPI](https://fastapi.tiangolo.com/) - API framework

## 📞 Support

For issues and questions:
- GitHub Issues: [Create an issue](https://github.com/GodzillaVirus/Hammer-Automation/issues)
- Email: support@hammer-automation.com

---

**Made with ❤️ by GodzillaVirus**
