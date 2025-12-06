# Fly.io Deployment Guide - Alternative Fast Option

## Why Fly.io?

✅ **Very fast** - Global edge network  
✅ **Free tier** - 3 shared VMs, 3GB storage  
✅ **SQLite support** - Works perfectly  
✅ **No cold starts** - Always responsive  
✅ **Global CDN** - Fast worldwide  

---

## Quick Deployment (5 minutes)

### 1. Install Fly CLI

```bash
# macOS
curl -L https://fly.io/install.sh | sh

# Or with Homebrew
brew install flyctl
```

### 2. Login

```bash
fly auth login
```

### 3. Initialize Project

```bash
cd /Users/hadia/mvp-cs391
fly launch
```

Follow prompts:
- App name: `lawyerconnect-mvp` (or any name)
- Region: Choose closest to you
- PostgreSQL: **No** (we'll use SQLite)
- Redis: **No**

### 4. Create `fly.toml` (if not auto-generated)

Fly should create this, but if not:

```toml
app = "lawyerconnect-mvp"
primary_region = "iad"

[build]

[env]
  PORT = "8080"

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = false
  auto_start_machines = true
  min_machines_running = 1

[[vm]]
  memory_mb = 256
```

### 5. Update `run.py` for Fly.io

Fly uses port 8080 by default. Update `run.py`:

```python
from app import create_app
import os

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
```

### 6. Deploy

```bash
fly deploy
```

### 7. Set Secrets

```bash
fly secrets set SECRET_KEY="your-secret-key-here"
```

### 8. Get URL

```bash
fly open
```

Or check dashboard: https://fly.io/dashboard

---

## Fly.io Free Tier

- **3 shared VMs** (256MB RAM each)
- **3GB persistent volume** (for SQLite)
- **160GB outbound data transfer**
- **No credit card required**

---

## Comparison: Railway vs Fly.io

| Feature | Railway | Fly.io |
|---------|---------|--------|
| Setup Time | 2-3 min | 5-7 min |
| Startup Speed | ⚡ Instant | ⚡ Instant |
| Free Tier | $5 credit/month | 3 VMs, 3GB storage |
| Ease of Use | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Global CDN | ❌ | ✅ |

**Recommendation:** Railway is easier and faster to set up. Fly.io is great if you need global CDN.

