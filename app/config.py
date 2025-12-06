import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    # Get database URL from environment, default to SQLite
    database_url = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(BASE_DIR, 'lawyerconnect.db')}",
    )
    # Fix for providers that use postgres:// instead of postgresql://
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Session configuration for persistent login
    PERMANENT_SESSION_LIFETIME = 86400 * 30  # 30 days
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'





