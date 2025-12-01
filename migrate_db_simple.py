"""
Simple migration script that doesn't require Flask imports.
Run this to add missing columns to your database.
"""
import sqlite3
import os

# Database file path (adjust if needed)
DB_PATH = "lawyerconnect.db"

if not os.path.exists(DB_PATH):
    print(f"Database '{DB_PATH}' doesn't exist yet.")
    print("It will be created automatically when you run the app.")
    exit(0)

print(f"Migrating database: {DB_PATH}")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

try:
    # Check existing columns
    cursor.execute("PRAGMA table_info(lawyer_profile)")
    columns = [column[1] for column in cursor.fetchall()]
    
    print(f"Existing columns: {', '.join(columns)}")
    
    # Add rating column if missing
    if 'rating' not in columns:
        print("\nAdding 'rating' column...")
        cursor.execute("ALTER TABLE lawyer_profile ADD COLUMN rating REAL DEFAULT 0.0")
        conn.commit()
        print("✓ Added 'rating' column")
    else:
        print("✓ 'rating' column already exists")
    
    # Add profile_picture column if missing
    if 'profile_picture' not in columns:
        print("Adding 'profile_picture' column...")
        cursor.execute("ALTER TABLE lawyer_profile ADD COLUMN profile_picture VARCHAR(255) DEFAULT 'default-avatar.png'")
        conn.commit()
        print("✓ Added 'profile_picture' column")
    else:
        print("✓ 'profile_picture' column already exists")

    # Add education column if missing
    if 'education' not in columns:
        print("Adding 'education' column...")
        cursor.execute("ALTER TABLE lawyer_profile ADD COLUMN education VARCHAR(255) DEFAULT ''")
        conn.commit()
        print("✓ Added 'education' column")
    else:
        print("✓ 'education' column already exists")

    # Add age column if missing
    if 'age' not in columns:
        print("Adding 'age' column...")
        cursor.execute("ALTER TABLE lawyer_profile ADD COLUMN age INTEGER DEFAULT 0")
        conn.commit()
        print("✓ Added 'age' column")
    else:
        print("✓ 'age' column already exists")

    # Add city column if missing
    if 'city' not in columns:
        print("Adding 'city' column...")
        cursor.execute("ALTER TABLE lawyer_profile ADD COLUMN city VARCHAR(120) DEFAULT ''")
        conn.commit()
        print("✓ Added 'city' column")
    else:
        print("✓ 'city' column already exists")

    # Add case_success_rate column if missing
    if 'case_success_rate' not in columns:
        print("Adding 'case_success_rate' column...")
        cursor.execute("ALTER TABLE lawyer_profile ADD COLUMN case_success_rate REAL DEFAULT 0.0")
        conn.commit()
        print("✓ Added 'case_success_rate' column")
    else:
        print("✓ 'case_success_rate' column already exists")
    
    # Update existing records with default values
    cursor.execute("UPDATE lawyer_profile SET rating = 0.0 WHERE rating IS NULL")
    cursor.execute("UPDATE lawyer_profile SET profile_picture = 'default-avatar.png' WHERE profile_picture IS NULL")
    cursor.execute("UPDATE lawyer_profile SET education = '' WHERE education IS NULL")
    cursor.execute("UPDATE lawyer_profile SET age = 0 WHERE age IS NULL")
    cursor.execute("UPDATE lawyer_profile SET city = '' WHERE city IS NULL")
    cursor.execute("UPDATE lawyer_profile SET case_success_rate = 0.0 WHERE case_success_rate IS NULL")
    conn.commit()
    
    print("\n✓ Migration completed successfully!")
    
except Exception as e:
    print(f"\n✗ Error during migration: {e}")
    conn.rollback()
finally:
    conn.close()


