# LawyerConnect - Legal Matching Platform

A Flask-based web application that connects users with lawyers based on their legal needs.

## Features

- User and Lawyer authentication
- Legal issue submission with category matching
- Advanced lawyer matching algorithm (Priority Queue + Trie)
- Real-time chat system
- Video call integration (Jitsi Meet)
- Responsive design with maroon theme
- SQLite database

## Quick Start

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app:**
   ```bash
   python run.py
   ```

3. **Access the app:**
   - Open http://localhost:5000
   - Database is automatically created
   - Sample lawyers are auto-seeded on first run

### Database Setup

The database is automatically initialized when the app starts. If you need to manually seed:

```bash
python seed_db.py
```

Or use the web endpoints:
- `/admin/migrate` - Create tables and run migrations
- `/admin/seed` - Add sample lawyers

**⚠️ Remove these endpoints after setup for security!**

## Deployment on Render

### Step 1: Push to GitHub

```bash
git add .
git commit -m "Ready for Render"
git push
```

### Step 2: Deploy on Render

1. Go to https://render.com
2. New → Web Service
3. Connect your GitHub repository
4. Settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn run:app`
5. Add Environment Variable:
   - `SECRET_KEY` - Generate with: `python -c "import secrets; print(secrets.token_hex(32))"`

### Step 3: Initialize Database

After deployment, visit:
- `https://your-app.onrender.com/admin/migrate`
- `https://your-app.onrender.com/admin/seed`

Then remove the endpoints from `app/routes.py` for security.

## Project Structure

```
mvp-cs391/
├── app/
│   ├── __init__.py          # App factory
│   ├── config.py            # Configuration
│   ├── models.py            # Database models
│   ├── routes.py             # Flask routes
│   ├── extensions.py         # Flask extensions
│   ├── matching.py           # Basic matching algorithm
│   └── advanced_matching.py  # Priority Queue + Trie algorithm
├── templates/                # Jinja2 templates
├── static/                   # CSS and static files
├── requirements.txt          # Python dependencies
├── Procfile                  # Render deployment config
├── run.py                    # Application entry point
└── seed_db.py                # Database seeding script
```

## Technologies

- **Backend:** Flask, SQLAlchemy, Flask-Login
- **Database:** SQLite
- **Frontend:** Jinja2, TailwindCSS
- **Deployment:** Render, Gunicorn

## License

Built as a student project at GIK.

