# Complete Vercel Deployment Guide with Database Setup

## Overview

This guide will walk you through:
1. Setting up a **free PostgreSQL database** (Supabase)
2. Deploying your Flask app to **Vercel**
3. Connecting the database
4. Running migrations and seeding data

**Total time: ~15-20 minutes**

---

## Part 1: Set Up Free PostgreSQL Database (Supabase)

### Step 1: Create Supabase Account

1. Go to **https://supabase.com**
2. Click **"Start your project"** or **"Sign up"**
3. Sign up with GitHub (easiest) or email
4. Verify your email if needed

### Step 2: Create New Project

1. Click **"New Project"**
2. Fill in:
   - **Name**: `lawyerconnect-db` (or any name)
   - **Database Password**: Create a strong password (save it!)
   - **Region**: Choose closest to you (e.g., `US East`)
3. Click **"Create new project"**
4. Wait 2-3 minutes for project to initialize

### Step 3: Get Database Connection String

1. Once project is ready, go to **Settings** (gear icon) → **Database**
2. Scroll down to **"Connection string"**
3. Select **"URI"** tab
4. Copy the connection string (looks like):
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
   ```
5. **Replace `[YOUR-PASSWORD]`** with the password you created in Step 2
6. **Save this connection string** - you'll need it for Vercel

**Example:**
```
postgresql://postgres:mypassword123@db.abcdefgh.supabase.co:5432/postgres
```

---

## Part 2: Update Code for PostgreSQL (If Needed)

### Check Your Models

Your code should already work with PostgreSQL! SQLAlchemy handles both SQLite and PostgreSQL.

However, we need to ensure the database URL format is correct. Your `app/config.py` already supports `DATABASE_URL` from environment variables, so you're good!

### Optional: Update Connection String Format

Vercel/Supabase might provide the connection string in a different format. If you get connection errors, you can update `app/config.py`:

```python
# In app/config.py
SQLALCHEMY_DATABASE_URI = os.environ.get(
    "DATABASE_URL",
    f"sqlite:///{os.path.join(BASE_DIR, 'lawyerconnect.db')}",
).replace("postgres://", "postgresql://")  # Fix for some providers
```

But try without this first - it should work as-is.

---

## Part 3: Deploy to Vercel

### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

If you don't have Node.js:
- **macOS**: `brew install node`
- **Or download**: https://nodejs.org

### Step 2: Login to Vercel

```bash
vercel login
```

- Choose **"Continue with GitHub"** (easiest)
- Authorize Vercel in browser

### Step 3: Navigate to Project

```bash
cd /Users/hadia/mvp-cs391
```

### Step 4: Deploy

```bash
vercel
```

Follow the prompts:
- **Set up and deploy?** → `Y`
- **Which scope?** → Select your account
- **Link to existing project?** → `N` (first time) or `Y` (if updating)
- **Project name?** → `lawyerconnect-mvp` (or press Enter for default)
- **Directory?** → `.` (current directory, press Enter)
- **Override settings?** → `N`

Vercel will:
- Detect Python
- Install dependencies
- Build your app
- Deploy

You'll get a URL like: `https://lawyerconnect-mvp-xxxxx.vercel.app`

### Step 5: Set Environment Variables

1. Go to **https://vercel.com/dashboard**
2. Click on your project (`lawyerconnect-mvp`)
3. Go to **Settings** → **Environment Variables**

4. **Add these variables:**

   **a) SECRET_KEY:**
   - **Name**: `SECRET_KEY`
   - **Value**: Generate with:
     ```bash
     python -c "import secrets; print(secrets.token_hex(32))"
     ```
   - **Environment**: Select all (Production, Preview, Development)
   - Click **Save**

   **b) DATABASE_URL:**
   - **Name**: `DATABASE_URL`
   - **Value**: Your Supabase connection string (from Part 1, Step 3)
   - **Environment**: Select all
   - Click **Save**

### Step 6: Redeploy

After adding environment variables, you need to redeploy:

```bash
vercel --prod
```

Or in Vercel dashboard: **Deployments** → Click **"..."** → **Redeploy**

---

## Part 4: Create Database Tables (Migrations)

### Option A: Add Temporary Migration Endpoint (Easiest)

1. **Add this to `app/routes.py`** (temporarily):

```python
@main_bp.route("/admin/setup-db", methods=["GET", "POST"])
def setup_database():
    """One-time database setup endpoint."""
    from app.extensions import db
    from app.models import User, LawyerProfile, Issue, Chat, Message
    
    try:
        # Create all tables
        db.create_all()
        
        # Run advanced migrations
        try:
            from migrate_db_advanced import migrate_database
            migrate_database()
        except:
            pass
        
        return """
        <h1>Database Setup Complete!</h1>
        <p>Tables created successfully.</p>
        <p><a href="/">Go to Home</a></p>
        <p><strong>IMPORTANT:</strong> Remove this endpoint after setup!</p>
        """
    except Exception as e:
        return f"<h1>Error: {str(e)}</h1>", 500
```

2. **Deploy again:**
   ```bash
   vercel --prod
   ```

3. **Visit:** `https://your-app.vercel.app/admin/setup-db`

4. **Remove the endpoint** from `app/routes.py` after setup

5. **Deploy again** to remove the endpoint

### Option B: Use Supabase SQL Editor

