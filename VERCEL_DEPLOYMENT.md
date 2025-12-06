# Vercel Deployment Guide for LawyerConnect

## Important Note

**Vercel is primarily designed for serverless functions and static sites.** Flask apps with SQLite databases have limitations on Vercel:

1. **SQLite files are read-only** on Vercel (ephemeral filesystem)
2. **No persistent storage** - database resets on each deployment
3. **Better alternatives**: Render, Railway, Heroku, or AWS

However, if you still want to deploy on Vercel, follow these steps:

---

## Option 1: Deploy with External Database (Recommended)

### Step 1: Set up External Database

Use a managed database service:
- **Supabase** (PostgreSQL) - Free tier available
- **PlanetScale** (MySQL) - Free tier available
- **MongoDB Atlas** - Free tier available

### Step 2: Update Database Configuration

1. Get your database connection string
2. Update `app/config.py` to use the external database URL
3. Update `requirements.txt` to include the appropriate driver (e.g., `psycopg2-binary` for PostgreSQL)

### Step 3: Deploy to Vercel

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel:**
   ```bash
   vercel login
   ```

3. **Deploy:**
   ```bash
   vercel
   ```

4. **Set Environment Variables:**
   - Go to Vercel Dashboard → Your Project → Settings → Environment Variables
   - Add:
     - `SECRET_KEY` - Your Flask secret key
     - `DATABASE_URL` - Your external database connection string

5. **Redeploy:**
   ```bash
   vercel --prod
   ```

---

## Option 2: Alternative Deployment Platforms (Better for Flask + Database)

### Render (Recommended)

1. Push code to GitHub
2. Go to https://render.com
3. New → Web Service
4. Connect GitHub repo
5. Set:
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn run:app`
6. Add environment variables
7. Deploy

### Railway

1. Push code to GitHub
2. Go to https://railway.app
3. New Project → Deploy from GitHub
4. Add PostgreSQL database (optional)
5. Set environment variables
6. Deploy

---

## Current Vercel Setup Files

The following files have been created for Vercel:

- `vercel.json` - Vercel configuration
- `api/index.py` - Serverless function entry point

**Note:** The current setup uses SQLite which won't work properly on Vercel. You need to switch to an external database.

---

## Quick Start (If Using External Database)

1. **Update `app/config.py`:**
   ```python
   SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "your-external-db-url")
   ```

2. **Deploy:**
   ```bash
   vercel
   ```

3. **Set environment variables in Vercel dashboard**

4. **Run migrations:**
   - You'll need to run migrations manually or via a script
   - Consider adding a migration endpoint or using a one-time script

---

## Recommendation

For a Flask app with a database, **Render or Railway are better choices** than Vercel because:
- ✅ Persistent file storage
- ✅ SQLite works out of the box
- ✅ Easier database management
- ✅ Better for Python/Flask apps
- ✅ Free tiers available

Vercel is excellent for:
- Static sites
- Next.js apps
- Serverless APIs without persistent storage

