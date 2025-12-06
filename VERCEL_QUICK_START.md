# Vercel Deployment - Quick Start Guide

## 🚀 Fast Track (15 minutes)

### Step 1: Get Free Database (5 min)

1. Go to **https://supabase.com** → Sign up
2. **New Project** → Name: `lawyerconnect-db`
3. **Create password** (save it!)
4. Wait 2-3 minutes
5. **Settings** → **Database** → Copy connection string
6. **Replace `[YOUR-PASSWORD]`** with your password

### Step 2: Deploy to Vercel (5 min)

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
cd /Users/hadia/mvp-cs391
vercel
```

Follow prompts, then:

### Step 3: Set Environment Variables (2 min)

1. Go to **https://vercel.com/dashboard**
2. Your project → **Settings** → **Environment Variables**
3. Add:
   - `SECRET_KEY`: Run `python -c "import secrets; print(secrets.token_hex(32))"`
   - `DATABASE_URL`: Your Supabase connection string
4. **Redeploy:** `vercel --prod`

### Step 4: Setup Database (2 min)

1. Visit: `https://your-app.vercel.app/admin/setup-db`
2. Visit: `https://your-app.vercel.app/admin/seed-db`
3. **Remove endpoints** from `app/routes.py` (lines with `/admin/setup-db` and `/admin/seed-db`)
4. **Redeploy:** `vercel --prod`

### Step 5: Test (1 min)

Visit: `https://your-app.vercel.app`

---

## 📋 Checklist

- [ ] Supabase project created
- [ ] Connection string copied
- [ ] Vercel CLI installed
- [ ] App deployed to Vercel
- [ ] `SECRET_KEY` set in Vercel
- [ ] `DATABASE_URL` set in Vercel
- [ ] Database tables created (`/admin/setup-db`)
- [ ] Sample data seeded (`/admin/seed-db`)
- [ ] Temporary endpoints removed
- [ ] App tested and working

---

## 🔗 Important Links

- **Vercel Dashboard:** https://vercel.com/dashboard
- **Supabase Dashboard:** https://supabase.com/dashboard
- **Full Guide:** See `VERCEL_COMPLETE_GUIDE.md`

---

## ⚠️ Common Issues

**Database connection error?**
- Check `DATABASE_URL` has correct password
- Ensure Supabase project is active

**Tables not found?**
- Visit `/admin/setup-db` first

**No lawyers showing?**
- Visit `/admin/seed-db` after setup

---

## 🎉 Done!

Your app is live on Vercel with PostgreSQL! 🚀

