import psycopg2
import os

# Set encoding
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Test basic database connection
try:
    # Use connection string
    connection_string = "host=127.0.0.1 port=5432 dbname=postgres user=postgres password=postgres"
    conn = psycopg2.connect(connection_string)
    print("✅ Database connection successful!")
    
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"PostgreSQL version: {version[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM users;")
    count = cursor.fetchone()
    print(f"Users table has {count[0]} records")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Database connection failed: {e}")
    import traceback
    traceback.print_exc()
