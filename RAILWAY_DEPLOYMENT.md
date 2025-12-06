# Railway Deployment Guide - Fast & Free

## Why Railway?

✅ **Fast startup** - No cold starts like Render  
✅ **Free tier** - $5 credit/month (enough for small apps)  
✅ **SQLite support** - Works out of the box  
✅ **Quick deployment** - 2-3 minutes  
✅ **Always-on** - No sleeping like Render free tier  

---

## Step-by-Step Deployment

### 1. Push Code to GitHub

```bash
cd /Users/hadia/mvp-cs391
git add .
git commit -m "Ready for Railway deployment"
git push
```

### 2. Deploy on Railway

1. **Go to:** https://railway.app
2. **Sign up** with GitHub (free)
3. **Click "New Project"**
4. **Select "Deploy from GitHub repo"**
5. **Choose your `lawyerconnect-mvp` repository**
6. **Railway auto-detects Python** - it will:
   - Install dependencies from `requirements.txt`
   - Use `Procfile` for start command
   - Deploy automatically

### 3. Set Environment Variables

1. In Railway dashboard → Your project → **Variables** tab
2. Add:
   - `SECRET_KEY` = (generate: `python -c "import secrets; print(secrets.token_hex(32))"`)
   - `DATABASE_URL` = (leave empty for SQLite, or add Postgres if you create one)

### 4. Get Your URL

- Railway gives you a URL like: `https://your-app.up.railway.app`
- Click **Settings** → **Generate Domain** for a custom domain (optional)

### 5. Run Database Setup (One Time)

1. Click **View Logs** in Railway
2. Click **Open Shell** (terminal access)
3. Run:
   ```bash
   python migrate_db_simple.py
   python migrate_db_advanced.py
   python seed_db.py
   ```

**That's it!** Your app is live and fast.

---

## Railway vs Other Platforms

| Platform | Startup Time | Free Tier | SQLite Support | Always-On |
|----------|-------------|-----------|----------------|-----------|
| **Railway** | ⚡ Instant | ✅ $5/month credit | ✅ Yes | ✅ Yes |
| **Render** | 🐌 15-30s (cold start) | ✅ Free | ✅ Yes | ❌ Sleeps after 15min |
| **Fly.io** | ⚡ Fast | ✅ Free | ✅ Yes | ✅ Yes |
| **Vercel** | ⚡ Fast | ✅ Free | ❌ No | ✅ Yes |

**Railway is the best choice** for your needs: fast, free, and works with SQLite.

---

## Railway Free Tier Details

- **$5 credit/month** (free)
- **500 hours** of usage (enough for always-on small app)
- **100GB** bandwidth
- **No credit card required** for free tier

---

## Troubleshooting

**App not starting?**
- Check logs in Railway dashboard
- Ensure `Procfile` has: `web: gunicorn run:app`

**Database issues?**
- Run migrations in Railway shell (see step 5 above)

**Need help?**
- Railway has excellent docs: https://docs.railway.app

