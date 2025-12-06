# Vercel Deployment - Free but Requires External Database

## ✅ Yes, Vercel is FREE!

Vercel has a generous free tier:
- ✅ Unlimited deployments
- ✅ Free SSL certificates
- ✅ Global CDN
- ✅ Serverless functions
- ✅ No credit card required

## ⚠️ BUT: Vercel Doesn't Support SQLite

**The Problem:**
- Vercel's filesystem is **read-only**
- SQLite needs to write to disk
- Your database will **reset on every deployment**

**The Solution:**
You **MUST** use an external database (PostgreSQL, MySQL, etc.)

---

## Option 1: Use Free PostgreSQL (Recommended)

### Step 1: Get Free PostgreSQL Database

**Option A: Supabase (Recommended)**
1. Go to https://supabase.com
2. Sign up (free)
3. Create new project
4. Go to **Settings** → **Database**
5. Copy the **Connection String** (looks like: `postgresql://...`)

**Option B: Neon (Alternative)**
1. Go to https://neon.tech
2. Sign up (free)
3. Create database
4. Copy connection string

### Step 2: Update Your Code

Your `app/config.py` already supports `DATABASE_URL` from environment variables, so it will work automatically!

### Step 3: Deploy to Vercel

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Login:**
   ```bash
   vercel login
   ```

3. **Deploy:**
   ```bash
   cd /Users/hadia/mvp-cs391
   vercel
   ```
   - Follow prompts
   - Link to existing project or create new

4. **Set Environment Variables:**
   - Go to https://vercel.com/dashboard
   - Your project → **Settings** → **Environment Variables**
   - Add:
     - `SECRET_KEY`: `python -c "import secrets; print(secrets.token_hex(32))"`
     - `DATABASE_URL`: Your Supabase/Neon PostgreSQL connection string

5. **Redeploy:**
   ```bash
   vercel --prod
   ```

### Step 4: Run Migrations

You'll need to run database migrations. Options:

**Option A: Add Migration Endpoint (Temporary)**
Add a route in `app/routes.py`:
```python
@main_bp.route("/admin/migrate", methods=["POST"])
def migrate_db():
    # Run migrations
    from migrate_db_advanced import migrate_database
    migrate_database()
    return "Migrations complete"
```

Then visit: `https://your-app.vercel.app/admin/migrate` (once, then remove)

**Option B: Use Vercel CLI**
```bash
vercel env pull .env.local
# Then run migrations locally pointing to production DB
```

**Option C: Use Supabase SQL Editor**
- Go to Supabase dashboard → SQL Editor
- Run SQL commands to create tables

---

## Option 2: Use Railway (Easier - No External DB Needed)

If you don't want to set up an external database, **Railway is easier**:
- ✅ Works with SQLite out of the box
- ✅ Free tier ($5 credit/month)
- ✅ No external database setup needed
- ✅ 2-3 minute deployment

See `RAILWAY_DEPLOYMENT.md` for Railway setup.

---

## Comparison: Vercel vs Railway

| Feature | Vercel | Railway |
|---------|--------|---------|
| **Free Tier** | ✅ Yes | ✅ Yes ($5 credit) |
| **SQLite Support** | ❌ No | ✅ Yes |
| **External DB Required** | ✅ Yes | ❌ No |
| **Setup Time** | 10-15 min | 2-3 min |
| **Startup Speed** | ⚡ Fast | ⚡ Fast |
| **Best For** | Static/Next.js | Flask + SQLite |

---

## My Recommendation

**For your Flask + SQLite app:**
- **Railway** is easier and faster (no external DB setup)
- **Vercel** works but requires external database setup

**Choose Vercel if:**
- You want to learn PostgreSQL
- You need Vercel's global CDN
- You're planning to scale beyond SQLite

**Choose Railway if:**
- You want the fastest setup
- You want to keep using SQLite
- You want the simplest deployment

---

## Quick Start: Vercel + Supabase

1. **Create Supabase project** (2 minutes)
2. **Copy connection string**
3. **Deploy to Vercel:**
   ```bash
   vercel
   ```
4. **Set `DATABASE_URL` in Vercel dashboard**
5. **Run migrations** (see Step 4 above)
6. **Done!**

Both are free, but Railway is simpler for your current setup.

