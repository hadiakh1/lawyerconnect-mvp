# Render Deployment Guide

## Quick Deployment Steps

### 1. Push to GitHub
```bash
git add .
git commit -m "Ready for Render deployment"
git push
```

### 2. Deploy on Render

1. Go to https://render.com
2. **New** → **Web Service**
3. Connect your GitHub repository
4. Settings:
   - **Name:** `lawyerconnect` (or your choice)
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn run:app`
   - **Plan:** Free (or your choice)

### 3. Environment Variables

In Render Dashboard → Your Service → Environment:

Add:
- **Name:** `SECRET_KEY`
- **Value:** Generate with: `python -c "import secrets; print(secrets.token_hex(32))"`

**Do NOT set `DATABASE_URL`** - SQLite will be used automatically.

### 4. Initialize Database

After first deployment:

1. Visit: `https://your-app.onrender.com/admin/migrate`
2. Then: `https://your-app.onrender.com/admin/seed`

This will:
- Create all database tables
- Add 20 sample lawyers covering all categories

### 5. Remove Admin Endpoints (Security)

After setup, edit `app/routes.py` and remove:
- `/admin/migrate` endpoint (lines ~386-454)
- `/admin/seed` endpoint (lines ~457-503)

Then commit and push:
```bash
git add app/routes.py
git commit -m "Remove admin endpoints"
git push
```

### 6. Test Your App

Visit your Render URL and test:
- ✅ Sign up as a user
- ✅ Submit a legal issue
- ✅ See lawyer matches
- ✅ Start a chat

---

## Sample Data

The app includes **20 sample lawyers** covering all categories:

- **Harassment:** 6 lawyers
- **Workplace Discrimination:** 6 lawyers
- **Domestic Violence:** 6 lawyers
- **Family Disputes:** 7 lawyers
- **Property Issues:** 5 lawyers
- **Fraud:** 6 lawyers

All lawyers have:
- Ratings (4.6 - 4.9)
- Experience descriptions
- Education backgrounds
- Pricing information
- Success rates
- Availability status

---

## Troubleshooting

### App Not Starting
- Check Render logs for errors
- Verify `SECRET_KEY` is set
- Check build logs for dependency issues

### Database Issues
- Visit `/admin/migrate` to create tables
- Visit `/admin/seed` to add lawyers
- Check Render logs for database errors

### No Lawyers Showing
- Make sure you visited `/admin/seed`
- Check database has lawyers: Render Shell → `python -c "from app import create_app; from app.models import LawyerProfile; app = create_app(); app.app_context().push(); print(LawyerProfile.query.count())"`

---

## Your App is Ready! 🚀

After deployment, your app will have:
- ✅ Clean maroon theme
- ✅ Logo support (add logo.png to static/)
- ✅ 20 sample lawyers
- ✅ All features working
- ✅ SQLite database connected

Visit your Render URL to see it live!

