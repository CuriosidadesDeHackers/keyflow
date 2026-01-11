import sys
import os
import shutil
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database import Database

def test_workflow():
    db_path = "test_vault.kdbx"
    # Clean up
    if os.path.exists(db_path):
        os.remove(db_path)

    db = Database()
    
    password = "masterpassword123"

    # 1. Test Creation
    print("Testing Creation...")
    db.create(db_path, password)
    assert os.path.exists(db_path), "Database file not created"
    
    # 2. Test Adding Entry
    print("Testing Adding Entry...")
    entry = db.add_entry("Google", "mario", "secret123", "https://google.com", "My notes")
    assert entry is not None
    assert entry.title == "Google"
    assert entry.username == "mario"
    
    # 3. Test Loading
    print("Testing Loading...")
    db2 = Database()
    db2.load(db_path, password)
    entries = db2.get_entries()
    assert len(entries) == 1
    assert entries[0].title == "Google"
    assert entries[0].password == "secret123"

    # 4. Test Update
    print("Testing Update...")
    db2.update_entry(entries[0].uuid, "Google Updated", "mario2", "newpass", "http://new.com", "new notes")
    # Reload to verify persistence
    db3 = Database()
    db3.load(db_path, password)
    entry_updated = db3.get_entries()[0]
    assert entry_updated.title == "Google Updated"
    assert entry_updated.password == "newpass"

    # 5. Test Delete
    print("Testing Delete...")
    db3.delete_entry(entry_updated.uuid)
    db4 = Database()
    db4.load(db_path, password)
    assert len(db4.get_entries()) == 0

    print("All tests passed!")
    
    # Cleanup
    if os.path.exists(db_path):
        os.remove(db_path)

if __name__ == "__main__":
    test_workflow()
