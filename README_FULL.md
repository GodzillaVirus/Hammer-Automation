# 🔨 Hammer Automation API

**Universal Browser Automation & Traffic Interception Platform**

Advanced automation API with Cloudflare/CAPTCHA bypass, MITM proxy, and comprehensive browser control.

---

## 🌟 Features

### 🛡️ Anti-Bot & CAPTCHA Bypass
- ✅ **Cloudflare Turnstile** - Automatic bypass
- ✅ **hCaptcha & reCAPTCHA** - Advanced solving
- ✅ **Canvas/WebGL Fingerprinting** - Complete spoofing
- ✅ **TLS Fingerprint** - Impersonation
- ✅ **Rate Limit Bypass** - Smart throttling & proxy rotation

### 🚀 Browser Automation
- ✅ **Playwright** - Full browser control with stealth mode
- ✅ **Scrapling** - Advanced web scraping with built-in Cloudflare bypass
- ✅ **Undetected Chrome** - Maximum stealth
- ✅ **Session Management** - Persistent sessions with cookie support
- ✅ **Proxy Support** - Rotating proxies with authentication
- ✅ **Multi-tasking** - Handle multiple sessions simultaneously

### 🔍 MITM Proxy (NEW!)
- ✅ **Traffic Interception** - Intercept all HTTP/HTTPS requests
- ✅ **Request Modification** - Modify requests on-the-fly
- ✅ **Response Modification** - Alter responses before delivery
- ✅ **URL Blocking** - Block specific URLs or patterns
- ✅ **Traffic Recording** - Record and replay traffic
- ✅ **Rule-based Filtering** - Advanced filtering rules

### 📊 Dashboard & Monitoring
- ✅ **Live Dashboard** - Real-time monitoring interface
- ✅ **WebSocket Stream** - Live activity updates
- ✅ **Traffic Viewer** - View intercepted requests/responses
- ✅ **Session Manager** - Manage all active sessions
- ✅ **Performance Metrics** - Monitor API performance

### 🎯 Browser Actions
- ✅ Navigate to any URL
- ✅ Click at coordinates or selectors
- ✅ Type text with human-like delays
- ✅ Execute JavaScript
- ✅ Scroll (up/down/to element)
- ✅ Take screenshots
- ✅ Extract data with CSS/XPath
- ✅ Upload files
- ✅ Handle dialogs
- ✅ Drag & drop
- ✅ Hover actions
- ✅ Key press simulation

### 🤖 Telegram Bot
- ✅ Monitor API status
- ✅ View active sessions
- ✅ Remote control
- ✅ Receive notifications

---

## 📦 Installation

### Local Development

```bash
pip install -r requirements.txt
playwright install chromium
python main.py
```

### Docker

```bash
docker build -t hammer-automation .
docker run -p 8000:8000 hammer-automation
```

### Railway Deployment

1. Fork this repository
2. Connect to Railway
3. Deploy automatically

---

## 🔧 Usage

### Create Session

```bash
curl -X POST http://localhost:8000/session/create \
  -H "Content-Type: application/json" \
  -d '{"use_scrapling": false, "proxy": "http://proxy:port"}'
```

### Navigate to URL

```bash
curl -X POST http://localhost:8000/session/{session_id}/navigate \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "wait_time": 5}'
```

### MITM Proxy - Start

```bash
curl -X POST http://localhost:8000/mitm/start \
  -H "Content-Type: application/json" \
  -d '{"port": 8080}'
```

### MITM Proxy - Add Intercept Rule

```bash
curl -X POST http://localhost:8000/mitm/intercept/add \
  -H "Content-Type: application/json" \
  -d '{
    "url_pattern": ".*api.*",
    "response_modify": {
      "status_code": 200,
      "headers": {"X-Custom": "Modified"}
    }
  }'
```

### MITM Proxy - Block URL

```bash
curl -X POST http://localhost:8000/mitm/block/add \
  -H "Content-Type: application/json" \
  -d '{"url_pattern": ".*ads.*"}'
```

### MITM Proxy - View Traffic

```bash
curl http://localhost:8000/mitm/requests?limit=50
curl http://localhost:8000/mitm/responses?limit=50
```

---

## 🌐 API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI).

Visit `http://localhost:8000/dashboard` for live monitoring dashboard.

---

## 🛠️ Technologies

- **FastAPI** - Modern web framework
- **Playwright** - Browser automation
- **Scrapling** - Advanced web scraping
- **mitmproxy** - Traffic interception
- **playwright-stealth** - Anti-detection
- **python-telegram-bot** - Telegram integration
- **WebSockets** - Real-time communication
- **Redis** - Session storage (optional)
- **Celery** - Task queue (optional)

---

## 🎯 Use Cases

- ✅ Web scraping any website
- ✅ Automated testing
- ✅ Data extraction
- ✅ Form submission
- ✅ Account creation
- ✅ Price monitoring
- ✅ API testing
- ✅ Traffic analysis
- ✅ Security testing
- ✅ Bot development

---

## 🔐 Environment Variables

Create `.env` file:

```env
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
PORT=8000
HOST=0.0.0.0
REDIS_URL=redis://localhost:6379
```

---

## 📊 Performance

- ⚡ Fast response times
- 🔋 Memory efficient
- 🚀 Handles 100+ concurrent sessions
- 💪 Production-ready
- 🛡️ Built-in rate limiting

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

MIT License

---

## 🔗 Links

- [API Documentation](http://localhost:8000/docs)
- [Live Dashboard](http://localhost:8000/dashboard)
- [Scrapling GitHub](https://github.com/D4Vinci/Scrapling)
- [Playwright Documentation](https://playwright.dev)

---

**Made with ❤️ by Hammer Automation Team**
