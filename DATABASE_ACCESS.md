# Database Access Instructions

## Private Database Access (Admin Only)

The database viewer has been removed from public navigation for security.

### Option 1: Command Line (Recommended)
```bash
python3 view_db.py
```
This shows all database records in your terminal.

### Option 2: Web Interface (Admin Only)

1. **Set your admin email** in `app/routes.py`:
   - Find the line: `ADMIN_EMAILS = ["your-email@example.com"]`
   - Replace with your actual email address

2. **Set a secret key** (optional but recommended):
   - Find the line: `ADMIN_SECRET == "admin123"`
   - Change `"admin123"` to a secure secret key

3. **Access the database viewer**:
   - Log in with your admin email
   - Visit: `http://localhost:5000/admin/database?key=your-secret-key`
   - Or just: `http://localhost:5000/admin/database` (if your email is in ADMIN_EMAILS)

### Security Notes

- The database viewer is NOT visible in navigation
- Only users with admin email or secret key can access it
- Change the default secret key before deploying to production
- For production, consider using environment variables for admin credentials

