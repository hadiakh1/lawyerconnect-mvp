# Quick Vercel Deployment Guide

## ⚠️ Important Warning

**Vercel does NOT support SQLite databases** (read-only filesystem). Your app will NOT work with SQLite on Vercel.

**You have 2 options:**

### Option A: Use External Database (Required for Vercel)

1. **Set up a free PostgreSQL database:**
   - Go to https://supabase.com (free tier)
   - Create a new project
   - Copy the connection string

2. **Update your code:**
   - Your `requirements.txt` already has `psycopg2-binary`
   - Set `DATABASE_URL` environment variable in Vercel

3. **Deploy:**
   ```bash
   npm install -g vercel
   vercel login
   vercel
   ```

### Option B: Use Render/Railway (Recommended - Works with SQLite)

**Render is already set up and working!** Just continue using Render.

---

## If You Still Want Vercel

### Step-by-Step Deployment

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Login:**
   ```bash
   vercel login
   ```

3. **Navigate to project:**
   ```bash
   cd /Users/hadia/mvp-cs391
   ```

4. **Deploy:**
   ```bash
   vercel
   ```
   - Follow prompts
   - Link to existing project or create new one

5. **Set Environment Variables:**
   - Go to https://vercel.com/dashboard
   - Select your project
   - Settings → Environment Variables
   - Add:
     - `SECRET_KEY`: (generate with `python -c "import secrets; print(secrets.token_hex(32))"`)
     - `DATABASE_URL`: Your external database URL (PostgreSQL, MySQL, etc.)

6. **Redeploy:**
   ```bash
   vercel --prod
   ```

---

## Why Render is Better for This App

✅ **Render (Current Setup):**
- Works with SQLite out of the box
- Persistent file storage
- Already deployed and working
- Free tier available
- Perfect for Flask apps

❌ **Vercel:**
- No SQLite support
- Requires external database
- More complex setup
- Better for serverless/static sites

---

## Recommendation

**Stick with Render** - it's already working and better suited for your Flask + SQLite app.

If you need Vercel for a specific reason, you'll need to:
1. Set up external database (Supabase, PlanetScale, etc.)
2. Update `DATABASE_URL` environment variable
3. Run migrations on the external database

