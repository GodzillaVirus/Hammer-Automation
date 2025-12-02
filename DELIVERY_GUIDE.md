# 🔨 Hammer Automation API - دليل التسليم النهائي

## 📦 نظرة عامة

**Hammer Automation** هو API متطور وشامل للأتمتة الكاملة للمتصفح مع قدرات متقدمة لتخطي Cloudflare وCAPTCHA.

---

## ✨ الميزات الرئيسية

### 1. **Browser Automation (أتمتة المتصفح)**
- ✅ Playwright + Playwright Stealth
- ✅ Scrapling Integration
- ✅ Undetected ChromeDriver
- ✅ Anti-detection techniques

### 2. **Cloudflare & CAPTCHA Bypass**
- ✅ Cloudflare Turnstile
- ✅ hCaptcha
- ✅ reCAPTCHA v2/v3
- ✅ Image CAPTCHA (OCR)

### 3. **MITM Proxy (اعتراض الاتصالات)**
- ✅ Request/Response interception
- ✅ Header modification
- ✅ SSL certificate handling
- ✅ Traffic recording

### 4. **Advanced Features**
- ✅ Rate Limit Bypass (Proxy rotation, User-Agent rotation)
- ✅ Fingerprint spoofing
- ✅ WebSocket Live Stream
- ✅ Dashboard للمراقبة
- ✅ Telegram Bot للتحكم

### 5. **Browser Actions**
- Navigate, Click, Type
- Scroll, Screenshot
- Execute JavaScript
- CSS/XPath selectors
- Drag & Drop
- Key Press
- File Upload

---

## 🔗 الروابط

- **GitHub Repository:** https://github.com/GodzillaVirus/Hammer-Automation
- **Local API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Dashboard:** http://localhost:8000/dashboard

---

## 📋 المتطلبات

```bash
Python 3.11+
pip3
playwright
```

---

## 🚀 التثبيت والتشغيل

### 1. استنساخ المشروع

```bash
git clone https://github.com/GodzillaVirus/Hammer-Automation.git
cd Hammer-Automation
```

### 2. تثبيت المكتبات

```bash
pip3 install -r requirements.txt
playwright install chromium
```

### 3. إعداد المتغيرات البيئية

```bash
cp .env.example .env
nano .env
```

أضف:
```
TELEGRAM_BOT_TOKEN=8563563429:AAGLW_hCpbeC2-JfStd_bveMWiBsaTaOh-E
TELEGRAM_CHAT_ID=5328767896
```

### 4. تشغيل الخادم

```bash
python3 main.py
```

أو مع sudo:
```bash
sudo python3 main.py
```

---

## 🧪 الاختبار

### اختبار سريع

```bash
curl http://localhost:8000/stats
```

### اختبار شامل

```bash
python3 test_full.py
```

---

## 📡 استخدام API

### 1. إنشاء جلسة

```bash
curl -X POST http://localhost:8000/session/create
```

Response:
```json
{
  "session_id": "abc123...",
  "status": "created"
}
```

### 2. فتح صفحة

```bash
curl -X POST http://localhost:8000/browser/open \
  -H "Content-Type: application/json" \
  -d '{"session_id": "abc123", "url": "https://example.com"}'
```

### 3. النقر على إحداثيات

```bash
curl -X POST http://localhost:8000/browser/click \
  -H "Content-Type: application/json" \
  -d '{"session_id": "abc123", "x": 500, "y": 300}'
```

### 4. كتابة نص

```bash
curl -X POST http://localhost:8000/browser/type \
  -H "Content-Type: application/json" \
  -d '{"session_id": "abc123", "x": 500, "y": 300, "text": "Hello"}'
```

### 5. أخذ screenshot

```bash
curl -X POST http://localhost:8000/browser/screenshot \
  -H "Content-Type: application/json" \
  -d '{"session_id": "abc123"}'
```

### 6. تنفيذ JavaScript

```bash
curl -X POST http://localhost:8000/browser/execute_js \
  -H "Content-Type: application/json" \
  -d '{"session_id": "abc123", "script": "document.title"}'
```

### 7. إغلاق الجلسة

```bash
curl -X POST http://localhost:8000/session/close \
  -H "Content-Type: application/json" \
  -d '{"session_id": "abc123"}'
```

---

## 🎯 استخدام MITM Proxy

### تفعيل MITM

```bash
curl -X POST http://localhost:8000/mitm/start
```

### اعتراض طلب

```bash
curl -X POST http://localhost:8000/mitm/intercept \
  -H "Content-Type: application/json" \
  -d '{
    "url_pattern": "example.com",
    "modify_headers": {"User-Agent": "Custom"}
  }'
```

### إيقاف MITM

```bash
curl -X POST http://localhost:8000/mitm/stop
```

---

## 🤖 Telegram Bot

### الأوامر المتاحة

- `/start` - بدء البوت
- `/status` - حالة API
- `/create_session` - إنشاء جلسة جديدة
- `/list_sessions` - عرض الجلسات النشطة
- `/close_session <id>` - إغلاق جلسة

---

## 🌐 النشر على Railway

### 1. ربط GitHub

افتح https://railway.com/new/github واختر `Hammer-Automation`

### 2. إضافة Environment Variables

```
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID=...
```

### 3. Generate Domain

اضغط على "Generate Domain" للحصول على رابط عام

### 4. الوصول للـ API

```
https://your-app.up.railway.app/
```

---

## 📚 الميزات المتقدمة

### 1. Scrapling Mode

```python
session_id = create_session(use_scrapling=True)
```

### 2. Proxy Rotation

```python
session_id = create_session(proxy="http://proxy:port")
```

### 3. Custom User-Agent

يتم تبديل User-Agent تلقائياً من قائمة محددة

### 4. Anti-Detection

جميع الجلسات تستخدم:
- Playwright Stealth
- Custom fingerprints
- Random delays
- Human-like behavior

---

## 🔧 الصيانة

### إعادة تشغيل الخادم

```bash
pkill -f "python3 main.py"
python3 main.py
```

### تحديث المشروع

```bash
git pull origin main
pip3 install -r requirements.txt --upgrade
```

### فحص Logs

```bash
tail -f server.log
```

---

## 📊 الإحصائيات

```bash
curl http://localhost:8000/stats
```

Response:
```json
{
  "active_sessions": 3,
  "total_requests": 1250,
  "uptime": "2h 30m"
}
```

---

## ⚠️ ملاحظات مهمة

1. **Playwright Browsers:** يجب تثبيت Chromium قبل التشغيل
2. **Permissions:** قد تحتاج sudo لبعض العمليات
3. **Railway Limits:** الخطة المجانية محدودة
4. **MITM Proxy:** يحتاج صلاحيات إضافية

---

## 🐛 حل المشاكل

### المشكلة: Playwright not found

```bash
playwright install chromium
```

### المشكلة: Permission denied

```bash
sudo python3 main.py
```

### المشكلة: Port already in use

```bash
lsof -ti:8000 | xargs kill -9
```

---

## 📞 الدعم

- **GitHub Issues:** https://github.com/GodzillaVirus/Hammer-Automation/issues
- **Telegram:** @YourUsername

---

## 📄 الترخيص

MIT License - استخدم المشروع بحرية!

---

## 🎉 الخلاصة

**Hammer Automation** جاهز للاستخدام الفوري مع جميع الميزات المطلوبة:

✅ Browser Automation
✅ Cloudflare Bypass
✅ MITM Proxy
✅ Dashboard
✅ Telegram Bot
✅ API Documentation
✅ Ready for Railway

**استمتع بالأتمتة القوية! 🚀**
