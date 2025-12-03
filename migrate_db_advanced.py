"""
Migration script to add new fields for advanced matching algorithm.
Adds fields to Issue and LawyerProfile models.
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
    # Check existing columns in issue table
    cursor.execute("PRAGMA table_info(issue)")
    issue_columns = [column[1] for column in cursor.fetchall()]
    
    print(f"Issue table columns: {', '.join(issue_columns)}")
    
    # Add new fields to Issue table
    new_issue_fields = {
        'budget_min': 'REAL DEFAULT 0.0',
        'budget_max': 'REAL DEFAULT 10000.0',
        'urgency': "VARCHAR(20) DEFAULT 'normal'",
        'preferred_pricing': "VARCHAR(20) DEFAULT 'hourly'",
    }
    
    for field, definition in new_issue_fields.items():
        if field not in issue_columns:
            print(f"Adding '{field}' column to issue table...")
            cursor.execute(f"ALTER TABLE issue ADD COLUMN {field} {definition}")
            conn.commit()
            print(f"✓ Added '{field}' column")
        else:
            print(f"✓ '{field}' column already exists")
    
    # Check existing columns in lawyer_profile table
    cursor.execute("PRAGMA table_info(lawyer_profile)")
    lawyer_columns = [column[1] for column in cursor.fetchall()]
    
    print(f"\nLawyerProfile table columns: {', '.join(lawyer_columns)}")
    
    # Add new fields to LawyerProfile table
    new_lawyer_fields = {
        'is_available': 'BOOLEAN DEFAULT 1',
        'hourly_rate': 'REAL DEFAULT 0.0',
        'fixed_rate_min': 'REAL DEFAULT 0.0',
        'fixed_rate_max': 'REAL DEFAULT 0.0',
        'accepts_contingency': 'BOOLEAN DEFAULT 0',
        'contingency_percentage': 'REAL DEFAULT 0.0',
        'max_cases': 'INTEGER DEFAULT 10',
        'current_cases': 'INTEGER DEFAULT 0',
    }
    
    for field, definition in new_lawyer_fields.items():
        if field not in lawyer_columns:
            print(f"Adding '{field}' column to lawyer_profile table...")
            cursor.execute(f"ALTER TABLE lawyer_profile ADD COLUMN {field} {definition}")
            conn.commit()
            print(f"✓ Added '{field}' column")
        else:
            print(f"✓ '{field}' column already exists")
    
    # Update existing records with default values
    cursor.execute("UPDATE issue SET budget_min = 0.0 WHERE budget_min IS NULL")
    cursor.execute("UPDATE issue SET budget_max = 10000.0 WHERE budget_max IS NULL")
    cursor.execute("UPDATE issue SET urgency = 'normal' WHERE urgency IS NULL")
    cursor.execute("UPDATE issue SET preferred_pricing = 'hourly' WHERE preferred_pricing IS NULL")
    
    cursor.execute("UPDATE lawyer_profile SET is_available = 1 WHERE is_available IS NULL")
    cursor.execute("UPDATE lawyer_profile SET hourly_rate = 0.0 WHERE hourly_rate IS NULL")
    cursor.execute("UPDATE lawyer_profile SET fixed_rate_min = 0.0 WHERE fixed_rate_min IS NULL")
    cursor.execute("UPDATE lawyer_profile SET fixed_rate_max = 0.0 WHERE fixed_rate_max IS NULL")
    cursor.execute("UPDATE lawyer_profile SET accepts_contingency = 0 WHERE accepts_contingency IS NULL")
    cursor.execute("UPDATE lawyer_profile SET contingency_percentage = 0.0 WHERE contingency_percentage IS NULL")
    cursor.execute("UPDATE lawyer_profile SET max_cases = 10 WHERE max_cases IS NULL")
    cursor.execute("UPDATE lawyer_profile SET current_cases = 0 WHERE current_cases IS NULL")
    
    conn.commit()
    
    print("\n✓ Advanced matching migration completed successfully!")
    
except Exception as e:
    print(f"\n✗ Error during migration: {e}")
    import traceback
    traceback.print_exc()
    conn.rollback()
finally:
    conn.close()

