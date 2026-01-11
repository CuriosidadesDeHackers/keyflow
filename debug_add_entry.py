import sys
import os
from src.database import Database

def test_add_entry():
    db_path = "debug_test.kdbx"
    if os.path.exists(db_path):
        os.remove(db_path)

    db = Database()
    password = "test"
    
    print("Creating DB...")
    db.create(db_path, password)
    
    print(f"Root group: {db.kp.root_group}")
    
    print("Adding entry...")
    try:
        db.add_entry("Test Title", "User", "Pass", "URL", "Notes")
        print("Entry added successfully.")
    except Exception as e:
        print(f"Caught exception: {e}")
        import traceback
        traceback.print_exc()

    # Clean up
    if os.path.exists(db_path):
        os.remove(db_path)

if __name__ == "__main__":
    test_add_entry()
