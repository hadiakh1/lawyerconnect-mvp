"""
Vercel serverless function entry point for LawyerConnect.

IMPORTANT: Vercel doesn't support SQLite (read-only filesystem).
You MUST use an external database (PostgreSQL, MySQL, etc.) for Vercel deployment.

For SQLite support, use Render or Railway instead.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

app = create_app()

# Vercel expects this to be the handler
# The @vercel/python builder will automatically wrap this