1. Go to Supabase dashboard → **SQL Editor**
2. Click **"New query"**
3. Run this SQL (creates basic tables):

```sql
-- Create users table
CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_lawyer BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create lawyer_profile table
CREATE TABLE IF NOT EXISTS lawyer_profile (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "user"(id) ON DELETE CASCADE,
    expertise_categories TEXT,
    experience_description TEXT,
    rating FLOAT DEFAULT 0.0,
    education VARCHAR(255) DEFAULT '',
    age INTEGER DEFAULT 0,
    city VARCHAR(120) DEFAULT '',
    case_success_rate FLOAT DEFAULT 0.0,
    hourly_rate FLOAT DEFAULT 0.0,
    fixed_fee_min FLOAT DEFAULT 0.0,
    fixed_fee_max FLOAT DEFAULT 0.0,
    contingency_fee FLOAT DEFAULT 0.0,
    is_available BOOLEAN DEFAULT TRUE,
    current_cases INTEGER DEFAULT 0,
    max_cases INTEGER DEFAULT 10,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create issue table
CREATE TABLE IF NOT EXISTS issue (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "user"(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(100) NOT NULL,
    budget_min FLOAT DEFAULT 0.0,
    budget_max FLOAT DEFAULT 0.0,
    urgency VARCHAR(50) DEFAULT 'normal',
    preferred_pricing VARCHAR(50) DEFAULT 'any',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create chat table
CREATE TABLE IF NOT EXISTS chat (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "user"(id) ON DELETE CASCADE,
    lawyer_id INTEGER REFERENCES "user"(id) ON DELETE CASCADE,
    issue_id INTEGER REFERENCES issue(id) ON DELETE CASCADE,
    jitsi_link VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create message table
CREATE TABLE IF NOT EXISTS message (
    id SERIAL PRIMARY KEY,
    chat_id INTEGER REFERENCES chat(id) ON DELETE CASCADE,
    sender_id INTEGER REFERENCES "user"(id) ON DELETE CASCADE,
    sender_role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

4. Click **"Run"** (or press Cmd/Ctrl + Enter)

**Note:** This creates basic tables. For full schema with all fields, use Option A.

---

## Part 5: Seed Database with Sample Lawyers

### Option A: Add Temporary Seed Endpoint

1. **Add to `app/routes.py`** (temporarily):

```python
@main_bp.route("/admin/seed-db", methods=["GET", "POST"])
def seed_database():
    """One-time database seeding."""
    try:
        from seed_db import seed_database
        seed_database()
        return """
        <h1>Database Seeded!</h1>
        <p>Sample lawyers added successfully.</p>
        <p><a href="/">Go to Home</a></p>
        <p><strong>IMPORTANT:</strong> Remove this endpoint after seeding!</p>
        """
    except Exception as e:
        return f"<h1>Error: {str(e)}</h1>", 500
```

2. **Deploy:**
   ```bash
   vercel --prod
   ```

3. **Visit:** `https://your-app.vercel.app/admin/seed-db`

4. **Remove endpoint** and redeploy

### Option B: Use Vercel CLI + Local Script

1. **Pull environment variables:**
   ```bash
   vercel env pull .env.local
   ```

2. **Run seed script locally** (pointing to production DB):
   ```bash
   python seed_db.py
   ```

---

## Part 6: Test Your Deployment

1. **Visit your Vercel URL:** `https://your-app.vercel.app`
2. **Test signup:** Create a user account
3. **Test login:** Log in with your account
4. **Test issue submission:** Submit a legal issue
5. **Check lawyer matches:** See if lawyers appear

---

## Troubleshooting

### Database Connection Error

**Error:** `could not connect to server`

**Solutions:**
1. Check `DATABASE_URL` in Vercel environment variables
2. Ensure password in connection string matches Supabase password
3. Check Supabase project is active (not paused)
4. Verify connection string format: `postgresql://...` (not `postgres://`)

### Tables Not Found

**Error:** `relation "user" does not exist`

**Solution:** Run migrations (Part 4)

### Import Errors

**Error:** `ModuleNotFoundError`

**Solution:** Check `requirements.txt` has all dependencies

### Port Binding Error

**Error:** `Address already in use`

**Solution:** Vercel handles this automatically - not an issue

---

## Quick Reference

### Vercel Commands

```bash
# Deploy
vercel

# Deploy to production
vercel --prod

# View logs
vercel logs

# Open project
vercel open
```

### Environment Variables

- `SECRET_KEY`: Flask secret key
- `DATABASE_URL`: PostgreSQL connection string

### Important URLs

- **Vercel Dashboard:** https://vercel.com/dashboard
- **Supabase Dashboard:** https://supabase.com/dashboard
- **Your App:** `https://your-app.vercel.app`

---

## Next Steps

1. ✅ Database set up (Supabase)
2. ✅ App deployed (Vercel)
3. ✅ Environment variables set
4. ✅ Tables created
5. ✅ Data seeded
6. 🎉 **Your app is live!**

**Remember to:**
- Remove temporary `/admin/setup-db` and `/admin/seed-db` endpoints after use
- Keep your Supabase password secure
- Monitor your Supabase usage (free tier has limits)

---

## Need Help?

- **Vercel Docs:** https://vercel.com/docs
- **Supabase Docs:** https://supabase.com/docs
- **Check logs:** `vercel logs` or Vercel dashboard

Good luck with your deployment! 🚀

